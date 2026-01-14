"""
Configuration file for Ryde University Student Records Application
"""

import os
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root


class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # MySQL Database configuration
    # In production, retrieve these from AWS Secrets Manager
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'ryde_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'ryde_password')
    DB_NAME = os.environ.get('DB_NAME', 'ryde_university')
    
    # For AWS RDS Multi-AZ deployment
    # DB_HOST should be the RDS endpoint (e.g., ryde-db.xxxxxxxxxxxx.ap-southeast-2.rds.amazonaws.com)
    
    # Connection pool settings
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', 10))
    DB_POOL_TIMEOUT = int(os.environ.get('DB_POOL_TIMEOUT', 30))
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    DB_HOST = 'localhost'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # In production, all sensitive values should come from environment variables
    # or AWS Secrets Manager
    

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DB_NAME = 'ryde_university_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
