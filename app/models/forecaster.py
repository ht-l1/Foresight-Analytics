import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
from prophet import Prophet
from app.config.settings import AppConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Forecaster:
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Prophet': Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        }
        self.is_fitted = {name: False for name in self.models}
        self.model_metrics = {name: {} for name in self.models}
    
    def prepare_data(self, data: pd.DataFrame) -> tuple:
        """Prepare Superstore data for forecasting - handles both column name formats"""
        try:
            if data.empty:
                raise ValueError("Input data is empty")
            
            # Use known column names from train.csv and database
            date_col = 'order_date'
            sales_col = 'sales'
            
            if date_col not in data.columns or sales_col not in data.columns:
                raise ValueError(f"Required columns not found. Expected 'Order Date' and 'Sales', got {data.columns.tolist()}")
            
            logger.info(f"Using columns: {date_col} and {sales_col}")
            
            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
                data[date_col] = pd.to_datetime(data[date_col])
            
            # Group by month and sum sales
            monthly_totals = data.groupby(
                pd.Grouper(key=date_col, freq='ME')
            )[sales_col].sum().reset_index()
            
            # Standardize column names for output
            monthly_totals.columns = ['order_date', 'sales']
            
            # Remove any zero or null sales months
            monthly_totals = monthly_totals[monthly_totals['sales'] > 0].reset_index(drop=True)
            
            if monthly_totals.empty:
                raise ValueError("No valid sales data found after aggregation")
            
            # For sklearn models
            X = np.arange(len(monthly_totals)).reshape(-1, 1)
            y = monthly_totals['sales'].values
            
            # For Prophet - needs 'ds' and 'y' columns
            prophet_df = monthly_totals.rename(columns={'order_date': 'ds', 'sales': 'y'})
            
            logger.info(f"Data prepared: {len(monthly_totals)} months, sales range: ${y.min():,.0f} - ${y.max():,.0f}")
            return X, y, monthly_totals, prophet_df
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def forecast(self, data: pd.DataFrame, months: int) -> dict:
        """Generate forecasts for multiple models"""
        try:
            if months < 1 or months > 24:
                raise ValueError("Forecast months must be between 1 and 24")
            
            # Prepare data
            X, y, monthly_totals, prophet_df = self.prepare_data(data)
            
            results = {}
            for name, model in self.models.items():
                try:
                    if name == 'Prophet':
                        # Suppress Prophet warnings
                        import warnings
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            
                            # Fit Prophet
                            model.fit(prophet_df)
                            future = model.make_future_dataframe(periods=months, freq='ME')
                            forecast = model.predict(future)
                            
                            # Get predictions for validation
                            y_pred = forecast['yhat'][:len(y)]
                            
                            # Get future predictions
                            predictions = forecast['yhat'][-months:]
                            future_dates = forecast['ds'][-months:]
                    else:
                        # Fit sklearn models
                        model.fit(X, y)
                        y_pred = model.predict(X)
                        
                        # Generate future predictions
                        future_X = np.arange(len(monthly_totals), len(monthly_totals) + months).reshape(-1, 1)
                        predictions = model.predict(future_X)
                        
                        # Generate future dates
                        future_dates = pd.date_range(
                            start=monthly_totals['order_date'].max() + pd.DateOffset(months=1),
                            periods=months, freq='ME'
                        )
                    
                    # Calculate metrics
                    mape = mean_absolute_percentage_error(y, y_pred)
                    mse = mean_squared_error(y, y_pred)
                    accuracy = max(0, 100 - (mape * 100))
                    
                    # Store metrics
                    self.model_metrics[name] = {
                        'mape': mape,
                        'mse': mse,
                        'accuracy': accuracy,
                        'data_points': len(monthly_totals)
                    }
                    self.is_fitted[name] = True
                    
                    # Ensure non-negative predictions
                    predictions = np.maximum(predictions, 0)
                    
                    # Create forecast DataFrame with standardized column names
                    forecast_data = pd.DataFrame({
                        'order_date': future_dates,
                        'sales': predictions
                    })
                    
                    results[name] = {
                        'forecast': forecast_data,
                        'metrics': self.model_metrics[name]
                    }
                    
                    logger.info(f"{name} forecast generated. Accuracy: {accuracy:.2f}%, MAPE: {mape:.3f}")
                
                except Exception as e:
                    logger.error(f"Error in {name} forecast: {str(e)}")
                    results[name] = {'forecast': pd.DataFrame(), 'metrics': {}}
            
            return results
        
        except Exception as e:
            logger.error(f"Error generating forecasts: {str(e)}")
            raise
    
    def aggregate_historical_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Aggregate historical data - handles both column name formats"""
        try:
            if data.empty:
                logger.warning("Empty data provided for aggregation")
                return pd.DataFrame(columns=['order_date', 'sales'])
            
            # Handle different column name formats
            date_col = 'order_date'
            sales_col = 'sales'
            
            if date_col not in data.columns or sales_col not in data.columns:
                logger.error(f"Required columns not found. Expected 'Order Date' and 'Sales', got {data.columns.tolist()}")
                return pd.DataFrame(columns=['order_date', 'sales'])
            
            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
                data[date_col] = pd.to_datetime(data[date_col])
            
            # Group by month and sum sales
            monthly_totals = data.groupby(
                pd.Grouper(key=date_col, freq='ME')
            )[sales_col].sum().reset_index()
            
            # Standardize column names
            monthly_totals.columns = ['order_date', 'sales']
            
            logger.info(f"Historical data aggregated: {len(monthly_totals)} months")
            return monthly_totals
            
        except Exception as e:
            logger.error(f"Error aggregating historical data: {str(e)}")
            return pd.DataFrame(columns=['order_date', 'sales'])
    
    def get_model_info(self) -> dict:
        """Get model information and metrics"""
        return {
            'is_fitted': self.is_fitted,
            'model_types': list(self.models.keys()),
            'metrics': self.model_metrics
        }