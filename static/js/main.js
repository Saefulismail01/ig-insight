// Main Application
(function () {
    'use strict';

    function escapeHtml(value) {
        const str = value === null || value === undefined ? '' : String(value);
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function escapeAttr(value) {
        // For HTML attributes: escapeHtml + strip newlines
        return escapeHtml(value).replace(/\r?\n/g, ' ');
    }

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        console.log('📊 Instagram Analytics Dashboard Initialized');

        // Setup file upload
        setupFileUpload();

        // Setup drag and drop
        setupDragDrop();

    }

    function setupFileUpload() {
        const fileInput = document.getElementById('fileInput');
        fileInput.addEventListener('change', handleFileUpload);
    }

    function setupDragDrop() {
        const uploadArea = document.getElementById('uploadArea');

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('fileInput').files = files;
                handleFileUpload({ target: { files } });
            }
        });
    }


    async function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Validate file size
        if (file.size > CONFIG.MAX_FILE_SIZE) {
            UI.showError('File too large. Maximum size is 16MB.');
            return;
        }

        // Validate file type
        if (!file.name.endsWith('.csv')) {
            UI.showError('Please upload a CSV file.');
            return;
        }

        // Show loading
        UI.show('loadingIndicator');
        document.getElementById('uploadStatus').innerHTML = '';

        try {
            const result = await API.uploadFile(file);

            if (result.success) {
                STATE.dashboardData = result.data;
                STATE.uploadId = result.upload_id || null;
                if (STATE.uploadId) {
                    API.setUploadId(STATE.uploadId);
                }
                UI.showSuccess('File processed successfully!');
                showDashboard();
            } else {
                UI.showError(result.error || 'Error processing file');
            }
        } catch (error) {
            console.error('Upload error:', error);
            UI.showError('Connection error. Please try again.');
        } finally {
            UI.hide('loadingIndicator');
        }
    }

    function showDashboard() {
        UI.hide('uploadSection');
        UI.show('dashboardContent');

        // Hide header and show navigation bar
        UI.hide('mainHeader');
        UI.show('analysisNavbar');

        // Show drawdown toggle when dashboard is visible
        const drawdownToggle = document.getElementById('drawdownToggle');
        if (drawdownToggle) {
            drawdownToggle.style.display = 'flex';
        }

        // Dispatch event for navbar with date range
        const dateRange = STATE.dashboardData.date_range;
        document.dispatchEvent(new CustomEvent('dataUploaded', {
            detail: {
                dateRange: dateRange ? {
                    start: dateRange.start,
                    end: dateRange.end
                } : null
            }
        }));

        // Update UI with data
        UI.updateDateRange(STATE.dashboardData.date_range);
        UI.createKPICards(STATE.dashboardData);

        // Create main charts
        Charts.create.engagement(STATE.dashboardData.post_type_performance);
        Charts.create.hourly(STATE.dashboardData.optimal_posting_time);

        // Render advanced analytics
        UI.renderAdvancedAnalytics(STATE.dashboardData);

        // Load additional analysis
        loadContentTypeAnalysis();
        loadOutlierAnalysis();
        loadQualityAnalysis();
        loadCategoryAnalysis();
        loadDurationAnalysis();
    }

    function loadContentTypeAnalysis() {
        // Use pre-loaded data from STATE
        const data = STATE.dashboardData.post_type_performance ?
            { content_type_performance: STATE.dashboardData.post_type_performance } :
            null;

        if (data) {
            renderContentTypeAnalysis(data);
        } else {
            const container = document.getElementById('contentTypeAnalysis');
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No content type data available</p>';
        }
    }

    function loadOutlierAnalysis() {
        // Use pre-loaded data from STATE
        const data = STATE.dashboardData.outlier_analysis;

        if (data && !data.error) {
            renderOutlierAnalysis(data);
        } else {
            const container = document.getElementById('outlierAnalysis');
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No outlier data available</p>';
        }
    }

    async function loadQualityAnalysis() {
        // Use pre-loaded data from STATE (async signature kept for compatibility if needed, but logic is sync)
        const data = STATE.dashboardData.quality_analysis;

        if (data && !data.error) {
            renderQualityAnalysis(data);
        } else {
            const container = document.getElementById('qualityAnalysis');
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No quality analysis data available</p>';
        }
    }

    function loadFollowerTrend() {
        // Use pre-loaded data from STATE
        const data = STATE.dashboardData.follower_trend;

        if (data && !data.error && data.dates && data.dates.length > 0) {
            Charts.create.followerTrend(data, 'followerTrendChart');

            // Update insight layer
            const insightEl = document.getElementById('followerTrendInsight');
            if (insightEl && data.summary_insight) {
                insightEl.textContent = `💡 ${data.summary_insight}`;
            }
        } else {
            console.warn('Follower trend data missing or invalid', data);
        }
    }

    function loadCategoryAnalysis() {
        // Use pre-loaded data from STATE
        const data = STATE.dashboardData.category_analysis;

        if (data && !data.error) {
            renderCategoryAnalysis(data);
        } else {
            const container = document.getElementById('captionAnalysis');
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No category data available</p>';
        }
    }

    function loadDurationAnalysis() {
        // Use pre-loaded data from STATE
        const data = STATE.dashboardData.duration_analysis;

        if (data && !data.error) {
            renderDurationAnalysis(data);
        } else {
            const container = document.getElementById('durationAnalysis');
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No duration data available</p>';
        }
    }

    function renderContentTypeAnalysis(data) {
        const container = document.getElementById('contentTypeAnalysis');
        const contentTypes = Object.keys(data.content_type_performance || {});

        if (contentTypes.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No content type data available</p>';
            return;
        }

        container.innerHTML = `
            <div class="content-type-grid">
                <div class="analysis-card">
                    <h4>📊 Views per Type</h4>
                    <canvas id="ctViewsChart" style="max-height: 250px;"></canvas>
                </div>
                <div class="analysis-card">
                    <h4>💝 Likes per Type</h4>
                    <canvas id="ctLikesChart" style="max-height: 250px;"></canvas>
                </div>
                <div class="analysis-card">
                    <h4>💬 Comments per Type</h4>
                    <canvas id="ctCommentsChart" style="max-height: 250px;"></canvas>
                </div>
                
            </div>
        `;

        // Create charts
        Charts.create.contentType(data.content_type_performance, 'ctViewsChart', 'Views');
        Charts.create.contentType(data.content_type_performance, 'ctLikesChart', 'Likes');
        Charts.create.contentType(data.content_type_performance, 'ctCommentsChart', 'Comments');
    }


    function renderOutlierAnalysis(data) {
        const container = document.getElementById('outlierAnalysis');

        container.innerHTML = `
            <div class="engagement-gap">
                <h4>🔥 Key Insights</h4>
                <div class="engagement-stats">
                    <div class="engagement-stat">
                        <div class="stat-value">${data.top_5_avg_views.toLocaleString()}</div>
                        <div class="stat-label">Top 5 Avg Views</div>
                    </div>
                    <div class="engagement-stat">
                        <div class="stat-value">${data.bottom_5_avg_views.toLocaleString()}</div>
                        <div class="stat-label">Bottom 5 Avg Views</div>
                    </div>
                    <div class="engagement-stat">
                        <div class="stat-value">${data.views_multiplier.toFixed(1)}x</div>
                        <div class="stat-label">Views Multiplier</div>
                    </div>
                </div>
            </div>
            
            <div class="outlier-grid">
                <div class="outlier-section">
                    <h4 style="margin: 0 0 1.5rem 0; color: var(--success);">📈 Top 5 Performers</h4>
                    ${renderPosts(data.top_5_posts)}
                </div>
                <div class="outlier-section">
                    <h4 style="margin: 0 0 1.5rem 0; color: var(--danger);">📉 Bottom 5 Performers</h4>
                    ${renderPosts(data.bottom_5_posts)}
                </div>
            </div>
        `;
    }

    function renderPosts(posts) {
        return posts.map((post, idx) => {
            const postType = post['Post type'] || '';
            const postUrl = post.Permalink || post.URL || post.Link || '';

            // Detect category from description
            const desc = (post.Description || '').toLowerCase();
            let category = '';
            if (desc.includes('#news')) { category = '#news'; }
            else if (desc.includes('#meme')) { category = '#meme'; }
            else if (desc.includes('#insight')) { category = '#insight'; }
            else if (desc.includes('#edu')) { category = '#edu'; }

            const cardStyle = postUrl ? 'cursor: pointer;' : '';
            const safeUrl = postUrl ? escapeAttr(postUrl) : '';

            return `
                <div class="post-card" style="${cardStyle}" data-url="${safeUrl}" title="${postUrl ? 'Klik untuk membuka postingan' : ''}">
                    <div class="post-rank">${idx + 1}</div>
                    <div class="post-details">
                        <div class="post-title">${escapeHtml(post.short_description || 'No description')}</div>
                        <div class="post-meta" style="display: flex; gap: 0.5rem; align-items: center; margin-top: 0.5rem; color: var(--text-secondary); font-size: 0.85rem;">
                            <span>${new Date(post.Posted || post['Publish time']).toLocaleDateString('id-ID')}</span>
                            ${postType ? `<span>|</span><span>${escapeHtml(postType)}</span>` : ''}
                            ${category ? `<span>|</span><span>${escapeHtml(category)}</span>` : ''}
                        </div>
                    </div>
                    <div class="post-metrics">
                        <div class="post-engagement">${(post.Engagement_Rate || 0).toFixed(2)}%</div>
                        <div class="post-views">${(post.Views || 0).toLocaleString()} views</div>
                    </div>
                </div>
            `;
        }).join('');
    }


    function renderQualityAnalysis(data) {
        const container = document.getElementById('qualityAnalysis');

        container.innerHTML = `
            <div style="text-align: center; margin-bottom: 2rem;">
                <h4 style="margin: 0 0 1rem 0;">📊 Engagement Rate Analysis</h4>
                <div class="quality-score">${data.overall_avg_score}%</div>
                <p style="color: var(--text-secondary);">Average Engagement Rate across ${data.total_posts_analyzed} posts</p>
            </div>
            
            <div class="tier-distribution">
                ${Object.entries(data.tier_distribution).map(([tier, count]) => `
                    <div class="tier-card tier-${tier.toLowerCase()}">
                        <div style="font-weight: 700;">${tier}</div>
                        <div class="quality-score">${data.tier_percentages[tier] || 0}%</div>
                        <div style="font-size: 0.875rem;">${count} posts</div>
                    </div>
                `).join('')}
            </div>
            
            <div class="quality-insights">
                <h4>💡 Quality Insights</h4>
                <div id="qualityInsightsList" style="text-align: left; max-width: 600px; margin: 0 auto;">
                    ${data.quality_insights.map(insight => `
                        <div style="margin-bottom: 0.75rem; display: flex; gap: 0.75rem;">
                            <span>✨</span>
                            <span>${escapeHtml(insight)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div style="margin-top: 3rem; border-top: 1px solid var(--border); padding-top: 2rem;">
                <h4 style="margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                    📈 Follower Growth Analysis
                </h4>
                <div class="chart-container" style="height: 450px; background: white; border-radius: 16px; padding: 1.5rem; border: 1px solid var(--border);">
                    <canvas id="followerTrendChart"></canvas>
                </div>
            </div>
        `;

        // Load follower trend
        loadFollowerTrend();
    }

    function renderCategoryAnalysis(data) {
        const container = document.getElementById('captionAnalysis');

        if (!data.available) {
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No category data available</p>';
            return;
        }

        const categories = ['news', 'meme', 'insight', 'edu'];
        const icons = { news: '📰', meme: '😂', insight: '💡', edu: '📚' };
        const colors = { news: '#3b82f6', meme: '#f59e0b', insight: '#8b5cf6', edu: '#10b981' };
        const perf = data.category_performance;
        const counts = data.category_counts;

        container.innerHTML = `
            <!-- Insights -->
            ${data.insights && data.insights.length > 0 ? `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    ${data.insights.map(ins => `
                        <div style="padding: 1.25rem; border-radius: 12px; background: var(--bg-card); border-left: 4px solid var(--${ins.type === 'success' ? 'success' : ins.type === 'warning' ? 'warning' : 'info'});">
                            <div style="font-weight: 700; margin-bottom: 0.5rem;">${escapeHtml(ins.title)}</div>
                            <p style="margin: 0 0 0.5rem 0; color: var(--text-secondary); font-size: 0.9rem;">${escapeHtml(ins.message)}</p>
                            <p style="margin: 0; color: var(--primary); font-weight: 600; font-size: 0.875rem;">💡 ${escapeHtml(ins.recommendation)}</p>
                        </div>
                    `).join('')}
                </div>
            ` : ''}

            <!-- Category Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem;">
                ${categories.map(cat => {
            const p = perf[cat];
            const c = counts[cat];
            const icon = icons[cat];
            const color = colors[cat];

            return `
                        <div style="padding: 1.5rem; background: var(--bg-card); border-radius: 16px; border: 2px solid ${color}30;">
                            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                                <span style="font-size: 2rem;">${icon}</span>
                                <div>
                                    <h4 style="margin: 0; font-size: 1.25rem; color: ${color};">#${cat.toUpperCase()}</h4>
                                    <span style="font-size: 0.875rem; color: var(--text-tertiary);">${c.count} posts (${c.percentage}%)</span>
                                </div>
                            </div>
                            
                            <div style="display: grid; gap: 0.5rem; font-size: 0.9rem;">
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-secondary);">Avg Views</span>
                                    <strong>${Number(p.avg_views).toLocaleString()}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-secondary);">Avg Likes</span>
                                    <strong>${Number(p.avg_likes).toLocaleString()}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-secondary);">Avg Comments</span>
                                    <strong>${p.avg_comments}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-secondary);">Avg Shares</span>
                                    <strong>${p.avg_shares}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-secondary);">Avg Saves</span>
                                    <strong>${p.avg_saves}</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                                    <span style="color: var(--text-secondary);">Engagement Rate</span>
                                    <strong>${p.avg_engagement_rate}%</strong>
                                </div>
                            </div>
                        </div>
                    `;
        }).join('')}
            </div>
        `;
    }


    function renderDurationAnalysis(data) {
        const container = document.getElementById('durationAnalysis');

        if (!data.available) {
            container.innerHTML = `<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">${escapeHtml(data.message || 'Duration data not available')}</p>`;
            return;
        }

        const sweet = data.sweet_spot;
        const dist = data.distribution;

        container.innerHTML = `
            <!-- Sweet Spot Highlight -->
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, var(--primary-light) 0%, var(--card-bg) 100%); border-radius: 12px; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
                <h3 style="margin: 0 0 1rem 0; color: var(--primary); display: block;">Sweet Spot Detected!</h3>
                <div style="font-size: 2.5rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">
                    ${sweet.range_start}-${sweet.range_end} seconds
                </div>
                <p style="color: var(--text-secondary); margin: 0.5rem 0;">${sweet.recommendation}</p>
                <div style="display: flex; gap: 2rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: var(--success);">${sweet.avg_engagement_rate.toFixed(2)}%</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">Engagement Rate</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary);">${sweet.avg_views.toLocaleString()}</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">Avg Views</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: 700;">${sweet.post_count}</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">Posts in Range</div>
                    </div>
                </div>
            </div>
            
            <!-- Insights -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                ${data.insights.map(insight => `
                    <div style="padding: 1.5rem; border-radius: 12px; background: var(--card-bg); border-left: 4px solid var(--${insight.type === 'success' ? 'success' :
                insight.type === 'warning' ? 'warning' : 'info'
            });">
                        <div style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">${escapeHtml(insight.title)}</div>
                        <p style="margin: 0.5rem 0; color: var(--text-secondary); font-size: 0.95rem;">${escapeHtml(insight.message)}</p>
                        <p style="margin: 0.5rem 0; font-weight: 600; color: var(--primary); font-size: 0.9rem;">${escapeHtml(insight.recommendation)}</p>
                    </div>
                `).join('')}
            </div>
            
            <!-- Statistics -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--primary);">${dist.avg_duration.toFixed(1)}s</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">Average Duration</div>
                </div>
                <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--success);">${dist.median_duration.toFixed(1)}s</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">Median Duration</div>
                </div>
                <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700;">${dist.min_duration.toFixed(0)}s</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">Shortest</div>
                </div>
                <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px; text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700;">${dist.max_duration.toFixed(0)}s</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">Longest</div>
                </div>
            </div>
            
            <!-- Duration Buckets -->
            ${data.bucket_analysis && data.bucket_analysis.buckets ? `
                <div style="margin-top: 2rem;">
                    <h4 style="margin-bottom: 1rem;">📊 Performance by Duration Range</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem;">
                        ${data.bucket_analysis.buckets.map(bucket => `
                            <div style="padding: 1rem; background: var(--card-bg); border-radius: 8px; ${bucket.duration_range === data.bucket_analysis.best_bucket ? 'border: 2px solid var(--primary);' : 'border: 1px solid var(--border);'}">
                                <div style="font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                                    <span>${bucket.duration_range}</span>
                                    ${bucket.duration_range === data.bucket_analysis.best_bucket ? '<span style="font-size: 1.25rem;">👑</span>' : ''}
                                </div>
                                <div style="font-size: 0.875rem; color: var(--text-secondary);">
                                    <div>ER: <strong style="color: var(--text-primary);">${bucket.avg_engagement_rate.toFixed(2)}%</strong></div>
                                    <div>Views: <strong style="color: var(--text-primary);">${bucket.avg_views.toLocaleString()}</strong></div>
                                    <div>Posts: <strong style="color: var(--text-primary);">${bucket.post_count}</strong></div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Optimal by Metric -->
            ${data.optimal_by_metric ? `
                <div style="margin-top: 2rem;">
                    <h4 style="margin-bottom: 1rem;">🎯 Optimal Duration by Metric</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">
                        ${Object.entries(data.optimal_by_metric).map(([metric, data]) => `
                            <div style="padding: 1rem; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border);">
                                <div style="font-weight: 700; text-transform: capitalize; margin-bottom: 0.5rem;">${metric}</div>
                                <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary);">${data.optimal_duration}s</div>
                                <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">
                                    Avg: ${typeof data.avg_value === 'number' ? data.avg_value.toFixed(2) : data.avg_value}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        `;
    }
})();
