import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

class Forecaster:
    def __init__(self):
        self.model = LinearRegression()
    
    def prepare_data(self, data: pd.DataFrame) -> tuple:
        monthly_totals = data.groupby(
            pd.Grouper(key='Transaction Date', freq='ME')
        )['Transaction Amount'].sum().reset_index()
        
        X = np.arange(len(monthly_totals)).reshape(-1, 1)
        y = monthly_totals['Transaction Amount'].values
        
        return X, y, monthly_totals
    
    def forecast(self, data: pd.DataFrame, months: int) -> tuple:
        X, y, monthly_totals = self.prepare_data(data)
        
        self.model.fit(X, y)
        
        y_pred = self.model.predict(X)
        mape = mean_absolute_percentage_error(y, y_pred)
        accuracy = 100 - (mape * 100)
        
        last_date = monthly_totals['Transaction Date'].max()
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=months,
            freq='ME'
        )
        
        future_X = np.arange(
            len(monthly_totals),
            len(monthly_totals) + months
        ).reshape(-1, 1)
        
        predictions = self.model.predict(future_X)
        
        forecast_data = pd.DataFrame({
            'Transaction Date': future_dates,
            'Transaction Amount': predictions
        })
        
        return forecast_data, accuracy
    
    def aggregate_historical_data(self, data: pd.DataFrame) -> pd.DataFrame:
        monthly_totals = data.groupby(
            pd.Grouper(key='Transaction Date', freq='ME')
        )['Transaction Amount'].sum().reset_index()
        
        return monthly_totals