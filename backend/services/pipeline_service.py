"""
Pipeline service for managing ML pipeline execution.
"""
from typing import Dict, Any, Callable
from backend.pipeline_state import PipelineState
from backend.pipeline_graph import test_pipeline
import asyncio


class PipelineService:
    """Service for managing pipeline execution with callbacks."""
    
    def __init__(self):
        self.callbacks = []
    
    def add_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add a callback for pipeline events."""
        self.callbacks.append(callback)
    
    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to all callbacks."""
        for callback in self.callbacks:
            await callback(event_type, data)
    
    async def run_pipeline(self, dataset_path: str) -> Dict[str, Any]:
        """Run the pipeline with event callbacks."""
        # Create initial state
        state = PipelineState(dataset_path=dataset_path)
        
        # Emit start event
        await self.emit_event("pipeline_started", {"dataset_path": dataset_path})
        
        try:
            # Run pipeline (blocking operation, so use thread)
            final_state = await asyncio.to_thread(test_pipeline.invoke, state)
            
            # Emit completion event
            await self.emit_event("pipeline_completed", final_state)
            
            return final_state
            
        except Exception as e:
            # Emit error event
            await self.emit_event("pipeline_failed", {"error": str(e)})
            raise
