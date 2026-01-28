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
        const data = await response.json();
        console.log('🔍 Follower Trend API Response:', data);
        
        // Fallback: if daily_views is missing, use daily_follows as placeholder
        if (!data.daily_views && data.daily_follows) {
            console.warn('⚠️ daily_views missing! Server needs restart. Using daily_follows as fallback.');
            data.daily_views = data.daily_follows.map(() => 0);
        }
        
        console.log('📊 Daily Views:', data.daily_views);
        console.log('👥 Cumulative Followers:', data.cumulative_followers);
        return data;
    },

    async getCategoryAnalysis() {
        const response = await fetch('/category-analysis');
        return await response.json();
    },

    async getDurationAnalysis() {
        const response = await fetch('/duration-analysis');
        return await response.json();
    },

};
