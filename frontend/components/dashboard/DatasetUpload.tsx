"use client";

import { useState } from "react";

interface DatasetUploadProps {
    onUpload: (datasetPath: string) => void;
    isLoading: boolean;
}

export default function DatasetUpload({ onUpload, isLoading }: DatasetUploadProps) {
    const [path, setPath] = useState("");
    const [isUploading, setIsUploading] = useState(false);

    const handleUpload = async () => {
        if (!path) return;
        setIsUploading(true);
        try {
            await onUpload(path);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="card-panel p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-primary">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                    </svg>
                </span>
                Dataset Configuration
            </h2>

            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-muted-foreground mb-2">
                        Dataset Path (Absolute Path)
                    </label>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={path}
                            onChange={(e) => setPath(e.target.value)}
                            placeholder="C:/path/to/dataset"
                            className="flex-1 bg-background border border-border/30 rounded-lg px-4 py-2 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                            disabled={isUploading}
                        />
                        <button
                            onClick={handleUpload}
                            disabled={isUploading || !path}
                            className="btn-primary-ghost"
                        >
                            {isUploading ? (
                                <span className="flex items-center gap-2">
                                    <span className="animate-spin">⟳</span> Processing
                                </span>
                            ) : (
                                "Load Dataset"
                            )}
                        </button>
                    </div>
                </div>

                <div className="upload-zone">
                    <div className="w-16 h-16 mb-4 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    </div>
                    <p className="text-lg font-medium text-foreground mb-1">Drag & Drop Dataset Folder</p>
                    <p className="text-sm text-muted-foreground">or paste the path above</p>
                </div>

                <div className="mt-6 p-4 rounded-lg bg-primary/5 border border-primary/20">
                    <p className="text-sm text-primary/80">
                        <strong>Tip:</strong> Ensure your dataset follows the structure:
                        <code className="block mt-2 text-xs bg-black/30 p-2 rounded font-mono">
                            dataset/<br />
                            ├── train/<br />
                            │   ├── class0/<br />
                            │   └── class1/<br />
                            └── test/<br />
                            &nbsp;&nbsp;&nbsp;&nbsp;├── class0/<br />
                            &nbsp;&nbsp;&nbsp;&nbsp;└── class1/
                        </code>
                    </p>
                </div>
            </div>
        </div>
    );
}
