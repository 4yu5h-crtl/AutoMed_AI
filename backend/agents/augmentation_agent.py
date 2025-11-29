import json
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from backend.logger import send_log

# IMPORTANT: Configure GEMINI KEY before running
genai.configure(api_key="your-api-key")
load_dotenv(find_dotenv(), override=False)
model = genai.GenerativeModel("gemini-2.5-flash")


def augmentation_agent_node(state):
    send_log("augmentation", "Augmentation Planner (Gemini) Running...")

    stats = state["dataset_stats"]

    prompt = f"""
    You are an expert deep learning engineer specializing in data augmentation.

    Here is the dataset analysis:
    {json.dumps(stats, indent=2)}

    Based on this, create an augmentation plan.

    Follow these RULES:
    - If dataset_size < 100: rotation = 10–20 degrees.
    - If imbalance_ratio > 3: flip = true.
    - If avg_blur > 10: reduce rotation (≤10) + color_jitter = "low".
    - If avg_noise > 0.15: color_jitter = "none".
    - Always include keys: rotation, flip, color_jitter.

    Output ONLY valid JSON in this EXACT format:

    {{
      "rotation": <int>,
      "flip": <true/false>,
      "color_jitter": "none" | "low" | "medium"
    }}
    """

    # Gemini call
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    send_log("augmentation", "Raw Gemini Output:")
    send_log("augmentation", raw_text)

    # Parse JSON safely
    try:
        aug_plan = json.loads(raw_text)
    except:
        send_log("augmentation", "JSON parse failed! Using fallback defaults.", level="warning")
        aug_plan = {
            "rotation": 10,
            "flip": True,
            "color_jitter": "low"
        }

    # Save to state
    state["aug_plan"] = aug_plan

    send_log("augmentation", "Final Augmentation Plan:")
    send_log("augmentation", str(aug_plan))
    send_log("augmentation", "Finished.")

    return state

