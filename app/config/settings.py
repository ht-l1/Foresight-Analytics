import logging
from pathlib import Path
from typing import Dict, List
import os

class AppConfig:
    """Centralized application configuration"""
    
    # Application Settings
    APP_NAME = "Foresight Analytics"
    VERSION = "2.0.0"
    # Important! Set to false after ready to deploy to prod
    DEBUG = True
    
    PAGE_TITLE = "Foresight Analytics"
    PAGE_LAYOUT = "wide"

    # Visualization Settings
    PLOT_WIDTH = 10
    PLOT_HEIGHT = 4
    
    COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent': '#2ca02c'
    }
    
    # Data Settings
    DEFAULT_FORECAST_MONTHS = 12
    MIN_FORECAST_MONTHS = 1
    MAX_FORECAST_MONTHS = 48

    # Model Settings
    MODEL_ACCURACY_THRESHOLD = 70.0  # Minimum acceptable accuracy percentage
    
    # Logging Settings
    LOG_LEVEL = logging.INFO
    # Defines the format for log messages.
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

    # added for database
    @classmethod
    def get_supabase_url(cls):
        return os.getenv('SUPABASE_URL', '')

    @classmethod
    def get_supabase_key(cls):
        return os.getenv('SUPABASE_KEY', '')

    @classmethod
    def get_database_mode(cls):
        return os.getenv('DATABASE_MODE', 'local')

    @classmethod
    def is_cloud_mode(cls):
        """Check if using cloud database"""
        return cls.get_database_mode() == 'cloud'