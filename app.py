import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import utility modules
from utils.data_models import EnterpriseFunction, AIInitiative
from utils.predictive_engine import PredictiveEngine
from utils.visualization import DashboardVisualizer
from utils.report_generator import ReportGenerator
from utils.database import DatabaseManager
from utils.benchmarking import IndustryBenchmarking, SensitivityAnalysis, ScenarioOptimization
from utils.session_manager import SessionManager

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

# Load data from database on first run
if db and not st.session_state.data_loaded:
    data = db.load_all_data()
    st.session_state.baseline_data = data['baseline_data']
    st.session_state.ai_initiatives = data['ai_initiatives']
    st.session_state.predictions = data['predictions']
    st.session_state.data_loaded = True

def main():
    st.title("🎯 AI Impact Predictive Dashboard")
    st.markdown("**Executive Dashboard for Predictive Modeling of AI Implementation Impact**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis View",
        ["Overview", "Function Analysis", "Scenario Comparison", "Temporal Analysis", "Benchmarking & Optimization", "Executive Summary"]
    )
    
    # Session Management Sidebar
    if session_manager:
        st.sidebar.markdown("---")
        st.sidebar.subheader("💾 Session Management")
        
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
        show_function_analysis()
    elif page == "Scenario Comparison":
        show_scenario_comparison()
    elif page == "Temporal Analysis":
        show_temporal_analysis()
    elif page == "Benchmarking & Optimization":
        show_benchmarking_optimization()
    elif page == "Executive Summary":
        show_executive_summary()

def show_overview():
    st.header("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Functions", len(st.session_state.ai_initiatives))
    with col2:
        total_investment = sum(init.get('investment', 0) for init in st.session_state.ai_initiatives.values())
        st.metric("Total AI Investment", f"${total_investment:,.0f}")
    with col3:
        if st.session_state.predictions:
            avg_roi = np.mean([p.get('roi', 0) for p in st.session_state.predictions.values()])
            st.metric("Average Projected ROI", f"{avg_roi:.1f}%")
        else:
            st.metric("Average Projected ROI", "N/A")
    with col4:
        if st.session_state.predictions:
            total_productivity = sum(p.get('productivity_gain', 0) for p in st.session_state.predictions.values())
            st.metric("Total Productivity Gain", f"{total_productivity:.1f}%")
        else:
            st.metric("Total Productivity Gain", "N/A")
    
    st.markdown("---")
    
    # Quick setup section
    st.subheader("🚀 Quick Setup")
    st.markdown("Get started by configuring AI initiatives for your enterprise functions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Enterprise Functions Available:**")
        functions = ["HR & Talent Management", "Finance & Accounting", "Operations & Supply Chain", 
                    "Sales & Marketing", "IT & Technology", "Customer Service", "Legal & Compliance", "R&D",
                    "Manufacturing & Production", "Quality Assurance", "Business Development", "Strategy & Planning",
                    "Risk Management", "Procurement", "Facilities Management", "Data & Analytics"]
        for func in functions:
            if func in st.session_state.ai_initiatives:
                st.success(f"✅ {func} - Configured")
            else:
                st.info(f"⚪ {func} - Not configured")
    
    with col2:
        st.markdown("**Next Steps:**")
        st.markdown("1. Navigate to **Function Analysis** to configure AI initiatives")
        st.markdown("2. Set baseline metrics and AI implementation parameters")
        st.markdown("3. Use **Scenario Comparison** to evaluate different approaches")
        st.markdown("4. Review **Temporal Analysis** for time-based projections")
        st.markdown("5. Generate **Executive Summary** for stakeholder presentations")

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
                                          min_value=0, value=100000, step=5000)
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
        
        # Visualization
        visualizer = DashboardVisualizer()
        fig = visualizer.create_impact_summary(predictions, selected_function)
        st.plotly_chart(fig, use_container_width=True)

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
    
    # Generate executive summary
    report_generator = ReportGenerator()
    summary_data = report_generator.generate_executive_summary(
        st.session_state.baseline_data,
        st.session_state.ai_initiatives,
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
            initiative = st.session_state.ai_initiatives[func]
            
            # Calculate priority score based on ROI and risk
            roi_score = min(pred['roi'] / 100, 1.0) * 50
            risk_score = (100 - (initiative['technical_risk'] + initiative['adoption_risk']) / 2) / 100 * 50
            priority_score = roi_score + risk_score
            
            priority_data.append({
                'Function': func,
                'Priority Score': priority_score,
                'ROI': pred['roi'],
                'Risk Level': (initiative['technical_risk'] + initiative['adoption_risk']) / 2
            })
        
        priority_df = pd.DataFrame(priority_data).sort_values('Priority Score', ascending=False)
        
        for _, row in priority_df.iterrows():
            if row['Priority Score'] > 70:
                st.success(f"🟢 {row['Function']} (Score: {row['Priority Score']:.1f})")
            elif row['Priority Score'] > 50:
                st.warning(f"🟡 {row['Function']} (Score: {row['Priority Score']:.1f})")
            else:
                st.error(f"🔴 {row['Function']} (Score: {row['Priority Score']:.1f})")
    
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
        st.session_state.predictions, st.session_state.ai_initiatives
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
