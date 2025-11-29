from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import json
import os
from datetime import datetime
import uuid

app = FastAPI(title="AutoMed AI API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for pipeline runs and logs
pipeline_runs: Dict[str, Dict[str, Any]] = {}
active_connections: List[WebSocket] = []


# ============================================
# Request/Response Models
# ============================================

class PipelineStartRequest(BaseModel):
    dataset_path: str


class PipelineStatusResponse(BaseModel):
    run_id: str
    status: str  # "running", "completed", "failed"
    current_stage: Optional[str]
    dataset_stats: Optional[Dict[str, Any]]
    aug_plan: Optional[Dict[str, Any]]
    selected_model: Optional[Dict[str, Any]]
    model_results: Optional[Dict[str, Any]]
    error: Optional[str]


class ModelTestRequest(BaseModel):
    model_name: str
    image_path: str


class ModelListResponse(BaseModel):
    models: List[Dict[str, str]]


class AgentLog(BaseModel):
    timestamp: str
    agent: str
    message: str
    level: str  # "info", "warning", "error"


# ============================================
# WebSocket Connection Manager
# ============================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    return {"message": "AutoMed AI API", "version": "1.0.0"}


@app.post("/api/pipeline/start")
async def start_pipeline(request: PipelineStartRequest):
    """Start the ML pipeline with the given dataset path."""
    run_id = str(uuid.uuid4())
    
    # Validate dataset path
    if not os.path.exists(request.dataset_path):
        raise HTTPException(status_code=400, detail="Dataset path does not exist")
    
    # Initialize pipeline run
    pipeline_runs[run_id] = {
        "run_id": run_id,
        "status": "running",
        "current_stage": "data_inspector",
        "dataset_path": request.dataset_path,
        "started_at": datetime.now().isoformat(),
        "dataset_stats": None,
        "aug_plan": None,
        "selected_model": None,
        "model_results": None,
        "error": None
    }
    
    # Start pipeline in background
    asyncio.create_task(run_pipeline(run_id, request.dataset_path))
    
    return {"run_id": run_id, "status": "started"}


@app.get("/api/pipeline/status/{run_id}", response_model=PipelineStatusResponse)
async def get_pipeline_status(run_id: str):
    """Get the current status of a pipeline run."""
    if run_id not in pipeline_runs:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    
    return pipeline_runs[run_id]


@app.get("/api/models", response_model=ModelListResponse)
async def list_models():
    """List all trained models."""
    models_dir = "models"
    if not os.path.exists(models_dir):
        return {"models": []}
    
    models = []
    for filename in os.listdir(models_dir):
        if filename.endswith(".pt"):
            model_name = filename.replace("_model.pt", "")
            models.append({
                "name": model_name,
                "path": os.path.join(models_dir, filename),
                "size": str(os.path.getsize(os.path.join(models_dir, filename)))
            })
    
    return {"models": models}


@app.get("/api/models/{model_name}/download")
async def download_model(model_name: str):
    """Download a trained model."""
    model_path = f"models/{model_name}_model.pt"
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    return FileResponse(
        model_path,
        media_type="application/octet-stream",
        filename=f"{model_name}_model.pt"
    )


@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """WebSocket endpoint for real-time agent logs."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ============================================
# Pipeline Execution
# ============================================

async def run_pipeline(run_id: str, dataset_path: str):
    """Run the ML pipeline asynchronously."""
    try:
        from backend.pipeline_graph import test_pipeline
        from backend.pipeline_state import PipelineState
        
        # Send initial log
        await manager.broadcast({
            "timestamp": datetime.now().isoformat(),
            "agent": "orchestrator",
            "message": f"Pipeline started for dataset: {dataset_path}",
            "level": "info"
        })
        
        # Create initial state
        state = PipelineState(dataset_path=dataset_path)
        
        # Run pipeline with logging
        await log_and_run_agent(run_id, "data_inspector", state)
        
        # The pipeline runs synchronously, so we'll wrap it
        final_state = await asyncio.to_thread(test_pipeline.invoke, state)
        
        # Update pipeline run with final state
        pipeline_runs[run_id].update({
            "status": "completed",
            "current_stage": "completed",
            "dataset_stats": final_state.get("dataset_stats"),
            "aug_plan": final_state.get("aug_plan"),
            "selected_model": final_state.get("selected_model"),
            "model_results": final_state.get("model_results"),
            "completed_at": datetime.now().isoformat()
        })
        
        # Send completion log
        await manager.broadcast({
            "timestamp": datetime.now().isoformat(),
            "agent": "orchestrator",
            "message": "Pipeline completed successfully! Model ready for testing.",
            "level": "info"
        })
        
    except Exception as e:
        pipeline_runs[run_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })
        
        await manager.broadcast({
            "timestamp": datetime.now().isoformat(),
            "agent": "orchestrator",
            "message": f"Pipeline failed: {str(e)}",
            "level": "error"
        })


async def log_and_run_agent(run_id: str, agent_name: str, state: dict):
    """Log agent execution to WebSocket."""
    await manager.broadcast({
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "message": f"{agent_name.replace('_', ' ').title()} started...",
        "level": "info"
    })


# ============================================
# Model Testing & XAI
# ============================================

class ModelTestResponse(BaseModel):
    predicted_class: int
    confidence: float
    explanation: str
    heatmap_base64: str


@app.post("/api/models/test", response_model=ModelTestResponse)
async def test_model(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):
    """Test a model on an uploaded image and generate Grad-CAM visualization."""
    temp_file_path = None
    try:
        from backend.services.xai_service import generate_gradcam
        import cv2
        import base64
        import numpy as np
        import shutil
        
        # Create temp directory if not exists
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        models_dir = "models"
        model_path = os.path.join(models_dir, f"{model_name}_model.pt")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model not found")
            
        # Generate Grad-CAM and prediction
        overlay, predicted_class, confidence, explanation = await asyncio.to_thread(
            generate_gradcam,
            temp_file_path,
            model_name,
            model_path
        )
        
        # Encode overlay image to base64
        _, buffer = cv2.imencode('.jpg', overlay)
        heatmap_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence),
            "explanation": explanation,
            "heatmap_base64": f"data:image/jpeg;base64,{heatmap_base64}"
        }
        
    except Exception as e:
        print(f"Error testing model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass


# ============================================
# Background Log Processor
# ============================================

async def log_processor():
    """Process logs from the queue and broadcast them via WebSocket."""
    from backend.logger import log_queue
    while True:
        try:
            # Non-blocking get from queue
            # We use a small sleep to avoid busy waiting if queue is empty
            if not log_queue.empty():
                log_entry = log_queue.get_nowait()
                await manager.broadcast(log_entry)
            else:
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error in log processor: {e}")
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(log_processor())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
