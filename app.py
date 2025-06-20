import streamlit as st
from datetime import datetime, timedelta

# Import dependencies through compatibility layer
try:
    from utils.compatibility import (
        np, pd, px, go, make_subplots,
        NUMPY_AVAILABLE, PANDAS_AVAILABLE, PLOTLY_AVAILABLE
    )
except ImportError:
    # Fallback if compatibility module isn't available
    try:
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = True
    except ImportError:
        st.error("Required dependencies are not available. Some features may be limited.")
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = False

# Import utility modules
from utils.data_models import EnterpriseFunction, AIInitiative
from utils.predictive_engine import PredictiveEngine
from utils.visualization import DashboardVisualizer
from utils.report_generator import ReportGenerator
try:
    from utils.database import DatabaseManager
except ImportError:
    from utils.database_fallback import DatabaseManagerFallback as DatabaseManager
from utils.benchmarking import IndustryBenchmarking, SensitivityAnalysis, ScenarioOptimization
from utils.session_manager import SessionManager
from utils.monte_carlo import MonteCarloSimulator, ScenarioModeler
from utils.strategic_scenarios import StrategicScenarioPlanner
from utils.category_manager import CategoryManager

# Page configuration
st.set_page_config(
    page_title="AI Impact Predictive Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database manager
@st.cache_resource
def init_database():
    try:
        return DatabaseManager()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

db = init_database()

# Initialize session manager
session_manager = SessionManager(db) if db else None

# Initialize session state
if 'ai_initiatives' not in st.session_state:
    st.session_state.ai_initiatives = {}
if 'baseline_data' not in st.session_state:
    st.session_state.baseline_data = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Initialize category manager
category_manager = CategoryManager()

# Load data from database on first run
if db and not st.session_state.data_loaded:
    try:
        data = db.load_all_data()
        st.session_state.baseline_data = data['baseline_data']
        st.session_state.ai_initiatives = data['ai_initiatives']
        st.session_state.predictions = data['predictions']
        st.session_state.data_loaded = True
    except Exception as e:
        print(f"Database load failed, using local session storage: {e}")
        st.session_state.data_loaded = True

# Auto-save mechanism to preserve data across page navigation
def auto_save_data():
    """Automatically save data to prevent loss during navigation"""
    if 'last_save_timestamp' not in st.session_state:
        st.session_state.last_save_timestamp = 0
    
    import time
    current_time = time.time()
    
    # Auto-save every 30 seconds if data has changed
    if current_time - st.session_state.last_save_timestamp > 30:
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
            
            # Try to save to database if available
            if db:
                try:
                    for func_name, baseline in st.session_state.baseline_data.items():
                        db.save_function_baseline(func_name, baseline)
                except Exception:
                    pass  # Silent fail, data is still preserved locally
                    
            st.session_state.last_save_timestamp = current_time
        except Exception:
            pass  # Continue even if auto-save fails

# Call auto-save
auto_save_data()

def main():
    st.title("🎯 AI Impact Predictive Dashboard")
    st.markdown("**Executive Dashboard for Predictive Modeling of AI Implementation Impact**")
    
    # Sidebar navigation with grouped buttons
    st.sidebar.title("Navigation")
    
    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Overview"
    
    # Overview (always visible)
    if st.sidebar.button("🏠 Overview", use_container_width=True, 
                        type="primary" if st.session_state.selected_page == "Overview" else "secondary"):
        st.session_state.selected_page = "Overview"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Inputs Section
    st.sidebar.markdown("### 📥 Inputs")
    if st.sidebar.button("🏢 Input by Department/Business", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Function Analysis" else "secondary"):
        st.session_state.selected_page = "Function Analysis"
        st.rerun()
    
    if st.sidebar.button("🎯 Corporate Objectives & KPIs", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Corporate Objectives" else "secondary"):
        st.session_state.selected_page = "Corporate Objectives"
        st.rerun()
    
    if st.sidebar.button("💰 Budget & Resource Constraints", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Budget Resources" else "secondary"):
        st.session_state.selected_page = "Budget Resources"
        st.rerun()
    
    if st.sidebar.button("🔄 Change Management Readiness", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Change Management" else "secondary"):
        st.session_state.selected_page = "Change Management"
        st.rerun()
    
    if st.sidebar.button("🔗 Enterprise Data Integration", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Enterprise Integration" else "secondary"):
        st.session_state.selected_page = "Enterprise Integration"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Analyses Section
    st.sidebar.markdown("### 🔬 Analyses")
    
    if st.sidebar.button("🎯 Strategic Planning", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Strategic Planning" else "secondary"):
        st.session_state.selected_page = "Strategic Planning"
        st.rerun()
    
    if st.sidebar.button("👥 Workforce Analytics", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Workforce Analytics" else "secondary"):
        st.session_state.selected_page = "Workforce Analytics"
        st.rerun()
    
    if st.sidebar.button("🎓 AI Learning & Upskilling Personas", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "AI Learning & Upskilling Personas" else "secondary"):
        st.session_state.selected_page = "AI Learning & Upskilling Personas"
        st.rerun()
    
    if st.sidebar.button("📊 Performance Analysis", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Performance Analysis" else "secondary"):
        st.session_state.selected_page = "Performance Analysis"
        st.rerun()
    
    if st.sidebar.button("⚖️ Benchmarking & Optimization", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Benchmarking & Optimization" else "secondary"):
        st.session_state.selected_page = "Benchmarking & Optimization"
        st.rerun()
    
    if st.sidebar.button("🎲 Monte Carlo Simulation", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Monte Carlo Simulation" else "secondary"):
        st.session_state.selected_page = "Monte Carlo Simulation"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Outputs Section
    st.sidebar.markdown("### 📤 Outputs")
    if st.sidebar.button("🤖 AI Strategic Assistant", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "AI Assistant" else "secondary"):
        st.session_state.selected_page = "AI Assistant"
        st.rerun()
    
    if st.sidebar.button("📋 Executive Summary", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Executive Summary" else "secondary"):
        st.session_state.selected_page = "Executive Summary"
        st.rerun()
    
    # Use the selected page
    page = st.session_state.selected_page
    
    # Session Management Sidebar
    if session_manager:
        st.sidebar.markdown("---")
        st.sidebar.subheader("💾 Session Management")
        
        # Create new session button
        if st.sidebar.button("🆕 Create New Session", use_container_width=True, type="secondary"):
            if session_manager.create_new_session():
                st.success("New session created! All data cleared.")
                st.rerun()
            else:
                st.error("Failed to create new session")
        
        # Save current session
        with st.sidebar.expander("Save Current Session"):
            session_name = st.text_input("Session Name", key="save_session_name")
            session_desc = st.text_area("Description (optional)", key="save_session_desc")
            
            if st.button("💾 Save Session") and session_name:
                if session_manager.save_session(session_name, session_desc):
                    st.success(f"Session '{session_name}' saved!")
                else:
                    st.error("Failed to save session")
        
        # Load saved session
        with st.sidebar.expander("Load Saved Session"):
            saved_sessions = session_manager.get_saved_sessions()
            
            if saved_sessions:
                session_options = [f"{s['name']} ({s['updated_at'].strftime('%Y-%m-%d %H:%M') if hasattr(s['updated_at'], 'strftime') else s['updated_at']})" for s in saved_sessions]
                selected_session = st.selectbox("Select Session", [""] + session_options, key="load_session_select")
                
                if selected_session and st.button("📂 Load Session"):
                    session_name = selected_session.split(" (")[0]
                    if session_manager.load_session(session_name):
                        st.success(f"Session '{session_name}' loaded!")
                        st.rerun()
                    else:
                        st.error("Failed to load session")
                
                # Display session info
                if saved_sessions:
                    st.markdown("**Saved Sessions:**")
                    for session in saved_sessions[:3]:
                        st.write(f"• {session['name']}")
                        st.caption(session['description'])
            else:
                st.write("No saved sessions found")
    
    # Main content based on page selection
    if page == "Overview":
        show_overview()
    elif page == "Function Analysis":
        from pages.enhanced_function_analysis import show_enhanced_function_analysis
        show_enhanced_function_analysis(category_manager, db)
    elif page == "Corporate Objectives":
        from pages.corporate_objectives import show_corporate_objectives
        show_corporate_objectives()
    elif page == "Budget Resources":
        from pages.budget_resources import show_budget_resources
        show_budget_resources()
    elif page == "Change Management":
        from pages.change_management import show_change_management
        show_change_management()
    elif page == "Enterprise Integration":
        from pages.enterprise_integrations import show_enterprise_integrations
        show_enterprise_integrations()
    elif page == "Monte Carlo Simulation":
        show_monte_carlo_simulation()
    elif page == "Strategic Planning":
        show_strategic_planning()
    elif page == "Benchmarking & Optimization":
        show_benchmarking_optimization()
    elif page == "Performance Analysis":
        from pages.performance_analysis import show_performance_analysis
        show_performance_analysis(category_manager)
    elif page == "Workforce Analytics":
        from pages.workforce_analytics import show_workforce_analytics
        show_workforce_analytics()
    elif page == "AI Learning & Upskilling Personas":
        from pages.learning_personas import show_learning_personas
        show_learning_personas()
    elif page == "AI Assistant":
        from pages.ai_assistant import show_ai_assistant
        show_ai_assistant()
    elif page == "Executive Summary":
        show_executive_summary()

def show_overview():
    # Add modern background styling
    st.markdown("""
    <style>
    .main > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-top: 2rem;
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h1 style="text-align: center; color: #4a5568; font-size: 3rem; font-weight: 700; 
               text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               background-clip: text;">
        📊 AI Strategic Dashboard
    </h1>
    """, unsafe_allow_html=True)
    
    # Modern metrics cards with gradient styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_functions = len(st.session_state.baseline_data)
        from utils.chart_styling import create_styled_metric_card
        st.markdown(create_styled_metric_card(
            f"{active_functions}", 
            "Active Functions",
            "teal"
        ), unsafe_allow_html=True)
    
    with col2:
        total_revenue = sum(data.get('annual_revenue', 0) for data in st.session_state.baseline_data.values())
        st.markdown(create_styled_metric_card(
            f"${total_revenue:,.0f}", 
            "Total Revenue",
            "purple"
        ), unsafe_allow_html=True)
    
    with col3:
        total_headcount = sum(data.get('headcount', 0) for data in st.session_state.baseline_data.values())
        st.markdown(create_styled_metric_card(
            f"{total_headcount:,}", 
            "Total Headcount",
            "orange"
        ), unsafe_allow_html=True)
    
    with col4:
        if st.session_state.predictions:
            avg_roi = np.mean([p.get('roi', 0) for p in st.session_state.predictions.values()])
            roi_display = f"{avg_roi:.1f}%"
        else:
            roi_display = "N/A"
        st.markdown(create_styled_metric_card(
            roi_display, 
            "Projected ROI",
            "pink"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced function status in styled cards
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 12px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border: 1px solid #e5e7eb;">
    """, unsafe_allow_html=True)
    
    st.subheader("🚀 Function Configuration Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Enterprise Functions:**")
        functions = ["HR & Talent Management", "Finance & Accounting", "Operations & Supply Chain", 
                    "Sales & Marketing", "IT & Technology", "Customer Service", "Legal & Compliance", "R&D",
                    "Manufacturing & Production", "Quality Assurance", "Business Development", "Strategy & Planning",
                    "Risk Management", "Procurement", "Facilities Management", "Data & Analytics"]
        
        for func in functions:
            if func in st.session_state.baseline_data:
                st.markdown(f"""
                <div style="background: #f0f9ff; padding: 0.75rem; border-radius: 8px; 
                            margin: 0.25rem 0; border-left: 4px solid #10b981;">
                    ✅ {func} - Configured
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f9fafb; padding: 0.75rem; border-radius: 8px; 
                            margin: 0.25rem 0; border-left: 4px solid #d1d5db;">
                    ⚪ {func} - Not configured
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Quick Start Guide:**")
        steps = [
            "Navigate to **Function Analysis** to configure departments",
            "Set baseline metrics and AI implementation parameters", 
            "Use **Strategic Planning** to evaluate scenarios",
            "Review **Workforce Analytics** for impact assessment",
            "Generate **Executive Summary** for stakeholder presentations"
        ]
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; 
                        margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
                <strong>{i}.</strong> {step}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Performance visualization if data exists
    if len(st.session_state.baseline_data) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 12px; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border: 1px solid #e5e7eb;">
        """, unsafe_allow_html=True)
        
        st.subheader("📈 Performance Overview")
        
        # Create enhanced performance visualization
        functions = []
        productivity = []
        satisfaction = []
        
        for func_name, data in st.session_state.baseline_data.items():
            functions.append(func_name)
            productivity.append(data.get('current_productivity', 0))
            satisfaction.append(data.get('performance_satisfaction', 0))
        
        fig = go.Figure()
        
        # Enhanced bar chart with modern styling
        fig.add_trace(go.Bar(
            name='Current Productivity', 
            x=functions, 
            y=productivity,
            marker_color='rgba(99, 102, 241, 0.8)',
            marker_line_color='rgba(99, 102, 241, 1.0)',
            marker_line_width=2,
            text=[f'{p}%' for p in productivity],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Performance Satisfaction', 
            x=functions, 
            y=satisfaction,
            marker_color='rgba(16, 185, 129, 0.8)',
            marker_line_color='rgba(16, 185, 129, 1.0)',
            marker_line_width=2,
            text=[f'{s}%' for s in satisfaction],
            textposition='outside'
        ))
        
        fig.update_layout(
            title={
                'text': "Current Performance Metrics by Function",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Arial, sans-serif', 'color': '#1f2937'}
            },
            xaxis_title="Business Functions",
            yaxis_title="Performance Score (0-100)",
            barmode='group',
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Arial, sans-serif', 'color': '#374151'},
            legend={
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'right',
                'x': 1,
                'bgcolor': 'rgba(255,255,255,0.8)'
            },
            margin={'t': 60, 'b': 40, 'l': 40, 'r': 40}
        )
        
        fig.update_xaxes(gridcolor='rgba(0,0,0,0.1)', tickangle=45)
        fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def show_function_analysis():
    st.header("🏢 Function Analysis")
    
    # Function selector
    functions = ["HR & Talent Management", "Finance & Accounting", "Operations & Supply Chain", 
                "Sales & Marketing", "IT & Technology", "Customer Service", "Legal & Compliance", "R&D",
                "Manufacturing & Production", "Quality Assurance", "Business Development", "Strategy & Planning",
                "Risk Management", "Procurement", "Facilities Management", "Data & Analytics"]
    
    selected_function = st.selectbox("Select Enterprise Function", functions)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Baseline Metrics")
        
        # Current metrics input
        current_productivity = st.number_input("Current Productivity Index (0-100)", 
                                             min_value=0.0, max_value=100.0, value=75.0, step=0.1)
        current_headcount = st.number_input("Current Headcount", min_value=1, value=100, step=1)
        current_revenue = st.number_input("Annual Revenue Contribution ($)", 
                                        min_value=0, value=1000000, step=10000)
        current_costs = st.number_input("Annual Operating Costs ($)", 
                                      min_value=0, value=500000, step=10000)
        current_satisfaction = st.number_input("Performance Satisfaction (0-100)", 
                                             min_value=0.0, max_value=100.0, value=80.0, step=0.1)
    
    with col2:
        st.subheader("🤖 AI Initiative Configuration")
        
        ai_type = st.selectbox("AI Implementation Type", 
                              ["Automation", "Augmentation", "Analytics", "Hybrid"])
        implementation_complexity = st.selectbox("Implementation Complexity", 
                                                ["Low", "Medium", "High"])
        investment_amount = st.number_input("Total Investment ($)", 
                                          min_value=0.0, value=100000.0, step=5000.0)
        implementation_timeline = st.selectbox("Implementation Timeline", 
                                             ["3 months", "6 months", "12 months", "18 months", "24 months"])
        change_management = st.selectbox("Change Management Approach", 
                                       ["Gradual", "Phased", "Big Bang"])
    
    st.markdown("---")
    
    # Advanced parameters
    with st.expander("🔧 Advanced Parameters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Risk Factors**")
            technical_risk = st.slider("Technical Risk (0-100)", 0, 100, 30)
            adoption_risk = st.slider("User Adoption Risk (0-100)", 0, 100, 40)
            integration_risk = st.slider("Integration Risk (0-100)", 0, 100, 35)
            regulatory_risk = st.slider("Regulatory Risk (0-100)", 0, 100, 25)
            competitive_risk = st.slider("Competitive Risk (0-100)", 0, 100, 20)
            data_risk = st.slider("Data Quality Risk (0-100)", 0, 100, 30)
        
        with col2:
            st.markdown("**Expected Improvements**")
            automation_level = st.slider("Automation Level (%)", 0, 100, 50)
            accuracy_improvement = st.slider("Accuracy Improvement (%)", 0, 100, 25)
            speed_improvement = st.slider("Speed Improvement (%)", 0, 100, 40)
        
        with col3:
            st.markdown("**Workforce Impact**")
            workforce_reduction = st.slider("Workforce Reduction (%)", 0, 50, 10)
            upskilling_required = st.slider("Upskilling Required (%)", 0, 100, 60)
            new_roles_created = st.slider("New Roles Created (%)", 0, 30, 5)
    
    # Save configuration
    if st.button("💾 Save Configuration & Run Predictions", type="primary"):
        # Store baseline data
        baseline_data = {
            'productivity': current_productivity,
            'headcount': int(current_headcount),
            'revenue': current_revenue,
            'costs': current_costs,
            'satisfaction': current_satisfaction
        }
        st.session_state.baseline_data[selected_function] = baseline_data
        
        # Store AI initiative data
        initiative_data = {
            'ai_type': ai_type,
            'complexity': implementation_complexity,
            'investment': investment_amount,
            'timeline': implementation_timeline,
            'change_management': change_management,
            'technical_risk': technical_risk,
            'adoption_risk': adoption_risk,
            'integration_risk': integration_risk,
            'regulatory_risk': regulatory_risk,
            'competitive_risk': competitive_risk,
            'data_risk': data_risk,
            'automation_level': automation_level,
            'accuracy_improvement': accuracy_improvement,
            'speed_improvement': speed_improvement,
            'workforce_reduction': workforce_reduction,
            'upskilling_required': upskilling_required,
            'new_roles_created': new_roles_created
        }
        st.session_state.ai_initiatives[selected_function] = {
            'type': ai_type,
            'complexity': implementation_complexity,
            'investment': investment_amount,
            'timeline': implementation_timeline,
            'change_management': change_management,
            'technical_risk': technical_risk,
            'adoption_risk': adoption_risk,
            'integration_risk': integration_risk,
            'regulatory_risk': regulatory_risk,
            'competitive_risk': competitive_risk,
            'data_risk': data_risk,
            'automation_level': automation_level,
            'accuracy_improvement': accuracy_improvement,
            'speed_improvement': speed_improvement,
            'workforce_reduction': workforce_reduction,
            'upskilling_required': upskilling_required,
            'new_roles_created': new_roles_created
        }
        
        # Save to database if available
        if db:
            db.save_function_baseline(selected_function, baseline_data)
            db.save_ai_initiative(selected_function, initiative_data)
        
        # Run predictions
        engine = PredictiveEngine()
        predictions = engine.predict_impact(baseline_data, initiative_data)
        st.session_state.predictions[selected_function] = predictions
        
        # Save predictions to database if available
        if db:
            db.save_prediction(selected_function, predictions)
        
        st.success("✅ Configuration saved and predictions generated!")
        st.rerun()
    
    # Display predictions if available
    if selected_function in st.session_state.predictions:
        st.markdown("---")
        st.subheader("📈 Prediction Results")
        
        predictions = st.session_state.predictions[selected_function]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Productivity Gain", f"{predictions['productivity_gain']:.1f}%")
        with col2:
            st.metric("ROI", f"{predictions['roi']:.1f}%")
        with col3:
            st.metric("Value Generated", f"${predictions['value_generated']:,.0f}")
        with col4:
            st.metric("Payback Period", f"{predictions['payback_period']:.1f} months")
        
        # Model confidence and quality indicators (if available)
        if 'confidence_metrics' in predictions:
            st.markdown("---")
            st.subheader("🎯 Prediction Quality & Confidence")
            
            confidence = predictions['confidence_metrics']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                confidence_color = "green" if confidence['overall_confidence'] > 0.8 else "orange" if confidence['overall_confidence'] > 0.6 else "red"
                st.metric(
                    "Overall Confidence", 
                    f"{confidence['overall_confidence']:.1%}",
                    help="Higher confidence indicates more reliable predictions"
                )
                st.markdown(f"**Quality Level:** :{confidence_color}[{confidence['confidence_level']}]")
            
            with col2:
                st.metric("Data Quality", f"{confidence['data_quality']:.1%}")
                st.metric("Feature Reliability", f"{confidence['feature_reliability']:.1%}")
            
            with col3:
                st.metric("Model Stability", f"{confidence['model_stability']:.1%}")
                if 'prediction_quality' in predictions:
                    quality_color = "green" if predictions['prediction_quality'] == "High" else "orange" if predictions['prediction_quality'] == "Medium" else "red"
                    st.markdown(f"**Prediction Quality:** :{quality_color}[{predictions['prediction_quality']}]")
        
        # Enhanced Workforce Impact Analysis
        if 'workforce_impact' in predictions:
            st.markdown("---")
            st.subheader("👥 Comprehensive Workforce Impact Analysis")
            
            workforce = predictions['workforce_impact']
            
            # Basic Workforce Metrics
            st.markdown("#### 📊 Workforce Changes")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Headcount", f"{workforce.get('current_headcount', 0):,}")
                st.metric("Positions Eliminated", f"{workforce.get('reduced_positions', 0):,}")
            
            with col2:
                st.metric("New Positions Created", f"{workforce.get('new_positions', 0):,}")
                st.metric("Employees to Upskill", f"{workforce.get('upskilling_count', 0):,}")
            
            with col3:
                net_change = workforce.get('net_change', 0)
                st.metric("Net Headcount Change", f"{net_change:+,}")
                st.metric("Final Headcount", f"{workforce.get('final_headcount', 0):,}")
            
            with col4:
                pct_change = workforce.get('percentage_change', 0)
                st.metric("Percentage Change", f"{pct_change:+.1f}%")
                avg_salary = workforce.get('avg_salary_estimate', 0)
                st.metric("Est. Avg Salary", f"${avg_salary:,.0f}")
            
            # Financial Impact of Workforce Changes
            st.markdown("#### 💰 Financial Impact")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                savings = workforce.get('reduction_savings', 0)
                st.metric("Reduction Savings", f"${savings:,.0f}", help="Annual savings from position eliminations")
                upskill_cost = workforce.get('upskilling_cost', 0)
                st.metric("Upskilling Investment", f"${upskill_cost:,.0f}", help="Cost to train existing employees")
            
            with col2:
                hire_cost = workforce.get('new_hire_cost', 0)
                st.metric("New Hire Costs", f"${hire_cost:,.0f}", help="Annual cost for new positions")
                recruit_cost = workforce.get('recruitment_cost', 0)
                st.metric("Recruitment Costs", f"${recruit_cost:,.0f}", help="One-time recruitment expenses")
            
            with col3:
                net_cost = workforce.get('net_cost_impact', 0)
                cost_color = "red" if net_cost > 0 else "green"
                st.metric("Net Cost Impact", f"${net_cost:,.0f}", 
                         help="Total financial impact (positive = cost, negative = savings)")
                if net_cost > 0:
                    st.markdown(f":{cost_color}[Additional Investment Required]")
                else:
                    st.markdown(f":{cost_color}[Net Savings Achieved]")
            
            # Timeline and Transition Management
            st.markdown("#### ⏱️ Implementation Timeline & Transition")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                impl_timeline = workforce.get('implementation_timeline_months', 0)
                st.metric("Implementation Period", f"{impl_timeline} months")
                transition_months = workforce.get('transition_period_months', 0)
                st.metric("Transition Period", f"{transition_months} months")
            
            with col2:
                training_duration = workforce.get('training_duration_months', 0)
                st.metric("Training Duration", f"{training_duration:.1f} months")
                productivity_loss = workforce.get('transition_productivity_loss_percent', 0)
                st.metric("Transition Productivity Loss", f"{productivity_loss:.1f}%")
            
            with col3:
                skill_gap = workforce.get('skill_gap_severity', 'Medium')
                gap_color = "red" if skill_gap == "High" else "orange" if skill_gap == "Medium" else "green"
                st.markdown(f"**Skill Gap Severity:** :{gap_color}[{skill_gap}]")
                
                resistance = workforce.get('change_resistance_level', 'Medium')
                resist_color = "red" if resistance == "High" else "orange" if resistance == "Medium" else "green"
                st.markdown(f"**Change Resistance:** :{resist_color}[{resistance}]")
                
                retention_risk = workforce.get('retention_risk_percent', 0)
                st.metric("Retention Risk", f"{retention_risk:.1f}%")
            
            # Role Transformation Analysis
            st.markdown("#### 🔄 Role Transformation Breakdown")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                eliminated = workforce.get('roles_eliminated', 0)
                st.metric("Roles Eliminated", f"{eliminated:,}", help="Positions completely removed")
            
            with col2:
                transformed = workforce.get('roles_transformed', 0)
                st.metric("Roles Transformed", f"{transformed:,}", help="Existing roles with major changes")
            
            with col3:
                augmented = workforce.get('roles_augmented', 0)
                st.metric("Roles Augmented", f"{augmented:,}", help="Roles enhanced with AI assistance")
            
            with col4:
                created = workforce.get('roles_created', 0)
                st.metric("New Roles Created", f"{created:,}", help="Entirely new positions")
            
            # Strategic Workforce Metrics
            st.markdown("#### 🚀 Strategic Workforce Capabilities")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                agility = workforce.get('workforce_agility_score', 0)
                agility_color = "green" if agility > 70 else "orange" if agility > 40 else "red"
                st.metric("Workforce Agility", f"{agility:.0f}/100")
                st.markdown(f":{agility_color}[{agility:.0f}/100 - Adaptability to change]")
                
                collaboration = workforce.get('human_ai_collaboration_index', 0)
                collab_color = "green" if collaboration > 70 else "orange" if collaboration > 40 else "red"
                st.metric("Human-AI Collaboration", f"{collaboration:.0f}/100")
                st.markdown(f":{collab_color}[{collaboration:.0f}/100 - Integration effectiveness]")
            
            with col2:
                future_ready = workforce.get('future_readiness_score', 0)
                ready_color = "green" if future_ready > 70 else "orange" if future_ready > 40 else "red"
                st.metric("Future Readiness", f"{future_ready:.0f}/100")
                st.markdown(f":{ready_color}[{future_ready:.0f}/100 - Preparedness for future]")
                
                digital_literacy = workforce.get('digital_literacy_improvement', 0)
                st.metric("Digital Literacy Gain", f"{digital_literacy:.0f}/100")
            
            with col3:
                automation_ready = workforce.get('process_automation_readiness', 0)
                auto_color = "green" if automation_ready > 70 else "orange" if automation_ready > 40 else "red"
                st.metric("Automation Readiness", f"{automation_ready:.0f}/100")
                st.markdown(f":{auto_color}[{automation_ready:.0f}/100 - Process automation capability]")
                
                adaptability = workforce.get('change_adaptability_score', 0)
                adapt_color = "green" if adaptability > 70 else "orange" if adaptability > 40 else "red"
                st.metric("Change Adaptability", f"{adaptability:.0f}/100")
                st.markdown(f":{adapt_color}[{adaptability:.0f}/100 - Organizational flexibility]")
        
        # Visualization
        visualizer = DashboardVisualizer()
        fig = visualizer.create_impact_summary(predictions, selected_function)
        st.plotly_chart(fig, use_container_width=True)

def show_monte_carlo_simulation():
    st.header("🎲 Monte Carlo Simulation")
    st.markdown("**Probabilistic Analysis with Uncertainty Quantification**")
    
    if len(st.session_state.predictions) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    # Function selection for simulation
    configured_functions = list(st.session_state.predictions.keys())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_function = st.selectbox("Select Function for Monte Carlo Analysis", configured_functions)
    
    with col2:
        n_simulations = st.selectbox("Number of Simulations", [500, 1000, 2500, 5000], index=1)
    
    if selected_function not in st.session_state.baseline_data or selected_function not in st.session_state.ai_initiatives:
        st.error("Missing baseline data or AI initiative configuration for the selected function.")
        return
    
    # Uncertainty parameter configuration
    st.markdown("---")
    st.subheader("⚙️ Uncertainty Parameters")
    st.markdown("Configure uncertainty ranges for key variables to model realistic variation in outcomes.")
    
    with st.expander("📊 Parameter Uncertainty Settings", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Investment & Financial**")
            investment_std = st.slider("Investment Uncertainty (%)", 5, 30, 15, 
                                     help="Standard deviation as % of base investment")
            market_volatility = st.slider("Market Conditions Volatility (%)", 5, 25, 12,
                                        help="Market condition variation affecting revenue")
        
        with col2:
            st.markdown("**Technical Performance**")
            automation_std = st.slider("Automation Level Uncertainty (%)", 10, 40, 20,
                                     help="Variation in achieved automation level")
            accuracy_std = st.slider("Accuracy Improvement Uncertainty (%)", 15, 40, 25,
                                   help="Variation in accuracy improvements")
            speed_std = st.slider("Speed Improvement Uncertainty (%)", 10, 30, 20,
                                help="Variation in speed improvements")
        
        with col3:
            st.markdown("**Risk Factors**")
            risk_distribution = st.selectbox("Risk Distribution Type", ["Beta", "Normal"], 
                                           help="Statistical distribution for risk modeling")
            baseline_uncertainty = st.slider("Baseline Productivity Uncertainty (%)", 5, 20, 10,
                                            help="Variation in baseline productivity measurements")
    
    # Custom uncertainty parameters
    uncertainty_params = {
        'investment': {'distribution': 'normal', 'std_pct': investment_std / 100},
        'productivity_baseline': {'distribution': 'normal', 'std_pct': baseline_uncertainty / 100},
        'automation_level': {'distribution': 'normal', 'std_pct': automation_std / 100},
        'accuracy_improvement': {'distribution': 'normal', 'std_pct': accuracy_std / 100},
        'speed_improvement': {'distribution': 'normal', 'std_pct': speed_std / 100},
        'market_conditions': {'distribution': 'normal', 'std_pct': market_volatility / 100},
    }
    
    if risk_distribution == "Beta":
        uncertainty_params.update({
            'technical_risk': {'distribution': 'beta', 'alpha': 2, 'beta': 5},
            'adoption_risk': {'distribution': 'beta', 'alpha': 2, 'beta': 4},
            'integration_risk': {'distribution': 'beta', 'alpha': 3, 'beta': 4},
        })
    else:
        uncertainty_params.update({
            'technical_risk': {'distribution': 'normal', 'std_pct': 0.3},
            'adoption_risk': {'distribution': 'normal', 'std_pct': 0.3},
            'integration_risk': {'distribution': 'normal', 'std_pct': 0.25},
        })
    
    # Run simulation button
    if st.button("🚀 Run Monte Carlo Simulation", type="primary"):
        with st.spinner(f"Running {n_simulations:,} simulations..."):
            try:
                # Initialize Monte Carlo simulator
                simulator = MonteCarloSimulator(n_simulations=n_simulations)
                
                # Get baseline data and AI initiative
                baseline_data = st.session_state.baseline_data[selected_function]
                ai_initiative = st.session_state.ai_initiatives[selected_function]
                
                # Run simulation
                simulation_results = simulator.run_simulation(
                    baseline_data, ai_initiative, uncertainty_params
                )
                
                # Store results in session state
                st.session_state[f'monte_carlo_{selected_function}'] = simulation_results
                
                st.success(f"✅ Simulation completed! {n_simulations:,} scenarios analyzed.")
                
            except Exception as e:
                st.error(f"Simulation failed: {str(e)}")
                return
    
    # Display results if available
    if f'monte_carlo_{selected_function}' in st.session_state:
        simulation_data = st.session_state[f'monte_carlo_{selected_function}']
        
        st.markdown("---")
        st.subheader("📊 Simulation Results")
        
        # Summary statistics
        summary_stats = simulation_data['summary_statistics']
        
        # Enhanced key metrics overview with styled cards
        col1, col2, col3, col4 = st.columns(4)
        
        roi_stats = summary_stats['roi']
        value_stats = summary_stats['value_generated']
        productivity_stats = summary_stats['productivity_gain']
        payback_stats = summary_stats['payback_period']
        
        with col1:
            from utils.chart_styling import create_styled_metric_card
            st.markdown(create_styled_metric_card(
                f"{roi_stats['mean']:.1f}%", 
                "Expected ROI",
                "ocean"
            ), unsafe_allow_html=True)
            st.caption(f"Range: {roi_stats['min']:.1f}% to {roi_stats['max']:.1f}%")
        
        with col2:
            st.markdown(create_styled_metric_card(
                f"${value_stats['mean']:,.0f}", 
                "Expected Value",
                "mint"
            ), unsafe_allow_html=True)
            st.caption(f"Range: ${value_stats['min']:,.0f} to ${value_stats['max']:,.0f}")
        
        with col3:
            st.markdown(create_styled_metric_card(
                f"{productivity_stats['mean']:.1f}%", 
                "Productivity Gain",
                "purple"
            ), unsafe_allow_html=True)
            st.caption(f"Std Dev: {productivity_stats['std']:.1f}%")
        
        with col4:
            st.markdown(create_styled_metric_card(
                f"{payback_stats['mean']:.1f}mo", 
                "Expected Payback",
                "coral"
            ), unsafe_allow_html=True)
            st.caption(f"Std Dev: {payback_stats['std']:.1f} months")
        
        # Risk metrics
        st.markdown("---")
        st.subheader("⚠️ Risk Analysis")
        
        risk_metrics = simulation_data['risk_metrics']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Success Probabilities**")
            st.metric("Probability of Positive ROI", f"{risk_metrics['probability_positive_roi']:.1%}")
            st.metric("Probability ROI > 15%", f"{risk_metrics['probability_roi_above_15']:.1%}")
            st.metric("Probability ROI > 25%", f"{risk_metrics['probability_roi_above_25']:.1%}")
        
        with col2:
            st.markdown("**Payback Risk**")
            st.metric("Probability Payback < 24 months", f"{risk_metrics['probability_payback_under_24_months']:.1%}")
            st.metric("Probability Payback < 36 months", f"{risk_metrics['probability_payback_under_36_months']:.1%}")
        
        with col3:
            st.markdown("**Value at Risk**")
            st.metric("5% Value at Risk", f"${risk_metrics['value_at_risk_5']:,.0f}",
                     help="Value exceeded in 95% of scenarios")
            st.metric("10% Value at Risk", f"${risk_metrics['value_at_risk_10']:,.0f}",
                     help="Value exceeded in 90% of scenarios")
            prob_loss = risk_metrics['probability_of_loss']
            loss_color = "red" if prob_loss > 0.1 else "orange" if prob_loss > 0.05 else "green"
            st.metric("Probability of Loss", f"{prob_loss:.1%}")
            st.markdown(f":{loss_color}[Loss probability: {prob_loss:.1%}]")
        
        # Enhanced visualizations
        st.markdown("---")
        st.subheader("📈 Distribution Analysis")
        
        # Create distribution charts
        from utils.chart_styling import EnhancedCharts, create_styled_card
        chart_creator = EnhancedCharts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ROI distribution chart
            roi_data = simulation_data.get('raw_results', {}).get('roi', [])
            if roi_data:
                roi_fig = chart_creator.create_distribution_chart(
                    roi_data, "ROI Distribution", "blue"
                )
                st.plotly_chart(roi_fig, use_container_width=True)
        
        with col2:
            # Value generation distribution chart
            value_data = simulation_data.get('raw_results', {}).get('value_generated', [])
            if value_data:
                value_fig = chart_creator.create_distribution_chart(
                    value_data, "Value Generation Distribution", "green"
                )
                st.plotly_chart(value_fig, use_container_width=True)
        
        # Risk analysis visualization
        st.markdown("---")
        st.subheader("⚠️ Risk Assessment")
        
        risk_metrics = simulation_data['risk_metrics']
        risk_data = {
            'Probability of Loss': risk_metrics.get('probability_of_loss', 0),
            'Technical Risk': 0.2,  # Example - would come from simulation
            'Market Risk': 0.15,   # Example - would come from simulation
            'Implementation Risk': 0.1  # Example - would come from simulation
        }
        
        risk_fig = chart_creator.create_risk_heatmap(risk_data)
        st.plotly_chart(risk_fig, use_container_width=True)
        
        # Confidence intervals in styled cards
        st.markdown("---")
        st.subheader("📊 Confidence Intervals")
        
        confidence_intervals = simulation_data['confidence_intervals']
        
        col1, col2 = st.columns(2)
        
        with col1:
            roi_ci = confidence_intervals['roi']
            roi_content = ""
            for conf_level, interval in roi_ci.items():
                roi_content += f"<p><strong>{conf_level}:</strong> {interval['lower']:.1f}% to {interval['upper']:.1f}%</p>"
            
            st.markdown(create_styled_card(roi_content, "ROI Confidence Intervals"), unsafe_allow_html=True)
        
        with col2:
            value_ci = confidence_intervals['value_generated']
            value_content = ""
            for conf_level, interval in value_ci.items():
                value_content += f"<p><strong>{conf_level}:</strong> ${interval['lower']:,.0f} to ${interval['upper']:,.0f}</p>"
            
            st.markdown(create_styled_card(value_content, "Value Generation Confidence Intervals"), unsafe_allow_html=True)

def show_strategic_planning():
    st.header("🎯 Strategic AI Planning")
    st.markdown("**Strategic scenario analysis based on critical business questions**")
    
    if len(st.session_state.baseline_data) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    # Strategic planning question framework
    st.markdown("---")
    st.subheader("📋 Strategic Planning Framework")
    
    questions_framework = {
        "Business Value": "Where will AI create real business value in the next 12 months?",
        "Integration Depth": "Are we building AI into the business — or just layering it on top?", 
        "Talent Readiness": "Do we have the talent to run an AI-augmented business?",
        "Risk Governance": "What risks are we not seeing — and what's our model for responsible AI use?",
        "Competitive Advantage": "What are we doing now that will give us an AI advantage three years from now?"
    }
    
    with st.expander("🧭 Strategic Questions Framework", expanded=True):
        for category, question in questions_framework.items():
            st.markdown(f"**{category}:** {question}")
    
    # Function selection for strategic analysis
    configured_functions = list(st.session_state.baseline_data.keys())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_function = st.selectbox("Select Function for Strategic Analysis", configured_functions)
    
    with col2:
        analysis_scope = st.selectbox("Analysis Scope", 
                                    ["Single Category", "Comprehensive Analysis"], index=1)
    
    if selected_function not in st.session_state.baseline_data:
        st.error("Missing baseline data for the selected function.")
        return
    
    baseline_data = st.session_state.baseline_data[selected_function]
    
    # Category selection for single category analysis
    if analysis_scope == "Single Category":
        st.markdown("---")
        selected_category = st.selectbox("Select Strategic Category", 
                                       list(questions_framework.keys()))
        
        # Category-specific configuration
        st.subheader(f"📊 {selected_category} Analysis")
        st.markdown(f"**Question:** {questions_framework[selected_category]}")
        
        categories_to_analyze = [selected_category.lower().replace(" ", "_")]
    else:
        categories_to_analyze = ["business_value", "integration_depth", "talent_readiness", 
                               "risk_governance", "competitive_advantage"]
    
    # Run strategic analysis
    if st.button("🚀 Run Strategic Analysis", type="primary"):
        with st.spinner("Analyzing strategic scenarios..."):
            try:
                planner = StrategicScenarioPlanner()
                
                # Run comprehensive scenario analysis
                strategic_results = planner.run_comprehensive_scenario_analysis(
                    baseline_data, categories_to_analyze
                )
                
                # Store results
                st.session_state[f'strategic_analysis_{selected_function}'] = strategic_results
                
                st.success("✅ Strategic analysis completed!")
                
            except Exception as e:
                st.error(f"Strategic analysis failed: {str(e)}")
                return
    
    # Display results if available
    if f'strategic_analysis_{selected_function}' in st.session_state:
        strategic_data = st.session_state[f'strategic_analysis_{selected_function}']
        
        st.markdown("---")
        st.subheader("📊 Strategic Analysis Results")
        
        # Strategic recommendations overview
        recommendations = strategic_data.get('strategic_recommendations', {})
        
        if recommendations:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Investment Priorities")
                for rec in recommendations.get('investment_priorities', []):
                    st.markdown(f"• {rec}")
                
                st.markdown("#### ⚠️ Risk Mitigation")
                for rec in recommendations.get('risk_mitigation', []):
                    st.markdown(f"• {rec}")
            
            with col2:
                st.markdown("#### 📅 Short-term Actions")
                for rec in recommendations.get('short_term', []):
                    st.markdown(f"• {rec}")
                
                st.markdown("#### 🔮 Long-term Strategy")
                for rec in recommendations.get('long_term', []):
                    st.markdown(f"• {rec}")
        
        # Detailed scenario analysis by category
        scenarios = strategic_data.get('scenarios', {})
        analysis_results = strategic_data.get('analysis_results', {})
        
        for category, category_scenarios in scenarios.items():
            st.markdown("---")
            category_title = category.replace("_", " ").title()
            st.subheader(f"📈 {category_title} Scenarios")
            
            # Question context
            question_key = category.replace("_", " ").title()
            if question_key in questions_framework:
                st.markdown(f"**Strategic Question:** {questions_framework[question_key]}")
            
            # Scenario comparison results
            if category in analysis_results:
                results = analysis_results[category]
                
                if 'comparative_analysis' in results and 'summary_table' in results['comparative_analysis']:
                    summary_table = results['comparative_analysis']['summary_table']
                    
                    # Create comparison table
                    comparison_data = []
                    for scenario_name, metrics in summary_table.items():
                        comparison_data.append({
                            'Scenario': scenario_name,
                            'Expected ROI (%)': f"{metrics['expected_roi']:.1f}%",
                            'ROI Risk (σ)': f"{metrics['roi_std']:.1f}%",
                            'Expected Value': f"${metrics['expected_value']:,.0f}",
                            'Success Probability': f"{metrics['probability_success']:.1%}"
                        })
                    
                    df = pd.DataFrame(comparison_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Risk comparison
                    if 'risk_comparison' in results['comparative_analysis']:
                        risk_data = results['comparative_analysis']['risk_comparison']
                        
                        st.markdown("#### ⚠️ Risk Analysis")
                        col1, col2, col3 = st.columns(3)
                        
                        for i, (scenario_name, risk_metrics) in enumerate(risk_data.items()):
                            with [col1, col2, col3][i % 3]:
                                st.markdown(f"**{scenario_name}**")
                                st.metric("Success Probability", f"{risk_metrics['probability_positive_roi']:.1%}")
                                st.metric("5% Value at Risk", f"${risk_metrics['value_at_risk_5']:,.0f}")
            
            # Scenario details
            with st.expander(f"📋 {category_title} Scenario Details"):
                for scenario_name, scenario_config in category_scenarios.items():
                    st.markdown(f"**{scenario_name}**")
                    st.markdown(f"*{scenario_config['description']}*")
                    
                    ai_init = scenario_config['ai_initiative']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"• AI Type: {ai_init['ai_type']}")
                        st.write(f"• Investment: ${ai_init['investment']:,.0f}")
                        st.write(f"• Timeline: {ai_init['timeline']}")
                    
                    with col2:
                        st.write(f"• Automation Level: {ai_init['automation_level']}%")
                        st.write(f"• Workforce Reduction: {ai_init['workforce_reduction']}%")
                        st.write(f"• Upskilling Required: {ai_init['upskilling_required']}%")
                    
                    with col3:
                        st.write(f"• Technical Risk: {ai_init.get('technical_risk', 0):.1%}")
                        st.write(f"• Adoption Risk: {ai_init.get('adoption_risk', 0):.1%}")
                        st.write(f"• Integration Risk: {ai_init.get('integration_risk', 0):.1%}")
                    
                    st.markdown("---")
        
        # Strategic insights summary
        st.markdown("---")
        st.subheader("💡 Strategic Insights Summary")
        
        # Cross-category analysis
        insights = []
        
        # Investment efficiency analysis
        all_summaries = []
        for category_results in analysis_results.values():
            if 'comparative_analysis' in category_results and 'summary_table' in category_results['comparative_analysis']:
                all_summaries.extend(category_results['comparative_analysis']['summary_table'].values())
        
        if all_summaries:
            avg_roi = np.mean([s['expected_roi'] for s in all_summaries])
            high_roi_scenarios = [s for s in all_summaries if s['expected_roi'] > avg_roi * 1.2]
            
            insights.append(f"Average expected ROI across all scenarios: {avg_roi:.1f}%")
            insights.append(f"High-performing scenarios ({len(high_roi_scenarios)} identified) exceed {avg_roi * 1.2:.1f}% ROI")
            
            # Risk vs Return analysis
            low_risk_high_return = [
                s for s in all_summaries 
                if s['expected_roi'] > avg_roi and s['probability_success'] > 0.8
            ]
            
            if low_risk_high_return:
                insights.append(f"Low-risk, high-return opportunities: {len(low_risk_high_return)} scenarios identified")
            
            # Investment range analysis
            investments = [s['expected_value'] for s in all_summaries]
            insights.append(f"Investment range: ${min(investments):,.0f} - ${max(investments):,.0f}")
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        # Export strategic analysis
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export Strategic Analysis"):
                # Create comprehensive report
                export_data = {
                    'function': selected_function,
                    'analysis_scope': analysis_scope,
                    'strategic_recommendations': recommendations,
                    'scenario_summaries': {}
                }
                
                # Add scenario summaries
                for category, results in analysis_results.items():
                    if 'comparative_analysis' in results:
                        export_data['scenario_summaries'][category] = results['comparative_analysis']
                
                # Convert to downloadable format
                import json
                report_json = json.dumps(export_data, indent=2, default=str)
                
                st.download_button(
                    label="Download Strategic Analysis Report",
                    data=report_json,
                    file_name=f"strategic_analysis_{selected_function}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Run New Analysis"):
                if f'strategic_analysis_{selected_function}' in st.session_state:
                    del st.session_state[f'strategic_analysis_{selected_function}']
                st.rerun()

def show_scenario_comparison():
    st.header("⚖️ Scenario Comparison")
    
    if len(st.session_state.predictions) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    configured_functions = list(st.session_state.predictions.keys())
    
    # Scenario selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Baseline Scenario (Current State)")
        baseline_functions = st.multiselect("Select Functions for Baseline", 
                                          configured_functions, 
                                          default=configured_functions)
    
    with col2:
        st.subheader("🤖 AI-Enabled Scenario")
        ai_functions = st.multiselect("Select Functions with AI Implementation", 
                                    configured_functions, 
                                    default=configured_functions)
    
    if st.button("🔄 Compare Scenarios", type="primary"):
        # Calculate baseline totals
        baseline_totals = calculate_scenario_totals(baseline_functions, use_ai=False)
        ai_totals = calculate_scenario_totals(ai_functions, use_ai=True)
        
        st.markdown("---")
        st.subheader("📈 Comparison Results")
        
        # Key metrics comparison
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            revenue_diff = ai_totals['revenue'] - baseline_totals['revenue']
            st.metric("Revenue Impact", f"${revenue_diff:,.0f}", 
                     delta=f"{(revenue_diff/baseline_totals['revenue']*100):.1f}%")
        
        with col2:
            cost_diff = ai_totals['costs'] - baseline_totals['costs']
            st.metric("Cost Impact", f"${cost_diff:,.0f}", 
                     delta=f"{(cost_diff/baseline_totals['costs']*100):.1f}%")
        
        with col3:
            headcount_diff = ai_totals['headcount'] - baseline_totals['headcount']
            st.metric("Headcount Impact", f"{headcount_diff:,.0f}", 
                     delta=f"{(headcount_diff/baseline_totals['headcount']*100):.1f}%")
        
        with col4:
            productivity_diff = ai_totals['productivity'] - baseline_totals['productivity']
            st.metric("Productivity Impact", f"{productivity_diff:.1f}%", 
                     delta=f"{productivity_diff:.1f}%")
        
        # Detailed comparison chart
        visualizer = DashboardVisualizer()
        fig = visualizer.create_scenario_comparison(baseline_totals, ai_totals)
        st.plotly_chart(fig, use_container_width=True)
        
        # Function-level breakdown
        st.subheader("🏢 Function-Level Breakdown")
        
        comparison_data = []
        for func in configured_functions:
            if (func in st.session_state.predictions and 
                func in st.session_state.ai_initiatives and 
                func in st.session_state.baseline_data):
                pred = st.session_state.predictions[func]
                baseline = st.session_state.baseline_data[func]
                ai_config = st.session_state.ai_initiatives[func]
                
                comparison_data.append({
                    'Function': func,
                    'Current Revenue': baseline['revenue'],
                    'AI Revenue': baseline['revenue'] + pred['value_generated'],
                    'Current Costs': baseline['costs'],
                    'AI Costs': baseline['costs'] + ai_config['investment'],
                    'ROI': pred['roi'],
                    'Productivity Gain': pred['productivity_gain']
                })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)

def show_temporal_analysis():
    st.header("📅 Temporal Analysis")
    
    if len(st.session_state.predictions) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    # Time horizon selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_horizon = st.selectbox("Analysis Time Horizon", 
                                  ["1 year", "2 years", "3 years", "5 years"])
    
    with col2:
        analysis_granularity = st.selectbox("Analysis Granularity", 
                                          ["Monthly", "Quarterly", "Yearly"])
    
    with col3:
        confidence_level = st.selectbox("Confidence Level", 
                                      ["90%", "95%", "99%"])
    
    # Function selection for temporal analysis
    selected_functions = st.multiselect("Select Functions for Temporal Analysis", 
                                      list(st.session_state.predictions.keys()),
                                      default=list(st.session_state.predictions.keys()))
    
    if st.button("📊 Generate Temporal Projections", type="primary"):
        engine = PredictiveEngine()
        
        # Generate time-series projections
        years = int(time_horizon.split()[0])
        months = years * 12
        
        # Create temporal projections for each selected function
        temporal_data = {}
        
        for func in selected_functions:
            if (func in st.session_state.baseline_data and 
                func in st.session_state.ai_initiatives and 
                func in st.session_state.predictions):
                baseline = st.session_state.baseline_data[func]
                ai_config = st.session_state.ai_initiatives[func]
                predictions = st.session_state.predictions[func]
                
                temporal_projection = engine.generate_temporal_projection(
                    baseline, ai_config, predictions, months
                )
                temporal_data[func] = temporal_projection
        
        # Visualize temporal trends
        st.markdown("---")
        st.subheader("📈 Temporal Projections")
        
        # Revenue and value generation over time
        visualizer = DashboardVisualizer()
        
        # Combined temporal view
        fig = visualizer.create_temporal_analysis(temporal_data, years)
        st.plotly_chart(fig, use_container_width=True)
        
        # Individual function temporal analysis
        st.subheader("🏢 Function-Specific Temporal Analysis")
        
        for func in selected_functions:
            if func in temporal_data:
                with st.expander(f"📊 {func} - Detailed Temporal View"):
                    fig_individual = visualizer.create_individual_temporal_analysis(
                        temporal_data[func], func
                    )
                    st.plotly_chart(fig_individual, use_container_width=True)
                    
                    # Key temporal insights
                    data = temporal_data[func]
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        break_even_month = next((i for i, val in enumerate(data['cumulative_roi']) if val > 0), None)
                        if break_even_month:
                            st.metric("Break-even Point", f"Month {break_even_month + 1}")
                        else:
                            st.metric("Break-even Point", "Beyond horizon")
                    
                    with col2:
                        max_roi = max(data['monthly_roi'])
                        st.metric("Peak Monthly ROI", f"{max_roi:.1f}%")
                    
                    with col3:
                        final_value = data['cumulative_value'][-1]
                        st.metric("Total Value at End", f"${final_value:,.0f}")

def show_executive_summary():
    st.header("📋 Executive Summary")
    
    if len(st.session_state.predictions) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    # Generate executive summary with aggregated data
    report_generator = ReportGenerator()
    
    # Aggregate AI initiatives from category structure
    aggregated_initiatives = {}
    for function_name in st.session_state.baseline_data.keys():
        if f'categories_{function_name}' in st.session_state:
            categories = st.session_state[f'categories_{function_name}']
            
            # Aggregate initiatives for this function
            total_investment = 0
            total_automation = 0
            total_workforce_reduction = 0
            initiative_count = 0
            
            for category_data in categories.values():
                initiatives = category_data.get('ai_initiatives', {})
                for init_data in initiatives.values():
                    total_investment += init_data.get('investment', 0)
                    total_automation += init_data.get('automation_level', 0)
                    total_workforce_reduction += init_data.get('workforce_reduction', 0)
                    initiative_count += 1
            
            if initiative_count > 0:
                aggregated_initiatives[function_name] = {
                    'investment': total_investment,
                    'automation_level': total_automation / initiative_count,
                    'workforce_reduction': total_workforce_reduction / initiative_count,
                    'initiative_count': initiative_count
                }
    
    summary_data = report_generator.generate_executive_summary(
        st.session_state.baseline_data,
        aggregated_initiatives,
        st.session_state.predictions
    )
    
    # Executive KPIs
    st.subheader("🎯 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Investment", f"${summary_data['total_investment']:,.0f}")
    with col2:
        st.metric("Expected ROI", f"{summary_data['average_roi']:.1f}%")
    with col3:
        st.metric("Payback Period", f"{summary_data['average_payback']:.1f} months")
    with col4:
        st.metric("Value Generated", f"${summary_data['total_value']:,.0f}")
    with col5:
        st.metric("Productivity Gain", f"{summary_data['average_productivity']:.1f}%")
    
    # Strategic overview
    st.markdown("---")
    st.subheader("🎯 Strategic Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Portfolio overview chart
        visualizer = DashboardVisualizer()
        fig = visualizer.create_portfolio_overview(st.session_state.predictions)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Implementation Priority Matrix**")
        
        priority_data = []
        for func, pred in st.session_state.predictions.items():
            if func in aggregated_initiatives:
                initiative = aggregated_initiatives[func]
                
                # Calculate priority score based on ROI and risk (use default risk values for aggregated data)
                roi_score = min(pred['roi'] / 100, 1.0) * 50
                # Use moderate risk assumption for aggregated initiatives
                risk_score = (100 - 30) / 100 * 50  # Assume 30% average risk
                priority_score = roi_score + risk_score
                
                priority_data.append({
                    'Function': func,
                    'Priority Score': priority_score,
                    'ROI': pred['roi'],
                    'Risk Level': 30  # Use default risk level for aggregated data
                })
        
        if priority_data:
            priority_df = pd.DataFrame(priority_data).sort_values('Priority Score', ascending=False)
            
            for _, row in priority_df.iterrows():
                if row['Priority Score'] > 70:
                    st.success(f"🟢 {row['Function']} (Score: {row['Priority Score']:.1f})")
                elif row['Priority Score'] > 50:
                    st.warning(f"🟡 {row['Function']} (Score: {row['Priority Score']:.1f})")
                else:
                    st.error(f"🔴 {row['Function']} (Score: {row['Priority Score']:.1f})")
        else:
            st.info("Configure AI initiatives in departments to see priority analysis.")
    
    # Risk assessment
    st.markdown("---")
    st.subheader("⚠️ Risk Assessment")
    
    risk_summary = report_generator.generate_risk_assessment(st.session_state.ai_initiatives)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**High Risk Functions**")
        for func in risk_summary['high_risk']:
            st.error(f"🔴 {func}")
    
    with col2:
        st.markdown("**Medium Risk Functions**")
        for func in risk_summary['medium_risk']:
            st.warning(f"🟡 {func}")
    
    with col3:
        st.markdown("**Low Risk Functions**")
        for func in risk_summary['low_risk']:
            st.success(f"🟢 {func}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Strategic Recommendations")
    
    recommendations = report_generator.generate_recommendations(
        st.session_state.predictions, aggregated_initiatives
    )
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}. {rec['title']}**")
        st.markdown(f"   {rec['description']}")
        st.markdown("")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Data to CSV"):
            export_data = report_generator.prepare_export_data(
                st.session_state.baseline_data,
                st.session_state.ai_initiatives,
                st.session_state.predictions
            )
            st.download_button(
                label="💾 Download CSV",
                data=export_data.to_csv(index=False),
                file_name=f"ai_impact_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Generate Report Summary"):
            report_text = report_generator.generate_text_report(summary_data, recommendations)
            st.download_button(
                label="📄 Download Report",
                data=report_text,
                file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🎯 Export for Presentation"):
            st.info("💡 Use the visualizations above for your presentation. Screenshots can be taken directly from the dashboard.")

def calculate_scenario_totals(functions, use_ai=False):
    """Calculate total metrics for a scenario"""
    totals = {
        'revenue': 0,
        'costs': 0,
        'headcount': 0,
        'productivity': 0
    }
    
    function_count = len(functions)
    if function_count == 0:
        return totals
    
    for func in functions:
        if func in st.session_state.baseline_data:
            baseline = st.session_state.baseline_data[func]
            
            if use_ai and func in st.session_state.predictions and func in st.session_state.ai_initiatives:
                pred = st.session_state.predictions[func]
                ai_config = st.session_state.ai_initiatives[func]
                
                totals['revenue'] += baseline['revenue'] + pred['value_generated']
                totals['costs'] += baseline['costs'] + ai_config['investment']
                totals['headcount'] += int(baseline['headcount'] * (1 - ai_config['workforce_reduction']/100))
                totals['productivity'] += baseline['productivity'] + pred['productivity_gain']
            else:
                totals['revenue'] += baseline['revenue']
                totals['costs'] += baseline['costs']
                totals['headcount'] += int(baseline['headcount'])
                totals['productivity'] += baseline['productivity']
    
    # Average productivity
    totals['productivity'] = totals['productivity'] / function_count
    
    return totals

def show_benchmarking_optimization():
    st.header("📊 Benchmarking & Optimization")
    
    if len(st.session_state.predictions) < 1:
        st.warning("⚠️ Please configure at least one function in Function Analysis first.")
        return
    
    # Initialize benchmarking tools
    benchmark_tool = IndustryBenchmarking()
    sensitivity_tool = SensitivityAnalysis()
    optimization_tool = ScenarioOptimization()
    
    # Tabs for different analysis types
    tab1, tab2, tab3 = st.tabs(["🏭 Industry Benchmarking", "📈 Sensitivity Analysis", "🎯 Scenario Optimization"])
    
    with tab1:
        st.subheader("Industry Benchmark Comparison")
        
        # Industry selection
        industry = st.selectbox(
            "Select your industry for benchmarking:",
            ["Technology", "Financial Services", "Manufacturing", "Healthcare", "Retail", "General"]
        )
        
        if st.button("🔍 Run Benchmark Analysis"):
            comparison = benchmark_tool.get_industry_comparison(industry, st.session_state.predictions)
            
            # Display comparison metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                perf = comparison['performance']['roi_vs_benchmark']
                st.metric("ROI vs Industry", f"{perf:+.1f}%", delta=f"vs {industry} average")
            
            with col2:
                perf = comparison['performance']['payback_vs_benchmark']
                st.metric("Payback vs Industry", f"{perf:+.1f}%", delta="better" if perf > 0 else "slower")
            
            with col3:
                perf = comparison['performance']['productivity_vs_benchmark']
                st.metric("Productivity vs Industry", f"{perf:+.1f}%", delta=f"vs {industry} average")
            
            # Benchmark comparison chart
            benchmark_fig = benchmark_tool.create_benchmark_comparison_chart(comparison)
            st.plotly_chart(benchmark_fig, use_container_width=True)
    
    with tab2:
        st.subheader("Sensitivity Analysis")
        
        # Function selection for sensitivity analysis
        selected_function = st.selectbox(
            "Select function for sensitivity analysis:",
            list(st.session_state.predictions.keys())
        )
        
        # Factor selection
        factor = st.selectbox(
            "Select factor to analyze:",
            ["investment", "automation_level", "accuracy_improvement", "speed_improvement", "technical_risk", "adoption_risk"]
        )
        
        if st.button("📊 Run Sensitivity Analysis"):
            baseline_data = st.session_state.baseline_data[selected_function]
            ai_initiative = st.session_state.ai_initiatives[selected_function]
            predictions = st.session_state.predictions[selected_function]
            
            sensitivity_results = sensitivity_tool.run_sensitivity_analysis(
                baseline_data, ai_initiative, predictions, factor
            )
            
            # Display sensitivity chart
            sensitivity_fig = sensitivity_tool.create_sensitivity_chart(sensitivity_results)
            st.plotly_chart(sensitivity_fig, use_container_width=True)
    
    with tab3:
        st.subheader("Scenario Optimization")
        
        # Function selection for optimization
        opt_function = st.selectbox(
            "Select function to optimize:",
            list(st.session_state.predictions.keys()),
            key="opt_function"
        )
        
        # Optimization target
        target_metric = st.selectbox(
            "Optimization target:",
            ["roi", "value_generated", "payback_period", "risk_adjusted_roi"]
        )
        
        if st.button("🎯 Optimize Scenario"):
            baseline_data = st.session_state.baseline_data[opt_function]
            ai_initiative = st.session_state.ai_initiatives[opt_function]
            
            optimization_results = optimization_tool.optimize_scenario(
                baseline_data, ai_initiative, target_metric
            )
            
            if optimization_results['best_result']:
                st.subheader("🏆 Optimization Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Current Configuration**")
                    current_pred = st.session_state.predictions[opt_function]
                    st.write(f"ROI: {current_pred['roi']:.1f}%")
                    st.write(f"Value: ${current_pred['value_generated']:,.0f}")
                
                with col2:
                    st.markdown("**Optimized Configuration**")
                    best_result = optimization_results['best_result']
                    st.write(f"ROI: {best_result['roi']:.1f}%")
                    st.write(f"Value: ${best_result['value_generated']:,.0f}")

if __name__ == "__main__":
    main()
