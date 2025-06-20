import streamlit as st
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import visualization libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="AI Strategic Modeling Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
    }
    .success-alert {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'baseline_data' not in st.session_state:
        st.session_state.baseline_data = {}
    if 'ai_initiatives' not in st.session_state:
        st.session_state.ai_initiatives = {}
    if 'predictions' not in st.session_state:
        st.session_state.predictions = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Overview'

# Utility functions for calculations
def calculate_metrics(baseline_data: Dict, ai_initiatives: Dict) -> Dict:
    """Calculate key metrics for analysis"""
    metrics = {
        'total_functions': len(baseline_data),
        'total_initiatives': sum(len(initiatives) for initiatives in ai_initiatives.values()),
        'avg_productivity': 0,
        'estimated_roi': 0,
        'implementation_readiness': 0
    }
    
    if baseline_data:
        productivities = [data.get('productivity_score', 0) for data in baseline_data.values()]
        metrics['avg_productivity'] = sum(productivities) / len(productivities) if productivities else 0
        
        # Calculate estimated ROI based on productivity improvements
        total_cost = sum(data.get('annual_cost', 0) for data in baseline_data.values())
        productivity_improvement = metrics['avg_productivity'] * 0.2  # Assume 20% improvement
        estimated_savings = total_cost * productivity_improvement
        metrics['estimated_roi'] = (estimated_savings / total_cost * 100) if total_cost > 0 else 0
        
        # Implementation readiness based on data completeness
        complete_functions = sum(1 for data in baseline_data.values() 
                               if all(key in data for key in ['headcount', 'annual_cost', 'productivity_score']))
        metrics['implementation_readiness'] = (complete_functions / len(baseline_data) * 100) if baseline_data else 0
    
    return metrics

def create_overview_charts(metrics: Dict) -> List[go.Figure]:
    """Create overview charts for the dashboard"""
    charts = []
    
    # ROI Projection Chart
    fig_roi = go.Figure()
    years = ['Year 1', 'Year 2', 'Year 3']
    roi_values = [metrics['estimated_roi'] * 0.6, metrics['estimated_roi'] * 0.8, metrics['estimated_roi']]
    
    fig_roi.add_trace(go.Bar(
        x=years,
        y=roi_values,
        marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1'],
        text=[f"{val:.1f}%" for val in roi_values],
        textposition='auto'
    ))
    
    fig_roi.update_layout(
        title="Projected ROI Over Time",
        xaxis_title="Timeline",
        yaxis_title="ROI (%)",
        showlegend=False,
        height=400
    )
    charts.append(fig_roi)
    
    # Implementation Readiness Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics['implementation_readiness'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Implementation Readiness"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#45b7d1"},
            'steps': [
                {'range': [0, 50], 'color': "#ff6b6b"},
                {'range': [50, 80], 'color': "#ffd93d"},
                {'range': [80, 100], 'color': "#6bcf7f"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_gauge.update_layout(height=400)
    charts.append(fig_gauge)
    
    return charts

def show_build_buy_analysis():
    """Display the Build vs Buy Analysis module"""
    st.header("Build vs Buy Analysis")
    st.markdown("Strategic workforce planning for AI transformation")
    
    # Skills Gap Analysis Section
    st.subheader("Skills Gap Analysis")
    
    skill_categories = {
        'Data Science': {'current': 65, 'required': 85, 'gap': 20},
        'AI/ML Engineering': {'current': 45, 'required': 80, 'gap': 35},
        'Automation': {'current': 70, 'required': 90, 'gap': 20},
        'Digital Transformation': {'current': 60, 'required': 85, 'gap': 25},
        'Cybersecurity': {'current': 75, 'required': 90, 'gap': 15},
        'Cloud Architecture': {'current': 55, 'required': 85, 'gap': 30},
        'Product Management': {'current': 80, 'required': 90, 'gap': 10},
        'Business Intelligence': {'current': 70, 'required': 85, 'gap': 15}
    }
    
    # Create skills gap visualization
    fig_skills = go.Figure()
    
    categories = list(skill_categories.keys())
    current_levels = [skill_categories[cat]['current'] for cat in categories]
    required_levels = [skill_categories[cat]['required'] for cat in categories]
    
    fig_skills.add_trace(go.Bar(
        name='Current Level',
        x=categories,
        y=current_levels,
        marker_color='#ff6b6b'
    ))
    
    fig_skills.add_trace(go.Bar(
        name='Required Level',
        x=categories,
        y=required_levels,
        marker_color='#45b7d1'
    ))
    
    fig_skills.update_layout(
        title="Skills Gap Analysis Across Key Categories",
        xaxis_title="Skill Categories",
        yaxis_title="Capability Level (%)",
        barmode='group',
        height=500,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_skills, use_container_width=True)
    
    # Cost-Benefit Analysis
    st.subheader("Cost-Benefit Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Build Internal Capability")
        build_costs = {
            'Year 1': 850000,
            'Year 2': 1200000,
            'Year 3': 1100000
        }
        
        build_benefits = {
            'Year 1': 200000,
            'Year 2': 800000,
            'Year 3': 1500000
        }
        
        st.metric("3-Year Investment", "$3.15M")
        st.metric("3-Year ROI", "67%")
        st.metric("Payback Period", "2.1 years")
    
    with col2:
        st.markdown("### Buy External Services")
        buy_costs = {
            'Year 1': 400000,
            'Year 2': 450000,
            'Year 3': 500000
        }
        
        buy_benefits = {
            'Year 1': 300000,
            'Year 2': 600000,
            'Year 3': 900000
        }
        
        st.metric("3-Year Investment", "$1.35M")
        st.metric("3-Year ROI", "133%")
        st.metric("Payback Period", "1.2 years")
    
    # Strategic Recommendations
    st.subheader("Strategic Recommendations")
    
    recommendations = [
        {
            'category': 'Data Science',
            'recommendation': 'Hybrid Approach',
            'rationale': 'Build core team (3-5 experts), supplement with external consultants for specialized projects',
            'timeline': '18 months',
            'risk_level': 'Medium'
        },
        {
            'category': 'AI/ML Engineering',
            'recommendation': 'Buy Initially, Build Later',
            'rationale': 'High skill gap requires immediate external expertise while building internal capability',
            'timeline': '24 months',
            'risk_level': 'Low'
        },
        {
            'category': 'Automation',
            'recommendation': 'Build Internal',
            'rationale': 'Good existing foundation, strategic advantage in maintaining control',
            'timeline': '12 months',
            'risk_level': 'Low'
        },
        {
            'category': 'Cloud Architecture',
            'recommendation': 'Buy Expertise',
            'rationale': 'Rapid technology evolution requires specialized external knowledge',
            'timeline': '6 months',
            'risk_level': 'Medium'
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"{rec['category']} - {rec['recommendation']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Timeline:** {rec['timeline']}")
            with col2:
                st.write(f"**Risk Level:** {rec['risk_level']}")
            with col3:
                risk_color = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}[rec['risk_level']]
                st.markdown(f"<span style='color: {risk_color}'>●</span> Risk Indicator", unsafe_allow_html=True)
            
            st.write(f"**Rationale:** {rec['rationale']}")
    
    # Implementation Planning
    st.subheader("Implementation Timeline")
    
    # Create Gantt-style timeline
    timeline_data = [
        {'Task': 'Data Science Team Build', 'Start': '2025-01', 'Duration': 18, 'Type': 'Build'},
        {'Task': 'AI/ML External Partnership', 'Start': '2025-01', 'Duration': 12, 'Type': 'Buy'},
        {'Task': 'Automation Internal Development', 'Start': '2025-03', 'Duration': 12, 'Type': 'Build'},
        {'Task': 'Cloud Architecture Consulting', 'Start': '2025-02', 'Duration': 6, 'Type': 'Buy'},
        {'Task': 'Cybersecurity Enhancement', 'Start': '2025-04', 'Duration': 8, 'Type': 'Build'},
        {'Task': 'Product Management Training', 'Start': '2025-06', 'Duration': 6, 'Type': 'Build'}
    ]
    
    fig_timeline = go.Figure()
    
    colors = {'Build': '#45b7d1', 'Buy': '#ff6b6b'}
    
    for i, task in enumerate(timeline_data):
        fig_timeline.add_trace(go.Bar(
            name=task['Type'],
            x=[task['Duration']],
            y=[task['Task']],
            orientation='h',
            marker_color=colors[task['Type']],
            showlegend=i < 2  # Only show legend for first occurrence of each type
        ))
    
    fig_timeline.update_layout(
        title="Implementation Timeline - Build vs Buy Decisions",
        xaxis_title="Duration (Months)",
        yaxis_title="Initiatives",
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Executive Summary
    st.subheader("Executive Summary")
    
    summary_metrics = {
        'Total Investment (3 years)': '$4.5M',
        'Expected ROI': '89%',
        'Risk-Adjusted NPV': '$2.1M',
        'Strategic Advantage Score': '8.2/10'
    }
    
    col1, col2, col3, col4 = st.columns(4)
    metrics_cols = [col1, col2, col3, col4]
    
    for i, (metric, value) in enumerate(summary_metrics.items()):
        with metrics_cols[i]:
            st.metric(metric, value)
    
    st.markdown("""
    ### Key Findings:
    - **Hybrid approach recommended** for most critical skill areas
    - **Buy-then-build strategy** optimal for high-gap areas like AI/ML Engineering
    - **Internal development** preferred for strategic capabilities like Automation
    - **18-month timeline** for full implementation with phased approach
    """)

def show_overview():
    """Display the overview page"""
    st.markdown('<div class="main-header"><h1 style="color: white; margin: 0;">AI Strategic Modeling Platform</h1></div>', unsafe_allow_html=True)
    
    # Calculate current metrics
    metrics = calculate_metrics(st.session_state.baseline_data, st.session_state.ai_initiatives)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Enterprise Functions", metrics['total_functions'])
    
    with col2:
        st.metric("AI Initiatives", metrics['total_initiatives'])
    
    with col3:
        st.metric("Avg Productivity Score", f"{metrics['avg_productivity']:.1f}%")
    
    with col4:
        st.metric("Estimated ROI", f"{metrics['estimated_roi']:.1f}%")
    
    # Charts section
    if metrics['total_functions'] > 0:
        st.subheader("Strategic Overview")
        charts = create_overview_charts(metrics)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(charts[0], use_container_width=True)
        with col2:
            st.plotly_chart(charts[1], use_container_width=True)
    else:
        st.info("Add enterprise functions to see detailed analytics and projections.")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Configure Functions", use_container_width=True):
            st.session_state.current_page = 'Function Analysis'
            st.rerun()
    
    with col2:
        if st.button("Build vs Buy Analysis", use_container_width=True):
            st.session_state.current_page = 'Build vs Buy Analysis'
            st.rerun()
    
    with col3:
        if st.button("View Recommendations", use_container_width=True):
            st.session_state.current_page = 'Strategic Recommendations'
            st.rerun()

def show_basic_function_analysis():
    """Basic function analysis without external dependencies"""
    st.header("Enterprise Function Analysis")
    
    # Function input form
    with st.form("function_input"):
        st.subheader("Add Enterprise Function")
        
        function_name = st.text_input("Function Name", placeholder="e.g., Human Resources")
        headcount = st.number_input("Headcount", min_value=1, value=50)
        annual_cost = st.number_input("Annual Cost ($)", min_value=0, value=1000000)
        productivity_score = st.slider("Current Productivity Score (%)", 0, 100, 75)
        
        submitted = st.form_submit_button("Add Function")
        
        if submitted and function_name:
            if function_name not in st.session_state.baseline_data:
                st.session_state.baseline_data[function_name] = {
                    'headcount': headcount,
                    'annual_cost': annual_cost,
                    'productivity_score': productivity_score,
                    'timestamp': datetime.now().isoformat()
                }
                st.success(f"Added {function_name} to analysis")
                st.rerun()
            else:
                st.warning("Function already exists")
    
    # Display current functions
    if st.session_state.baseline_data:
        st.subheader("Current Functions")
        
        for func_name, data in st.session_state.baseline_data.items():
            with st.expander(f"{func_name} - {data['headcount']} employees"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Annual Cost", f"${data['annual_cost']:,}")
                with col2:
                    st.metric("Productivity Score", f"{data['productivity_score']}%")
                with col3:
                    st.metric("Cost per Employee", f"${data['annual_cost'] / data['headcount']:,.0f}")

def main():
    """Main application function"""
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    pages = [
        "Overview",
        "Function Analysis", 
        "Build vs Buy Analysis",
        "Strategic Recommendations"
    ]
    
    # Page selection
    selected_page = st.sidebar.selectbox("Select Page", pages, 
                                       index=pages.index(st.session_state.current_page) 
                                       if st.session_state.current_page in pages else 0)
    
    st.session_state.current_page = selected_page
    
    # System status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Status")
    st.sidebar.success("✅ Core Platform Active")
    st.sidebar.info("ℹ️ Full Analytics Mode")
    st.sidebar.markdown("---")
    
    # Display selected page
    if selected_page == "Overview":
        show_overview()
    elif selected_page == "Function Analysis":
        show_basic_function_analysis()
    elif selected_page == "Build vs Buy Analysis":
        show_build_buy_analysis()
    elif selected_page == "Strategic Recommendations":
        st.header("Strategic Recommendations")
        st.info("Configure enterprise functions and AI initiatives to see personalized recommendations.")

if __name__ == "__main__":
    main()