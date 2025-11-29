"use client";

import { useState, useEffect } from "react";
import { modelsApi } from "../api/models";
import { Model, TestResult } from "../types/model";

export function useModelTesting() {
    const [models, setModels] = useState<Model[]>([]);
    const [selectedModel, setSelectedModel] = useState<string | null>(null);
    const [testResult, setTestResult] = useState<TestResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        loadModels();
    }, []);

    const loadModels = async () => {
        try {
            const response = await modelsApi.listModels();
            setModels(response.models);
            if (response.models.length > 0) {
                setSelectedModel(response.models[0].name);
            }
        } catch (error) {
            console.error("Failed to load models:", error);
        }
    };

    const testModel = async (imageFile: File) => {
        if (!selectedModel) return;

        setIsLoading(true);
        try {
            const result = await modelsApi.testModel(selectedModel, imageFile);
            setTestResult(result);
        } catch (error) {
            console.error("Failed to test model:", error);
            // Optional: Add error state handling here
        } finally {
            setIsLoading(false);
        }
    };

    return {
        models,
        selectedModel,
        setSelectedModel,
        testResult,
        testModel,
        isLoading,
    };
}
