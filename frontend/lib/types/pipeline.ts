export interface PipelineState {
    dataset_path: string;
    dataset_stats?: DatasetStats;
    aug_plan?: AugmentationPlan;
    selected_model?: ModelSelection;
    model_results?: ModelResults;
    explain_result?: any;
    engineer_feedback?: any;
}

export interface DatasetStats {
    size: number;
    class_dist: Record<string, number>;
    imbalance_ratio: number;
    avg_blur: number;
    avg_noise: number;
    num_classes: number;
}

export interface AugmentationPlan {
    rotation: number;
    flip: boolean;
    color_jitter: "none" | "low" | "medium";
}

export interface ModelSelection {
    selected_model: string;
    reason: string;
}

export interface ModelResults {
    accuracy: number;
    f1_score: number;
    model: string;
    model_path: string;
}

export interface PipelineStatus {
    run_id: string;
    status: "running" | "completed" | "failed";
    current_stage?: string;
    dataset_stats?: DatasetStats;
    aug_plan?: AugmentationPlan;
    selected_model?: ModelSelection;
    model_results?: ModelResults;
    error?: string;
}
