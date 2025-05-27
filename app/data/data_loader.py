import pandas as pd
from pathlib import Path
from app.database.models import DatabaseManager
from app.utils.logger import get_logger
from app.utils.validators import DataValidator
import os
import streamlit as st
from dotenv import load_dotenv
import kaggle

load_dotenv()
logger = get_logger(__name__)

class DataLoader:
    """data loader with database integration"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.validator = DataValidator()

    def load_superstore_data(self) -> pd.DataFrame:
        """Load Superstore data via Kaggle API or local file"""
        try:
            # Check if train.csv exists locally
            local_path = "data/train.csv"
            if Path(local_path).exists():
                logger.info("Loading local train.csv")
                df = pd.read_csv(local_path)
            else:
                # Download from Kaggle
                kaggle.api.authenticate()
                kaggle.api.dataset_download_file(
                    'rohitsahoo/sales-forecasting', 
                    'train.csv', 
                    path='data/'
                )
                df = pd.read_csv('data/train.csv')
            
            # Convert dates
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
            df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
            
            # Validate required columns
            required_columns = ['Row ID', 'Order Date', 'Sales', 'Region', 'Category', 
                              'Sub-Category', 'Segment', 'Ship Mode', 'Product Name', 
                              'City', 'State', 'Postal Code']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Missing required columns")
            
            logger.info(f"Loaded {len(df)} Superstore records")
            return df
        except Exception as e:
            logger.error(f"Failed to load Superstore data: {str(e)}")
            raise
    
    def initialize_database(self) -> bool:
        """Initialize database with Superstore data"""
        try:
            if self.db_manager.has_data():
                logger.info("Database already contains data")
                return True
            
            df = self.load_superstore_data()
            records_inserted = self.db_manager.insert_dataframe(df)
            logger.info(f"Database initialized with {records_inserted} records")
            return True
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            return False
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all data from database"""
        try:
            return self.db_manager.get_all_transactions()
        except Exception as e:
            logger.error(f"Failed to get all data: {str(e)}")
            return pd.DataFrame()
        
    def check_data_exists(self) -> bool:
        """Quick check if database has data without loading it"""
        try:
            return self.db_manager.has_data()
        except Exception as e:
            logger.error(f"Failed to check data existence: {str(e)}")
            return False

    def filter_by_region(self, region: str) -> pd.DataFrame:
        """Filter data by region from database"""
        try:
            return self.db_manager.filter_by_region(region)
        except Exception as e:
            logger.error(f"Failed to filter by region: {str(e)}")
            return pd.DataFrame()
    
    def get_regions(self) -> list:
        """Get available regions"""
        try:
            return self.db_manager.get_regions()
        except Exception as e:
            logger.error(f"Failed to get regions: {str(e)}")
            return []
    
    def get_segments(self) -> list:
        """Get available segments"""
        try:
            return self.db_manager.get_segments()
        except Exception as e:
            logger.error(f"Failed to get segments: {str(e)}")
            return []
    
    def get_categories(self) -> list:
        """Get available categories"""
        try:
            return self.db_manager.get_categories()
        except Exception as e:
            logger.error(f"Failed to get categories: {str(e)}")
            return []
        
    def get_data_info(self):
        # Return summary info (like record counts)
        return {
            "total_records": len(self.get_all_data()),
            "regions": len(self.get_regions()),
            "categories": len(self.get_categories())
        }
    
    def close(self):
        """Close database connections"""
        self.db_manager.close()
