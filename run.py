import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import backend
from app.data.data_loader import DataLoader
from app.models.forecaster import Forecaster
from app.utils.logger import get_logger

logger = get_logger(__name__)

# theme config
st.set_page_config(
    page_title="Foresight Analytics - ML Forecasting",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 0.5rem;
        border-radius: 8px;
        border-left: 3px solid #00d4ff;
        margin: 0.2rem 0;
        font-size: 0.9rem;
    }
    
    .forecast-header {
        color: #00d4ff;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .model-accuracy {
        background: linear-gradient(90deg, #2d2d2d, #1e1e1e);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_data_loader():
    return DataLoader()

@st.cache_data(ttl=1800)
def load_and_prepare_data():
    """Load data from database or CSV fallback"""
    try:
        data_loader = get_data_loader()
        
        # Try database first
        if data_loader.check_data_exists():
            df = data_loader.get_all_data()
            regions = data_loader.get_regions()
            categories = data_loader.get_categories()
        else:
            # Fallback to CSV
            st.warning("Loading from CSV file...")
            df = pd.read_csv('data/train.csv')
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
            
            # Map column names to match the database structure
            df = df.rename(columns={
                'Row ID': 'row_id',
                'Order Date': 'order_date',
                'Sales': 'sales',
                'Region': 'region',
                'Category': 'category',
                'Sub-Category': 'sub_category',
                'Segment': 'segment',
                'Product Name': 'product_name',
                'City': 'city',
                'State': 'state',
                'Ship Mode': 'ship_mode',
                'Postal Code': 'postal_code'
            })
            
            regions = df['region'].unique().tolist()
            categories = df['category'].unique().tolist()
        
        return df, regions, categories
    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame(), [], []

def create_metrics_cards(df, filtered_df):
    """Create metric cards showing key statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = filtered_df['sales'].sum()
    total_orders = len(filtered_df)
    avg_order = filtered_df['sales'].mean()
    growth_rate = calculate_growth_rate(filtered_df)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h6 style="color: #00d4ff; margin: 0;">Total Sales</h6>
            <h5 style="color: white; margin: 0;">${total_sales:,.0f}</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h6 style="color: #00d4ff; margin: 0;">Total Orders</h6>
            <h5 style="color: white; margin: 0;">{total_orders:,}</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h6 style="color: #00d4ff; margin: 0;">Avg Order Value</h6>
            <h5 style="color: white; margin: 0;">${avg_order:.0f}</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h6 style="color: #00d4ff; margin: 0;">Growth Rate</h6>
            <h5 style="color: white; margin: 0;">{growth_rate:+.1f}%</h5>
        </div>
        """, unsafe_allow_html=True)

def calculate_growth_rate(df):
    """Calculate month-over-month growth rate"""
    try:
        monthly_sales = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
        if len(monthly_sales) >= 2:
            recent_growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
            return recent_growth
        return 0
    except:
        return 0

def create_forecast_visualizations(df, months_to_forecast):
    """Create comprehensive forecast visualizations"""
    forecaster = Forecaster()
    
    # Generate forecasts
    forecast_results = forecaster.forecast(df, months_to_forecast)
    historical_monthly = forecaster.aggregate_historical_data(df)
    
    # Create main forecast plot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Sales Forecast Comparison', 'Model Accuracy Comparison', 
                       'Sales by Category', 'Monthly Sales Trend'),
        specs=[[{"colspan": 2}, None],
               [{"type": "bar"}, {"type": "pie"}]],
        vertical_spacing=0.12
    )
    
    # Main forecast plot
    colors = ['#00d4ff', '#ff6b6b', '#4ecdc4', '#45b7d1']
    
    # Historical data
    fig.add_trace(
        go.Scatter(
            x=historical_monthly['order_date'] if 'order_date' in historical_monthly.columns else historical_monthly['Order Date'],
            y=historical_monthly['sales'] if 'sales' in historical_monthly.columns else historical_monthly['Sales'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#ffffff', width=3),
            marker=dict(size=6)
        ),
        row=1, col=1
    )
    
    # Forecast lines
    for i, (model_name, result) in enumerate(forecast_results.items()):
        if not result['forecast'].empty:
            forecast_df = result['forecast']
            fig.add_trace(
                go.Scatter(
                    x=forecast_df['order_date'] if 'order_date' in forecast_df.columns else forecast_df['Order Date'],
                    y=forecast_df['sales'] if 'sales' in forecast_df.columns else forecast_df['Sales'],
                    mode='lines+markers',
                    name=f'{model_name}',
                    line=dict(color=colors[i % len(colors)], width=2, dash='dash'),
                    marker=dict(size=5)
                ),
                row=1, col=1
            )
    
    # Model accuracy comparison
    model_names = []
    accuracies = []
    for model_name, result in forecast_results.items():
        if result.get('metrics'):
            model_names.append(model_name)
            accuracies.append(result['metrics'].get('accuracy', 0))
    
    fig.add_trace(
        go.Bar(
            x=model_names,
            y=accuracies,
            marker_color=['#00d4ff', '#ff6b6b', '#4ecdc4'],
            name='Accuracy %'
        ),
        row=2, col=1
    )
    
    # Sales by category pie chart
    category_sales = df.groupby('category')['sales'].sum()
    fig.add_trace(
        go.Pie(
            labels=category_sales.index,
            values=category_sales.values,
            marker_colors=['#00d4ff', '#ff6b6b', '#4ecdc4'],
            name="Category Sales"
        ),
        row=2, col=2
    )
    
    # Update layout for dark theme
    fig.update_layout(
        height=800,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='white',
            borderwidth=1
        )
    )
    
    # Update all axes for dark theme
    fig.update_xaxes(gridcolor='#444', color='white')
    fig.update_yaxes(gridcolor='#444', color='white')
    
    return fig, forecast_results

