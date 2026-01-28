// UI Helper Functions
const UI = {
    escapeHtml(value) {
        const str = value === null || value === undefined ? '' : String(value);
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    },

    show(elementId) {
        const element = document.getElementById(elementId);
        if (element) element.classList.remove('hidden');
    },

    hide(elementId) {
        const element = document.getElementById(elementId);
        if (element) element.classList.add('hidden');
    },

    showSuccess(message) {
        const status = document.getElementById('uploadStatus');
        const safe = this.escapeHtml(message);
        status.innerHTML = `<div class="status-message status-success">✅ ${safe}</div>`;
    },

    showError(message) {
        const status = document.getElementById('uploadStatus');
        const safe = this.escapeHtml(message);
        status.innerHTML = `<div class="status-message status-error">❌ ${safe}</div>`;
    },

    updateDateRange(dateRange) {
        if (dateRange.start && dateRange.end) {
            const start = new Date(dateRange.start).toLocaleDateString('id-ID');
            const end = new Date(dateRange.end).toLocaleDateString('id-ID');
            document.getElementById('dateRange').textContent = `${start} - ${end}`;
        }
    },

    createKPICards(data) {
        const kpiData = [
            {
                icon: '📝',
                label: 'Total Posts',
                value: data.total_posts.toLocaleString(),
                gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
            },
            {
                icon: '💝',
                label: 'Engagement Rate',
                value: `${(data.content_performance.avg_engagement_rate || 0).toFixed(2)}%`,
                gradient: 'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)'
            },
            {
                icon: '🎬',
                label: 'Best Format',
                value: data.best_post_type || 'N/A',
                gradient: 'linear-gradient(135deg, #3b82f6 0%, #2dd4bf 100%)'
            },
            {
                icon: '🔥',
                label: 'Viral Posts',
                value: data.content_performance.viral_posts_count || 0,
                gradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
            }
        ];

        const grid = document.getElementById('kpiGrid');
        grid.innerHTML = kpiData.map(kpi => `
            <div class="kpi-card">
                <div class="kpi-icon" style="background: ${kpi.gradient};">
                    ${kpi.icon}
                </div>
                <div class="kpi-label">${kpi.label}</div>
                <div class="kpi-value">${kpi.value}</div>
            </div>
        `).join('');
    },

    renderAdvancedAnalytics(data) {
        const container = document.getElementById('advancedAnalytics');

        container.innerHTML = `
            <div style="margin-bottom: 2rem;">
                <h4 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--text-primary);">📅 Best Days to Post</h4>
                <div class="chart-container" style="height: 300px;">
                    <canvas id="dayOfWeekChart"></canvas>
                </div>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <h4 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--text-primary);">💡 Key Insights</h4>
                <div id="insightsList" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;"></div>
            </div>
        `;

        // Create day of week chart
        if (data.optimal_posting_time?.daily_performance) {
            Charts.create.dayOfWeek(data.optimal_posting_time.daily_performance, 'dayOfWeekChart');
        }

        // Create insights
        this.renderInsights(data);
    },

    renderInsights(data) {
        const container = document.getElementById('insightsList');
        const insights = [];

        if (data.optimal_posting_time?.best_hour) {
            insights.push({
                icon: '⏰',
                title: 'Best Time to Post',
                value: `${data.optimal_posting_time.best_hour}:00`,
                description: 'Highest engagement rate'
            });
        }

        if (data.optimal_posting_time?.best_day) {
            insights.push({
                icon: '📅',
                title: 'Best Day to Post',
                value: data.optimal_posting_time.best_day,
                description: 'Most active audience'
            });
        }

        if (data.best_post_type) {
            insights.push({
                icon: '🎯',
                title: 'Top Content Format',
                value: data.best_post_type,
                description: 'Highest performing type'
            });
        }

        // Only display the first 3 insights
        const displayInsights = insights.slice(0, 3);

        container.innerHTML = displayInsights.map(insight => `
            <div style="
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 2rem 1.5rem;
                transition: all 0.3s ease;
                cursor: pointer;
                text-align: center;
                box-shadow: var(--shadow-sm);
            " onmouseover="this.style.borderColor='var(--primary)'; this.style.transform='translateY(-6px)'; this.style.boxShadow='var(--shadow-lg)'"
               onmouseout="this.style.borderColor='var(--border)'; this.style.transform='translateY(0)'; this.style.boxShadow='var(--shadow-sm)'">
                <div style="font-size: 3rem; margin-bottom: 1rem;">${this.escapeHtml(insight.icon)}</div>
                <div style="font-size: 0.75rem; color: var(--text-tertiary); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">
                    ${this.escapeHtml(insight.title)}
                </div>
                <div style="font-size: 2rem; font-weight: 900; margin-bottom: 0.5rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    ${this.escapeHtml(insight.value)}
                </div>
                <div style="font-size: 0.875rem; color: var(--text-secondary); font-weight: 500;">
                    ${this.escapeHtml(insight.description)}
                </div>
            </div>
        `).join('');
    }
};
