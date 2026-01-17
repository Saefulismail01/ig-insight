"""
Caption Analysis Service
Analyze captions, hashtags, and text content for performance insights
"""
import re
from collections import Counter
import pandas as pd


class CaptionAnalyzer:
    """Analyze caption content for optimization insights"""
    
    def __init__(self):
        self.emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+",
            flags=re.UNICODE
        )
    
    def perform_caption_analysis(self, df):
        """Perform comprehensive caption analysis"""
        try:
            # Ensure Description column exists
            if 'Description' not in df.columns:
                return {'error': 'Description column not found in data'}
            
            # Clean and prepare data
            df_clean = df.copy()
            df_clean['Description'] = df_clean['Description'].fillna('').astype(str)
            
            # Extract features
            df_clean = self._extract_caption_features(df_clean)
            
            # Analyze hashtags
            hashtag_analysis = self._analyze_hashtags(df_clean)
            
            # Analyze caption length
            length_analysis = self._analyze_caption_length(df_clean)
            
            # Analyze emoji usage
            emoji_analysis = self._analyze_emoji_usage(df_clean)
            
            # Analyze CTA presence
            cta_analysis = self._analyze_cta(df_clean)
            
            # Top performing captions
            top_captions = self._get_top_captions(df_clean)
            
            # Keywords analysis
            keyword_analysis = self._analyze_keywords(df_clean)
            
            # Overall insights
            insights = self._generate_caption_insights(
                hashtag_analysis, length_analysis, emoji_analysis, cta_analysis
            )
            
            return {
                'hashtag_analysis': hashtag_analysis,
                'length_analysis': length_analysis,
                'emoji_analysis': emoji_analysis,
                'cta_analysis': cta_analysis,
                'top_captions': top_captions,
                'keyword_analysis': keyword_analysis,
                'insights': insights,
                'total_posts_analyzed': len(df_clean)
            }
            
        except Exception as e:
            print(f"Error in perform_caption_analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _extract_caption_features(self, df):
        """Extract features from captions"""
        # Word count
        df['word_count'] = df['Description'].str.split().str.len()
        
        # Character count
        df['char_count'] = df['Description'].str.len()
        
        # Hashtag count
        df['hashtag_count'] = df['Description'].str.count('#')
        
        # Extract hashtags
        df['hashtags'] = df['Description'].apply(self._extract_hashtags)
        
        # Emoji count
        df['emoji_count'] = df['Description'].apply(lambda x: len(self.emoji_pattern.findall(x)))
        
        # Has CTA
        df['has_cta'] = df['Description'].apply(self._has_cta)
        
        # Question mark (engagement trigger)
        df['has_question'] = df['Description'].str.contains('?', regex=False)
        
        return df
    
    def _extract_hashtags(self, text):
        """Extract hashtags from text"""
        return re.findall(r'#(\w+)', text)
    
    def _has_cta(self, text):
        """Check if text has CTA (Call-to-Action)"""
        cta_keywords = [
            'link in bio', 'click', 'swipe', 'tap', 'comment', 'share', 
            'follow', 'subscribe', 'watch', 'check out', 'visit', 'download',
            'get', 'buy', 'shop', 'order', 'dm', 'message', 'tag', 'save'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in cta_keywords)
    
    def _analyze_hashtags(self, df):
        """Analyze hashtag performance"""
        # Posts with hashtags
        posts_with_hashtags = df[df['hashtag_count'] > 0]
        posts_without_hashtags = df[df['hashtag_count'] == 0]
        
        # Performance comparison
        with_hashtags_er = posts_with_hashtags['Engagement_Rate'].mean() if len(posts_with_hashtags) > 0 else 0
        without_hashtags_er = posts_without_hashtags['Engagement_Rate'].mean() if len(posts_without_hashtags) > 0 else 0
        
        # Top performing hashtags
        all_hashtags = []
        for idx, row in posts_with_hashtags.iterrows():
            for hashtag in row['hashtags']:
                all_hashtags.append({
                    'hashtag': hashtag,
                    'engagement_rate': row['Engagement_Rate'],
                    'views': row['Views'],
                    'likes': row['Likes']
                })
        
        if all_hashtags:
            hashtag_df = pd.DataFrame(all_hashtags)
            top_hashtags = hashtag_df.groupby('hashtag').agg({
                'engagement_rate': 'mean',
                'views': 'mean',
                'likes': 'mean'
            }).round(2).sort_values('engagement_rate', ascending=False).head(10)
            
            top_hashtags_list = [
                {
                    'hashtag': f"#{hashtag}",
                    'avg_engagement_rate': float(row['engagement_rate']),
                    'avg_views': int(row['views']),
                    'avg_likes': int(row['likes']),
                    'usage_count': len(hashtag_df[hashtag_df['hashtag'] == hashtag])
                }
                for hashtag, row in top_hashtags.iterrows()
            ]
        else:
            top_hashtags_list = []
        
        # Optimal hashtag count
        hashtag_count_performance = df.groupby('hashtag_count').agg({
            'Engagement_Rate': 'mean',
            'Views': 'mean'
        }).round(2)
        
        optimal_count = hashtag_count_performance['Engagement_Rate'].idxmax() if not hashtag_count_performance.empty else 0
        
        return {
            'posts_with_hashtags': int(len(posts_with_hashtags)),
            'posts_without_hashtags': int(len(posts_without_hashtags)),
            'avg_er_with_hashtags': float(with_hashtags_er),
            'avg_er_without_hashtags': float(without_hashtags_er),
            'performance_lift': float(with_hashtags_er - without_hashtags_er),
            'top_hashtags': top_hashtags_list,
            'optimal_hashtag_count': int(optimal_count) if pd.notna(optimal_count) else 0,
            'avg_hashtag_per_post': float(df['hashtag_count'].mean())
        }
    
    def _analyze_caption_length(self, df):
        """Analyze caption length impact on performance"""
        # Create length buckets
        df['length_bucket'] = pd.cut(
            df['word_count'],
            bins=[0, 20, 50, 100, 200, 1000],
            labels=['Very Short (0-20)', 'Short (21-50)', 'Medium (51-100)', 'Long (101-200)', 'Very Long (200+)']
        )
        
        length_performance = df.groupby('length_bucket', observed=True).agg({
            'Engagement_Rate': 'mean',
            'Views': 'mean',
            'Likes': 'mean',
            'Comments': 'mean',
            'Shares': 'mean',
            'Saves': 'mean'
        }).round(2)
        
        # Find optimal length
        optimal_bucket = length_performance['Engagement_Rate'].idxmax() if not length_performance.empty else None
        
        # Convert to dictionary
        length_data = []
        for bucket in length_performance.index:
            length_data.append({
                'length_range': str(bucket),
                'avg_engagement_rate': float(length_performance.loc[bucket, 'Engagement_Rate']),
                'avg_views': int(length_performance.loc[bucket, 'Views']),
                'avg_likes': int(length_performance.loc[bucket, 'Likes']),
                'post_count': int(len(df[df['length_bucket'] == bucket]))
            })
        
        return {
            'length_performance': length_data,
            'optimal_length': str(optimal_bucket) if optimal_bucket else 'Unknown',
            'avg_word_count': float(df['word_count'].mean()),
            'median_word_count': float(df['word_count'].median())
        }
    
    def _analyze_emoji_usage(self, df):
        """Analyze emoji usage impact"""
        posts_with_emoji = df[df['emoji_count'] > 0]
        posts_without_emoji = df[df['emoji_count'] == 0]
        
        with_emoji_er = posts_with_emoji['Engagement_Rate'].mean() if len(posts_with_emoji) > 0 else 0
        without_emoji_er = posts_without_emoji['Engagement_Rate'].mean() if len(posts_without_emoji) > 0 else 0
        
        # Optimal emoji count
        emoji_count_performance = df.groupby('emoji_count').agg({
            'Engagement_Rate': 'mean'
        }).round(2)
        
        optimal_emoji_count = emoji_count_performance['Engagement_Rate'].idxmax() if not emoji_count_performance.empty else 0
        
        return {
            'posts_with_emoji': int(len(posts_with_emoji)),
            'posts_without_emoji': int(len(posts_without_emoji)),
            'avg_er_with_emoji': float(with_emoji_er),
            'avg_er_without_emoji': float(without_emoji_er),
            'performance_lift': float(with_emoji_er - without_emoji_er),
            'optimal_emoji_count': int(optimal_emoji_count) if pd.notna(optimal_emoji_count) else 0,
            'avg_emoji_per_post': float(df['emoji_count'].mean())
        }
    
    def _analyze_cta(self, df):
        """Analyze CTA (Call-to-Action) impact"""
        posts_with_cta = df[df['has_cta'] == True]
        posts_without_cta = df[df['has_cta'] == False]
        
        with_cta_er = posts_with_cta['Engagement_Rate'].mean() if len(posts_with_cta) > 0 else 0
        without_cta_er = posts_without_cta['Engagement_Rate'].mean() if len(posts_without_cta) > 0 else 0
        
        # Specific metrics
        with_cta_comments = posts_with_cta['Comments'].mean() if len(posts_with_cta) > 0 else 0
        without_cta_comments = posts_without_cta['Comments'].mean() if len(posts_without_cta) > 0 else 0
        
        return {
            'posts_with_cta': int(len(posts_with_cta)),
            'posts_without_cta': int(len(posts_without_cta)),
            'avg_er_with_cta': float(with_cta_er),
            'avg_er_without_cta': float(without_cta_er),
            'performance_lift': float(with_cta_er - without_cta_er),
            'avg_comments_with_cta': float(with_cta_comments),
            'avg_comments_without_cta': float(without_cta_comments),
            'comment_lift': float(with_cta_comments - without_cta_comments)
        }
    
    def _get_top_captions(self, df, limit=5):
        """Get top performing captions"""
        top_posts = df.nlargest(limit, 'Engagement_Rate')
        
        captions = []
        for _, post in top_posts.iterrows():
            caption_text = post['Description'][:150] + '...' if len(post['Description']) > 150 else post['Description']
            
            captions.append({
                'caption': caption_text,
                'engagement_rate': float(post['Engagement_Rate']),
                'views': int(post['Views']),
                'word_count': int(post['word_count']),
                'hashtag_count': int(post['hashtag_count']),
                'emoji_count': int(post['emoji_count']),
                'has_cta': bool(post['has_cta'])
            })
        
        return captions
    
    def _analyze_keywords(self, df):
        """Analyze common keywords in top performing posts"""
        # Get top 25% performing posts
        top_performers = df[df['Engagement_Rate'] >= df['Engagement_Rate'].quantile(0.75)]
        
        # Extract words (excluding hashtags and common words)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'this',
                    'that', 'it', 'they', 'we', 'you', 'i', 'my', 'your', 'our'}
        
        all_words = []
        for caption in top_performers['Description']:
            # Remove hashtags and special characters
            caption_clean = re.sub(r'#\w+', '', caption)
            caption_clean = re.sub(r'[^\w\s]', '', caption_clean)
            
            words = caption_clean.lower().split()
            words = [w for w in words if len(w) > 3 and w not in stopwords]
            all_words.extend(words)
        
        # Count word frequency
        word_counts = Counter(all_words).most_common(20)
        
        return [
            {'word': word, 'frequency': count}
            for word, count in word_counts
        ]
    
    def _generate_caption_insights(self, hashtag_analysis, length_analysis, emoji_analysis, cta_analysis):
        """Generate actionable insights"""
        insights = []
        
        # Hashtag insights
        if hashtag_analysis['performance_lift'] > 0:
            insights.append({
                'type': 'success',
                'title': '🏷️ Hashtags Boost Performance',
                'message': f"Posts with hashtags get {hashtag_analysis['performance_lift']:.2f}% higher engagement",
                'recommendation': f"Use {hashtag_analysis['optimal_hashtag_count']} hashtags per post for best results"
            })
        else:
            insights.append({
                'type': 'warning',
                'title': '🏷️ Hashtags Not Helping',
                'message': "Hashtags are reducing engagement on your posts",
                'recommendation': "Focus on relevant, niche hashtags instead of popular ones"
            })
        
        # Caption length insights
        insights.append({
            'type': 'info',
            'title': '📝 Optimal Caption Length',
            'message': f"Your best performing captions are {length_analysis['optimal_length']}",
            'recommendation': f"Current average: {length_analysis['avg_word_count']:.0f} words. Adjust based on optimal range."
        })
        
        # Emoji insights
        if emoji_analysis['performance_lift'] > 0:
            insights.append({
                'type': 'success',
                'title': '😊 Emojis Increase Engagement',
                'message': f"Posts with emojis get {emoji_analysis['performance_lift']:.2f}% higher engagement",
                'recommendation': f"Use {emoji_analysis['optimal_emoji_count']} emojis per caption for best results"
            })
        
        # CTA insights
        if cta_analysis['performance_lift'] > 0:
            insights.append({
                'type': 'success',
                'title': '📢 CTAs Drive Engagement',
                'message': f"Posts with CTAs get {cta_analysis['comment_lift']:.1f} more comments on average",
                'recommendation': "Include clear call-to-actions in your captions"
            })
        
        return insights
