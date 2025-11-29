from typing import TypedDict, Dict, Any


class PipelineState(TypedDict, total=False):
    # INPUT
    dataset_path: str

    # AGENT 1 OUTPUT — Data Inspector
    dataset_stats: Dict[str, Any]        # size, blur, noise, class_dist, etc.

    # AGENT 2 OUTPUT — Augmentation Planner
    aug_plan: Dict[str, Any]            # rotation, flip, color_jitter

    # AGENT 3 OUTPUT — Model Selection Agent
    selected_model: Dict[str, Any]      # {"selected_model": "...", "reason": "..."}

    # AGENT 4 OUTPUT — Model Trainer
    model_results: Dict[str, Any]       # accuracy, f1, model_path

    # OPTIONAL: Grad-CAM / Explainability Agent
    explain_result: Dict[str, Any]

    # OPTIONAL: Feedback from AI Engineer
    engineer_feedback: Dict[str, Any]
