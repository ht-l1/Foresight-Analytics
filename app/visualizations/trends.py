from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from app.visualizations.base import BaseVisualizer

class TrendsVisualizer(BaseVisualizer):
    def plot_monthly_trends(self, data, category=None):
        fig = self.create_figure()
        
        monthly_data = data.groupby([
            pd.Grouper(key='Transaction Date', freq='ME'),
            'Category'
        ])['Transaction Amount'].sum().reset_index()
        
        sns.lineplot(
            data=monthly_data,
            x='Transaction Date',
            y='Transaction Amount',
            hue='Category' if not category else None
        )
        
        plt.xticks(rotation=45)
        plt.title('Monthly Transaction Trends')
        
        return fig