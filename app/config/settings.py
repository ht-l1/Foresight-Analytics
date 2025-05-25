import logging
from pathlib import Path
from typing import Dict, List

class AppConfig:
    """Centralized application configuration"""
    
    # Application Settings
    APP_NAME = "Foresight Analytics"
    VERSION = "1.0.0"
    # Important! Set to false after ready to deploy to prod
    DEBUG = True
    
    PAGE_TITLE = "Foresight Analytics"
    PAGE_LAYOUT = "wide"

    # Visualization Settings
    PLOT_WIDTH = 12
    PLOT_HEIGHT = 8
    
    COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent': '#2ca02c'
    }
    
    # Data Settings
    DEFAULT_FORECAST_MONTHS = 6
    MIN_FORECAST_MONTHS = 1
    MAX_FORECAST_MONTHS = 24
    
    # Account Type Mappings
    ACCOUNT_TYPE_MAPPING: Dict[str, List[str]] = {
        'Assets': ['Assets'],
        'Liabilities': ['Loans'],
        'Expenses': ['Salaries', 'Supplies', 'Utilities', 'Rent', 'Royalties'],
        'Revenue': ['Product Sales', 'Service Revenue']
    }
    
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
    def get_account_categories(cls, account_type: str) -> List[str]:
        """Get categories for a specific account type"""
        return cls.ACCOUNT_TYPE_MAPPING.get(account_type, [])
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)