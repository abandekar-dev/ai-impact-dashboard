import streamlit as st
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="AI Strategic Workforce Modeling Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = True
    st.session_state.functions = {}
    st.session_state.corporate_objectives = {}
    st.session_state.budget_constraints = {}
    st.session_state.change_management = {}

def main():
    st.title("🚀 AI Strategic Workforce Modeling Platform")
    st.markdown("**Advanced AI-powered strategic workforce modeling platform that transforms enterprise talent management**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis",
        [
            "Overview",
            "Function Analysis", 
            "Corporate Objectives",
            "Budget & Resources",
            "Change Management",
            "Performance Analysis",
            "Executive Summary"
        ]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Function Analysis":
        show_function_analysis()
    elif page == "Corporate Objectives":
        show_corporate_objectives()
    elif page == "Budget & Resources":
        show_budget_resources()
    elif page == "Change Management":
        show_change_management()
    elif page == "Performance Analysis":
        show_performance_analysis()
    elif page == "Executive Summary":
        show_executive_summary()

def show_overview():
    st.header("Platform Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Configured Functions", len(st.session_state.functions))
    
    with col2:
        st.metric("Active Objectives", len(st.session_state.corporate_objectives))
    
    with col3:
        st.metric("Platform Status", "Ready")
    
    st.markdown("---")
    
    st.subheader("Key Capabilities")
    
    capabilities = [
        "🎯 **Strategic Planning** - Comprehensive AI initiative planning and analysis",
        "📊 **Performance Modeling** - Advanced predictive analytics and scenario modeling",
        "🔄 **Monte Carlo Simulation** - Risk assessment and uncertainty quantification",
        "🏢 **Enterprise Integration** - Cross-functional dependency analysis",
        "📈 **ROI Analysis** - Investment optimization and financial modeling",
        "🎨 **Interactive Visualization** - Dynamic charts and executive dashboards"
    ]
    
    for capability in capabilities:
        st.markdown(capability)
    
    st.markdown("---")
    
    st.info("👆 Use the sidebar to navigate between different analysis sections. Start with Function Analysis to configure your enterprise functions.")

def show_function_analysis():
    st.header("Function Analysis")
    
    # Function selection
    function_options = [
        "Finance & Accounting",
        "Human Resources", 
        "Sales & Marketing",
        "Operations & Supply Chain",
        "IT & Technology",
        "Customer Service",
        "Legal & Compliance",
        "Research & Development",
        "Executive Leadership"
    ]
    
    selected_function = st.selectbox("Select Enterprise Function", function_options)
    
    if selected_function:
        st.subheader(f"Analyzing: {selected_function}")
        
        # Baseline data input
        with st.expander("Baseline Data Configuration", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                headcount = st.number_input("Current Headcount", min_value=1, value=50)
                avg_salary = st.number_input("Average Salary ($)", min_value=30000, value=75000)
                
            with col2:
                productivity_score = st.slider("Current Productivity Score", 1, 10, 7)
                efficiency_rating = st.slider("Current Efficiency Rating", 1, 10, 6)
        
        # AI Initiative Configuration
        with st.expander("AI Initiative Configuration"):
            ai_type = st.selectbox(
                "AI Initiative Type",
                ["Process Automation", "Predictive Analytics", "Natural Language Processing", "Computer Vision", "Machine Learning"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                implementation_cost = st.number_input("Implementation Cost ($)", min_value=10000, value=150000)
                timeline_months = st.number_input("Timeline (months)", min_value=3, value=12)
                
            with col2:
                expected_productivity_gain = st.slider("Expected Productivity Gain (%)", 5, 50, 20)
                risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
        
        # Save configuration
        if st.button("Save Function Configuration"):
            function_data = {
                "headcount": headcount,
                "avg_salary": avg_salary,
                "productivity_score": productivity_score,
                "efficiency_rating": efficiency_rating,
                "ai_initiative": {
                    "type": ai_type,
                    "cost": implementation_cost,
                    "timeline": timeline_months,
                    "expected_gain": expected_productivity_gain,
                    "risk": risk_level
                },
                "configured_at": datetime.now().isoformat()
            }
            
            st.session_state.functions[selected_function] = function_data
            st.success(f"✅ Configuration saved for {selected_function}")
        
        # Display current configuration
        if selected_function in st.session_state.functions:
            st.subheader("Current Configuration")
            config = st.session_state.functions[selected_function]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Headcount", config["headcount"])
                st.metric("Avg Salary", f"${config['avg_salary']:,}")
                
            with col2:
                st.metric("Productivity Score", f"{config['productivity_score']}/10")
                st.metric("Efficiency Rating", f"{config['efficiency_rating']}/10")
                
            with col3:
                st.metric("AI Initiative", config["ai_initiative"]["type"])
                st.metric("Expected Gain", f"{config['ai_initiative']['expected_gain']}%")

def show_corporate_objectives():
    st.header("Corporate Objectives & KPIs")
    
    st.markdown("Define your strategic objectives and key performance indicators.")
    
    # Strategic objectives
    with st.expander("Strategic Objectives", expanded=True):
        revenue_target = st.number_input("Annual Revenue Target ($M)", min_value=1, value=100)
        growth_target = st.slider("Growth Target (%)", 5, 30, 15)
        market_expansion = st.selectbox("Market Expansion Priority", ["Domestic", "International", "Both"])
        
        cost_reduction_target = st.slider("Cost Reduction Target (%)", 5, 25, 10)
        efficiency_improvement = st.slider("Efficiency Improvement Target (%)", 10, 40, 20)
    
    # Performance metrics
    with st.expander("Performance Metrics"):
        customer_satisfaction = st.slider("Customer Satisfaction Target", 70, 100, 85)
        employee_engagement = st.slider("Employee Engagement Target", 60, 100, 80)
        innovation_index = st.slider("Innovation Index Target", 50, 100, 75)
    
    if st.button("Save Corporate Objectives"):
        objectives_data = {
            "revenue_target": revenue_target,
            "growth_target": growth_target,
            "market_expansion": market_expansion,
            "cost_reduction": cost_reduction_target,
            "efficiency_improvement": efficiency_improvement,
            "customer_satisfaction": customer_satisfaction,
            "employee_engagement": employee_engagement,
            "innovation_index": innovation_index,
            "configured_at": datetime.now().isoformat()
        }
        
        st.session_state.corporate_objectives = objectives_data
        st.success("✅ Corporate objectives saved successfully")

def show_budget_resources():
    st.header("Budget & Resource Constraints")
    
    with st.expander("Budget Allocation", expanded=True):
        total_budget = st.number_input("Total AI Investment Budget ($)", min_value=50000, value=1000000)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Budget Distribution")
            tech_budget = st.slider("Technology & Infrastructure (%)", 20, 60, 40)
            training_budget = st.slider("Training & Development (%)", 10, 30, 20)
            
        with col2:
            consulting_budget = st.slider("Consulting & External Support (%)", 10, 40, 25)
            remaining = 100 - tech_budget - training_budget - consulting_budget
            st.metric("Operations & Maintenance (%)", f"{remaining}%")
    
    # Timeline constraints
    with st.expander("Timeline Constraints"):
        project_duration = st.selectbox("Project Duration", ["6 months", "12 months", "18 months", "24+ months"])
        phases = st.multiselect("Implementation Phases", 
                               ["Planning", "Pilot", "Rollout", "Optimization", "Scaling"])
        
        resource_availability = st.slider("Resource Availability (%)", 50, 100, 80)
    
    if st.button("Save Budget Configuration"):
        budget_data = {
            "total_budget": total_budget,
            "tech_budget": tech_budget,
            "training_budget": training_budget,
            "consulting_budget": consulting_budget,
            "operations_budget": remaining,
            "project_duration": project_duration,
            "phases": phases,
            "resource_availability": resource_availability,
            "configured_at": datetime.now().isoformat()
        }
        
        st.session_state.budget_constraints = budget_data
        st.success("✅ Budget configuration saved successfully")

def show_change_management():
    st.header("Change Management Readiness")
    
    with st.expander("Organizational Culture Assessment", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            innovation_culture = st.slider("Innovation Culture", 1, 10, 7)
            risk_tolerance = st.slider("Risk Tolerance", 1, 10, 6)
            digital_maturity = st.slider("Digital Maturity", 1, 10, 6)
            
        with col2:
            change_adaptability = st.slider("Change Adaptability", 1, 10, 7)
            leadership_support = st.slider("Leadership Support", 1, 10, 8)
            employee_engagement = st.slider("Employee Engagement", 1, 10, 7)
    
    # Readiness calculation
    overall_readiness = (innovation_culture + risk_tolerance + digital_maturity + 
                        change_adaptability + leadership_support + employee_engagement) / 6
    
    # Display readiness assessment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Readiness", f"{overall_readiness:.1f}/10")
    
    with col2:
        if overall_readiness >= 8:
            readiness_level = "High"
            color = "🟢"
        elif overall_readiness >= 6:
            readiness_level = "Medium"
            color = "🟡"
        else:
            readiness_level = "Low"
            color = "🔴"
        
        st.metric("Readiness Level", f"{color} {readiness_level}")
    
    with col3:
        success_probability = min(95, overall_readiness * 10 + 10)
        st.metric("Success Probability", f"{success_probability:.0f}%")
    
    if st.button("Save Change Management Assessment"):
        change_data = {
            "innovation_culture": innovation_culture,
            "risk_tolerance": risk_tolerance,
            "digital_maturity": digital_maturity,
            "change_adaptability": change_adaptability,
            "leadership_support": leadership_support,
            "employee_engagement": employee_engagement,
            "overall_readiness": overall_readiness,
            "readiness_level": readiness_level,
            "success_probability": success_probability,
            "configured_at": datetime.now().isoformat()
        }
        
        st.session_state.change_management = change_data
        st.success("✅ Change management assessment saved successfully")

def show_performance_analysis():
    st.header("Performance Analysis")
    
    if not st.session_state.functions:
        st.warning("⚠️ Please configure at least one function in Function Analysis before proceeding.")
        return
    
    st.subheader("Configured Functions Summary")
    
    # Create summary table
    summary_data = []
    for func_name, func_data in st.session_state.functions.items():
        ai_init = func_data.get("ai_initiative", {})
        summary_data.append({
            "Function": func_name,
            "Headcount": func_data.get("headcount", 0),
            "AI Initiative": ai_init.get("type", "Not specified"),
            "Investment": f"${ai_init.get('cost', 0):,}",
            "Expected Gain": f"{ai_init.get('expected_gain', 0)}%",
            "Risk Level": ai_init.get("risk", "Unknown")
        })
    
    # Display summary
    for item in summary_data:
        with st.expander(f"📊 {item['Function']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Headcount", item["Headcount"])
                st.metric("Investment", item["Investment"])
                
            with col2:
                st.metric("AI Initiative", item["AI Initiative"])
                st.metric("Expected Gain", item["Expected Gain"])
                
            with col3:
                st.metric("Risk Level", item["Risk Level"])
    
    # Aggregate analysis
    st.subheader("Aggregate Analysis")
    
    total_headcount = sum(func_data.get("headcount", 0) for func_data in st.session_state.functions.values())
    total_investment = sum(func_data.get("ai_initiative", {}).get("cost", 0) for func_data in st.session_state.functions.values())
    avg_expected_gain = sum(func_data.get("ai_initiative", {}).get("expected_gain", 0) for func_data in st.session_state.functions.values()) / len(st.session_state.functions)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Headcount", total_headcount)
    
    with col2:
        st.metric("Total Investment", f"${total_investment:,}")
    
    with col3:
        st.metric("Avg Expected Gain", f"{avg_expected_gain:.1f}%")

def show_executive_summary():
    st.header("Executive Summary")
    
    if not st.session_state.functions:
        st.warning("⚠️ Please configure functions and objectives before generating executive summary.")
        return
    
    st.subheader("Strategic Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_functions = len(st.session_state.functions)
        st.metric("Functions Analyzed", total_functions)
    
    with col2:
        total_investment = sum(func_data.get("ai_initiative", {}).get("cost", 0) for func_data in st.session_state.functions.values())
        st.metric("Total Investment", f"${total_investment:,}")
    
    with col3:
        avg_timeline = sum(func_data.get("ai_initiative", {}).get("timeline", 0) for func_data in st.session_state.functions.values()) / len(st.session_state.functions)
        st.metric("Avg Timeline", f"{avg_timeline:.1f} months")
    
    with col4:
        if st.session_state.change_management:
            readiness = st.session_state.change_management.get("overall_readiness", 0)
            st.metric("Change Readiness", f"{readiness:.1f}/10")
        else:
            st.metric("Change Readiness", "Not assessed")
    
    # Recommendations
    st.subheader("Key Recommendations")
    
    recommendations = [
        "🎯 **Strategic Focus**: Prioritize high-impact, low-risk AI initiatives for initial implementation",
        "📊 **Data Foundation**: Establish robust data governance and quality frameworks before scaling",
        "🔄 **Phased Approach**: Implement pilot programs in 2-3 functions before enterprise-wide rollout",
        "📈 **Performance Monitoring**: Establish clear KPIs and monitoring systems for AI initiative success",
        "🎓 **Capability Building**: Invest in comprehensive training programs for affected workforce",
        "🤝 **Change Management**: Strengthen change management practices to ensure successful adoption"
    ]
    
    for rec in recommendations:
        st.markdown(rec)
    
    # Export functionality
    st.subheader("Export Options")
    
    if st.button("Generate Detailed Report"):
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "functions": st.session_state.functions,
            "objectives": st.session_state.corporate_objectives,
            "budget": st.session_state.budget_constraints,
            "change_management": st.session_state.change_management,
            "summary": {
                "total_functions": len(st.session_state.functions),
                "total_investment": sum(func_data.get("ai_initiative", {}).get("cost", 0) for func_data in st.session_state.functions.values()),
                "avg_timeline": sum(func_data.get("ai_initiative", {}).get("timeline", 0) for func_data in st.session_state.functions.values()) / len(st.session_state.functions) if st.session_state.functions else 0
            }
        }
        
        st.json(report_data)
        st.success("✅ Detailed report generated successfully")

if __name__ == "__main__":
    main()