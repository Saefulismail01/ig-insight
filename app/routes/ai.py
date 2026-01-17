"""
AI Chat Routes
Handle AI-powered chat interactions
"""
from flask import Blueprint, request, jsonify
import requests
from ..config import Config

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/ai-chat', methods=['POST'])
def ai_chat():
    """Handle AI chat requests"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    if not Config.GROQ_API_KEY:
        return jsonify({'error': 'Groq API key not configured. Set GROQ_API_KEY environment variable.'}), 500
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        
        if not message:
            return jsonify({'error': 'Message cannot be empty.'}), 400
        
        # Get data context
        all_posts = processed_data.get('all_posts', [])
        if not all_posts:
            return jsonify({'error': 'No post data available for analysis.'}), 400
        
        # Create data summary
        data_summary = _create_data_summary(all_posts)
        
        # Build conversation for Groq
        messages = _build_groq_messages(message, conversation_history, data_summary)
        
        # Call Groq API
        groq_payload = {
            "model": Config.GROQ_MODEL,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 800
        }
        
        headers = {
            "Authorization": f"Bearer {Config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(Config.GROQ_API_URL, headers=headers, json=groq_payload, timeout=30)
        response.raise_for_status()
        groq_data = response.json()
        ai_response = groq_data['choices'][0]['message']['content'].strip()
        
        return jsonify({'response': ai_response})
        
    except requests.exceptions.RequestException as req_err:
        print(f"Groq API error: {req_err}")
        return jsonify({'error': 'AI service is currently unavailable. Please try again later.'}), 502
    except Exception as e:
        print(f"Error in ai_chat: {str(e)}")
        return jsonify({'error': 'Failed to generate AI response. Please try again.'}), 500


def _create_data_summary(all_posts):
    """Create summary of data for AI context"""
    return {
        'total_posts': len(all_posts),
        'date_range': {
            'start': min(post['Publish time'] for post in all_posts if post.get('Publish time')),
            'end': max(post['Publish time'] for post in all_posts if post.get('Publish time'))
        },
        'engagement_stats': {
            'avg_engagement_rate': sum(post.get('Engagement_Rate', 0) for post in all_posts) / len(all_posts),
            'total_engagement': sum(post.get('Likes', 0) + post.get('Comments', 0) + 
                                  post.get('Shares', 0) + post.get('Saves', 0) for post in all_posts),
            'total_views': sum(post.get('Views', 0) for post in all_posts),
            'total_follows': sum(post.get('Follows', 0) for post in all_posts)
        },
        'content_performance': {
            'top_performing_posts': sorted(all_posts, key=lambda x: x.get('Engagement_Rate', 0), reverse=True)[:5],
            'lowest_performing_posts': sorted(all_posts, key=lambda x: x.get('Engagement_Rate', 0))[:5],
            'content_types': list(set(post.get('Post type', 'Unknown') for post in all_posts))
        },
        'quality_tiers': {
            'excellent': len([p for p in all_posts if p.get('Quality_Tier') == 'Excellent']),
            'high': len([p for p in all_posts if p.get('Quality_Tier') == 'High']),
            'medium': len([p for p in all_posts if p.get('Quality_Tier') == 'Medium']),
            'low': len([p for p in all_posts if p.get('Quality_Tier') == 'Low'])
        }
    }


def _build_groq_messages(message, conversation_history, data_summary):
    """Build messages array for Groq API"""
    system_prompt = (
        "You are an AI data analyst specializing in Instagram performance. "
        "Provide actionable, data-driven insights using the supplied metrics. "
        "Use concrete numbers, highlight trends, and keep responses concise and helpful."
    )
    
    messages = [{'role': 'system', 'content': system_prompt}]
    
    for hist in conversation_history[-5:]:
        role = hist.get('role')
        content = hist.get('content')
        if role in ('assistant', 'user') and content:
            messages.append({'role': role, 'content': content})
    
    summary_text = [
        f"Total Posts: {data_summary['total_posts']}",
        f"Date Range: {data_summary['date_range']['start']} to {data_summary['date_range']['end']}",
        f"Average Engagement Rate: {data_summary['engagement_stats']['avg_engagement_rate']:.2f}%",
        f"Total Views: {data_summary['engagement_stats']['total_views']:,}",
        f"Total Follows: {data_summary['engagement_stats']['total_follows']:,}",
        f"Content Types: {', '.join(data_summary['content_performance']['content_types'])}"
    ]
    
    top_posts_str = "\n".join(
        f"- {post.get('short_description', 'N/A')} | ER {post.get('Engagement_Rate', 0):.2f}% | {post.get('Views', 0):,} views"
        for post in data_summary['content_performance']['top_performing_posts']
    ) or "No top posts data."
    
    user_prompt = (
        "Instagram dataset summary:\n"
        f"{chr(10).join(summary_text)}\n\n"
        f"Top Performing Posts:\n{top_posts_str}\n\n"
        f"User Question: {message}\n\n"
        "Provide insights and recommendations referencing the metrics above."
    )
    
    messages.append({'role': 'user', 'content': user_prompt})
    
    return messages
