"""
Data Processing Service
Handles Instagram Insight data processing and analysis
"""
import pandas as pd
import numpy as np
from ..utils.serializer import serialize_data
from ..utils.validators import validate_csv_columns


class DataProcessor:
    """Process Instagram Insight data with advanced analysis"""
    
    def __init__(self):
        self.engagement_metrics = ['Views', 'Reach', 'Likes', 'Shares', 'Follows', 'Comments', 'Saves']
    
    def process_insight_data(self, df):
        """Process Instagram Insight data with advanced data science analysis"""
        try:
            # Validate required columns
            validate_csv_columns(df)
            
            print(f"Original columns: {df.columns.tolist()}")
            print(f"Data shape: {df.shape}")
            
            # Clean and prepare data
            df = self._clean_data(df)
            
            # Get available metrics
            available_metrics = [metric for metric in self.engagement_metrics if metric in df.columns]
            print(f"Available metrics: {available_metrics}")
            
            # Add calculated columns
            df = self._add_time_features(df)
            df = self._calculate_engagement_metrics(df)
            
            # Perform various analyses
            post_type_performance = self._analyze_post_type_performance(df, available_metrics)
            time_performance = self._analyze_time_performance(df, available_metrics)
            content_performance = self._analyze_content_performance(df)
            optimal_posting_time = self._analyze_optimal_posting_time(df, available_metrics)
            
            # Get descriptive statistics
            descriptive_stats = self._get_descriptive_stats(df, available_metrics)
            
            # Calculate correlation matrix
            correlation_matrix = self._calculate_correlation_matrix(df, available_metrics)
            
            # Get recent and top posts
            recent_posts = self._get_recent_posts(df)
            top_posts = self._get_top_posts(df)
            all_posts = self._get_all_posts(df)
            
            # Calculate totals and summary metrics
            totals = self._calculate_totals(df, available_metrics)
            date_range = self._get_date_range(df)
            
            # Best performing analysis
            best_performing = self._get_best_performing(df)
            
            # Content mix analysis
            content_mix = self._analyze_content_mix(df)
            
            # Weekly trends
            weekly_trends = self._analyze_weekly_trends(df)
            
            # Generate insights
            from .insights_generator import InsightsGenerator
            insights_gen = InsightsGenerator()
            insights = insights_gen.generate_advanced_insights(
                df, post_type_performance, content_performance,
                optimal_posting_time['best_hour'], optimal_posting_time['best_day']
            )
            
            print("Successfully processed all data")
            
            return serialize_data({
                'post_type_performance': post_type_performance,
                'time_performance': time_performance,
                'descriptive_stats': descriptive_stats,
                'correlation_matrix': correlation_matrix,
                'recent_posts': recent_posts,
                'all_posts': all_posts,
                'total_posts': len(df),
                'date_range': date_range,
                'totals': totals,
                'best_post_type': max(post_type_performance.keys(), 
                                     key=lambda x: post_type_performance[x].get('Engagement_Rate', 0)) if post_type_performance else None,
                'avg_views_best': post_type_performance[max(post_type_performance.keys(), 
                                                            key=lambda x: post_type_performance[x].get('Engagement_Rate', 0))]['Views'] if post_type_performance else 0,
                'top_posts': top_posts,
                'content_performance': content_performance,
                'content_mix': content_mix,
                'optimal_posting_time': optimal_posting_time,
                'weekly_trends': weekly_trends,
                'best_performing': best_performing,
                'advanced_insights': insights
            })
            
        except Exception as e:
            print(f"Error in process_insight_data: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _clean_data(self, df):
        """Clean and prepare data"""
        df['Publish time'] = pd.to_datetime(df['Publish time'], format='%m/%d/%Y %H:%M', errors='coerce')
        
        # Convert metrics to numeric
        for metric in self.engagement_metrics:
            if metric in df.columns:
                df[metric] = pd.to_numeric(df[metric], errors='coerce').fillna(0)
        
        return df
    
    def _add_time_features(self, df):
        """Add time-based features"""
        df['Publish_Week'] = df['Publish time'].dt.to_period('W')
        df['Hour'] = df['Publish time'].dt.hour
        df['DayOfWeek'] = df['Publish time'].dt.day_name()
        df['DayNum'] = df['Publish time'].dt.dayofweek
        return df
    
    def _calculate_engagement_metrics(self, df):
        """Calculate engagement metrics"""
        df['Engagement_Rate'] = ((df['Likes'] + df['Comments'] + df['Shares'] + df['Saves']) / 
                                  df['Views'].replace(0, 1) * 100).round(2)
        df['Like_Rate'] = (df['Likes'] / df['Views'].replace(0, 1) * 100).round(2)
        df['Comment_Rate'] = (df['Comments'] / df['Views'].replace(0, 1) * 100).round(2)
        df['Share_Rate'] = (df['Shares'] / df['Views'].replace(0, 1) * 100).round(2)
        df['Save_Rate'] = (df['Saves'] / df['Views'].replace(0, 1) * 100).round(2)
        
        # Calculate virality score
        df['Virality_Score'] = (
            df['Likes'] * 1 + 
            df['Comments'] * 5 + 
            df['Shares'] * 10 + 
            df['Saves'] * 3
        ).round(2)
        
        return df
    
    def _analyze_post_type_performance(self, df, available_metrics):
        """Analyze performance by post type"""
        post_type_performance_raw = df.groupby('Post type')[available_metrics + ['Engagement_Rate', 'Virality_Score']].mean()
        post_type_performance = {}
        
        for post_type in post_type_performance_raw.index:
            post_type_performance[post_type] = {}
            for metric in post_type_performance_raw.columns:
                value = post_type_performance_raw.loc[post_type, metric]
                post_type_performance[post_type][metric] = None if pd.isna(value) else float(value)
        
        return post_type_performance
    
    def _analyze_time_performance(self, df, available_metrics):
        """Analyze performance over time"""
        time_performance = df.groupby('Publish_Week')[available_metrics].mean()
        time_performance_reset = time_performance.reset_index()
        time_performance_reset['Publish_Week'] = time_performance_reset['Publish_Week'].dt.start_time.dt.strftime('%Y-%m-%d')
        return time_performance_reset.to_dict('records')
    
    def _analyze_content_performance(self, df):
        """Analyze overall content performance"""
        return {
            'avg_views_per_post': float(df['Views'].mean()),
            'median_views_per_post': float(df['Views'].median()),
            'std_views': float(df['Views'].std()),
            'avg_engagement_rate': float(df['Engagement_Rate'].mean()),
            'median_engagement_rate': float(df['Engagement_Rate'].median()),
            'total_impressions': float(df['Views'].sum()),
            'total_engagements': float((df['Likes'] + df['Comments'] + df['Shares'] + df['Saves']).sum()),
            'viral_posts_count': int(len(df[df['Virality_Score'] > df['Virality_Score'].quantile(0.9)])),
            'high_engagement_posts': int(len(df[df['Engagement_Rate'] > df['Engagement_Rate'].quantile(0.75)]))
        }
    
    def _analyze_optimal_posting_time(self, df, available_metrics):
        """Analyze optimal posting times"""
        hourly_performance = df.groupby('Hour')[available_metrics + ['Engagement_Rate']].mean().round(2)
        best_hour = hourly_performance['Engagement_Rate'].idxmax() if not hourly_performance.empty else None
        
        daily_performance = df.groupby('DayNum')[available_metrics + ['Engagement_Rate']].mean().round(2)
        daily_performance['DayName'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        best_day = daily_performance.loc[daily_performance['Engagement_Rate'].idxmax(), 'DayName'] if not daily_performance.empty else None
        
        return {
            'best_hour': best_hour,
            'best_day': best_day,
            'hourly_performance': hourly_performance.to_dict(),
            'daily_performance': daily_performance.set_index('DayName').to_dict()
        }
    
    def _get_descriptive_stats(self, df, available_metrics):
        """Get descriptive statistics"""
        descriptive_stats_raw = df[available_metrics + ['Engagement_Rate', 'Virality_Score']].describe()
        descriptive_stats = {}
        
        for col in descriptive_stats_raw.columns:
            descriptive_stats[col] = {}
            for stat in descriptive_stats_raw.index:
                value = descriptive_stats_raw.loc[stat, col]
                if pd.isna(value):
                    descriptive_stats[col][stat] = None
                elif isinstance(value, (int, float)):
                    descriptive_stats[col][stat] = float(value) if '.' in str(value) else int(value)
                else:
                    descriptive_stats[col][stat] = str(value)
        
        return descriptive_stats
    
    def _calculate_correlation_matrix(self, df, available_metrics):
        """Calculate correlation matrix"""
        correlation_metrics = available_metrics + ['Engagement_Rate', 'Virality_Score', 'Like_Rate', 
                                                    'Comment_Rate', 'Share_Rate', 'Save_Rate']
        correlation_matrix_raw = df[correlation_metrics].corr().round(2)
        correlation_matrix = {}
        
        for col in correlation_matrix_raw.columns:
            correlation_matrix[col] = {}
            for row in correlation_matrix_raw.index:
                value = correlation_matrix_raw.loc[row, col]
                correlation_matrix[col][row] = None if pd.isna(value) else float(value)
        
        return correlation_matrix
    
    def _get_recent_posts(self, df, limit=10):
        """Get recent posts"""
        recent_posts_data = df.sort_values('Publish time', ascending=False).head(limit)
        recent_posts = []
        
        for _, post in recent_posts_data.iterrows():
            post_dict = post.to_dict()
            if pd.notna(post_dict.get('Publish time')):
                post_dict['Publish time'] = post_dict['Publish time'].strftime('%Y-%m-%d %H:%M:%S')
            recent_posts.append(post_dict)
        
        return recent_posts
    
    def _get_top_posts(self, df, limit=5):
        """Get top performing posts"""
        top_posts = df.sort_values('Virality_Score', ascending=False).head(limit)
        top_posts_data = []
        
        for _, post in top_posts.iterrows():
            post_dict = post.to_dict()
            if pd.notna(post_dict.get('Publish time')):
                post_dict['Publish time'] = post_dict['Publish time'].strftime('%Y-%m-%d %H:%M:%S')
            top_posts_data.append(post_dict)
        
        return top_posts_data
    
    def _get_all_posts(self, df):
        """Get all posts data"""
        all_posts_data = []
        
        for _, post in df.iterrows():
            post_dict = post.to_dict()
            if pd.notna(post_dict.get('Publish time')):
                post_dict['Publish time'] = post_dict['Publish time'].strftime('%Y-%m-%d %H:%M:%S')
            all_posts_data.append(post_dict)
        
        return all_posts_data
    
    def _calculate_totals(self, df, available_metrics):
        """Calculate total metrics"""
        totals = {}
        for metric in available_metrics:
            totals[metric] = int(df[metric].sum())
        return totals
    
    def _get_date_range(self, df):
        """Get date range"""
        return {
            'start': df['Publish time'].min().strftime('%Y-%m-%d') if pd.notna(df['Publish time'].min()) else None,
            'end': df['Publish time'].max().strftime('%Y-%m-%d') if pd.notna(df['Publish time'].max()) else None
        }
    
    def _get_best_performing(self, df):
        """Get best performing posts by different metrics"""
        best_by_views = df.loc[df['Views'].idxmax()].to_dict() if not df.empty else {}
        best_by_engagement = df.loc[df['Engagement_Rate'].idxmax()].to_dict() if not df.empty else {}
        best_by_virality = df.loc[df['Virality_Score'].idxmax()].to_dict() if not df.empty else {}
        
        return {
            'by_views': best_by_views,
            'by_engagement': best_by_engagement,
            'by_virality': best_by_virality
        }
    
    def _analyze_content_mix(self, df):
        """Analyze content mix"""
        post_type_counts = df['Post type'].value_counts().to_dict()
        total_posts = len(df)
        
        return {
            'reel_percentage': round((post_type_counts.get('IG Reel', 0) / total_posts * 100), 1),
            'image_percentage': round((post_type_counts.get('IG Image', 0) / total_posts * 100), 1),
            'carousel_percentage': round((post_type_counts.get('IG Carousel', 0) / total_posts * 100), 1)
        }
    
    def _analyze_weekly_trends(self, df):
        """Analyze weekly trends"""
        weekly_trends = df.groupby('Publish_Week').agg({
            'Views': 'mean',
            'Engagement_Rate': 'mean',
            'Virality_Score': 'mean'
        }).reset_index()
        weekly_trends['Publish_Week'] = weekly_trends['Publish_Week'].dt.start_time.dt.strftime('%Y-%m-%d')
        return weekly_trends.to_dict('records')
