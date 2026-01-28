"""
Analysis Routes
Handle various analysis endpoints
"""
from flask import Blueprint, jsonify
import pandas as pd
from ..services import QualityAnalyzer, OutlierAnalyzer, HashtagCategoryAnalyzer, DurationOptimizer

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/quality-analysis')
def get_quality_analysis():
    """Get quality analysis"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for quality analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'])
        
        analyzer = QualityAnalyzer()
        quality_data = analyzer.perform_quality_analysis(df)
        
        return jsonify(quality_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/outlier-analysis')
def get_outlier_analysis():
    """Get outlier analysis"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for outlier analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'])
        
        analyzer = OutlierAnalyzer()
        outlier_data = analyzer.perform_outlier_analysis(df)
        
        return jsonify(outlier_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/follower-trend')
def get_follower_trend():
    """Get follower trend analysis"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for follower trend analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'], errors='coerce')
        df = df.dropna(subset=['Publish time'])
        df = df.sort_values('Publish time')
        
        df['Date'] = df['Publish time'].dt.date
        daily_data = df.groupby('Date').agg({
            'Follows': 'sum',
            'Views': 'sum',
            'Likes': 'sum',
            'Shares': 'sum',
            'Saves': 'sum',
            'Comments': 'sum'
        }).reset_index()
        
        daily_data['Cumulative_Followers'] = daily_data['Follows'].cumsum()
        daily_data['Engagement_Rate'] = (
            (daily_data['Likes'] + daily_data['Comments'] + daily_data['Shares'] + daily_data['Saves']) / 
            daily_data['Views'].replace(0, 1)
        ) * 100
        
        chart_data = {
            'dates': [date.strftime('%Y-%m-%d') for date in daily_data['Date']],
            'cumulative_followers': daily_data['Cumulative_Followers'].tolist(),
            'daily_follows': daily_data['Follows'].tolist(),
            'engagement_rate': daily_data['Engagement_Rate'].round(2).tolist(),
            'total_followers': int(daily_data['Cumulative_Followers'].iloc[-1]) if len(daily_data) > 0 else 0,
            'total_days': len(daily_data),
            'avg_daily_follows': round(daily_data['Follows'].mean(), 1) if len(daily_data) > 0 else 0,
            'peak_follows': int(daily_data['Follows'].max()) if len(daily_data) > 0 else 0,
            'insights': [
                f"Total followers gained: {daily_data['Cumulative_Followers'].iloc[-1] if len(daily_data) > 0 else 0}",
                f"Average daily follows: {daily_data['Follows'].mean():.1f}",
                f"Peak daily follows: {daily_data['Follows'].max() if len(daily_data) > 0 else 0}",
                f"Analysis period: {len(daily_data)} days"
            ]
        }
        
        return jsonify(chart_data)
        
    except Exception as e:
        print(f"Error in get_follower_trend: {str(e)}")
        return jsonify({'error': str(e)})


@analysis_bp.route('/content-type-analysis')
def get_content_type_analysis():
    """Get content type analysis"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        post_type_performance = processed_data.get('post_type_performance', {})
        all_posts = processed_data.get('all_posts', [])
        
        if not post_type_performance:
            return jsonify({'error': 'No post type data available for analysis.'}), 400
        
        post_counts = {}
        for post in all_posts:
            post_type = post.get('Post type', 'Unknown')
            post_counts[post_type] = post_counts.get(post_type, 0) + 1
        
        for post_type in post_type_performance:
            post_type_performance[post_type]['post_count'] = post_counts.get(post_type, 0)
        
        insights = _generate_content_type_insights(post_type_performance, post_counts)
        
        content_type_analysis = {
            'content_type_performance': post_type_performance,
            'total_content_types': len(post_type_performance),
            'insights': insights
        }
        
        return jsonify(content_type_analysis)
        
    except Exception as e:
        print(f"Error in get_content_type_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/category-analysis')
def get_category_analysis():
    """Get hashtag category analysis (#news, #meme, #insight, #edu)"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for category analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'])
        
        analyzer = HashtagCategoryAnalyzer()
        category_data = analyzer.perform_category_analysis(df)
        
        return jsonify(category_data)
        
    except Exception as e:
        print(f"Error in get_category_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/duration-analysis')
def get_duration_analysis():
    """Get duration analysis"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for duration analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'])
        
        analyzer = DurationOptimizer()
        duration_data = analyzer.perform_duration_analysis(df)
        
        return jsonify(duration_data)
        
    except Exception as e:
        print(f"Error in get_duration_analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


def _generate_content_type_insights(post_type_performance, post_counts):
    """Generate insights for content type analysis"""
    insights = []
    
    if not post_type_performance:
        return ["No content type data available for analysis."]
    
    best_by_views = max(post_type_performance.keys(), 
                       key=lambda x: post_type_performance[x].get('Views', 0))
    best_by_engagement = max(post_type_performance.keys(), 
                           key=lambda x: post_type_performance[x].get('Engagement_Rate', 0))
    
    insights.append(f"Best performing by views: {best_by_views} with avg {post_type_performance[best_by_views].get('Views', 0):.0f} views")
    insights.append(f"Best engagement rate: {best_by_engagement} with {post_type_performance[best_by_engagement].get('Engagement_Rate', 0):.2f}% ER")
    
    if len(post_type_performance) > 1:
        total_posts = sum(post_counts.values())
        content_mix = []
        for post_type, count in post_counts.items():
            percentage = (count / total_posts) * 100
            content_mix.append(f"{post_type}: {percentage:.1f}%")
        
        insights.append(f"Current content mix: {', '.join(content_mix)}")
    
    return insights
