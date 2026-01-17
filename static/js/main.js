// Main Application
(function() {
    'use strict';

    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        console.log('📊 Instagram Analytics Dashboard Initialized');
        
        // Initialize chat widget
        Chat.init();
        
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
        UI.show('downloadSection');
        
        // Show navigation bar
        document.getElementById('analysisNavbar').classList.remove('hidden');
        
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
        loadCaptionAnalysis();
        loadDurationAnalysis();
    }

    async function loadContentTypeAnalysis() {
        const container = document.getElementById('contentTypeAnalysis');
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Loading content type analysis...</p>';
        
        try {
            const data = await API.getContentTypeAnalysis();
            if (data.error) throw new Error(data.error);
            
            renderContentTypeAnalysis(data);
        } catch (error) {
            container.innerHTML = `<p style="color: var(--danger); text-align: center; padding: 2rem;">❌ ${error.message}</p>`;
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

    async function loadOutlierAnalysis() {
        const container = document.getElementById('outlierAnalysis');
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Loading outlier analysis...</p>';
        
        try {
            const data = await API.getOutlierAnalysis();
            if (data.error) throw new Error(data.error);
            
            renderOutlierAnalysis(data);
        } catch (error) {
            container.innerHTML = `<p style="color: var(--danger); text-align: center; padding: 2rem;">❌ ${error.message}</p>`;
        }
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
            const postType = post['Post type'] || 'Unknown';
            const badgeClass = postType.toLowerCase().includes('reel') ? 'badge-reel' : 
                              postType.toLowerCase().includes('carousel') ? 'badge-carousel' : 'badge-image';
            
            return `
                <div class="post-card">
                    <div class="post-rank">${idx + 1}</div>
                    <div class="post-details">
                        <div class="post-title">
                            ${post.short_description || 'No description'}
                            ${postType !== 'Unknown' ? `<span class="badge ${badgeClass}">${postType}</span>` : ''}
                        </div>
                        <div class="post-date">${new Date(post.Posted || post['Publish time']).toLocaleDateString('id-ID')}</div>
                    </div>
                    <div class="post-metrics">
                        <div class="post-engagement">${(post.Engagement_Rate || 0).toFixed(2)}%</div>
                        <div class="post-views">${(post.Views || 0).toLocaleString()} views</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    async function loadQualityAnalysis() {
        const container = document.getElementById('qualityAnalysis');
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Loading quality analysis...</p>';
        
        try {
            const data = await API.getQualityAnalysis();
            if (data.error) throw new Error(data.error);
            
            renderQualityAnalysis(data);
        } catch (error) {
            container.innerHTML = `<p style="color: var(--danger); text-align: center; padding: 2rem;">❌ ${error.message}</p>`;
        }
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
                <ul>
                    ${data.quality_insights.map(insight => `<li>${insight}</li>`).join('')}
                </ul>
            </div>
            
            <div style="margin-top: 2rem;">
                <h4 style="margin-bottom: 1rem;">📈 Follower Trend</h4>
                <div class="chart-container" style="height: 400px;">
                    <canvas id="followerTrendChart"></canvas>
                </div>
            </div>
        `;

        // Load follower trend
        loadFollowerTrend();
    }

    async function loadFollowerTrend() {
        try {
            const data = await API.getFollowerTrend();
            if (data.error) throw new Error(data.error);
            
            if (data.dates && data.dates.length > 0) {
                Charts.create.followerTrend(data, 'followerTrendChart');
            }
        } catch (error) {
            console.error('Error loading follower trend:', error);
        }
    }

    async function loadCaptionAnalysis() {
        const container = document.getElementById('captionAnalysis');
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Loading caption analysis...</p>';
        
        try {
            const data = await API.getCaptionAnalysis();
            if (data.error) throw new Error(data.error);
            
            renderCaptionAnalysis(data);
        } catch (error) {
            container.innerHTML = `<p style="color: var(--danger); text-align: center; padding: 2rem;">❌ ${error.message}</p>`;
        }
    }

    function renderCaptionAnalysis(data) {
        const container = document.getElementById('captionAnalysis');
        
        // Check if data is available
        if (!data.hashtag_analysis) {
            container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No caption data available for analysis</p>';
            return;
        }
        
        const hashtag = data.hashtag_analysis;
        const length = data.length_analysis;
        const emoji = data.emoji_analysis;
        const cta = data.cta_analysis;
        
        container.innerHTML = `
            <!-- Insights Cards -->
            <div class="insight-cards" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                ${data.insights.map(insight => `
                    <div class="insight-card" style="padding: 1.5rem; border-radius: 12px; background: var(--card-bg); border-left: 4px solid var(--${
                        insight.type === 'success' ? 'success' : 
                        insight.type === 'warning' ? 'warning' : 'info'
                    });">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">${insight.title}</div>
                        <p style="margin: 0.5rem 0; color: var(--text-secondary);">${insight.message}</p>
                        <p style="margin: 0.5rem 0; font-weight: 600; color: var(--primary);">${insight.recommendation}</p>
                    </div>
                `).join('')}
            </div>
            
            <!-- Analysis Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
                <!-- Hashtag Performance -->
                <div class="analysis-section" style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px;">
                    <h4 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                        <span>🏷️</span> Hashtag Performance
                    </h4>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>With Hashtags ER:</span>
                        <strong>${hashtag.avg_er_with_hashtags.toFixed(2)}%</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>Without Hashtags ER:</span>
                        <strong>${hashtag.avg_er_without_hashtags.toFixed(2)}%</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0;">
                        <span>Performance Lift:</span>
                        <strong style="color: ${hashtag.performance_lift > 0 ? 'var(--success)' : 'var(--danger)'}">
                            ${hashtag.performance_lift > 0 ? '+' : ''}${hashtag.performance_lift.toFixed(2)}%
                        </strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; background: var(--primary-light); margin-top: 1rem; padding: 1rem; border-radius: 8px;">
                        <span style="font-weight: 600;">Optimal Count:</span>
                        <strong style="font-size: 1.25rem; color: var(--primary);">${hashtag.optimal_hashtag_count} hashtags</strong>
                    </div>
                </div>
                
                <!-- Caption Length -->
                <div class="analysis-section" style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px;">
                    <h4 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                        <span>📝</span> Caption Length
                    </h4>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>Average Words:</span>
                        <strong>${length.avg_word_count.toFixed(0)} words</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>Median Words:</span>
                        <strong>${length.median_word_count.toFixed(0)} words</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; background: var(--primary-light); margin-top: 1rem; padding: 1rem; border-radius: 8px;">
                        <span style="font-weight: 600;">Best Performing:</span>
                        <strong style="font-size: 1.25rem; color: var(--primary);">${length.optimal_length}</strong>
                    </div>
                </div>
                
                <!-- Emoji Usage -->
                <div class="analysis-section" style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px;">
                    <h4 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                        <span>😊</span> Emoji Impact
                    </h4>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>With Emoji ER:</span>
                        <strong>${emoji.avg_er_with_emoji.toFixed(2)}%</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>Without Emoji ER:</span>
                        <strong>${emoji.avg_er_without_emoji.toFixed(2)}%</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0;">
                        <span>Performance Lift:</span>
                        <strong style="color: ${emoji.performance_lift > 0 ? 'var(--success)' : 'var(--danger)'}">
                            ${emoji.performance_lift > 0 ? '+' : ''}${emoji.performance_lift.toFixed(2)}%
                        </strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; background: var(--primary-light); margin-top: 1rem; padding: 1rem; border-radius: 8px;">
                        <span style="font-weight: 600;">Optimal Count:</span>
                        <strong style="font-size: 1.25rem; color: var(--primary);">${emoji.optimal_emoji_count} emojis</strong>
                    </div>
                </div>
                
                <!-- CTA Impact -->
                <div class="analysis-section" style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px;">
                    <h4 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                        <span>📢</span> Call-to-Action
                    </h4>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>With CTA ER:</span>
                        <strong>${cta.avg_er_with_cta.toFixed(2)}%</strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border);">
                        <span>Comment Lift:</span>
                        <strong style="color: ${cta.comment_lift > 0 ? 'var(--success)' : 'var(--danger)'}">
                            ${cta.comment_lift > 0 ? '+' : ''}${cta.comment_lift.toFixed(1)} comments
                        </strong>
                    </div>
                    <div class="stat-row" style="display: flex; justify-content: space-between; padding: 0.75rem 0; background: var(--primary-light); margin-top: 1rem; padding: 1rem; border-radius: 8px;">
                        <span style="font-weight: 600;">Posts with CTA:</span>
                        <strong style="font-size: 1.25rem; color: var(--primary);">${cta.posts_with_cta} posts</strong>
                    </div>
                </div>
            </div>
            
            <!-- Top Hashtags -->
            ${hashtag.top_hashtags && hashtag.top_hashtags.length > 0 ? `
                <div style="margin-top: 2rem;">
                    <h4 style="margin-bottom: 1rem;">🏆 Top Performing Hashtags</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem;">
                        ${hashtag.top_hashtags.slice(0, 6).map((tag, idx) => `
                            <div style="padding: 1rem; background: var(--card-bg); border-radius: 8px; border-left: 3px solid var(--primary);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                    <span style="font-weight: 700; color: var(--primary); font-size: 1.1rem;">${tag.hashtag}</span>
                                    <span style="background: var(--primary-light); color: var(--primary); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">#${idx + 1}</span>
                                </div>
                                <div style="font-size: 0.875rem; color: var(--text-secondary);">
                                    <div>ER: <strong>${tag.avg_engagement_rate.toFixed(2)}%</strong></div>
                                    <div>Avg Views: <strong>${tag.avg_views.toLocaleString()}</strong></div>
                                    <div>Used: <strong>${tag.usage_count}x</strong></div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Top Captions -->
            ${data.top_captions && data.top_captions.length > 0 ? `
                <div style="margin-top: 2rem;">
                    <h4 style="margin-bottom: 1rem;">✨ Top Performing Captions</h4>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        ${data.top_captions.map((caption, idx) => `
                            <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 8px; border-left: 3px solid var(--success);">
                                <div style="display: flex; justify-content: between; align-items: start; gap: 1rem; margin-bottom: 1rem;">
                                    <div style="flex: 1;">
                                        <div style="font-size: 0.95rem; line-height: 1.6; color: var(--text-primary); margin-bottom: 0.75rem;">${caption.caption}</div>
                                        <div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.875rem; color: var(--text-secondary);">
                                            <span>📊 ER: <strong>${caption.engagement_rate.toFixed(2)}%</strong></span>
                                            <span>👁️ Views: <strong>${caption.views.toLocaleString()}</strong></span>
                                            <span>📝 ${caption.word_count} words</span>
                                            <span>🏷️ ${caption.hashtag_count} hashtags</span>
                                            <span>😊 ${caption.emoji_count} emojis</span>
                                            ${caption.has_cta ? '<span style="color: var(--success);">✅ Has CTA</span>' : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        `;
    }

    async function loadDurationAnalysis() {
        const container = document.getElementById('durationAnalysis');
        container.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">Loading duration analysis...</p>';
        
        try {
            const data = await API.getDurationAnalysis();
            if (data.error) throw new Error(data.error);
            
            renderDurationAnalysis(data);
        } catch (error) {
            container.innerHTML = `<p style="color: var(--danger); text-align: center; padding: 2rem;">❌ ${error.message}</p>`;
        }
    }

    function renderDurationAnalysis(data) {
        const container = document.getElementById('durationAnalysis');
        
        if (!data.available) {
            container.innerHTML = `<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">${data.message || 'Duration data not available'}</p>`;
            return;
        }
        
        const sweet = data.sweet_spot;
        const dist = data.distribution;
        
        container.innerHTML = `
            <!-- Sweet Spot Highlight -->
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, var(--primary-light) 0%, var(--card-bg) 100%); border-radius: 12px; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
                <h3 style="margin: 0 0 1rem 0; color: var(--primary);">Sweet Spot Detected!</h3>
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
                    <div style="padding: 1.5rem; border-radius: 12px; background: var(--card-bg); border-left: 4px solid var(--${
                        insight.type === 'success' ? 'success' : 
                        insight.type === 'warning' ? 'warning' : 'info'
                    });">
                        <div style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">${insight.title}</div>
                        <p style="margin: 0.5rem 0; color: var(--text-secondary); font-size: 0.95rem;">${insight.message}</p>
                        <p style="margin: 0.5rem 0; font-weight: 600; color: var(--primary); font-size: 0.9rem;">${insight.recommendation}</p>
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
