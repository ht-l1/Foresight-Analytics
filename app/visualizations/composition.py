from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from .base import BaseVisualizer

class CompositionVisualizer(BaseVisualizer):
    def plot_category_composition(self, data, account_type):
        fig, ax = plt.subplots(figsize=(12, 8))
        
        account_types = {
            'Assets': ['Assets'],
            'Liabilities': ['Loans'],
            'Expenses': ['Salaries', 'Supplies', 'Utilities', 'Rent', 'Royalties'],
            'Revenue': ['Product Sales', 'Service Revenue']
        }
        
        selected_categories = account_types[account_type]
        filtered_data = data[data['Category'].isin(selected_categories)]
        
        quarterly_data = filtered_data.groupby([
            pd.Grouper(key='Transaction Date', freq='Q-DEC'),
            'Category'
        ])['Transaction Amount'].sum().reset_index()
        
        pivot_data = quarterly_data.pivot(index='Transaction Date', columns='Category', values='Transaction Amount').fillna(0)
        
        pivot_data.plot(kind='bar', stacked=True, ax=ax)
        
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        
        plt.xticks(rotation=45)
        plt.title(f'Quarterly {account_type} Composition')
        plt.ylabel('Transaction Amount (in millions)')
        plt.xlabel('Transaction Date')
        plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        return fig