def display_model_performance(forecast_results):
    """Display detailed model performance metrics"""
    st.markdown("<h3 style='color: #00d4ff;'>Model Performance Details</h3>", unsafe_allow_html=True)
    
    for model_name, result in forecast_results.items():
        metrics = result.get('metrics', {})
        if metrics:
            accuracy = metrics.get('accuracy', 0)
            mape = metrics.get('mape', 0)
            
            # Color coding based on accuracy
            if accuracy >= 80:
                color = "#4ecdc4"  # Green
            elif accuracy >= 60:
                color = "#ff6b6b"  # Orange
            else:
                color = "#ff4444"  # Red
            
            st.markdown(f"""
            <div class="model-accuracy" style="border-left: 4px solid {color};">
                <strong style="color: white; font-size: 1.1em;">{model_name}</strong><br>
                <span style="color: #00d4ff;">Accuracy:</span> <strong style="color: white;">{accuracy:.1f}%</strong> | 
                <span style="color: #00d4ff;">MAPE:</span> <strong style="color: white;">{mape:.3f}</strong>
            </div>
            """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="forecast-header">Foresight Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-size: 0.9em;">Machine Learning Forecasting & Analytics Platform</p>', unsafe_allow_html=True)
    
    # Load data
    df, regions, categories = load_and_prepare_data()
    
    if df.empty:
        st.error("No data available. Please check the data source.")
        return
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("## Filters & Controls")
        
        # Region filter
        selected_region = st.selectbox(
            "Select Region",
            ["All"] + regions,
            help="Filter data by geographic region"
        )
        
        # Category filter
        selected_category = st.selectbox(
            "Select Category", 
            ["All"] + categories,
            help="Filter data by product category"
        )
        
        # Forecast months
        forecast_months = st.slider(
            "Forecast Months",
            min_value=1,
            max_value=24,
            value=12,
            help="Number of months to forecast ahead"
        )
        
        # st.markdown("---")
        
        # Data info
        st.markdown("### Data Overview")
        st.info(f"""
        **Total Records:** {len(df):,}
        
        **Range:** {df['order_date'].min().strftime('%Y-%m-%d')} to {df['order_date'].max().strftime('%Y-%m-%d')}
        
        """)
        
        # Refresh button
        if st.button("Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Apply filters
    filtered_df = df.copy()
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust the selection.")
        return
    
    # Main content
    # Metrics cards
    create_metrics_cards(df, filtered_df)
    
    # st.markdown("---")
    
    # Main forecast visualization
    with st.spinner("Generating forecasts..."):
        try:
            fig, forecast_results = create_forecast_visualizations(filtered_df, forecast_months)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating forecasts: {str(e)}")
            return

    # Two columns for additional insights
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Model performance details
        display_model_performance(forecast_results)
        
        # Recent trends table
        st.markdown("<h3 style='color: #00d4ff;'>Recent Sales Trends</h3>", unsafe_allow_html=True)
        recent_data = filtered_df.groupby(filtered_df['order_date'].dt.to_period('M'))['sales'].agg(['sum', 'count', 'mean']).tail(6)
        recent_data.columns = ['Total Sales', 'Orders', 'Avg Order Value']
        recent_data.index = recent_data.index.astype(str)
        st.dataframe(recent_data.style.format({
            'Total Sales': '${:,.0f}',
            'Orders': '{:,}',
            'Avg Order Value': '${:.0f}'
        }), use_container_width=True)
    
    with col2:
        # Top performing segments
        st.markdown("<h3 style='color: #00d4ff;'>Top Segments</h3>", unsafe_allow_html=True)
        segment_performance = filtered_df.groupby('segment')['sales'].sum().sort_values(ascending=False)
        
        for segment, sales in segment_performance.items():
            percentage = (sales / segment_performance.sum()) * 100
            st.markdown(f"""
            <div style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 4px;">
                <strong style="color: white;">{segment}</strong><br>
                <span style="color: #00d4ff;">${sales:,.0f}</span> ({percentage:.1f}%)
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; padding: 1rem;">'
        'Developed by <strong>Hannah Lin</strong> | 2025'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()