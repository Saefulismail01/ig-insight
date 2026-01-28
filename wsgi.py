"""
Instagram Meta Insight Dashboard
Main entry point for the application
"""
import os
from app import create_app
from app.config import Config

# Create Flask app
# Default to production for safer deployments
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    print("🚀 Starting Instagram Meta Insight Dashboard...")
    print(f"📊 Server running on http://{Config.HOST}:{Config.PORT}")
    print(f"🔍 Debug mode: {Config.DEBUG}")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
