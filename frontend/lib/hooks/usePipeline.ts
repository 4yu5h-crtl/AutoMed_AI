"use client";

import { useState, useEffect } from "react";
import { pipelineApi } from "../api/pipeline";
import { PipelineStatus } from "../types/pipeline";

export function usePipeline() {
    const [runId, setRunId] = useState<string | null>(null);
    const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);
    const [isRunning, setIsRunning] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startPipeline = async (datasetPath: string) => {
        try {
            setError(null);
            setIsRunning(true);
            const response = await pipelineApi.startPipeline(datasetPath);
            setRunId(response.run_id);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to start pipeline");
            setIsRunning(false);
        }
    };

    useEffect(() => {
        if (!runId) return;

        const pollStatus = async () => {
            try {
                const status = await pipelineApi.getPipelineStatus(runId);
                setPipelineStatus(status);

                if (status.status === "completed" || status.status === "failed") {
                    setIsRunning(false);
                    if (status.status === "failed") {
                        setError(status.error || "Pipeline failed");
                    }
                }
            } catch (err) {
                console.error("Failed to fetch pipeline status:", err);
            }
        };

        // Poll every 2 seconds while running
        const interval = setInterval(pollStatus, 2000);
        pollStatus(); // Initial fetch

        return () => clearInterval(interval);
    }, [runId]);

    return {
        startPipeline,
        pipelineStatus,
        isRunning,
        error,
    };
}
