const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient = {
    async get<T>(endpoint: string): Promise<T> {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            let errorMessage = response.statusText;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
            } catch (e) {
                // Ignore JSON parse error
            }
            throw new Error(`API error: ${errorMessage}`);
        }
        return response.json();
    },

    async post<T>(endpoint: string, data?: any): Promise<T> {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: data ? JSON.stringify(data) : undefined,
        });
        if (!response.ok) {
            let errorMessage = response.statusText;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
            } catch (e) {
                // Ignore JSON parse error
            }
            throw new Error(`API error: ${errorMessage}`);
        }
        return response.json();
    },

    getDownloadUrl(endpoint: string): string {
        return `${API_BASE_URL}${endpoint}`;
    },
};

export { API_BASE_URL };
