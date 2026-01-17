"""
Insights Generation Service
Generate actionable insights from analyzed data
"""


class InsightsGenerator:
    """Generate senior data scientist level insights"""
    
    def generate_advanced_insights(self, df, post_type_performance, content_performance, best_hour, best_day):
        """Generate comprehensive insights"""
        insights = []
        
        # Content format insights
        if post_type_performance:
            insights.extend(self._generate_content_format_insights(post_type_performance))
        
        # Posting time insights
        if best_hour is not None:
            insights.append(self._generate_timing_insight(best_hour, best_day))
        
        # Virality insights
        if content_performance['viral_posts_count'] > 0:
            insights.append(self._generate_virality_insight(content_performance, len(df)))
        
        # Engagement quality insights
        insights.extend(self._generate_engagement_insights(content_performance))
        
        # Content consistency insights
        insights.extend(self._generate_consistency_insights(content_performance))
        
        return insights
    
    def _generate_content_format_insights(self, post_type_performance):
        """Generate content format insights"""
        insights = []
        
        best_format = max(post_type_performance.keys(), 
                         key=lambda x: post_type_performance[x].get('Engagement_Rate', 0))
        worst_format = min(post_type_performance.keys(), 
                          key=lambda x: post_type_performance[x].get('Engagement_Rate', 0))
        
        diff = abs(post_type_performance[best_format]["Engagement_Rate"] - 
                  post_type_performance[worst_format]["Engagement_Rate"])
        
        insights.append({
            'type': 'content_strategy',
            'title': '📱 Format Optimization',
            'insight': f'{best_format} outperforms {worst_format} by {diff:.2f}% engagement rate',
            'recommendation': f'Increase {best_format} production to 60-70% of content mix',
            'priority': 'high'
        })
        
        return insights
    
    def _generate_timing_insight(self, best_hour, best_day):
        """Generate optimal posting time insight"""
        return {
            'type': 'timing_optimization',
            'title': '⏰ Optimal Posting Time',
            'insight': f'Best engagement at {best_hour}:00 on {best_day}',
            'recommendation': f'Schedule high-value content for {best_hour}:00-{best_hour+1}:00 on {best_day}s',
            'priority': 'medium'
        }
    
    def _generate_virality_insight(self, content_performance, total_posts):
        """Generate virality insights"""
        viral_percentage = (content_performance['viral_posts_count'] / total_posts) * 100
        
        return {
            'type': 'viral_content',
            'title': '🚀 Viral Content Analysis',
            'insight': f'{viral_percentage:.1f}% of posts achieved viral status (top 10% virality score)',
            'recommendation': 'Analyze viral posts for common themes and replicate successful patterns',
            'priority': 'high'
        }
    
    def _generate_engagement_insights(self, content_performance):
        """Generate engagement quality insights"""
        insights = []
        avg_engagement = content_performance['avg_engagement_rate']
        
        if avg_engagement < 2.0:
            insights.append({
                'type': 'engagement_quality',
                'title': '💬 Engagement Quality',
                'insight': f'Low engagement rate ({avg_engagement:.2f}%) indicates content optimization needed',
                'recommendation': 'Focus on creating more interactive and save-worthy content',
                'priority': 'high'
            })
        elif avg_engagement > 5.0:
            insights.append({
                'type': 'engagement_quality',
                'title': '🎉 High Engagement Performance',
                'insight': f'Excellent engagement rate ({avg_engagement:.2f}%) above industry average',
                'recommendation': 'Maintain current content strategy and scale successful formats',
                'priority': 'low'
            })
        
        return insights
    
    def _generate_consistency_insights(self, content_performance):
        """Generate content consistency insights"""
        insights = []
        
        std_views = content_performance['std_views']
        mean_views = content_performance['avg_views_per_post']
        cv = (std_views / mean_views) * 100 if mean_views > 0 else 0
        
        if cv > 100:
            insights.append({
                'type': 'content_consistency',
                'title': '📊 Content Consistency',
                'insight': f'High performance variability (CV: {cv:.1f}%) indicates inconsistent content quality',
                'recommendation': 'Develop content guidelines and quality control processes',
                'priority': 'medium'
            })
        
        return insights
