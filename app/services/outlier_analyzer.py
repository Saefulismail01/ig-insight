"""
Outlier Analysis Service
Analyze top and bottom performing posts
"""
import pandas as pd
from ..utils.serializer import serialize_data


class OutlierAnalyzer:
    """Analyze outlier posts (top 5 vs bottom 5)"""
    
    def perform_outlier_analysis(self, df):
        """Perform outlier analysis based on Views"""
        try:
            df_sorted = df.sort_values('Views', ascending=False)
            
            top_5 = df_sorted.head(5)
            bottom_5 = df_sorted.tail(5)
            
            # Calculate averages
            top_5_avg_views = top_5['Views'].mean()
            bottom_5_avg_views = bottom_5['Views'].mean()
            
            # Duration analysis
            duration_analysis = self._analyze_duration(top_5, bottom_5, df)
            
            # Engagement metrics analysis
            engagement_metrics = ['Likes', 'Comments', 'Shares', 'Saves']
            available_metrics = [metric for metric in engagement_metrics if metric in df.columns]
            
            top_5_structure = {}
            bottom_5_structure = {}
            
            for metric in available_metrics:
                top_5_structure[metric] = float(top_5[metric].mean())
                bottom_5_structure[metric] = float(bottom_5[metric].mean())
            
            # Prepare post data
            top_5_posts = self._prepare_posts_data(top_5)
            bottom_5_posts = self._prepare_posts_data(bottom_5)
            
            return {
                'top_5_posts': serialize_data(top_5_posts),
                'bottom_5_posts': serialize_data(bottom_5_posts),
                'top_5_avg_views': float(top_5_avg_views),
                'bottom_5_avg_views': float(bottom_5_avg_views),
                'views_gap': float(top_5_avg_views - bottom_5_avg_views),
                'views_multiplier': float(top_5_avg_views / bottom_5_avg_views) if bottom_5_avg_views > 0 else 0,
                'duration_analysis': duration_analysis,
                'top_5_structure': top_5_structure,
                'bottom_5_structure': bottom_5_structure
            }
            
        except Exception as e:
            print(f"Error in perform_outlier_analysis: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_duration(self, top_5, bottom_5, df):
        """Analyze video duration if available"""
        duration_columns = ['Duration', 'Video Duration', 'duration', 'video_duration']
        duration_col = None
        
        for col in duration_columns:
            if col in df.columns:
                duration_col = col
                break
        
        if duration_col:
            top_5_avg_duration = top_5[duration_col].mean()
            bottom_5_avg_duration = bottom_5[duration_col].mean()
            
            return {
                'available': True,
                'top_5_avg_duration': float(top_5_avg_duration),
                'bottom_5_avg_duration': float(bottom_5_avg_duration),
                'difference': float(abs(top_5_avg_duration - bottom_5_avg_duration)),
                'insight': 'Post top performer cenderung lebih panjang' if top_5_avg_duration > bottom_5_avg_duration else 'Post top performer cenderung lebih pendek'
            }
        else:
            return {'available': False}
    
    def _prepare_posts_data(self, posts_df):
        """Prepare posts data with metadata"""
        posts_data = []
        
        for _, post in posts_df.iterrows():
            post_dict = post.to_dict()
            if pd.notna(post_dict.get('Publish time')):
                post_dict['Publish time'] = post_dict['Publish time'].strftime('%Y-%m-%d %H:%M:%S')
            
            description = str(post_dict.get('Description', post_dict.get('Caption', '')))
            post_dict['short_description'] = description[:50] + '...' if len(description) > 50 else description
            
            content_url = (post_dict.get('URL') or post_dict.get('Link') or 
                          post_dict.get('Content URL') or post_dict.get('permalink') or '')
            post_dict['content_url'] = content_url
            
            posts_data.append(post_dict)
        
        return posts_data
