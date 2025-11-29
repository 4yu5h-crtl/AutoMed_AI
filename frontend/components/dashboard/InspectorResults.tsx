"use client";

import { DatasetStats } from "@/lib/types/pipeline";

interface InspectorResultsProps {
    stats: DatasetStats | null | undefined;
}

export default function InspectorResults({ stats }: InspectorResultsProps) {
    if (!stats) {
        return (
            <div className="card-panel p-6 h-full flex items-center justify-center">
                <div className="text-center text-muted-foreground">
                    <p>Upload a dataset to see analysis results</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card-panel p-6">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <span className="text-primary">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                </span>
                Data Inspector Results
            </h2>

            <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-background/50 p-4 rounded-lg border border-border/20">
                    <p className="text-sm text-muted-foreground">Total Images</p>
                    <p className="text-2xl font-bold text-foreground">{stats.size}</p>
                </div>
                <div className="bg-background/50 p-4 rounded-lg border border-border/20">
                    <p className="text-sm text-muted-foreground">Classes</p>
                    <p className="text-2xl font-bold text-foreground">{Object.keys(stats.class_dist).length}</p>
                </div>
            </div>

            <div className="space-y-4">
                <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Average Blur Score</span>
                        <span className="text-primary font-medium">{stats.avg_blur.toFixed(1)}</span>
                    </div>
                    <div className="h-2 bg-background rounded-full overflow-hidden">
                        <div
                            className="h-full bg-primary transition-all duration-500"
                            style={{ width: `${Math.min(stats.avg_blur * 10, 100)}%` }}
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Noise Level</span>
                        <span className="text-secondary font-medium">{stats.avg_noise.toFixed(3)}</span>
                    </div>
                    <div className="h-2 bg-background rounded-full overflow-hidden">
                        <div
                            className="h-full bg-secondary transition-all duration-500"
                            style={{ width: `${Math.min(stats.avg_noise * 1000, 100)}%` }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
