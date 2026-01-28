"""
Hashtag Category Analysis Service
Analyze content based on hashtag categories: #news, #meme, #insight, #edu
"""
import pandas as pd
import numpy as np


class HashtagCategoryAnalyzer:
    """Analyze content performance based on hashtag categories"""
    
    def __init__(self):
        self.categories = ['news', 'meme', 'insight', 'edu']
    
    def perform_category_analysis(self, df):
        """Perform comprehensive hashtag category analysis"""
        
        if 'Description' not in df.columns:
            return {'error': 'No Description column found', 'available': False}
        
        # Extract categories from descriptions
        df = self._extract_categories(df)
        
        # Get category counts
        category_counts = self._get_category_counts(df)
        
        # Get category performance metrics
        category_performance = self._get_category_performance(df)
        
        # Generate insights
        insights = self._generate_insights(category_counts, category_performance)
        
        return {
            'available': True,
            'category_counts': category_counts,
            'category_performance': category_performance,
            'insights': insights,
            'total_posts': int(len(df)),
            'categorized_posts': int(df['has_category'].sum()),
            'uncategorized_posts': int((~df['has_category']).sum())
        }
    
    def _extract_categories(self, df):
        """Extract category information from descriptions"""
        
        df = df.copy()  # Prevent SettingWithCopyWarning
        
        for cat in self.categories:
            df[f'is_{cat}'] = df['Description'].fillna('').str.lower().str.contains(f'#{cat}', regex=False)
        
        df['has_category'] = df[[f'is_{cat}' for cat in self.categories]].any(axis=1)
        
        return df
    
    def _get_category_counts(self, df):
        """Count posts per category"""
        
        counts = {}
        total = len(df)
        
        for cat in self.categories:
            count = df[f'is_{cat}'].sum()
            counts[cat] = {
                'count': int(count),
                'percentage': round((count / total) * 100, 1) if total > 0 else 0
            }
        
        return counts
    
    def _get_category_performance(self, df):
        """Calculate performance metrics for each category"""
        
        performance = {}
        
        for cat in self.categories:
            cat_df = df[df[f'is_{cat}'] == True]
            
            if len(cat_df) == 0:
                performance[cat] = {
                    'count': 0,
                    'avg_views': 0,
                    'avg_likes': 0,
                    'avg_comments': 0,
                    'avg_shares': 0,
                    'avg_saves': 0,
                    'avg_engagement_rate': 0,
                    'total_views': 0,
                    'total_likes': 0
                }
                continue
            
            performance[cat] = {
                'count': int(len(cat_df)),
                'avg_views': float(round(cat_df['Views'].mean(), 0)) if 'Views' in cat_df.columns else 0,
                'avg_likes': float(round(cat_df['Likes'].mean(), 0)) if 'Likes' in cat_df.columns else 0,
                'avg_comments': float(round(cat_df['Comments'].mean(), 1)) if 'Comments' in cat_df.columns else 0,
                'avg_shares': float(round(cat_df['Shares'].mean(), 1)) if 'Shares' in cat_df.columns else 0,
                'avg_saves': float(round(cat_df['Saves'].mean(), 1)) if 'Saves' in cat_df.columns else 0,
                'avg_engagement_rate': float(round(cat_df['Engagement_Rate'].mean(), 2)) if 'Engagement_Rate' in cat_df.columns else 0,
                'total_views': int(cat_df['Views'].sum()) if 'Views' in cat_df.columns else 0,
                'total_likes': int(cat_df['Likes'].sum()) if 'Likes' in cat_df.columns else 0
            }
        
        return performance
    
    def _generate_insights(self, counts, performance):
        """Generate actionable insights"""
        
        insights = []
        
        # Find categories with posts
        active_cats = {k: v for k, v in performance.items() if v['count'] > 0}
        
        if not active_cats:
            return [{
                'type': 'info',
                'title': 'No Categorized Content',
                'message': 'Tidak ada post dengan hashtag #news, #meme, #insight, atau #edu',
                'recommendation': 'Tambahkan hashtag kategori ke deskripsi konten Anda'
            }]
        
        # Best engagement category
        best_er = max(active_cats.items(), key=lambda x: x[1]['avg_engagement_rate'])
        insights.append({
            'type': 'success',
            'title': f'#{best_er[0].upper()} Terbaik',
            'message': f'Konten #{best_er[0]} memiliki engagement rate tertinggi: {best_er[1]["avg_engagement_rate"]}%',
            'recommendation': f'Fokus membuat lebih banyak konten #{best_er[0]}'
        })
        
        # Most views category
        best_views = max(active_cats.items(), key=lambda x: x[1]['avg_views'])
        if best_views[0] != best_er[0]:
            insights.append({
                'type': 'info',
                'title': f'#{best_views[0].upper()} Paling Banyak Views',
                'message': f'Rata-rata {int(best_views[1]["avg_views"]):,} views per post',
                'recommendation': f'Gunakan #{best_views[0]} untuk jangkauan maksimal'
            })
        
        # Most common category
        most_common = max(active_cats.items(), key=lambda x: x[1]['count'])
        insights.append({
            'type': 'info',
            'title': 'Distribusi Konten',
            'message': f'#{most_common[0]} adalah kategori terbanyak dengan {most_common[1]["count"]} post',
            'recommendation': 'Diversifikasi konten untuk pertumbuhan seimbang'
        })
        
        return insights
