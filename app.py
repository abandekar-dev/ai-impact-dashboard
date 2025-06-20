import streamlit as st
import sys
import os

# Temporary fix for numpy import issue
try:
    import pandas as pd
    import numpy as np
    DEPS_AVAILABLE = True
except ImportError as e:
    st.error(f"Dependency issue detected: {e}")
    st.info("Running in limited mode. Some features may be unavailable.")
    DEPS_AVAILABLE = False
    
    # Create mock modules for essential functionality
    class MockPandas:
        def DataFrame(self, data):
            return data
    
    class MockNumpy:
        def array(self, data):
            return data
        def mean(self, data):
            return sum(data) / len(data) if data else 0
    
    pd = MockPandas()
    np = MockNumpy()

if DEPS_AVAILABLE:
    # Import all other dependencies normally
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    from datetime import datetime, timedelta
    import json
    from typing import Dict, List, Any, Optional
    
    # Import utility modules with error handling
    try:
        from utils.database import DatabaseManager
        from utils.category_manager import CategoryManager
        from utils.predictive_engine import PredictiveEngine
        from utils.benchmarking import IndustryBenchmarking, SensitivityAnalysis
        from utils.dashboard_visualizer import DashboardVisualizer
        
        # Initialize components
        category_manager = CategoryManager()
        
        # Database initialization
        db = None
        try:
            db = DatabaseManager()
        except Exception as e:
            st.sidebar.warning("Database connection unavailable. Using session storage only.")
    except ImportError as e:
        st.warning(f"Some utility modules unavailable: {e}")
        category_manager = None
        db = None

def init_database():
    """Initialize database tables if needed"""
    if db:
        try:
            # Database operations only if available
            pass
        except Exception as e:
            st.sidebar.warning(f"Database initialization warning: {str(e)}")

def auto_save_data():
    """Automatically save data to prevent loss during navigation"""
    if 'baseline_data' not in st.session_state:
        st.session_state.baseline_data = {}
    if 'ai_initiatives' not in st.session_state:
        st.session_state.ai_initiatives = {}
    if 'predictions' not in st.session_state:
        st.session_state.predictions = {}
    
    # Auto-save every 30 seconds
    current_time = datetime.now()
    if 'last_save_timestamp' not in st.session_state:
        st.session_state.last_save_timestamp = current_time
    
    time_diff = (current_time - st.session_state.last_save_timestamp).total_seconds()
    
    if time_diff > 30:  # Auto-save every 30 seconds
        try:
            # Save to local session storage as backup
            if not hasattr(st.session_state, 'local_backup'):
                st.session_state.local_backup = {}
            
            st.session_state.local_backup = {
                'baseline_data': dict(st.session_state.baseline_data),
                'ai_initiatives': dict(st.session_state.ai_initiatives),
                'predictions': dict(st.session_state.predictions),
                'timestamp': current_time
            }
            
            st.session_state.last_save_timestamp = current_time
        except Exception:
            pass  # Continue even if auto-save fails

# Call auto-save
if DEPS_AVAILABLE:
    auto_save_data()

