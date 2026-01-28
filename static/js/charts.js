// Chart Management
const Charts = {
    create: {
        engagement(data) {
            const ctx = document.getElementById('engagementChart').getContext('2d');
            const labels = Object.keys(data);
            const values = labels.map(type => data[type].Engagement_Rate || 0);

            if (STATE.charts.engagement) {
                STATE.charts.engagement.destroy();
            }

            STATE.charts.engagement = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Engagement Rate (%)',
                        data: values,
                        backgroundColor: [
                            CONFIG.CHART_COLORS.primary,
                            CONFIG.CHART_COLORS.secondary,
                            CONFIG.CHART_COLORS.accent
                        ],
                        borderRadius: 12,
                        borderWidth: 0
                    }]
                },
                options: {
                    ...CONFIG.CHART_OPTIONS,
                    plugins: {
                        ...CONFIG.CHART_OPTIONS.plugins,
                        legend: { display: false }
                    }
                }
            });
        },

        hourly(data) {
            const ctx = document.getElementById('hourlyChart').getContext('2d');
            const hourlyData = data.hourly_performance;

            const hours = Object.keys(hourlyData.Engagement_Rate || {}).map(h => `${h}:00`);
            const values = Object.values(hourlyData.Engagement_Rate || {});

            if (STATE.charts.hourly) {
                STATE.charts.hourly.destroy();
            }

            STATE.charts.hourly = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: hours,
                    datasets: [{
                        label: 'Engagement Rate (%)',
                        data: values,
                        borderColor: CONFIG.CHART_COLORS.primary,
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: CONFIG.CHART_COLORS.primary,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    ...CONFIG.CHART_OPTIONS,
                    plugins: {
                        ...CONFIG.CHART_OPTIONS.plugins,
                        legend: { display: false }
                    }
                }
            });
        },

        dayOfWeek(data, canvasId) {
            const ctx = document.getElementById(canvasId).getContext('2d');
            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            const engagementRates = days.map(day => data.Engagement_Rate?.[day] || 0);

            return new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: days,
                    datasets: [{
                        label: 'Engagement Rate (%)',
                        data: engagementRates,
                        backgroundColor: CONFIG.CHART_COLORS.primary,
                        borderRadius: 12,
                        borderWidth: 0
                    }]
                },
                options: {
                    ...CONFIG.CHART_OPTIONS,
                    plugins: {
                        ...CONFIG.CHART_OPTIONS.plugins,
                        legend: { display: false }
                    }
                }
            });
        },

        contentType(contentTypeData, canvasId, metric) {
            const ctx = document.getElementById(canvasId).getContext('2d');
            const types = Object.keys(contentTypeData);
            const colors = [
                CONFIG.CHART_COLORS.primary,
                CONFIG.CHART_COLORS.success,
                CONFIG.CHART_COLORS.warning,
                CONFIG.CHART_COLORS.accent,
                CONFIG.CHART_COLORS.danger,
                CONFIG.CHART_COLORS.info
            ];

            const values = types.map(type => contentTypeData[type][metric] || 0);

            return new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: types,
                    datasets: [{
                        label: `Avg ${metric}`,
                        data: values,
                        backgroundColor: colors,
                        borderRadius: 12,
                        borderWidth: 0
                    }]
                },
                options: {
                    ...CONFIG.CHART_OPTIONS,
                    plugins: {
                        ...CONFIG.CHART_OPTIONS.plugins,
                        legend: { display: false }
                    },
                    scales: {
                        ...CONFIG.CHART_OPTIONS.scales,
                        y: {
                            ...CONFIG.CHART_OPTIONS.scales.y,
                            ticks: {
                                ...CONFIG.CHART_OPTIONS.scales.y.ticks,
                                callback: function (value) {
                                    return value.toLocaleString('id-ID');
                                }
                            }
                        }
                    }
                }
            });
        },

        doughnut(labels, data, canvasId) {
            const ctx = document.getElementById(canvasId).getContext('2d');
            const colors = [
                CONFIG.CHART_COLORS.primary,
                CONFIG.CHART_COLORS.success,
                CONFIG.CHART_COLORS.warning,
                CONFIG.CHART_COLORS.accent,
                CONFIG.CHART_COLORS.danger,
                CONFIG.CHART_COLORS.info
            ];

            return new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: {
                                    family: 'Inter',
                                    size: 12,
                                    weight: '600'
                                },
                                color: '#cbd5e1'
                            }
                        }
                    }
                }
            });
        },

        followerTrend(data, canvasId) {
            const ctx = document.getElementById(canvasId).getContext('2d');

            // Find growth phases if provided
            const annotations = {};

            // 1. Strategy Change Annotation
            if (data.strategy_change_date) {
                annotations.strategyLine = {
                    type: 'line',
                    mode: 'vertical',
                    scaleID: 'x',
                    value: data.strategy_change_date,
                    borderColor: '#6366f1',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    label: {
                        display: true,
                        content: 'Content Strategy Change',
                        position: 'start',
                        backgroundColor: 'rgba(99, 102, 241, 0.9)',
                        color: '#fff',
                        font: { size: 11, weight: 'bold' },
                        padding: 6,
                        yAdjust: -20
                    }
                };
            }

            // 2. Growth Phase Annotations (Box highlights)
            if (data.phases) {
                data.phases.forEach((phase, index) => {
                    annotations[`phaseBox${index}`] = {
                        type: 'box',
                        xMin: phase.start_date,
                        xMax: phase.end_date,
                        backgroundColor: phase.color,
                        borderWidth: 0,
                        drawTime: 'beforeDatasetsDraw',
                        label: {
                            display: true,
                            content: phase.name,
                            position: { x: 'center', y: 'start' },
                            color: 'rgba(71, 85, 105, 0.8)',
                            font: { size: 10, weight: 'bold', style: 'italic' },
                            yAdjust: 10
                        }
                    };
                });
            }

            return new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [
                        {
                            label: '👥 Cumulative Followers',
                            data: data.cumulative_followers,
                            borderColor: '#6366f1',
                            backgroundColor: 'rgba(99, 102, 241, 0.35)', // 35% opacity as requested
                            borderWidth: 3,
                            fill: true,
                            tension: 0.3,
                            yAxisID: 'y',
                            pointRadius: 0, // Cleaner look, emphasis on trend
                            pointHoverRadius: 6,
                            zIndex: 10
                        },
                        {
                            label: '👁️ Daily Views (Secondary)',
                            data: data.daily_views,
                            borderColor: '#f59e0b', // Specific orange/amber color for visibility
                            backgroundColor: 'transparent',
                            borderWidth: 2, // Slightly thicker
                            borderDash: [5, 5],
                            fill: false,
                            tension: 0.4,
                            yAxisID: 'y1',
                            pointRadius: 2, // Re-enable small points for better tracking
                            pointHoverRadius: 5,
                            zIndex: 20 // Bring to very front
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                            align: 'end',
                            labels: {
                                usePointStyle: true,
                                padding: 15,
                                font: { family: 'Inter', size: 11, weight: '600' },
                                color: '#475569'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(255, 255, 255, 0.98)',
                            titleColor: '#0f172a',
                            bodyColor: '#475569',
                            borderColor: '#e2e8f0',
                            borderWidth: 1,
                            padding: 12,
                            boxPadding: 4,
                            usePointStyle: true,
                            callbacks: {
                                label: function (context) {
                                    return ` ${context.dataset.label.split(' (')[0]}: ${context.parsed.y.toLocaleString('id-ID')}`;
                                }
                            }
                        },
                        annotation: {
                            annotations: annotations
                        }
                    },
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            beginAtZero: false,
                            grid: { color: 'rgba(0, 0, 0, 0.03)', drawBorder: false },
                            ticks: {
                                color: '#64748b',
                                font: { size: 10, weight: '600' },
                                callback: value => value >= 1000 ? (value / 1000).toFixed(1) + 'k' : value
                            },
                            title: {
                                display: true,
                                text: 'Total Followers',
                                color: '#6366f1',
                                font: { weight: '700', size: 11 }
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            beginAtZero: true,
                            grid: { drawOnChartArea: false, drawBorder: false },
                            ticks: {
                                color: '#94a3b8',
                                font: { size: 10 },
                                callback: value => value >= 1000 ? (value / 1000).toFixed(1) + 'k' : value
                            },
                            title: {
                                display: true,
                                text: 'Daily Views',
                                color: '#94a3b8',
                                font: { weight: '700', size: 11 }
                            }
                        },
                        x: {
                            grid: { display: false },
                            ticks: {
                                color: '#94a3b8',
                                maxRotation: 0,
                                autoSkip: true,
                                maxTicksLimit: 8, // Reduced density as requested
                                font: { size: 10 }
                            }
                        }
                    }
                }
            });
        }
    },

    destroy(chartName) {
        if (STATE.charts[chartName]) {
            STATE.charts[chartName].destroy();
            delete STATE.charts[chartName];
        }
    },

    destroyAll() {
        Object.keys(STATE.charts).forEach(chartName => {
            this.destroy(chartName);
        });
    }
};
