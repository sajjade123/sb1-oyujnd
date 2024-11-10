"""Main Streamlit dashboard application"""
import streamlit as st
import logging
from datetime import datetime, timedelta
from config import SHEET_CONFIG, CSS_STYLES, THEME_COLORS
from data_processor import DataProcessor
from analytics import (
    analyze_trends,
    create_trend_plot,
    create_distribution_plot,
    generate_summary_stats
)
from cache_manager import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_summary_cards(summary_stats: dict, value_column: str):
    """Create summary metric cards with error handling"""
    try:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label=f"Total {value_column}",
                value=f"${summary_stats['total']:,.2f}"
            )
        
        with col2:
            st.metric(
                label=f"Average {value_column}",
                value=f"${summary_stats['average']:,.2f}"
            )
        
        with col3:
            st.metric(
                label=f"Median {value_column}",
                value=f"${summary_stats['median']:,.2f}"
            )
    except Exception as e:
        logger.error(f"Error creating summary cards: {e}")
        st.error("Unable to display summary cards")

def initialize_session_state():
    """Initialize session state variables"""
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor("Copy of Autodesk Order Tracker(1).xlsx")
    if 'cache_manager' not in st.session_state:
        st.session_state.cache_manager = CacheManager()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Order Tracking Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    # Header with refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Order Tracking Dashboard")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.session_state.cache_manager.clear_cache()
            success, error_message = st.session_state.data_processor.load_data()
            if not success:
                st.error(f"Error refreshing data: {error_message}")
            else:
                st.session_state.last_update = datetime.now()
                st.success("Data refreshed successfully!")
    
    st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Load data if not already loaded
        if not st.session_state.data_processor.sheets_data:
            success, error_message = st.session_state.data_processor.load_data()
            if not success:
                st.error(f"Error loading data: {error_message}")
                return
        
        # Date filters with improved UX
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start date",
                datetime.now() - timedelta(days=30),
                help="Select start date for filtering data"
            )
        with col2:
            end_date = st.date_input(
                "End date",
                datetime.now(),
                help="Select end date for filtering data"
            )
        
        # Sheet selector with search
        sheet_option = st.selectbox(
            "Select a sheet to view",
            options=list(SHEET_CONFIG.keys()),
            help="Choose which data sheet to analyze"
        )
        
        # Apply filters with loading indicator
        if st.button("Apply Filters", help="Click to apply date filters to the data"):
            with st.spinner("Applying filters..."):
                st.session_state.data_processor.filter_by_date(start_date, end_date)
            st.success("Filters applied successfully!")
        
        # Create tabs with loading states
        tab_overview, tab_trends, tab_distribution = st.tabs([
            "Overview 📊",
            "Trends Analysis 📈",
            "Distribution Analysis 📉"
        ])
        
        df = st.session_state.data_processor.get_sheet_data(sheet_option)
        if df is not None:
            config = SHEET_CONFIG[sheet_option]
            
            with tab_overview:
                st.subheader("Summary Statistics")
                for value_col in config['value_columns']:
                    summary_stats = st.session_state.cache_manager.cache_analysis(
                        f"summary_{sheet_option}_{value_col}",
                        generate_summary_stats(df, [value_col])[value_col]
                    )
                    create_summary_cards(summary_stats, value_col)
                
                st.subheader("Data Table")
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=400
                )
            
            with tab_trends:
                st.subheader("Trend Analysis")
                for value_col in config['value_columns']:
                    with st.spinner(f"Generating trend analysis for {value_col}..."):
                        trends = st.session_state.cache_manager.cache_analysis(
                            f"trends_{sheet_option}_{value_col}",
                            analyze_trends(df, config['date_column'], [value_col])
                        )
                        fig = create_trend_plot(trends[value_col], value_col)
                        st.plotly_chart(fig, use_container_width=True)
            
            with tab_distribution:
                st.subheader("Distribution Analysis")
                for value_col in config['value_columns']:
                    with st.spinner(f"Generating distribution analysis for {value_col}..."):
                        fig = st.session_state.cache_manager.cache_analysis(
                            f"distribution_{sheet_option}_{value_col}",
                            create_distribution_plot(df, value_col)
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No data available for the selected sheet")
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An error occurred while running the application. Please try refreshing the page.")

if __name__ == "__main__":
    main()