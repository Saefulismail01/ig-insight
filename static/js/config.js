// Configuration
const CONFIG = {
    API_BASE_URL: '',
    MAX_FILE_SIZE: 16 * 1024 * 1024, // 16MB
    CHART_COLORS: {
        primary: 'rgba(99, 102, 241, 0.8)',
        secondary: 'rgba(139, 92, 246, 0.8)',
        accent: 'rgba(236, 72, 153, 0.8)',
        success: 'rgba(16, 185, 129, 0.8)',
        warning: 'rgba(245, 158, 11, 0.8)',
        danger: 'rgba(239, 68, 68, 0.8)',
        info: 'rgba(59, 130, 246, 0.8)',
    },
    CHART_OPTIONS: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#cbd5e1',
                    font: {
                        family: 'Inter',
                        size: 12,
                        weight: '600'
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)'
                },
                ticks: {
                    color: '#94a3b8',
                    font: {
                        family: 'Inter',
                        size: 11
                    }
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: '#94a3b8',
                    font: {
                        family: 'Inter',
                        size: 11
                    }
                }
            }
        }
    }
};

// Global state
const STATE = {
    dashboardData: null,
    charts: {},
    currentPage: 1
};
