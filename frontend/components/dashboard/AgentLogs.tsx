"use client";

import { AgentLog } from "@/lib/types/agent";
import { useEffect, useRef } from "react";

interface AgentLogsProps {
    logs: AgentLog[];
}

export default function AgentLogs({ logs }: AgentLogsProps) {
    const logsEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [logs]);

    return (
        <div className="card-panel p-6 h-[600px] flex flex-col">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-secondary">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                </span>
                Live Agent Activity
            </h2>

            <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                {logs.length === 0 ? (
                    <div className="text-center text-muted-foreground py-10">
                        Waiting for pipeline to start...
                    </div>
                ) : (
                    logs.map((log, index) => (
                        <div key={index} className="log-entry animate-fade-in">
                            <div className="flex justify-between items-start mb-1">
                                <span className="text-xs font-mono text-primary">
                                    {new Date(log.timestamp).toLocaleTimeString()}
                                </span>
                                <span className={`text-xs px-2 py-0.5 rounded-full border ${log.level === 'error'
                                        ? 'border-destructive text-destructive bg-destructive/10'
                                        : 'border-secondary text-secondary bg-secondary/10'
                                    }`}>
                                    {log.agent}
                                </span>
                            </div>
                            <p className="text-sm text-muted-foreground">{log.message}</p>
                        </div>
                    ))
                )}
                <div ref={logsEndRef} />
            </div>
        </div>
    );
}
