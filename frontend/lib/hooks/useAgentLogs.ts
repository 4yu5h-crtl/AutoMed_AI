"use client";

import { useState, useEffect } from "react";
import { WebSocketClient } from "../api/websocket";
import { AgentLog } from "../types/agent";

export function useAgentLogs() {
    const [logs, setLogs] = useState<AgentLog[]>([]);

    useEffect(() => {
        const client = new WebSocketClient(
            (data: AgentLog) => {
                setLogs((prev) => [...prev, data]);
            },
            (error) => {
                console.error("WebSocket error:", error);
            }
        );

        client.connect();

        return () => {
            client.disconnect();
        };
    }, []);

    const clearLogs = () => setLogs([]);

    return {
        logs,
        clearLogs,
    };
}
