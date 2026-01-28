"""
Analysis Routes
Handle various analysis endpoints
"""
from flask import Blueprint, jsonify, request, current_app
import pandas as pd
from ..services import QualityAnalyzer, OutlierAnalyzer, HashtagCategoryAnalyzer, DurationOptimizer
from ..services import load_processed_data

analysis_bp = Blueprint('analysis', __name__)

def _get_processed_data_or_400():
    upload_id = request.args.get('upload_id') or request.headers.get('X-Upload-Id')
    if not upload_id:
        return None, (jsonify({'error': 'Missing upload_id. Please upload a CSV file first.'}), 400)
    data = load_processed_data(current_app.config['UPLOAD_FOLDER'], upload_id)
    if data is None:
        return None, (jsonify({'error': 'No data available for this upload_id. Please upload again.'}), 400)
    return data, None


@analysis_bp.route('/test-version')
def test_version():
    """Test endpoint to check server version"""
    # Do not expose debug info in production
    if not current_app.config.get('DEBUG', False):
        return jsonify({'error': 'Not found'}), 404
    from datetime import datetime
    return jsonify({
        'version': 'v2.1_with_daily_views_and_reach_fix',
        'timestamp': datetime.now().isoformat(),
        'status': 'Server is running updated code'
    })


@analysis_bp.route('/debug-daily-views')
def debug_daily_views():
    """Debug endpoint to check daily views data"""
    # Do not expose debug info in production
    if not current_app.config.get('DEBUG', False):
        return jsonify({'error': 'Not found'}), 404
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available'}), 400
        
        df = pd.DataFrame(all_posts)
        
        # Check available columns
        available_cols = df.columns.tolist()
        
        # Check Views and Reach columns
        views_data = {}
        if 'Views' in df.columns:
            views_data['Views'] = {
                'exists': True,
                'sum': float(df['Views'].sum()),
                'mean': float(df['Views'].mean()),
                'sample': df['Views'].head(10).tolist()
            }
        
        reach_data = {}
        if 'Reach' in df.columns:
            reach_data['Reach'] = {
                'exists': True,
                'sum': float(df['Reach'].sum()),
                'mean': float(df['Reach'].mean()),
                'sample': df['Reach'].head(10).tolist()
            }
        
        return jsonify({
            'status': 'success',
            'total_posts': len(df),
            'available_columns': available_cols,
            'views_data': views_data,
            'reach_data': reach_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/quality-analysis')
def get_quality_analysis():
    """Get quality analysis"""
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
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
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
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
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
    try:
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for follower trend analysis.'}), 400
        
        df = pd.DataFrame(all_posts)
        df['Publish time'] = pd.to_datetime(df['Publish time'], errors='coerce')
        df = df.dropna(subset=['Publish time'])
        df = df.sort_values('Publish time')
        
        # Ensure potential columns are numeric
        potential_cols = ['Follows', 'follows', 'Net Followers', 'Views', 'Impressions', 'Reach', 'Plays', 'views', 'impressions', 'Likes', 'Shares', 'Saves', 'Comments']
        for col in potential_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Robust column mapping with Reach as primary fallback
        def find_col(possible_names, default=None):
            for name in possible_names:
                if name in df.columns:
                    col_sum = df[name].sum()
                    if col_sum > 0:
                        print(f"✓ Found non-zero column: {name} (sum={col_sum})")
                        return name
            # Fallback to first existing column even if zero
            for name in possible_names:
                if name in df.columns:
                    print(f"⚠ Using zero-sum column: {name}")
                    return name
            print(f"✗ No column found from {possible_names}, using default: {default}")
            return default

        # Try Reach first since Instagram CSV often uses Reach instead of Views
        view_col = find_col(['Reach', 'Views', 'Impressions', 'Plays', 'views', 'impressions', 'reach'], 'Reach')
        follow_col = find_col(['Follows', 'follows', 'Net Followers'], 'Follows')
        
        # DEBUG: Print available columns and their sums
        print("\n=== DEBUG: Available Columns ===")
        print(f"All columns: {df.columns.tolist()}")
        for col in ['Views', 'Impressions', 'Reach', 'Plays', 'views', 'impressions']:
            if col in df.columns:
                print(f"{col}: sum={df[col].sum()}, sample={df[col].head(3).tolist()}")
        print(f"Selected view_col: {view_col}")
        print(f"Selected follow_col: {follow_col}")
        print("================================\n")
        
        if view_col not in df.columns: df[view_col] = 0
        if follow_col not in df.columns: df[follow_col] = 0

        df['Date'] = df['Publish time'].dt.date
        cols_to_agg = {
            follow_col: 'sum',
            view_col: 'sum',
            'Likes': 'sum',
            'Shares': 'sum',
            'Saves': 'sum',
            'Comments': 'sum'
        }
        cols_to_agg = {k: v for k, v in cols_to_agg.items() if k in df.columns}
        
        daily_data = df.groupby('Date').agg(cols_to_agg).reset_index()
        
        # Rename for internal consistency
        daily_data = daily_data.rename(columns={follow_col: 'Follows', view_col: 'Views'})
        if 'Follows' not in daily_data.columns: daily_data['Follows'] = 0
        if 'Views' not in daily_data.columns: daily_data['Views'] = 0
        
        print(f"DEBUG Follower Trend: Data points: {len(daily_data)}, View Col: {view_col}, View Sum: {daily_data['Views'].sum()}")
        print(f"DEBUG Daily Views Sample: {daily_data['Views'].head(5).tolist()}")
        print(f"DEBUG Daily Follows Sample: {daily_data['Follows'].head(5).tolist()}")
        
        daily_data['Cumulative_Followers'] = daily_data['Follows'].cumsum()
        daily_data['Engagement_Rate'] = (
            (daily_data['Likes'] + daily_data['Comments'] + daily_data['Shares'] + daily_data['Saves']) / 
            daily_data['Views'].replace(0, 1)
        ) * 100
        
        # Advanced Analysis: Growth Phases & Strategy Change
        # 1. Identify Strategy Change (first major view spike or growth acceleration)
        views_mean = daily_data['Views'].mean()
        views_std = daily_data['Views'].std()
        # Strategy change is either when views > mean + 1.5 * std OR growth accelerates significantly
        strategy_change_idx = 0
        for i in range(1, len(daily_data)):
            if daily_data.loc[i, 'Views'] > (views_mean + 1.5 * views_std):
                strategy_change_idx = i
                break
        
        strategy_change_date = daily_data.loc[strategy_change_idx, 'Date'].strftime('%Y-%m-%d')
        
        # 2. Identify Growth Phases
        # Split data into before and after strategy change
        phases = []
        if strategy_change_idx > 0:
            phases.append({
                'name': 'Dormant Phase',
                'start_date': daily_data.loc[0, 'Date'].strftime('%Y-%m-%d'),
                'end_date': daily_data.loc[strategy_change_idx-1, 'Date'].strftime('%Y-%m-%d'),
                'color': 'rgba(148, 163, 184, 0.1)'
            })
        
        # Detect Plateau (when growth slows down significantly after a peak)
        growth_period = daily_data.iloc[strategy_change_idx:]
        plateau_idx = len(daily_data) - 1
        if len(growth_period) > 10:
            # Look at the last 7 days vs previous 7 days
            recent_growth = daily_data['Follows'].iloc[-7:].mean()
            mid_growth = daily_data['Follows'].iloc[strategy_change_idx:-7].mean()
            if recent_growth < mid_growth * 0.5: # 50% drop in growth rate
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

        # Generate specific summary insight
        total_growth = daily_data['Cumulative_Followers'].iloc[-1] - daily_data['Cumulative_Followers'].iloc[0]
        summary_insight = f"Follower growth accelerated after strategy change on {strategy_change_date}"
        if plateau_idx < len(daily_data) - 1:
            summary_insight += ", followed by a plateau phase recently."
        else:
            summary_insight += ", continuing a steady upward trend."

        from datetime import datetime
        
        chart_data = {
            '_server_version': 'v2.1_with_daily_views',  # Version check
            '_timestamp': datetime.now().isoformat(),
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
        
        return jsonify(chart_data)
        
    except Exception as e:
        print(f"Error in get_follower_trend: {str(e)}")
        return jsonify({'error': str(e)})


@analysis_bp.route('/content-type-analysis')
def get_content_type_analysis():
    """Get content type analysis"""
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
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
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
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
    processed_data, err = _get_processed_data_or_400()
    if err:
        return err
    
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
