import streamlit as st
from app.config.settings import AppConfig
from app.data.data_loader import DataLoader
from app.ui.sidebar import Sidebar
from app.ui.tabs import TabManager

def main():
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        layout=AppConfig.PAGE_LAYOUT
    )
    
    data_loader = DataLoader()
    df = data_loader.load_data('data/managerial_accounting.csv')
    
    department, category, account_type, months = Sidebar.render(df)
    
    dept_data = data_loader.filter_by_department(df, department)
    
    tab_manager = TabManager()
    tabs = st.tabs(["Overview", "Monthly Trends", "Category Composition", "Forecast", "Raw Data"])
    
    with tabs[0]:
        tab_manager.render_overview()
    with tabs[1]:
        st.markdown("""
        Visualize transaction patterns over time to identify trends and insights. Not driven by filters.
        """)
        tab_manager.render_trends(dept_data, department)
    with tabs[2]:
        st.markdown(f"""
        Gain a clear understanding of how transactions are distributed across different categories.  
        From sidebar, use filter "Department" and "Account Type".  
                    
        Below shows the breakdown for the selected account type: **`{account_type}`** and department: **`{department}`**.
        """)
        tab_manager.render_composition(dept_data, account_type, department)
    with tabs[3]:
        st.markdown(f"""
        Predict future financial performance based on historical data.  
        From sidebar, use filter "Department", "Account Type" and "Months to Forecast".  
          
        Below shows the **`{months}`** months **`{account_type}`** forecasting for **`{department}`**.
        """)
        tab_manager.render_forecast(dept_data, account_type, department, months)
    with tabs[4]:
        st.markdown("""
        Below is a small sample of the dataset. To see the full dataset used, please visit [Kaggle](https://www.kaggle.com/datasets/jazidesigns/managerial-accounting/data).
        """)
        st.dataframe(df.head(20))

if __name__ == "__main__":
    main()