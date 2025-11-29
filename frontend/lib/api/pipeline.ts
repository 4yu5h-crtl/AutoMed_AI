import { apiClient } from "./client";
import { PipelineStatus } from "../types/pipeline";

export const pipelineApi = {
    async startPipeline(datasetPath: string): Promise<{ run_id: string; status: string }> {
        return apiClient.post("/api/pipeline/start", { dataset_path: datasetPath });
    },

    async getPipelineStatus(runId: string): Promise<PipelineStatus> {
        return apiClient.get(`/api/pipeline/status/${runId}`);
    },
};
