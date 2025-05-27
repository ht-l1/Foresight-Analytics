import pandas as pd
from typing import List, Dict, Any
from app.utils.logger import get_logger
from app.config.settings import AppConfig

logger = get_logger(__name__)

class DataValidator:
    """Data validation and quality checks"""
    REQUIRED_COLUMNS = ['Row ID', 'Order Date', 'Sales', 'Region', 'Category', 'Sub-Category', 'Segment', 'Product Name', 'Ship Mode', 'Customer Name', 'City', 'State', 'Postal Code']
    
    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Dataframe validation
        Returns: Dictionary with validation results
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'row_count': len(df),
            'null_counts': {}
        }
        
        try:
            # Check if dataframe is empty
            if df.empty:
                validation_results['is_valid'] = False
                validation_results['errors'].append("DataFrame is empty")
                return validation_results
            
            # Check required columns
            missing_cols = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                validation_results['is_valid'] = False
                validation_results['errors'].append(f"Missing required columns: {missing_cols}")
            
            # Check for null values
            for col in cls.REQUIRED_COLUMNS:
                if col in df.columns:
                    null_count = df[col].isnull().sum()
                    validation_results['null_counts'][col] = null_count
                    
                    if null_count > 0:
                        validation_results['warnings'].append(
                            f"Column '{col}' has {null_count} null values"
                        )
            
            # Validate data types
            if 'Order Date' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['Order Date']):
                    validation_results['warnings'].append(
                        "Order Date column is not datetime type"
                    )
            
            if 'Sales' in df.columns:
                if not pd.api.types.is_numeric_dtype(df['Sales']):
                    validation_results['is_valid'] = False
                    validation_results['errors'].append(
                        "Sales column is not numeric"
                    )
                else:
                    negative_count = (df['Sales'] < 0).sum()
                    if negative_count > 0:
                        validation_results['warnings'].append(
                            f"Sales column has {negative_count} negative values"
                        )
            
            logger.info(f"Data validation completed. Valid: {validation_results['is_valid']}")
            
        except Exception as e:
            validation_results['is_valid'] = False
            validation_results['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"Data validation failed: {str(e)}")
        
        return validation_results
    
    @classmethod
    def clean_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Basic data cleaning operations
        """
        try:
            df_clean = df.copy()
            
            # Ensure Order Date is datetime
            if 'Order Date' in df_clean.columns:
                if not pd.api.types.is_datetime64_any_dtype(df_clean['Order Date']):
                    df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'], format='%d/%m/%Y')
            
            # Remove rows with null Sales
            if 'Sales' in df_clean.columns:
                initial_count = len(df_clean)
                df_clean = df_clean.dropna(subset=['Sales'])
                removed_count = initial_count - len(df_clean)
                if removed_count > 0:
                    logger.warning(f"Removed {removed_count} rows with null Sales")
            
            # Strip whitespace from string columns
            string_columns = df_clean.select_dtypes(include=['object']).columns
            for col in string_columns:
                df_clean[col] = df_clean[col].astype(str).str.strip()
            
            logger.info(f"Data cleaning completed. Rows: {len(df_clean)}")
            return df_clean
            
        except Exception as e:
            logger.error(f"Data cleaning failed: {str(e)}")
            return df