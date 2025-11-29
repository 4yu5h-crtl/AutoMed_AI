"use client";

import ModelSelector from "@/components/testing/ModelSelector";
import ImageUpload from "@/components/testing/ImageUpload";
import XAIVisualization from "@/components/testing/XAIVisualization";
import ModelDownload from "@/components/testing/ModelDownload";
import { useModelTesting } from "@/lib/hooks/useModelTesting";
import Link from "next/link";

export default function TestPage() {
    const {
        models,
        selectedModel,
        setSelectedModel,
        testResult,
        testModel,
        isLoading
    } = useModelTesting();

    const handleImageUpload = async (imageFile: File) => {
        if (!selectedModel) {
            alert("Please select a model first");
            return;
        }
        await testModel(imageFile);
    };

    return (
        <div className="space-y-6">
            {/* Navigation */}
            <div className="flex justify-between items-center">
                <Link
                    href="/"
                    className="px-4 py-2 rounded-lg glass hover:bg-white/10 transition-all duration-200"
                >
                    ← Back to Dashboard
                </Link>
                <h2 className="text-2xl font-bold gradient-text">
                    Model Evaluation & XAI
                </h2>
            </div>

            {/* Model Selection */}
            <div className="glass rounded-xl p-6">
                <ModelSelector
                    models={models}
                    selectedModel={selectedModel}
                    onSelect={setSelectedModel}
                />
            </div>

            {/* Main Testing Area */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left - Image Upload */}
                <div className="glass rounded-xl p-6">
                    <h3 className="text-xl font-semibold mb-4">Test Image</h3>
                    <ImageUpload onUpload={handleImageUpload} isLoading={isLoading} />
                </div>

                {/* Right - XAI Visualization */}
                <div className="glass rounded-xl p-6">
                    <h3 className="text-xl font-semibold mb-4">XAI Analysis</h3>
                    <XAIVisualization result={testResult} />
                </div>
            </div>

            {/* Model Download */}
            {selectedModel && (
                <div className="glass rounded-xl p-6">
                    <ModelDownload modelName={selectedModel} />
                </div>
            )}
        </div>
    );
}
