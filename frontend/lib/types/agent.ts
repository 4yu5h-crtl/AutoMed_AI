export interface AgentLog {
    timestamp: string;
    agent: string;
    message: string;
    level: "info" | "warning" | "error";
}
