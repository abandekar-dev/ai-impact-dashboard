import streamlit as st
import json
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI Impact Predictive Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light theme styling
st.markdown("""
<style>
    .main > div {
        background-color: white;
        color: #333333;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        color: #333333;
    }
    
    .stNumberInput > div > div {
        background-color: white;
        color: #333333;
    }
    
    .stTextInput > div > div {
        background-color: white;
        color: #333333;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .info-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load data from session state or initialize defaults"""
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = {
            'functions': {},
            'scenarios': {},
            'last_updated': datetime.now().isoformat()
        }
    return st.session_state.dashboard_data

def save_data(data):
    """Save data to session state"""
    st.session_state.dashboard_data = data
    data['last_updated'] = datetime.now().isoformat()

def create_metric_card(value, label, color="blue"):
    """Create a styled metric card"""
    colors = {
        'blue': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'green': 'linear-gradient(135deg, #56CCF2 0%, #2F80ED 100%)',
        'purple': 'linear-gradient(135deg, #A8EDEA 0%, #FED6E3 100%)',
        'orange': 'linear-gradient(135deg, #FF9A8B 0%, #F093FB 100%)'
    }
    
    return f"""
    <div class="metric-card" style="background: {colors.get(color, colors['blue'])};">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{label}</p>
    </div>
    """

def show_overview():
    """Show dashboard overview"""
    st.title("🤖 AI Impact Predictive Dashboard")
    st.markdown("### Enterprise AI Initiative Analysis Platform")
    
    data = load_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("12", "Active Functions", "blue"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("8", "AI Initiatives", "green"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card("$2.4M", "Projected ROI", "purple"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card("85%", "Implementation Ready", "orange"), unsafe_allow_html=True)
    
    # Welcome section
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Welcome to Your AI Strategy Dashboard</h3>
        <p>This executive dashboard helps you analyze and predict the business impact of AI implementations across your organization. Use the navigation menu to explore different analysis modules.</p>
        
        <h4>📊 Key Features:</h4>
        <ul>
            <li><strong>Function Analysis:</strong> Evaluate AI initiatives by department</li>
            <li><strong>Predictive Modeling:</strong> ROI forecasting and scenario planning</li>
            <li><strong>Workforce Analytics:</strong> Human-AI integration planning</li>
            <li><strong>Executive Summary:</strong> High-level insights and recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_function_analysis():
    """Show function analysis page"""
    st.title("📈 Function Analysis")
    st.markdown("### Configure AI initiatives by enterprise function")
    
    # Function selector
    functions = [
        "Finance & Accounting", "Human Resources", "Operations", "Sales & Marketing",
        "Customer Service", "IT & Technology", "Legal & Compliance", "R&D",
        "Supply Chain", "Manufacturing", "Quality Assurance", "Executive Management"
    ]
    
    selected_function = st.selectbox("Select Enterprise Function:", functions)
    
    if selected_function:
        st.subheader(f"AI Initiative Configuration - {selected_function}")
        
        # Initiative form
        with st.form(f"form_{selected_function}"):
            col1, col2 = st.columns(2)
            
            with col1:
                initiative_name = st.text_input("Initiative Name", 
                    value=f"AI Enhancement for {selected_function}")
                ai_type = st.selectbox("AI Technology Type", [
                    "Machine Learning", "Natural Language Processing", 
                    "Computer Vision", "Robotic Process Automation",
                    "Predictive Analytics", "Generative AI"
                ])
                implementation_timeline = st.slider("Implementation Timeline (months)", 3, 24, 12)
            
            with col2:
                investment_amount = st.number_input("Investment Amount ($)", 
                    min_value=10000, max_value=10000000, value=250000, step=10000)
                expected_roi = st.number_input("Expected ROI (%)", 
                    min_value=0, max_value=500, value=150, step=10)
                automation_percentage = st.slider("Process Automation (%)", 0, 100, 35)
            
            # Additional details
            st.markdown("#### Implementation Details")
            col3, col4 = st.columns(2)
            
            with col3:
                headcount_impact = st.number_input("Headcount Affected", 
                    min_value=1, max_value=1000, value=25)
                training_required = st.selectbox("Training Required", 
                    ["Minimal", "Moderate", "Extensive"])
            
            with col4:
                risk_level = st.selectbox("Risk Level", 
                    ["Low", "Medium", "High"])
                priority = st.selectbox("Strategic Priority", 
                    ["High", "Medium", "Low"])
            
            submitted = st.form_submit_button("Save Initiative")
            
            if submitted:
                data = load_data()
                if 'functions' not in data:
                    data['functions'] = {}
                
                data['functions'][selected_function] = {
                    'initiative_name': initiative_name,
                    'ai_type': ai_type,
                    'implementation_timeline': implementation_timeline,
                    'investment_amount': investment_amount,
                    'expected_roi': expected_roi,
                    'automation_percentage': automation_percentage,
                    'headcount_impact': headcount_impact,
                    'training_required': training_required,
                    'risk_level': risk_level,
                    'priority': priority
                }
                
                save_data(data)
                st.success(f"✅ AI initiative saved for {selected_function}")
                st.rerun()
    
    # Show configured functions
    data = load_data()
    if data.get('functions'):
        st.markdown("---")
        st.subheader("📋 Configured Functions")
        
        for func, config in data['functions'].items():
            with st.expander(f"{func} - {config['initiative_name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Investment", f"${config['investment_amount']:,}")
                    st.metric("Timeline", f"{config['implementation_timeline']} months")
                
                with col2:
                    st.metric("Expected ROI", f"{config['expected_roi']}%")
                    st.metric("Automation", f"{config['automation_percentage']}%")
                
                with col3:
                    st.metric("Headcount Impact", config['headcount_impact'])
                    st.write(f"**Priority:** {config['priority']}")
                    st.write(f"**Risk Level:** {config['risk_level']}")

def show_executive_summary():
    """Show executive summary"""
    st.title("📊 Executive Summary")
    st.markdown("### Strategic AI Implementation Overview")
    
    data = load_data()
    functions = data.get('functions', {})
    
    if not functions:
        st.info("No functions configured yet. Please configure AI initiatives in the Function Analysis section.")
        return
    
    # Calculate summary metrics
    total_investment = sum(f.get('investment_amount', 0) for f in functions.values())
    avg_roi = sum(f.get('expected_roi', 0) for f in functions.values()) / len(functions) if functions else 0
    total_headcount = sum(f.get('headcount_impact', 0) for f in functions.values())
    avg_timeline = sum(f.get('implementation_timeline', 0) for f in functions.values()) / len(functions) if functions else 0
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(f"${total_investment:,.0f}", "Total Investment", "blue"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(f"{avg_roi:.0f}%", "Average ROI", "green"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(f"{total_headcount:,}", "Total Headcount Impact", "purple"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(f"{avg_timeline:.0f}", "Average Timeline (months)", "orange"), unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("---")
    st.subheader("📈 Initiative Breakdown")
    
    for func, config in functions.items():
        st.markdown(f"#### {func}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Initiative:** {config['initiative_name']}  
            **AI Type:** {config['ai_type']}  
            **Priority:** {config['priority']}
            """)
        
        with col2:
            st.markdown(f"""
            **Investment:** ${config['investment_amount']:,}  
            **Expected ROI:** {config['expected_roi']}%  
            **Timeline:** {config['implementation_timeline']} months
            """)
        
        with col3:
            st.markdown(f"""
            **Automation:** {config['automation_percentage']}%  
            **Headcount Impact:** {config['headcount_impact']}  
            **Risk Level:** {config['risk_level']}
            """)
        
        st.markdown("---")
    
    # Strategic recommendations
    st.subheader("🎯 Strategic Recommendations")
    
    high_priority_count = sum(1 for f in functions.values() if f.get('priority') == 'High')
    high_risk_count = sum(1 for f in functions.values() if f.get('risk_level') == 'High')
    
    recommendations = []
    
    if high_priority_count > 3:
        recommendations.append("Consider phasing high-priority initiatives to manage resource allocation effectively.")
    
    if high_risk_count > 0:
        recommendations.append(f"{high_risk_count} initiative(s) marked as high-risk. Implement additional risk mitigation strategies.")
    
    if avg_roi > 200:
        recommendations.append("Exceptional ROI projections detected. Validate assumptions with pilot programs.")
    
    if total_investment > 5000000:
        recommendations.append("Significant investment planned. Consider staged rollout approach for risk management.")
    
    if not recommendations:
        recommendations.append("Current AI initiative portfolio appears well-balanced. Monitor implementation progress closely.")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

def main():
    """Main application function"""
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Select Page:", [
        "📊 Overview",
        "📈 Function Analysis", 
        "📋 Executive Summary"
    ])
    
    # Show selected page
    if page == "📊 Overview":
        show_overview()
    elif page == "📈 Function Analysis":
        show_function_analysis()
    elif page == "📋 Executive Summary":
        show_executive_summary()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**AI Impact Dashboard**  \nLight Theme Version  \nLast Updated: " + 
                       datetime.now().strftime("%Y-%m-%d %H:%M"))

if __name__ == "__main__":
    main()