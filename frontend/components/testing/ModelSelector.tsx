"use client";

import { Model } from "@/lib/types/model";

interface ModelSelectorProps {
    models: Model[];
    selectedModel: string | null;
    onSelect: (modelName: string) => void;
}

export default function ModelSelector({ models, selectedModel, onSelect }: ModelSelectorProps) {
    if (models.length === 0) {
        return (
            <div className="text-center py-8">
                <p className="text-gray-400">No trained models available</p>
                <p className="text-sm text-gray-500 mt-2">
                    Please train a model first from the dashboard
                </p>
            </div>
        );
    }

    return (
        <div>
            <label htmlFor="model-select" className="block text-sm text-gray-300 mb-2">
                Select Base Model
            </label>
            <select
                id="model-select"
                value={selectedModel || ""}
                onChange={(e) => onSelect(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 
                 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20
                 transition-all cursor-pointer"
            >
                {models.map((model) => (
                    <option key={model.name} value={model.name} className="bg-gray-900">
                        {model.name.charAt(0).toUpperCase() + model.name.slice(1)} Model
                        ({(parseInt(model.size) / 1024 / 1024).toFixed(2)} MB)
                    </option>
                ))}
            </select>
        </div>
    );
}
