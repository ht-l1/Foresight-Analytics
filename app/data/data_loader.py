import pandas as pd
from pathlib import Path
from app.database.models import DatabaseManager
from app.utils.logger import get_logger
from app.utils.validators import DataValidator

logger = get_logger(__name__)

class DataLoader:
    """data loader with database integration"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.validator = DataValidator()
    
    def load_data_from_csv(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            df = pd.read_csv(file_path)
            df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
            
            # Validate data
            validation_results = self.validator.validate_dataframe(df)
            if not validation_results['is_valid']:
                logger.error(f"Data validation failed: {validation_results['errors']}")
                raise ValueError("Invalid data format")
            
            # Clean data
            df = self.validator.clean_dataframe(df)
            
            logger.info(f"Loaded {len(df)} records from CSV: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load CSV data: {str(e)}")
            raise
    
    def initialize_database(self, csv_file_path: str) -> bool:
        """Initialize database with CSV data"""
        try:
            # Check if database already has data
            existing_data = self.db_manager.get_all_transactions()
            if not existing_data.empty:
                logger.info("Database already contains data. Skipping initialization.")
                return True
            
            # Load and insert CSV data
            df = self.load_data_from_csv(csv_file_path)
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
    
    def filter_by_department(self, department: str) -> pd.DataFrame:
        """Filter data by department from database"""
        try:
            return self.db_manager.filter_by_department(department)
        except Exception as e:
            logger.error(f"Failed to filter by department: {str(e)}")
            return pd.DataFrame()
    
    def get_departments(self) -> list:
        """Get available departments"""
        try:
            return self.db_manager.get_departments()
        except Exception as e:
            logger.error(f"Failed to get departments: {str(e)}")
            return []
    
    def get_categories(self) -> list:
        """Get available categories"""
        try:
            return self.db_manager.get_categories()
        except Exception as e:
            logger.error(f"Failed to get categories: {str(e)}")
            return []
    
    def get_data_info(self) -> dict:
        """Get basic data information"""
        try:
            df = self.get_all_data()
            if df.empty:
                return {"total_records": 0, "date_range": "No data"}
            
            return {
                "total_records": len(df),
                "date_range": f"{df['Transaction Date'].min().strftime('%Y-%m-%d')} to {df['Transaction Date'].max().strftime('%Y-%m-%d')}",
                "departments": len(self.get_departments()),
                "categories": len(self.get_categories())
            }
        except Exception as e:
            logger.error(f"Failed to get data info: {str(e)}")
            return {"error": str(e)}
    
    def close(self):
        """Close database connections"""
        self.db_manager.close()
