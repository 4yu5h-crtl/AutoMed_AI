# ================================================
# 6. AGENT 3 — MODEL SELECTION AGENT (GEMINI)
# ================================================
import json
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from backend.logger import send_log

# IMPORTANT: Configure GEMINI KEY before running
genai.configure(api_key="AIzaSyBaY8lV5seyGjvJ6ScMvZ6h7jfGuh5VbAU")
load_dotenv(find_dotenv(), override=False)
model_selector = genai.GenerativeModel("gemini-2.5-flash")


def model_selection_agent_node(state):
    send_log("model_selector", "Model Selection Agent Running...")

    stats = state["dataset_stats"]
    dataset_size = stats["size"]
    imbalance = stats["imbalance_ratio"]
    blur = stats["avg_blur"]
    noise = stats["avg_noise"]

    prompt = f"""
    You are an AI agent that selects the most appropriate deep learning architecture.

    Available models:
    - ResNet18 (strong on small datasets, quick to train)
    - EfficientNet-B0 (best generalization, stable on imbalance/noise)
    - MobileNetV2 (fast, lightweight, robust to low-quality images)

    Dataset stats:
    {json.dumps(stats, indent=2)}

    Selection Rules:
    - If dataset_size < 150 → ResNet18
    - If imbalance_ratio > 3 → EfficientNet-B0
    - If avg_noise > 0.20 → MobileNetV2
    - If avg_blur > 12 → EfficientNet-B0
    - If no special conditions → EfficientNet-B0

    Output ONLY JSON:
    {{
        "selected_model": "resnet" | "efficientnet" | "mobilenet",
        "reason": "<one sentence reason>"
    }}
    """

    response = model_selector.generate_content(prompt).text.strip()

    send_log("model_selector", "Raw Gemini Output:")
    send_log("model_selector", response)

    try:
        selection = json.loads(response)
    except:
        send_log("model_selector", "JSON parsing failed, using default = ResNet18", level="warning")
        selection = {
            "selected_model": "resnet",
            "reason": "Fallback selection"
        }

    state["selected_model"] = selection

    send_log("model_selector", f"Selected Model: {selection}")
    send_log("model_selector", "Finished.")

    return state
