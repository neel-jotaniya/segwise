import os

class Config:
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # For JWT and other secure features
    DEBUG = os.getenv('FLASK_DEBUG', True)

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///triggers.db')  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppress SQLAlchemy warnings

    # Celery Config
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Caching Config
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/0')

    # JWT Config
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')  # Change in production
