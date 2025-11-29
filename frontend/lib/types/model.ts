export interface Model {
    name: string;
    path: string;
    size: string;
}

export interface TestResult {
    predicted_class: number;
    confidence: number;
    heatmap_base64?: string;
    explanation?: string;
}
