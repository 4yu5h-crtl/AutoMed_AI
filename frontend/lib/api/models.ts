import { apiClient, API_BASE_URL } from "./client";
import { Model, TestResult } from "../types/model";

export const modelsApi = {
    async listModels(): Promise<{ models: Model[] }> {
        return apiClient.get("/api/models");
    },

    getDownloadUrl(modelName: string): string {
        return apiClient.getDownloadUrl(`/api/models/${modelName}/download`);
    },

    async testModel(modelName: string, imageFile: File): Promise<TestResult> {
        const formData = new FormData();
        formData.append("model_name", modelName);
        formData.append("file", imageFile);

        // We use fetch directly here because apiClient.post expects JSON by default
        // and we need to let the browser set the Content-Type header for FormData
        const response = await fetch(`${API_BASE_URL}/api/models/test`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            let errorMessage = response.statusText;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
            } catch (e) {
                // Ignore JSON parse error
            }
            throw new Error(`API error: ${errorMessage}`);
        }

        return response.json();
    },
};
