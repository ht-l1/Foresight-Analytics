import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from app.config.settings import AppConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Forecaster:
    def __init__(self):
        self.model = LinearRegression()
        self.is_fitted = False
        self.model_metrics = {}
    
    def prepare_data(self, data: pd.DataFrame) -> tuple:
        """Prepare data for forecasting with validation"""
        try:
            if data.empty: #is the df empty
                raise ValueError("Input data is empty")
                
            # below two checks if the column exist 
            if 'Transaction Date' not in data.columns:
                raise ValueError("Transaction Date column not found")
                
            if 'Transaction Amount' not in data.columns:
                raise ValueError("Transaction Amount column not found")

            # Group by month and sum amounts
            monthly_totals = data.groupby(
                pd.Grouper(key='Transaction Date', freq='ME')
            )['Transaction Amount'].sum().reset_index()
            
            # Create feature matrix (time indices)
            X = np.arange(len(monthly_totals)).reshape(-1, 1)
            y = monthly_totals['Transaction Amount'].values
            
            logger.info(f"Data prepared successfully. {len(monthly_totals)} months of data")
            return X, y, monthly_totals
    
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def forecast(self, data: pd.DataFrame, months: int) -> tuple:
        """Generate forecast with error handling"""
        try:
            # Validate inputs
            if months < AppConfig.MIN_FORECAST_MONTHS or months > AppConfig.MAX_FORECAST_MONTHS:
                raise ValueError(f"Forecast months must be between {AppConfig.MIN_FORECAST_MONTHS} and {AppConfig.MAX_FORECAST_MONTHS}")
            
            # Prepare data
            X, y, monthly_totals = self.prepare_data(data)
        
            # Fit model
            self.model.fit(X, y)
            self.is_fitted = True
            
            # Calculate model performance
            y_pred = self.model.predict(X)
            mape = mean_absolute_percentage_error(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            accuracy = max(0, 100 - (mape * 100))  # Ensure non-negative accuracy
            
            # Store model metrics
            self.model_metrics = {
                'mape': mape,
                'mse': mse,
                'accuracy': accuracy,
                'data_points': len(monthly_totals)
            }

            # Check model quality
            if accuracy < AppConfig.MODEL_ACCURACY_THRESHOLD:
                logger.warning(f"Model accuracy ({accuracy:.2f}%) below threshold ({AppConfig.MODEL_ACCURACY_THRESHOLD}%)")
  
             # Generate future dates
            last_date = monthly_totals['Transaction Date'].max()
            future_dates = pd.date_range(
                start=last_date + pd.DateOffset(months=1),
                periods=months,
                freq='ME'
            )
            
            # Create future feature matrix
            future_X = np.arange(
                len(monthly_totals),
                len(monthly_totals) + months
            ).reshape(-1, 1)
            
            # Generate predictions
            predictions = self.model.predict(future_X)
            
            # Ensure predictions are reasonable (no negative values for positive historical data)
            if all(y > 0):  # If all historical data is positive
                predictions = np.maximum(predictions, 0)

            forecast_data = pd.DataFrame({
                'Transaction Date': future_dates,
                'Transaction Amount': predictions
            })

            logger.info(f"Forecast generated successfully. {months} months, accuracy: {accuracy:.2f}%")
            return forecast_data, accuracy
            
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            raise
        
    def aggregate_historical_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Aggregate historical data with error handling"""
        try:
            if data.empty:
                logger.warning("Empty data provided for aggregation")
                return pd.DataFrame(columns=['Transaction Date', 'Transaction Amount'])
            
            monthly_totals = data.groupby(
                pd.Grouper(key='Transaction Date', freq='ME')
            )['Transaction Amount'].sum().reset_index()
            
            logger.info(f"Historical data aggregated: {len(monthly_totals)} months")
            return monthly_totals
            
        except Exception as e:
            logger.error(f"Error aggregating historical data: {str(e)}")
            raise

    def get_model_info(self) -> dict:
        """Get model information and metrics"""
        return {
            'is_fitted': self.is_fitted,
            'model_type': 'Linear Regression',
            'metrics': self.model_metrics
        }