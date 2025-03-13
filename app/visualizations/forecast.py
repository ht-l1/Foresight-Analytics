from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from .base import BaseVisualizer

class ForecastVisualizer(BaseVisualizer):
    def plot_forecast(self, historical_data, forecast_data, account_type):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.lineplot(
            data=historical_data,
            x='Transaction Date',
            y='Transaction Amount',
            label='Historical',
            ax=ax
        )
        
        sns.lineplot(
            data=forecast_data,
            x='Transaction Date',
            y='Transaction Amount',
            label='Forecast',
            linestyle='--',
            ax=ax
        )
        
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        
        plt.xticks(rotation=45)
        plt.title(f'Financial Forecast for {account_type}')
        plt.xlabel('Transaction Date')
        plt.ylabel('Transaction Amount (in millions)')
        
        return fig