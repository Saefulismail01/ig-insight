// API Functions
const API = {
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    },

    async getContentTypeAnalysis() {
        const response = await fetch('/content-type-analysis');
        return await response.json();
    },

    async getOutlierAnalysis() {
        const response = await fetch('/outlier-analysis');
        return await response.json();
    },

    async getQualityAnalysis() {
        const response = await fetch('/quality-analysis');
        return await response.json();
    },

    async getFollowerTrend() {
        const response = await fetch('/follower-trend');
        return await response.json();
    },

    async getCaptionAnalysis() {
        const response = await fetch('/caption-analysis');
        return await response.json();
    },

    async getDurationAnalysis() {
        const response = await fetch('/duration-analysis');
        return await response.json();
    },

    async sendChatMessage(message, history) {
        const response = await fetch('/ai-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_history: history
            })
        });

        return await response.json();
    }
};
