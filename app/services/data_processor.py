"""
Data Processing Service
Handles Instagram Insight data processing and analysis
"""
import pandas as pd
import numpy as np
from ..utils.serializer import serialize_data
from ..utils.validators import validate_csv_columns
from .quality_analyzer import QualityAnalyzer
from .outlier_analyzer import OutlierAnalyzer
from .hashtag_category_analyzer import HashtagCategoryAnalyzer
from .duration_optimizer import DurationOptimizer


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
            
            # --- INTEGRATED ANALYSES FOR STATELESS VERCEL DEPLOYMENT ---
            
            # Quality Analysis
            print("Running Quality Analysis...")
            quality_analyzer = QualityAnalyzer()
            quality_analysis = quality_analyzer.perform_quality_analysis(df)
            
            # Outlier Analysis
            print("Running Outlier Analysis...")
            outlier_analyzer = OutlierAnalyzer()
            outlier_analysis = outlier_analyzer.perform_outlier_analysis(df)
            
            # Category Analysis
            print("Running Category Analysis...")
            category_analyzer = HashtagCategoryAnalyzer()
            category_analysis = category_analyzer.perform_category_analysis(df)
            
            # Duration Analysis
            print("Running Duration Analysis...")
            duration_optimizer = DurationOptimizer()
            duration_analysis = duration_optimizer.perform_duration_analysis(df)
            
            # Follower Trend Analysis
            print("Running Follower Trend Analysis...")
            follower_trend = self._analyze_follower_trend(df)

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
                'advanced_insights': insights,
                
                # Add integrated analysis results
                'quality_analysis': quality_analysis,
                'outlier_analysis': outlier_analysis,
                'category_analysis': category_analysis,
                'duration_analysis': duration_analysis,
                'follower_trend': follower_trend
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
        weekly_trends['Publish_Week'] = weekly_trends['Publish_Week'].dt.start_time.dt.strftime('%Y-%m-%d')
        return weekly_trends.to_dict('records')

    def _analyze_follower_trend(self, df):
        """Analyze follower trend (moved from analysis.py for stateless architecture)"""
        try:
            # Prepare DF for time series
            df_trend = df.copy()
            if 'Publish time' not in df_trend.columns:
                return {'error': 'Publish time column missing'}
                
            df_trend = df_trend.sort_values('Publish time')
            
            # Ensure potential columns are numeric
            potential_cols = ['Follows', 'follows', 'Net Followers', 'Views', 'Impressions', 'Reach', 'Plays', 'views', 'impressions', 'Likes', 'Shares', 'Saves', 'Comments']
            for col in potential_cols:
                if col in df_trend.columns:
                    df_trend[col] = pd.to_numeric(df_trend[col], errors='coerce').fillna(0)
            
            # Robust column mapping with Reach as primary fallback
            def find_col(possible_names, default=None):
                for name in possible_names:
                    if name in df_trend.columns:
                        col_sum = df_trend[name].sum()
                        if col_sum > 0:
                            return name
                # Fallback to first existing column even if zero
                for name in possible_names:
                    if name in df_trend.columns:
                        return name
                return default

            # Try Reach first since Instagram CSV often uses Reach instead of Views
            view_col = find_col(['Reach', 'Views', 'Impressions', 'Plays', 'views', 'impressions', 'reach'], 'Reach')
            follow_col = find_col(['Follows', 'follows', 'Net Followers'], 'Follows')
            
            if view_col not in df_trend.columns: df_trend[view_col] = 0
            if follow_col not in df_trend.columns: df_trend[follow_col] = 0

            df_trend['Date'] = df_trend['Publish time'].dt.date
            cols_to_agg = {
                follow_col: 'sum',
                view_col: 'sum',
                'Likes': 'sum',
                'Shares': 'sum',
                'Saves': 'sum',
                'Comments': 'sum'
            }
            cols_to_agg = {k: v for k, v in cols_to_agg.items() if k in df_trend.columns}
            
            daily_data = df_trend.groupby('Date').agg(cols_to_agg).reset_index()
            
            # Rename for internal consistency
            daily_data = daily_data.rename(columns={follow_col: 'Follows', view_col: 'Views'})
            if 'Follows' not in daily_data.columns: daily_data['Follows'] = 0
            if 'Views' not in daily_data.columns: daily_data['Views'] = 0
            
            daily_data['Cumulative_Followers'] = daily_data['Follows'].cumsum()
            daily_data['Engagement_Rate'] = (
                (daily_data['Likes'] + daily_data['Comments'] + daily_data['Shares'] + daily_data['Saves']) / 
                daily_data['Views'].replace(0, 1)
            ) * 100
            
            if len(daily_data) == 0:
                return {'error': 'No daily data available'}

            # Advanced Analysis: Growth Phases & Strategy Change
            views_mean = daily_data['Views'].mean()
            views_std = daily_data['Views'].std()
            strategy_change_idx = 0
            
            for i in range(1, len(daily_data)):
                if daily_data.loc[i, 'Views'] > (views_mean + 1.5 * views_std):
                    strategy_change_idx = i
                    break
            
            strategy_change_date = daily_data.loc[strategy_change_idx, 'Date'].strftime('%Y-%m-%d')
            
            # Identify Growth Phases
            phases = []
            if strategy_change_idx > 0:
                phases.append({
                    'name': 'Dormant Phase',
                    'start_date': daily_data.loc[0, 'Date'].strftime('%Y-%m-%d'),
                    'end_date': daily_data.loc[strategy_change_idx-1, 'Date'].strftime('%Y-%m-%d'),
                    'color': 'rgba(148, 163, 184, 0.1)'
                })
            
            growth_period = daily_data.iloc[strategy_change_idx:]
            plateau_idx = len(daily_data) - 1
            if len(growth_period) > 10:
                recent_growth = daily_data['Follows'].iloc[-7:].mean()
                mid_growth = daily_data['Follows'].iloc[strategy_change_idx:-7].mean()
                if recent_growth < mid_growth * 0.5:
                    plateau_idx = len(daily_data) - 7
            
            phases.append({
                'name': 'Growth Phase',
                'start_date': strategy_change_date,
                'end_date': daily_data.loc[plateau_idx, 'Date'].strftime('%Y-%m-%d'),
                'color': 'rgba(34, 197, 94, 0.1)'
            })
            
            if plateau_idx < len(daily_data) - 1:
                phases.append({
                    'name': 'Plateau Phase',
                    'start_date': daily_data.loc[plateau_idx + 1, 'Date'].strftime('%Y-%m-%d'),
                    'end_date': daily_data.loc[len(daily_data)-1, 'Date'].strftime('%Y-%m-%d'),
                    'color': 'rgba(234, 179, 8, 0.1)'
                })

            # Calculate peaks
            peak_follows_idx = daily_data['Follows'].idxmax()
            peak_follows_val = int(daily_data.loc[peak_follows_idx, 'Follows'])
            peak_follows_date = daily_data.loc[peak_follows_idx, 'Date'].strftime('%Y-%m-%d')
            
            peak_views_idx = daily_data['Views'].idxmax()
            peak_views_val = int(daily_data.loc[peak_views_idx, 'Views'])
            peak_views_date = daily_data.loc[peak_views_idx, 'Date'].strftime('%Y-%m-%d')

            # Generate summary insight
            total_growth = daily_data['Cumulative_Followers'].iloc[-1] - daily_data['Cumulative_Followers'].iloc[0]
            summary_insight = f"Follower growth accelerated after strategy change on {strategy_change_date}"
            if plateau_idx < len(daily_data) - 1:
                summary_insight += ", followed by a plateau phase recently."
            else:
                summary_insight += ", continuing a steady upward trend."

            from datetime import datetime
            return {
                '_generated_at': datetime.now().isoformat(),
                'dates': [date.strftime('%Y-%m-%d') for date in daily_data['Date']],
                'cumulative_followers': daily_data['Cumulative_Followers'].tolist(),
                'daily_views': daily_data['Views'].tolist(),
                'daily_follows': daily_data['Follows'].tolist(),
                'engagement_rate': daily_data['Engagement_Rate'].round(2).tolist(),
                'total_followers': int(daily_data['Cumulative_Followers'].iloc[-1]) if len(daily_data) > 0 else 0,
                'total_views': int(daily_data['Views'].sum()) if len(daily_data) > 0 else 0,
                'total_days': len(daily_data),
                'avg_daily_follows': round(daily_data['Follows'].mean(), 1) if len(daily_data) > 0 else 0,
                'avg_daily_views': round(daily_data['Views'].mean(), 1) if len(daily_data) > 0 else 0,
                'peak_follows': peak_follows_val,
                'peak_date': peak_follows_date,
                'peak_views': peak_views_val,
                'peak_views_date': peak_views_date,
                'strategy_change_date': strategy_change_date,
                'phases': phases,
                'summary_insight': summary_insight,
                'insights': [
                    f"Total followers gained: {total_growth:,.0f}",
                    f"Total views accumulated: {daily_data['Views'].sum() if len(daily_data) > 0 else 0:,.0f}",
                    f"Average daily follows: {daily_data['Follows'].mean():.1f}",
                    f"Peak daily follows: {peak_follows_val:,} on {peak_follows_date}",
                    f"Strategy Change detected on {strategy_change_date}"
                ]
            }

        except Exception as e:
            print(f"Error in follower trend analysis: {str(e)}")
            return {'error': str(e)}
