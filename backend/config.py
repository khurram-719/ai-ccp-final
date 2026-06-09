import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

DIFFICULTY_LEVELS = {
    'Easy': {'min_cells': 35, 'max_cells': 40},
    'Medium': {'min_cells': 30, 'max_cells': 34},
    'Hard': {'min_cells': 25, 'max_cells': 29},
    'Expert': {'min_cells': 20, 'max_cells': 24}
}
