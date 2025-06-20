import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
import math

# Simple in-memory storage for this demo version
def init_database():
    """Mock database initialization for simplified version"""
    return None

# Initialize database
db = None

def main():
    st.title("🎯 Analytics and Insights Engine")
    st.markdown("**Executive Platform for Strategic AI Implementation and Workforce Transformation Analytics**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Overview"
    
    # Navigation buttons
    if st.sidebar.button("🏠 Overview", use_container_width=True):
        st.session_state.selected_page = "Overview"
        st.rerun()
    
    if st.sidebar.button("🔧 Enhanced Function Analysis", use_container_width=True):
        st.session_state.selected_page = "Enhanced Function Analysis"
        st.rerun()
    
    if st.sidebar.button("📊 Comparative Analysis", use_container_width=True):
        st.session_state.selected_page = "Comparative Analysis"
        st.rerun()
    
    if st.sidebar.button("🔧 Build vs Buy Analysis", use_container_width=True):
        st.session_state.selected_page = "Build Buy Analysis"
        st.rerun()
    
    # Route to selected page
    page = st.session_state.selected_page
    
    if page == "Overview":
        show_overview()
    elif page == "Enhanced Function Analysis":
        show_enhanced_function_analysis()
    elif page == "Comparative Analysis":
        show_comparative_analysis()
    elif page == "Build Buy Analysis":
        show_build_buy_analysis()

def show_overview():
    st.header("🎯 Strategic AI Implementation Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Functions", len(st.session_state.get('baseline_data', {})))
    with col2:
        total_initiatives = sum(
            len(getattr(st.session_state, f'categories_{func}', {}).get(cat, {}).get('ai_initiatives', {}))
            for func in st.session_state.get('baseline_data', {})
            for cat in getattr(st.session_state, f'categories_{func}', {})
        )
        st.metric("AI Initiatives", total_initiatives)
    with col3:
        st.metric("Analysis Modules", "4")
    
    st.markdown("---")
    
    st.markdown("### 🚀 Platform Capabilities")
    
    features = [
        ("Enhanced Function Analysis", "Configure enterprise functions and AI initiatives with natural language processing"),
        ("Comparative Analysis", "Before/after impact assessment with financial and workforce metrics"),
        ("Build vs Buy Analysis", "Strategic workforce planning for AI skills and capabilities"),
        ("Predictive Analytics", "Monte Carlo simulations and ROI forecasting")
    ]
    
    for feature, description in features:
        with st.expander(f"📈 {feature}"):
            st.write(description)

def show_enhanced_function_analysis():
    st.header("🎯 Enhanced Function Analysis")
    
    # Initialize session state
    if 'baseline_data' not in st.session_state:
        st.session_state.baseline_data = {}
    
    # Function configuration
    st.subheader("Configure Enterprise Function")
    
    functions = ['IT', 'Sales', 'Marketing', 'Operations', 'Finance', 'HR', 'Customer Service', 'Supply Chain', 'R&D']
    selected_function = st.selectbox("Select Function:", functions)
    
    if selected_function:
        col1, col2 = st.columns(2)
        
        with col1:
            headcount = st.number_input("Current Headcount", min_value=1, value=50)
            annual_revenue = st.number_input("Annual Revenue ($)", min_value=0, value=1000000)
        
        with col2:
            annual_costs = st.number_input("Annual Costs ($)", min_value=0, value=500000)
            productivity = st.slider("Current Productivity (1-10)", 1, 10, 7)
        
        if st.button("Save Function Configuration"):
            st.session_state.baseline_data[selected_function] = {
                'headcount': headcount,
                'annual_revenue': annual_revenue,
                'annual_costs': annual_costs,
                'current_productivity': productivity,
                'performance_satisfaction': 7.5
            }
            st.success(f"Configuration saved for {selected_function}")
            st.rerun()
    
    # AI Initiatives
    if selected_function in st.session_state.baseline_data:
        st.subheader("AI Initiatives")
        
        categories_key = f'categories_{selected_function}'
        if not hasattr(st.session_state, categories_key):
            setattr(st.session_state, categories_key, {})
        
        categories = getattr(st.session_state, categories_key)
        
        # Add new initiative
        with st.expander("➕ Add New AI Initiative"):
            initiative_name = st.text_input("Initiative Name")
            ai_types = ['Machine Learning', 'Automation', 'Data Analytics', 'Natural Language Processing', 'Computer Vision']
            ai_type = st.selectbox("AI Type", ai_types)
            investment = st.number_input("Investment ($)", min_value=0, value=100000)
            automation_level = st.slider("Automation Level (%)", 0, 100, 30)
            
            if st.button("Add Initiative") and initiative_name:
                category_name = "AI Initiatives"
                if category_name not in categories:
                    categories[category_name] = {'ai_initiatives': {}}
                
                init_id = len(categories[category_name]['ai_initiatives']) + 1
                categories[category_name]['ai_initiatives'][str(init_id)] = {
                    'name': initiative_name,
                    'ai_type': ai_type,
                    'investment': investment,
                    'automation_level': automation_level,
                    'productivity_gain': automation_level * 0.8,
                    'predictions': {
                        'roi': investment * 0.15,
                        'annual_cost_savings': investment * 0.2,
                        'productivity_gain': automation_level * 0.8
                    }
                }
                
                setattr(st.session_state, categories_key, categories)
                st.success(f"Added initiative: {initiative_name}")
                st.rerun()
        
        # Display existing initiatives
        if categories:
            st.subheader("Current Initiatives")
            for category_name, category_data in categories.items():
                for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                    with st.expander(f"📊 {init_data.get('name', 'Unnamed Initiative')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Type:** {init_data.get('ai_type', 'Unknown')}")
                            st.write(f"**Investment:** ${init_data.get('investment', 0):,}")
                            st.write(f"**Automation Level:** {init_data.get('automation_level', 0)}%")
                        
                        with col2:
                            if 'predictions' in init_data:
                                pred = init_data['predictions']
                                st.write(f"**Expected ROI:** ${pred.get('roi', 0):,.0f}")
                                st.write(f"**Annual Savings:** ${pred.get('annual_cost_savings', 0):,.0f}")
                                st.write(f"**Productivity Gain:** {pred.get('productivity_gain', 0):.1f}%")

def show_comparative_analysis():
    st.header("📊 Comparative Analysis")
    
    if not st.session_state.get('baseline_data'):
        st.warning("Please configure enterprise functions first.")
        return
    
    # Get functions with AI initiatives
    functions_with_ai = []
    for func_name in st.session_state.baseline_data.keys():
        categories_key = f'categories_{func_name}'
        if hasattr(st.session_state, categories_key):
            categories = getattr(st.session_state, categories_key)
            if categories and any(cat.get('ai_initiatives') for cat in categories.values()):
                functions_with_ai.append(func_name)
    
    if not functions_with_ai:
        st.info("No AI initiatives configured yet.")
        return
    
    selected_function = st.selectbox("Select Function for Analysis:", functions_with_ai)
    
    if selected_function:
        baseline = st.session_state.baseline_data[selected_function]
        categories_key = f'categories_{selected_function}'
        categories = getattr(st.session_state, categories_key, {})
        
        # Calculate impact
        total_investment = 0
        total_savings = 0
        total_productivity_gain = 0
        
        for category_data in categories.values():
            for init_data in category_data.get('ai_initiatives', {}).values():
                total_investment += init_data.get('investment', 0)
                if 'predictions' in init_data:
                    pred = init_data['predictions']
                    total_savings += pred.get('annual_cost_savings', 0)
                    total_productivity_gain += pred.get('productivity_gain', 0)
        
        # Before/After comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Current State")
            st.metric("Annual Revenue", f"${baseline['annual_revenue']:,}")
            st.metric("Annual Costs", f"${baseline['annual_costs']:,}")
            st.metric("Productivity", f"{baseline['current_productivity']}/10")
        
        with col2:
            st.subheader("🚀 Future State (With AI)")
            future_revenue = baseline['annual_revenue'] * (1 + total_productivity_gain / 200)
            future_costs = baseline['annual_costs'] - total_savings
            future_productivity = min(10, baseline['current_productivity'] * (1 + total_productivity_gain / 100))
            
            st.metric("Annual Revenue", f"${future_revenue:,.0f}", 
                     delta=f"${future_revenue - baseline['annual_revenue']:,.0f}")
            st.metric("Annual Costs", f"${future_costs:,.0f}", 
                     delta=f"${future_costs - baseline['annual_costs']:,.0f}")
            st.metric("Productivity", f"{future_productivity:.1f}/10", 
                     delta=f"{future_productivity - baseline['current_productivity']:+.1f}")
        
        # ROI Analysis
        st.subheader("💰 Financial Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        net_benefit = total_savings + (future_revenue - baseline['annual_revenue'])
        roi_percentage = (net_benefit / max(total_investment, 1)) * 100
        payback_years = total_investment / max(net_benefit, 1)
        
        with col1:
            st.metric("Total Investment", f"${total_investment:,}")
        with col2:
            st.metric("Annual Net Benefit", f"${net_benefit:,.0f}")
        with col3:
            st.metric("ROI", f"{roi_percentage:.1f}%")
        
        # Visualization
        st.subheader("📊 Performance Comparison")
        
        # Create simple comparison table
        comparison_df = {
            'Metric': ['Revenue ($M)', 'Costs ($M)', 'Productivity (1-10)'],
            'Current': [f"{baseline['annual_revenue']/1000000:.1f}", f"{baseline['annual_costs']/1000000:.1f}", f"{baseline['current_productivity']:.1f}"],
            'Future': [f"{future_revenue/1000000:.1f}", f"{future_costs/1000000:.1f}", f"{future_productivity:.1f}"]
        }
        
        st.table(comparison_df)

def show_build_buy_analysis():
    st.header("🔧 Build vs Buy Analysis")
    
    if not st.session_state.get('baseline_data'):
        st.warning("Please configure enterprise functions first.")
        return
    
    # Skills database
    skills_db = {
        'Data Science': {'salary': 120000, 'training_cost': 15000, 'training_months': 8},
        'AI/ML Engineering': {'salary': 140000, 'training_cost': 25000, 'training_months': 12},
        'Automation': {'salary': 95000, 'training_cost': 12000, 'training_months': 6},
        'Digital Transformation': {'salary': 110000, 'training_cost': 8000, 'training_months': 4}
    }
    
    # Analyze skill requirements
    skill_requirements = {}
    
    for func_name in st.session_state.baseline_data.keys():
        categories_key = f'categories_{func_name}'
        if hasattr(st.session_state, categories_key):
            categories = getattr(st.session_state, categories_key)
            for category_data in categories.values():
                for init_data in category_data.get('ai_initiatives', {}).values():
                    ai_type = init_data.get('ai_type', '')
                    
                    # Map AI types to skills
                    if 'Machine Learning' in ai_type or 'Data' in ai_type:
                        skill = 'Data Science'
                    elif 'Automation' in ai_type:
                        skill = 'Automation'
                    elif 'AI' in ai_type or 'ML' in ai_type:
                        skill = 'AI/ML Engineering'
                    else:
                        skill = 'Digital Transformation'
                    
                    if skill not in skill_requirements:
                        skill_requirements[skill] = {'functions': [], 'people_needed': 0}
                    
                    if func_name not in skill_requirements[skill]['functions']:
                        skill_requirements[skill]['functions'].append(func_name)
                        skill_requirements[skill]['people_needed'] += 2  # Estimate 2 people per function
    
    if not skill_requirements:
        st.info("No skill requirements identified. Please add AI initiatives first.")
        return
    
    st.subheader("Skills Requirements Analysis")
    
    # Build vs Buy comparison
    comparison_data = []
    
    for skill, req_data in skill_requirements.items():
        skill_info = skills_db.get(skill, {'salary': 100000, 'training_cost': 10000, 'training_months': 6})
        people_needed = req_data['people_needed']
        
        # Buy scenario (hire externally)
        buy_annual_cost = skill_info['salary'] * 1.2 * people_needed  # 20% premium
        buy_onetime_cost = 15000 * people_needed  # Recruitment cost
        buy_total_3yr = buy_annual_cost * 3 + buy_onetime_cost
        
        # Build scenario (train internally)
        build_annual_cost = skill_info['salary'] * 0.8 * people_needed  # Internal salary
        build_onetime_cost = skill_info['training_cost'] * people_needed
        build_total_3yr = build_annual_cost * 3 + build_onetime_cost
        
        recommendation = 'Build' if build_total_3yr < buy_total_3yr else 'Buy'
        savings = buy_total_3yr - build_total_3yr
        
        comparison_data.append({
            'Skill': skill,
            'People Needed': people_needed,
            'Buy Cost (3yr)': buy_total_3yr,
            'Build Cost (3yr)': build_total_3yr,
            'Savings (Build)': savings,
            'Recommendation': recommendation,
            'Training Time': f"{skill_info['training_months']} months"
        })
    
    # Display comparison table
    for data in comparison_data:
        with st.expander(f"📊 {data['Skill']} - {data['Recommendation']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**People Needed:** {data['People Needed']}")
                st.write(f"**Buy Cost (3 years):** ${data['Buy Cost (3yr)']:,.0f}")
                st.write(f"**Build Cost (3 years):** ${data['Build Cost (3yr)']:,.0f}")
            
            with col2:
                st.write(f"**Potential Savings:** ${data['Savings (Build)']:,.0f}")
                st.write(f"**Training Time:** {data['Training Time']}")
                st.write(f"**Recommendation:** {data['Recommendation']}")
    
    # Summary metrics
    st.subheader("📈 Summary")
    
    col1, col2, col3 = st.columns(3)
    
    total_people = sum(data['People Needed'] for data in comparison_data)
    total_buy_cost = sum(data['Buy Cost (3yr)'] for data in comparison_data)
    total_build_cost = sum(data['Build Cost (3yr)'] for data in comparison_data)
    total_savings = total_buy_cost - total_build_cost
    
    with col1:
        st.metric("Total People Needed", total_people)
    with col2:
        st.metric("Total Build Cost", f"${total_build_cost:,.0f}")
    with col3:
        st.metric("Potential Savings", f"${total_savings:,.0f}")
    
    # Visualization
    st.subheader("📊 Cost Comparison Chart")
    
    # Create comparison table
    chart_table = {
        'Skill': [data['Skill'] for data in comparison_data],
        'Buy Cost (3yr)': [f"${data['Buy Cost (3yr)']:,.0f}" for data in comparison_data],
        'Build Cost (3yr)': [f"${data['Build Cost (3yr)']:,.0f}" for data in comparison_data],
        'Recommendation': [data['Recommendation'] for data in comparison_data]
    }
    
    st.table(chart_table)

if __name__ == "__main__":
    main()