def main():
    st.title("🎯 Analytics and Insights Engine")
    st.markdown("**Executive Platform for Strategic AI Implementation and Workforce Transformation Analytics**")
    
    if not DEPS_AVAILABLE:
        st.warning("Application running in limited mode due to dependency issues. Some visualizations may be unavailable.")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Overview"
    
    # Navigation buttons
    pages = [
        ("🏠 Overview", "Overview"),
        ("🏢 Enhanced Function Analysis", "Enhanced Function Analysis"),
        ("📊 Comparative Analysis", "Comparative Analysis"),
        ("🔧 Build vs Buy Analysis", "Build Buy Analysis"),
        ("📈 Performance Analysis", "Performance Analysis"),
        ("💰 Budget & Resource Constraints", "Budget Resources"),
        ("🎯 Corporate Objectives & KPIs", "Corporate Objectives"),
    ]
    
    for button_text, page_name in pages:
        if st.sidebar.button(button_text, use_container_width=True,
                            type="primary" if st.session_state.selected_page == page_name else "secondary"):
            st.session_state.selected_page = page_name
            st.rerun()
    
    # Page routing
    page = st.session_state.selected_page
    
    if page == "Overview":
        show_overview()
    elif page == "Enhanced Function Analysis":
        if DEPS_AVAILABLE:
            from pages.enhanced_function_analysis import show_enhanced_function_analysis
            show_enhanced_function_analysis(category_manager, db)
        else:
            st.error("This page requires full dependencies. Please resolve import issues.")
    elif page == "Comparative Analysis":
        if DEPS_AVAILABLE:
            from pages.comparative_analysis import show_comparative_analysis
            show_comparative_analysis()
        else:
            st.error("This page requires full dependencies. Please resolve import issues.")
    elif page == "Build Buy Analysis":
        if DEPS_AVAILABLE:
            from pages.build_buy_analysis import show_build_buy_analysis
            show_build_buy_analysis()
        else:
            st.error("This page requires full dependencies. Please resolve import issues.")
    elif page == "Performance Analysis":
        if DEPS_AVAILABLE:
            from pages.performance_analysis import show_performance_analysis
            show_performance_analysis(category_manager)
        else:
            st.error("This page requires full dependencies. Please resolve import issues.")
    else:
        show_basic_info()

def show_overview():
    """Show overview page with basic functionality"""
    st.markdown("""
    ## 🎯 AI-Powered Strategic Modeling Platform
    
    Welcome to the Analytics and Insights Engine - your comprehensive platform for enterprise AI transformation and workforce analytics.
    
    ### 🔧 Current Status
    """)
    
    if DEPS_AVAILABLE:
        st.success("✅ All systems operational")
        st.markdown("""
        ### 🚀 Available Modules
        
        - **Enhanced Function Analysis**: Configure enterprise functions and AI initiatives
        - **Comparative Analysis**: Before/after impact assessment with financial projections
        - **Build vs Buy Analysis**: Strategic workforce planning and skills gap analysis  
        - **Performance Analysis**: Cross-function optimization and benchmarking
        - **Budget & Resource Constraints**: Financial planning and resource allocation
        - **Corporate Objectives & KPIs**: Strategic alignment and goal setting
        """)
    else:
        st.warning("⚠️ Running in limited mode - dependency issues detected")
        st.markdown("""
        ### 🔧 Troubleshooting
        
        The application is currently experiencing dependency import issues. To resolve:
        
        1. **Check Python Environment**: Ensure numpy and pandas are properly installed
        2. **Clear Cache**: Restart the application server
        3. **Reinstall Dependencies**: Use the package manager to reinstall core packages
        
        ### 📋 Basic Information Available
        
        - Platform architecture overview
        - Module descriptions and capabilities
        - System requirements and setup guides
        """)
    
    # System information
    st.markdown("### 📊 System Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Platform Version", "2.0.1")
    with col2:
        st.metric("Modules Available", "6+")
    with col3:
        if DEPS_AVAILABLE:
            st.metric("System Status", "Operational", delta="Full")
        else:
            st.metric("System Status", "Limited", delta="Degraded")

def show_basic_info():
    """Show basic information when full functionality is unavailable"""
    st.markdown("""
    ## 📋 Platform Information
    
    This AI-powered strategic modeling platform provides comprehensive analytics for enterprise AI transformation.
    
    ### 🏗️ Architecture Overview
    
    - **Frontend**: Streamlit interactive dashboard
    - **Backend**: Python-based analytics engine
    - **Database**: PostgreSQL with vector extensions
    - **AI Services**: OpenAI integration for natural language processing
    
    ### 🎯 Key Capabilities
    
    1. **Function Analysis**: Enterprise function modeling and AI initiative planning
    2. **Comparative Analysis**: Before/after impact assessment
    3. **Workforce Planning**: Build vs buy strategic decisions
    4. **Performance Analytics**: Cross-function optimization
    5. **Financial Modeling**: ROI calculations and budget planning
    
    ### 🔧 Technical Requirements
    
    - Python 3.11+
    - NumPy, Pandas for data processing
    - Plotly for visualizations
    - PostgreSQL database
    - OpenAI API access (optional)
    """)

if __name__ == "__main__":
    main()