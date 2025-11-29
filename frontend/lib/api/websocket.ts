import { API_BASE_URL } from "./client";

export class WebSocketClient {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000;

    constructor(
        private onMessage: (data: any) => void,
        private onError?: (error: Event) => void
    ) { }

    connect() {
        const wsUrl = API_BASE_URL.replace("http", "ws");
        this.ws = new WebSocket(`${wsUrl}/ws/logs`);

        this.ws.onopen = () => {
            console.log("WebSocket connected");
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.onMessage(data);
            } catch (error) {
                console.error("Failed to parse WebSocket message:", error);
            }
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            if (this.onError) {
                this.onError(error);
            }
        };

        this.ws.onclose = () => {
            console.log("WebSocket disconnected");
            this.attemptReconnect();
        };
    }

    private attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
            setTimeout(() => this.connect(), this.reconnectDelay * this.reconnectAttempts);
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    send(data: any) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}
