"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Environment Detection
    IS_VERCEL = 'VERCEL' in os.environ
    IS_AWS = 'AWS_LAMBDA_FUNCTION_NAME' in os.environ
    IS_CLOUD = os.getenv('ENV_TYPE') == 'cloud' or IS_VERCEL or IS_AWS

    # Upload settings
    # Use /tmp for serverless/cloud environments where root is read-only
    if IS_CLOUD:
        UPLOAD_FOLDER = os.path.join('/tmp', 'uploads')
        print(f"☁️ Cloud environment detected. Using ephemeral storage: {UPLOAD_FOLDER}")
    else:
        UPLOAD_FOLDER = os.path.abspath(os.getenv('UPLOAD_FOLDER', 'uploads'))
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Groq AI Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Application settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

    @classmethod
    def validate(cls):
        # Enforce strong/explicit SECRET_KEY in production
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise RuntimeError("SECRET_KEY must be set for production")


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
