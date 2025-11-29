"use client";

import { modelsApi } from "@/lib/api/models";

interface ModelDownloadProps {
    modelName: string;
}

export default function ModelDownload({ modelName }: ModelDownloadProps) {
    const handleDownload = () => {
        const downloadUrl = modelsApi.getDownloadUrl(modelName);
        window.open(downloadUrl, "_blank");
    };

    return (
        <div className="flex items-center justify-between">
            <div>
                <h3 className="text-lg font-semibold mb-1">Download Final Model</h3>
                <p className="text-sm text-gray-400">
                    Download the trained {modelName} model for deployment
                </p>
            </div>
            <button
                onClick={handleDownload}
                className="px-6 py-3 rounded-lg bg-gradient-to-r from-green-600 to-emerald-600
                 hover:from-green-500 hover:to-emerald-500 transition-all duration-200 
                 font-semibold shadow-lg hover:shadow-xl flex items-center space-x-2"
            >
                <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                </svg>
                <span>Download Model</span>
            </button>
        </div>
    );
}
