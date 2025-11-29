"use client";

import DatasetUpload from "@/components/dashboard/DatasetUpload";
import InspectorResults from "@/components/dashboard/InspectorResults";
import AgentLogs from "@/components/dashboard/AgentLogs";
import { usePipeline } from "@/lib/hooks/usePipeline";
import { useAgentLogs } from "@/lib/hooks/useAgentLogs";
import Link from "next/link";

export default function Home() {
  const { startPipeline, pipelineStatus, isRunning } = usePipeline();
  const { logs } = useAgentLogs();

  const handleUpload = async (datasetPath: string) => {
    await startPipeline(datasetPath);
  };

  return (
    <div className="space-y-6">
      {/* Navigation */}
      {pipelineStatus?.status === "completed" && (
        <div className="flex justify-end">
          <Link
            href="/test"
            className="px-6 py-3 rounded-lg glass hover:bg-white/10 transition-all duration-200 glow"
          >
            Test Trained Models →
          </Link>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Panel - Upload */}
        <div className="lg:col-span-1">
          <DatasetUpload onUpload={handleUpload} isLoading={isRunning} />
        </div>

        {/* Center Panel - Inspector Results */}
        <div className="lg:col-span-1">
          <InspectorResults stats={pipelineStatus?.dataset_stats} />
        </div>

        {/* Right Panel - Agent Logs */}
        <div className="lg:col-span-1">
          <AgentLogs logs={logs} />
        </div>
      </div>

      {/* Pipeline Progress */}
      {isRunning && (
        <div className="glass rounded-xl p-6">
          <div className="flex items-center space-x-3">
            <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full" />
            <span className="text-lg">
              Pipeline Running: <span className="text-blue-400">{pipelineStatus?.current_stage}</span>
            </span>
          </div>
        </div>
      )}

      {/* Completion Message */}
      {pipelineStatus?.status === "completed" && (
        <div className="glass rounded-xl p-6 border-green-500/30 bg-green-500/10">
          <h3 className="text-xl font-semibold text-green-400 mb-2">
            ✓ Pipeline Completed Successfully!
          </h3>
          <p className="text-gray-300">
            Model ready for testing. Click "Test Trained Models" to evaluate your model.
          </p>
        </div>
      )}
    </div>
  );
}
