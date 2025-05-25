import streamlit as st
from app.config.settings import AppConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Sidebar:
    @staticmethod
    def render(departments: list, categories: list, data_info: dict):
        """Render sidebar with optimized data loading"""
        try:
            st.sidebar.header("Filters")

            # Department selection
            if not departments:
                st.sidebar.error("No departments found in data")
                return None, None, None, None
            
            department = st.sidebar.selectbox("Select Department", departments)
            
            # Account type selection
            account_types = ['Expenses', 'Revenue', 'Assets', 'Liabilities']
            account_type = st.sidebar.selectbox("Select Account Type", account_types)

            # Category selection
            if not categories:
                st.sidebar.error("No categories found in data")
                return department, None, account_type, None
            
            category = st.sidebar.selectbox("Select Category", categories)
            
            # Months slider with validation
            months = st.sidebar.slider(
                "Months to Forecast", 
                AppConfig.MIN_FORECAST_MONTHS, 
                AppConfig.MAX_FORECAST_MONTHS, 
                AppConfig.DEFAULT_FORECAST_MONTHS
            )

            # Add data quality info in sidebar
            st.sidebar.markdown("---")
            st.sidebar.subheader("Data Info")
            st.sidebar.write(f"Total Records: {data_info.get('total_records', 0):,}")
            st.sidebar.write(f"Date Range: {data_info.get('date_range', 'Unknown')}")
            st.sidebar.write(f"Departments: {data_info.get('departments', 0)}")
            st.sidebar.write(f"Categories: {data_info.get('categories', 0)}")
            
            logger.info(f"Sidebar rendered successfully. Department: {department}, Category: {category}")
            return department, category, account_type, months
            
        except Exception as e:
            logger.error(f"Error rendering sidebar: {str(e)}")
            st.sidebar.error("Error loading filters. Please check your data.")
            return None, None, None, None