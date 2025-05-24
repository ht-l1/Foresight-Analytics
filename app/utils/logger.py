"""
Adding to provide a centralized logging setup for the app.
It configures loggers to output messages to both the console and a dedicated log file.
Log levels and formats are sourced from the central configuration under config/settings.py
"""

import logging
import sys
from pathlib import Path
from app.config.settings import AppConfig

class Logger:
    """Centralized logging configuration"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name not in cls._loggers:
            cls._loggers[name] = cls._setup_logger(name)
        return cls._loggers[name]
    
    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(AppConfig.LOG_LEVEL)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Create formatters
        formatter = logging.Formatter(AppConfig.LOG_FORMAT)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(AppConfig.LOG_LEVEL)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (only if not in debug mode)
        if not AppConfig.DEBUG:
            AppConfig.setup_directories()
            file_handler = logging.FileHandler(
                AppConfig.LOGS_DIR / f"{AppConfig.APP_NAME.lower().replace(' ', '_')}.log"
            )
            file_handler.setLevel(AppConfig.LOG_LEVEL)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

# for quick logger access
def get_logger(name: str) -> logging.Logger:
    """Quick access to logger"""
    return Logger.get_logger(name)