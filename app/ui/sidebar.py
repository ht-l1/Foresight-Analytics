import streamlit as st
from app.config.settings import AppConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Sidebar:
    @staticmethod
    def render(df):
        """Render sidebar with error handling"""
        try:
            st.sidebar.header("Filters")
            
            # Department selection with error handling
            departments = df['Department'].unique() if 'Department' in df.columns else []
            if len(departments) == 0:
                st.sidebar.error("No departments found in data")
                return None, None, None, None
            
            department = st.sidebar.selectbox("Select Department", departments)
            
            # Account type selection
            account_types = ['Expenses', 'Revenue', 'Assets', 'Liabilities']
            account_type = st.sidebar.selectbox("Select Account Type", account_types)

            # Category selection with error handling
            categories = df['Category'].unique() if 'Category' in df.columns else []
            if len(categories) == 0:
                st.sidebar.error("No categories found in data")
                return department, None, account_type, None
            
            category = st.sidebar.selectbox("Select Category", categories)
            
            # Months slider with validation
            # months = st.sidebar.slider("Months to Forecast", 1, 12, 3)
            months = st.sidebar.slider(
                "Months to Forecast", 
                AppConfig.MIN_FORECAST_MONTHS, 
                AppConfig.MAX_FORECAST_MONTHS, 
                AppConfig.DEFAULT_FORECAST_MONTHS
            )

            # Add data quality info in sidebar
            st.sidebar.markdown("---")
            st.sidebar.subheader("Data Info")
            st.sidebar.write(f"Total Records: {len(df):,}")
            st.sidebar.write(f"Date Range: {df['Transaction Date'].min().strftime('%Y-%m-%d')} to {df['Transaction Date'].max().strftime('%Y-%m-%d')}")
            
            logger.info(f"Sidebar rendered successfully. Department: {department}, Category: {category}")
            return department, category, account_type, months
            
        except Exception as e:
            logger.error(f"Error rendering sidebar: {str(e)}")
            st.sidebar.error("Error loading filters. Please check your data.")
            return None, None, None, None