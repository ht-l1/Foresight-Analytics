import streamlit as st
from app.visualizations.trends import TrendsVisualizer
from app.visualizations.composition import CompositionVisualizer
from app.visualizations.forecast import ForecastVisualizer
from app.models.forecaster import Forecaster

class TabManager:
    def __init__(self):
        self.trends_viz = TrendsVisualizer()
        self.comp_viz = CompositionVisualizer()
        self.forecast_viz = ForecastVisualizer()
        self.forecaster = Forecaster()
    
    def render_overview(self):
        st.header("Welcome to Foresight Analytics")
        st.markdown("""
        This website helps analyze financial trends and generate forecasts across different departments and categories.
        
        ### How to Use This website:
        1. **Select Department** (sidebar)
           - Choose the department you want to analyze
           - Each department has its own set of categories

        2. **Select Account Type** (sidebar)
           - Choose the account type you want to analyze (Assets, Liabilities, Expenses, Revenue)
           - This will be used for the category composition analysis
                   
        3. **Select Category** (sidebar)
           - Pick a specific category within the chosen department
           - This will be used for detailed forecasting
        
        4. **Set Forecast Period** (sidebar)
           - Use the slider to select how many months to forecast
           - Range: 1-12 months  

        ### Forecasting Metrics
        The accuracy of the forecasting model is measured using the Mean Absolute Percentage Error (MAPE). MAPE calculates the average absolute percentage error between the predicted values and the actual values. The accuracy is then calculated as \( \text{Accuracy} = 100 - (\text{MAPE}) \). A lower MAPE value indicates a more accurate model.
        """)

        st.markdown("""
        <div style="position: fixed; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: gray;">
            Developed by <strong>Hannah Lin</strong> | 2025
        </div>
        """, unsafe_allow_html=True)
    
    def render_trends(self, data, department):
        fig = self.trends_viz.plot_monthly_trends(data)
        st.pyplot(fig)
    
    def render_composition(self, data, account_type, department):
        fig = self.comp_viz.plot_category_composition(data, account_type)
        st.pyplot(fig)
    
    def render_forecast(self, data, account_type, department, months):
        account_types = {
            'Assets': ['Assets'],
            'Liabilities': ['Loans'],
            'Expenses': ['Salaries', 'Supplies', 'Utilities', 'Rent', 'Royalties'],
            'Revenue': ['Product Sales', 'Service Revenue']
        }
        selected_categories = account_types[account_type]
        filtered_data = data[data['Category'].isin(selected_categories)]
        
        historical_data = self.forecaster.aggregate_historical_data(filtered_data)
        
        forecast_data, accuracy = self.forecaster.forecast(filtered_data, months)
        
        st.sidebar.header("Model Accuracy")
        st.sidebar.write(f"Accuracy: {accuracy:.2f}%")
        
        fig = self.forecast_viz.plot_forecast(historical_data, forecast_data, account_type)
        st.pyplot(fig)
        
        st.subheader("Forecasted Monthly Dollar Amounts")
        st.dataframe(forecast_data)

def render_forecast(historical_data, forecast_data):
    visualizer = ForecastVisualizer()
    fig = visualizer.plot_forecast(historical_data, forecast_data)
    st.pyplot(fig)