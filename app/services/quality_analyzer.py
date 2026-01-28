"""
Quality Analysis Service
Analyze content quality based on engagement metrics
"""
import pandas as pd
import numpy as np
from ..utils.serializer import serialize_data


class QualityAnalyzer:
    """Analyze content quality with percentile-based categorization"""
    
    def calculate_content_quality_score(self, df):
        """Content quality scoring based on Engagement Rate"""
        df_clean = df.copy()
        
        # Calculate Engagement Rate with Reach fallback to Views
        df_clean['Reach_for_ER'] = df_clean['Reach'].replace(0, pd.NA)
        df_clean['Reach_for_ER'] = df_clean['Reach_for_ER'].fillna(df_clean['Views'])
        df_clean['Reach_for_ER'] = df_clean['Reach_for_ER'].replace(0, pd.NA).fillna(1)
        
        df_clean['Engagement_Rate'] = (
            (df_clean['Likes'] + df_clean['Comments'] + df_clean['Shares'] + df_clean['Saves']) / 
            df_clean['Reach_for_ER']
        ) * 100
        
        # Percentile-based categorization
        df_clean['ER_Percentile'] = df_clean['Engagement_Rate'].rank(pct=True) * 100
        
        def categorize_by_percentile(percentile):
            if percentile >= 90:
                return 'Excellent'
            elif percentile >= 70:
                return 'High'
            elif percentile >= 30:
                return 'Medium'
            else:
                return 'Low'
        
        df_clean['Quality_Tier'] = df_clean['ER_Percentile'].apply(categorize_by_percentile)
        
        # Secondary metrics
        df_clean['Engagement_Depth'] = (
            (df_clean['Saves'] * 0.4) + 
            (df_clean['Shares'] * 0.3) + 
            (df_clean['Comments'] * 0.2) + 
            (df_clean['Likes'] * 0.1)
        ) / df_clean['Reach_for_ER']
        
        df_clean['Virality_Potential'] = df_clean['Shares'] / df_clean['Reach_for_ER'] * 100
        df_clean['Retention_Score'] = df_clean['Saves'] / df_clean['Reach_for_ER'] * 100
        
        # Content Quality Score
        df_clean['Content_Quality_Score'] = (
            (df_clean['Engagement_Rate'].rank(pct=True) * 40) +
            (df_clean['Engagement_Depth'].rank(pct=True) * 30) +
            (df_clean['Virality_Potential'].rank(pct=True) * 20) +
            (df_clean['Retention_Score'].rank(pct=True) * 10)
        ).round(1)
        
        df_clean['Used_Views_Fallback'] = df_clean['Reach'].replace(0, pd.NA).isna() & (df_clean['Views'] > 0)
        
        return df_clean
    
    def perform_quality_analysis(self, df):
        """Perform comprehensive content quality analysis"""
        try:
            df_with_scores = self.calculate_content_quality_score(df)
            
            # Quality tier distribution
            tier_counts = df_with_scores['Quality_Tier'].value_counts().to_dict()
            tier_percentages = (df_with_scores['Quality_Tier'].value_counts(normalize=True) * 100).round(1).to_dict()
            
            # Average scores by tier
            avg_scores_by_tier = {}
            for tier in ['Excellent', 'High', 'Medium', 'Low']:
                tier_data = df_with_scores[df_with_scores['Quality_Tier'] == tier]
                if len(tier_data) > 0:
                    avg_score = tier_data['Content_Quality_Score'].mean()
                    avg_scores_by_tier[tier] = float(avg_score.round(1)) if pd.notna(avg_score) else 0.0
            
            # Prepare all posts data
            all_posts_data = []
            for _, post in df_with_scores.iterrows():
                post_dict = post.to_dict()
                if pd.notna(post_dict.get('Publish time')):
                    post_dict['Publish time'] = post_dict['Publish time'].strftime('%Y-%m-%d %H:%M:%S')
                
                description = str(post_dict.get('Description', post_dict.get('Caption', '')))
                post_dict['short_description'] = description[:40] + '...' if len(description) > 50 else description
                
                content_url = (post_dict.get('URL') or post_dict.get('Link') or 
                              post_dict.get('Content URL') or post_dict.get('permalink') or '')
                post_dict['content_url'] = content_url
                
                all_posts_data.append(post_dict)
            
            # Calculate insights
            views_fallback_count = df_with_scores['Used_Views_Fallback'].sum()
            fallback_note = f"*Note: {views_fallback_count} posts used Views instead of Reach*" if views_fallback_count > 0 else ""
            
            return {
                'tier_distribution': {k: int(v) if pd.notna(v) else 0 for k, v in tier_counts.items()},
                'tier_percentages': {k: float(v) if pd.notna(v) else 0.0 for k, v in tier_percentages.items()},
                'avg_scores_by_tier': avg_scores_by_tier,
                'total_posts_analyzed': len(df_with_scores),
                'overall_avg_score': float(df_with_scores['Content_Quality_Score'].mean().round(2)),
                'all_posts': serialize_data(all_posts_data),
                'quality_insights': [insight for insight in [
                    f"Total {tier_counts.get('Excellent', 0)} posts ({tier_percentages.get('Excellent', 0)}%) dengan ER Excellent (Top 10%)",
                    f"Total {tier_counts.get('Low', 0)} posts ({tier_percentages.get('Low', 0)}%) dengan ER Low (Bottom 30%)",
                    f"Rata-rata Engagement Rate: {df_with_scores['Engagement_Rate'].mean().round(2):.2f}%",
                    fallback_note
                ] if insight]
            }
            
        except Exception as e:
            print(f"Error in perform_quality_analysis: {str(e)}")
            return {'error': str(e)}
