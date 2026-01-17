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
                                callback: function(value) {
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

            return new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [
                        {
                            label: 'Cumulative Followers',
                            data: data.cumulative_followers,
                            borderColor: CONFIG.CHART_COLORS.primary,
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            yAxisID: 'y',
                            pointRadius: 3,
                            pointHoverRadius: 6,
                            pointBackgroundColor: CONFIG.CHART_COLORS.primary,
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2
                        },
                        {
                            label: 'Daily Follows',
                            data: data.daily_follows,
                            borderColor: CONFIG.CHART_COLORS.success,
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderWidth: 3,
                            fill: false,
                            tension: 0.4,
                            yAxisID: 'y1',
                            pointRadius: 3,
                            pointHoverRadius: 6,
                            pointBackgroundColor: CONFIG.CHART_COLORS.success,
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2
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
                                font: {
                                    family: 'Inter',
                                    size: 12,
                                    weight: '600'
                                },
                                color: '#cbd5e1'
                            }
                        }
                    },
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)'
                            },
                            ticks: {
                                color: '#94a3b8',
                                callback: function(value) {
                                    return value >= 1000 ? (value/1000).toFixed(1) + 'k' : value.toLocaleString();
                                }
                            },
                            title: {
                                display: true,
                                text: 'Cumulative',
                                color: '#cbd5e1'
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            beginAtZero: true,
                            grid: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                color: '#94a3b8',
                                callback: function(value) {
                                    return value >= 1000 ? (value/1000).toFixed(1) + 'k' : value.toLocaleString();
                                }
                            },
                            title: {
                                display: true,
                                text: 'Daily',
                                color: '#cbd5e1'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: '#94a3b8',
                                maxRotation: 45,
                                minRotation: 0
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
