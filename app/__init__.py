"""
Flask Application Factory
"""
from flask import Flask, render_template
import os
from .config import config
from .routes import upload_bp, data_bp, analysis_bp


def create_app(config_name='default'):
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(analysis_bp)
    
    # Root route
    @app.route('/')
    def index():
        return render_template('index_dynamic.html')
    
    return app
