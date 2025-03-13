import streamlit as st

class Sidebar:
    @staticmethod
    def render(df):
        st.sidebar.header("Filters")
        
        department = st.sidebar.selectbox("Select Department", df['Department'].unique())
        
        account_types = ['Expenses', 'Revenue', 'Assets', 'Liabilities']
        account_type = st.sidebar.selectbox("Select Account Type", account_types)

        category = st.sidebar.selectbox("Select Category", df['Category'].unique())
                
        months = st.sidebar.slider("Months to Forecast", 1, 12, 3)
        
        return department, category, account_type, months