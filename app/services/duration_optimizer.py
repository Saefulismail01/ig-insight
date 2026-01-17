"""
Duration Optimizer Service
Analyze video duration for optimal performance
"""
import pandas as pd
import numpy as np


class DurationOptimizer:
    """Analyze video duration to find sweet spots for engagement"""
    
    def perform_duration_analysis(self, df):
        """Perform comprehensive duration analysis"""
        try:
            # Check if Duration column exists
            duration_col = self._find_duration_column(df)
            
            if not duration_col:
                return {
                    'available': False,
                    'message': 'Duration data not available in this dataset'
                }
            
            # Filter to only posts with duration (Reels/Videos)
            df_video = df[df[duration_col].notna() & (df[duration_col] > 0)].copy()
            
            if len(df_video) == 0:
                return {
                    'available': False,
                    'message': 'No video posts with duration data found'
                }
            
            # Rename for consistency
            df_video['duration'] = df_video[duration_col]
            
            # Duration distribution
            distribution = self._analyze_duration_distribution(df_video)
            
            # Duration buckets analysis
            bucket_analysis = self._analyze_duration_buckets(df_video)
            
            # Sweet spot detection
            sweet_spot = self._detect_sweet_spot(df_video)
            
            # Performance by duration
            performance_curve = self._create_performance_curve(df_video)
            
            # Optimal duration by metric
            optimal_by_metric = self._find_optimal_by_metric(df_video)
            
            # Duration vs specific metrics
            correlation_analysis = self._analyze_duration_correlations(df_video)
            
            # Insights
            insights = self._generate_duration_insights(
                sweet_spot, bucket_analysis, correlation_analysis, df_video
            )
            
            return {
                'available': True,
                'distribution': distribution,
                'bucket_analysis': bucket_analysis,
                'sweet_spot': sweet_spot,
                'performance_curve': performance_curve,
                'optimal_by_metric': optimal_by_metric,
                'correlation_analysis': correlation_analysis,
                'insights': insights,
                'total_videos_analyzed': len(df_video)
            }
            
        except Exception as e:
            print(f"Error in perform_duration_analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e), 'available': False}
    
    def _find_duration_column(self, df):
        """Find duration column in dataframe"""
        possible_names = ['Duration (sec)', 'Duration', 'Video Duration', 'duration', 'video_duration']
        
        for name in possible_names:
            if name in df.columns:
                return name
        
        return None
    
    def _analyze_duration_distribution(self, df):
        """Analyze duration distribution"""
        return {
            'min_duration': float(df['duration'].min()),
            'max_duration': float(df['duration'].max()),
            'avg_duration': float(df['duration'].mean()),
            'median_duration': float(df['duration'].median()),
            'std_duration': float(df['duration'].std()),
            'quartiles': {
                'q1': float(df['duration'].quantile(0.25)),
                'q2': float(df['duration'].quantile(0.50)),
                'q3': float(df['duration'].quantile(0.75))
            }
        }
    
    def _analyze_duration_buckets(self, df):
        """Analyze performance by duration buckets"""
        # Create duration buckets
        df['duration_bucket'] = pd.cut(
            df['duration'],
            bins=[0, 10, 20, 30, 45, 60, 90, 1000],
            labels=['0-10s', '10-20s', '20-30s', '30-45s', '45-60s', '60-90s', '90s+']
        )
        
        bucket_performance = df.groupby('duration_bucket', observed=True).agg({
            'Engagement_Rate': 'mean',
            'Views': 'mean',
            'Likes': 'mean',
            'Comments': 'mean',
            'Shares': 'mean',
            'Saves': 'mean',
            'Virality_Score': 'mean'
        }).round(2)
        
        # Convert to list of dictionaries
        bucket_data = []
        for bucket in bucket_performance.index:
            bucket_data.append({
                'duration_range': str(bucket),
                'post_count': int(len(df[df['duration_bucket'] == bucket])),
                'avg_engagement_rate': float(bucket_performance.loc[bucket, 'Engagement_Rate']),
                'avg_views': int(bucket_performance.loc[bucket, 'Views']),
                'avg_likes': int(bucket_performance.loc[bucket, 'Likes']),
                'avg_comments': int(bucket_performance.loc[bucket, 'Comments']),
                'avg_shares': int(bucket_performance.loc[bucket, 'Shares']),
                'avg_saves': int(bucket_performance.loc[bucket, 'Saves']),
                'avg_virality': float(bucket_performance.loc[bucket, 'Virality_Score'])
            })
        
        # Find best performing bucket
        best_bucket = bucket_performance['Engagement_Rate'].idxmax()
        
        return {
            'buckets': bucket_data,
            'best_bucket': str(best_bucket)
        }
    
    def _detect_sweet_spot(self, df):
        """Detect optimal duration sweet spot"""
        # Use rolling window to find sweet spot
        df_sorted = df.sort_values('duration')
        
        # Group by 5-second windows
        df_sorted['duration_window'] = (df_sorted['duration'] // 5) * 5
        
        window_performance = df_sorted.groupby('duration_window').agg({
            'Engagement_Rate': 'mean',
            'Views': 'mean',
            'Virality_Score': 'mean'
        }).reset_index()
        
        # Find sweet spot (highest engagement rate)
        best_window = window_performance.loc[window_performance['Engagement_Rate'].idxmax()]
        
        sweet_spot_start = int(best_window['duration_window'])
        sweet_spot_end = sweet_spot_start + 5
        
        # Get posts in sweet spot
        sweet_spot_posts = df[(df['duration'] >= sweet_spot_start) & (df['duration'] < sweet_spot_end)]
        
        return {
            'range_start': sweet_spot_start,
            'range_end': sweet_spot_end,
            'avg_engagement_rate': float(best_window['Engagement_Rate']),
            'avg_views': int(best_window['Views']),
            'avg_virality': float(best_window['Virality_Score']),
            'post_count': len(sweet_spot_posts),
            'recommendation': f"Optimal duration is {sweet_spot_start}-{sweet_spot_end} seconds"
        }
    
    def _create_performance_curve(self, df):
        """Create duration vs performance curve"""
        # Group by duration (rounded to nearest 5 seconds)
        df['duration_rounded'] = (df['duration'] // 5) * 5
        
        curve_data = df.groupby('duration_rounded').agg({
            'Engagement_Rate': 'mean',
            'Views': 'mean',
            'Likes': 'mean'
        }).reset_index().sort_values('duration_rounded')
        
        return [
            {
                'duration': int(row['duration_rounded']),
                'engagement_rate': float(row['Engagement_Rate']),
                'views': int(row['Views']),
                'likes': int(row['Likes'])
            }
            for _, row in curve_data.iterrows()
        ]
    
    def _find_optimal_by_metric(self, df):
        """Find optimal duration for each metric"""
        metrics = {
            'Engagement_Rate': 'engagement',
            'Views': 'views',
            'Likes': 'likes',
            'Comments': 'comments',
            'Shares': 'shares',
            'Saves': 'saves',
            'Virality_Score': 'virality'
        }
        
        optimal = {}
        
        for metric_col, metric_name in metrics.items():
            if metric_col in df.columns:
                # Find duration with highest average for this metric
                df['duration_window'] = (df['duration'] // 5) * 5
                window_perf = df.groupby('duration_window')[metric_col].mean()
                
                best_duration = window_perf.idxmax()
                best_value = window_perf.max()
                
                optimal[metric_name] = {
                    'optimal_duration': int(best_duration),
                    'avg_value': float(best_value)
                }
        
        return optimal
    
    def _analyze_duration_correlations(self, df):
        """Analyze correlation between duration and metrics"""
        metrics = ['Engagement_Rate', 'Views', 'Likes', 'Comments', 'Shares', 'Saves']
        available_metrics = [m for m in metrics if m in df.columns]
        
        correlations = {}
        for metric in available_metrics:
            corr = df['duration'].corr(df[metric])
            correlations[metric] = {
                'correlation': float(corr),
                'interpretation': self._interpret_correlation(corr)
            }
        
        return correlations
    
    def _interpret_correlation(self, corr):
        """Interpret correlation value"""
        if abs(corr) < 0.1:
            return 'No relationship'
        elif abs(corr) < 0.3:
            return 'Weak relationship'
        elif abs(corr) < 0.5:
            return 'Moderate relationship'
        elif abs(corr) < 0.7:
            return 'Strong relationship'
        else:
            return 'Very strong relationship'
    
    def _generate_duration_insights(self, sweet_spot, bucket_analysis, correlation_analysis, df):
        """Generate actionable insights"""
        insights = []
        
        # Sweet spot insight
        insights.append({
            'type': 'success',
            'title': '🎯 Optimal Duration Sweet Spot',
            'message': f"Your best performing videos are {sweet_spot['range_start']}-{sweet_spot['range_end']} seconds long",
            'recommendation': sweet_spot['recommendation']
        })
        
        # Best bucket insight
        best_bucket = bucket_analysis['best_bucket']
        insights.append({
            'type': 'info',
            'title': '📊 Best Duration Range',
            'message': f"Videos in the {best_bucket} range perform best overall",
            'recommendation': f"Focus on creating content in this duration range"
        })
        
        # Duration trend
        avg_duration = df['duration'].mean()
        if avg_duration < 30:
            insights.append({
                'type': 'info',
                'title': '⚡ Short-Form Content',
                'message': f"Your average video is {avg_duration:.1f} seconds - perfect for quick consumption",
                'recommendation': "Continue with short-form content, but test 30-45s for deeper topics"
            })
        elif avg_duration < 60:
            insights.append({
                'type': 'info',
                'title': '⏱️ Medium-Length Content',
                'message': f"Your average video is {avg_duration:.1f} seconds",
                'recommendation': "Good balance. Consider A/B testing shorter (<30s) and longer (60s+) formats"
            })
        else:
            insights.append({
                'type': 'warning',
                'title': '📺 Long-Form Content',
                'message': f"Your average video is {avg_duration:.1f} seconds",
                'recommendation': "Long videos work for deep content, but ensure first 3 seconds hook viewers"
            })
        
        # Correlation insights
        if 'Engagement_Rate' in correlation_analysis:
            corr_value = correlation_analysis['Engagement_Rate']['correlation']
            if corr_value > 0.3:
                insights.append({
                    'type': 'success',
                    'title': '📈 Longer = More Engagement',
                    'message': "Your longer videos tend to get better engagement",
                    'recommendation': "Don't be afraid to go longer if content is valuable"
                })
            elif corr_value < -0.3:
                insights.append({
                    'type': 'warning',
                    'title': '⚡ Shorter = More Engagement',
                    'message': "Your shorter videos perform significantly better",
                    'recommendation': "Focus on concise, punchy content under 30 seconds"
                })
        
        return insights
