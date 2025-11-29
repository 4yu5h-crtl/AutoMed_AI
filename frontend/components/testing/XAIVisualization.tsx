"use client";

import { TestResult } from "@/lib/types/model";

interface XAIVisualizationProps {
    result: TestResult | null;
}

export default function XAIVisualization({ result }: XAIVisualizationProps) {
    if (!result) {
        return (
            <div className="upload-zone border-dashed border-2 border-border/30 bg-background/20">
                <svg className="w-16 h-16 mb-4 text-muted-foreground/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-lg font-medium text-muted-foreground">Ready for Analysis</p>
                <p className="text-sm text-muted-foreground/60 mt-2">Upload an image and click Test to see results</p>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in h-full flex flex-col">
            <div className="relative rounded-lg overflow-hidden border border-border/30 bg-background/50">
                <img
                    src={result.heatmap_base64}
                    alt="Grad-CAM Visualization"
                    className="w-full h-64 object-contain"
                />
                <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-background to-transparent">
                    <div className="flex justify-between items-end">
                        <div>
                            <p className="text-sm text-muted-foreground mb-1">Prediction</p>
                            <p className="text-2xl font-bold text-foreground">
                                Class {result.predicted_class}
                            </p>
                        </div>
                        <div className="text-right">
                            <p className="text-sm text-muted-foreground mb-1">Confidence</p>
                            <p className="text-2xl font-bold text-primary">
                                {(result.confidence * 100).toFixed(1)}%
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="card-panel p-4 bg-primary/5 border-primary/20">
                <h4 className="text-sm font-semibold text-primary mb-2 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    AI Explanation
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                    {result.explanation}
                </p>
            </div>
        </div>
    );
}
