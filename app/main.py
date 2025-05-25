import streamlit as st
from app.config.settings import AppConfig
from app.data.data_loader import DataLoader
from app.ui.sidebar import Sidebar
from app.ui.tabs import TabManager
from app.utils.logger import get_logger

logger = get_logger(__name__)

@st.cache_resource
def get_data_loader():
    """Cached data loader instance"""
    return DataLoader()

def initialize_app():
    """Initialize the application"""
    try:
        data_loader = get_data_loader()
        
        # Quick check if database has data
        if not data_loader.check_data_exists():
            # Initialize database with CSV data only if empty
            csv_path = 'data/managerial_accounting.csv'
            if not data_loader.initialize_database(csv_path):
                st.error("Failed to initialize database. Please check the data file.")
                return None
        
        return data_loader
        
    except Exception as e:
        logger.error(f"App initialization failed: {str(e)}")
        st.error(f"Application initialization failed: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        layout=AppConfig.PAGE_LAYOUT,
        initial_sidebar_state="expanded",
    )

    # st.title("Foresight Analytics")
    # st.markdown("*Advanced Financial Forecasting & Analytics Platform*")
    
    # Initialize application
    data_loader = initialize_app()
    if not data_loader:
        st.stop()

    # Get basic info for sidebar (NOT full dataset)
    departments = data_loader.get_departments()
    categories = data_loader.get_categories()

    if not departments:
        st.error("No data available. Please check your database.")
        st.stop()

    # Render sidebar
    data_info = data_loader.get_data_info()
    department, category, account_type, months = Sidebar.render(departments, categories, data_info)
    
    if not department:
        st.warning("Please select filters from the sidebar to view data.")
        st.stop()

    # Get filtered data
    dept_data = data_loader.filter_by_department(department)

    if dept_data.empty:
        st.error(f"No data found for department: {department}")
        st.stop()
    
    # Initialize tab manager
    tab_manager = TabManager()

    # Create tabs
    tabs = st.tabs([
        "Overview", 
        "Monthly Trends", 
        "Category Composition", 
        "Forecast", 
        "Raw Data"
    ])
   
    with tabs[0]:
        tab_manager.render_overview()

        # Add data summary
        st.subheader("Data Summary")
        data_info = data_loader.get_data_info()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{data_info.get('total_records', 0):,}")
        with col2:
            st.metric("Departments", data_info.get('departments', 0))
        with col3:
            st.metric("Categories", data_info.get('categories', 0))
        with col4:
            st.metric("Selected Dept Records", f"{len(dept_data):,}")

    with tabs[1]:
        st.subheader("Monthly Transaction Trends")
        st.markdown(f"""
        Visualize transaction patterns over time for **{department}** department.
        This helps identify seasonal patterns and long-term trends.
        """)
        tab_manager.render_trends(dept_data, department)

    with tabs[2]:
        st.subheader("Category Composition Analysis")
        st.markdown(f"""
        Understand how transactions are distributed across different categories.  
        **Department:** {department} | **Account Type:** {account_type}
        """)
        tab_manager.render_composition(dept_data, account_type, department)

    with tabs[3]:
        st.subheader("Financial Forecasting")
        st.markdown(f"""
        AI-powered forecast for the next **{months} months** of **{account_type}** 
        transactions in **{department}** department.

        Driven by filter "Department", "Account Type" and "Months to Forecast".  
        """)
        tab_manager.render_forecast(dept_data, account_type, department, months)
    with tabs[4]:      
        st.subheader("Raw Data View")
        st.markdown(f"""
        Sample data from **{department}** department. 
        Full dataset available on [Kaggle](https://www.kaggle.com/datasets/jazidesigns/managerial-accounting/data).
        """)
        
        # Add data filters
        col1, col2 = st.columns(2)
        with col1:
            show_records = st.slider("Records to display", 10, 100, 20)
        with col2:
            sort_by = st.selectbox("Sort by", ["Transaction Date", "Transaction Amount"])
        
        display_data = dept_data.sort_values(sort_by, ascending=False).head(show_records)
        st.dataframe(display_data, use_container_width=True)
        
        # Download button
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{department}_transactions.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()