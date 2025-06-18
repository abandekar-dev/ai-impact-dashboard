import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json

# Skills database for different industries and roles
SKILLS_DATABASE = {
    'Data Science & Analytics': {
        'skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'Data Visualization', 'Big Data'],
        'avg_salary': 120000,
        'training_time_months': 8,
        'training_cost': 15000,
        'market_availability': 'Medium',
        'criticality': 'High'
    },
    'AI/ML Engineering': {
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'MLOps', 'Cloud Platforms', 'Deep Learning', 'Computer Vision'],
        'avg_salary': 140000,
        'training_time_months': 12,
        'training_cost': 25000,
        'market_availability': 'Low',
        'criticality': 'High'
    },
    'Automation Engineering': {
        'skills': ['RPA Tools', 'Process Design', 'Programming', 'System Integration', 'Workflow Design'],
        'avg_salary': 95000,
        'training_time_months': 6,
        'training_cost': 12000,
        'market_availability': 'Medium',
        'criticality': 'Medium'
    },
    'Digital Transformation': {
        'skills': ['Change Management', 'Digital Strategy', 'Project Management', 'Business Analysis', 'Technology Assessment'],
        'avg_salary': 110000,
        'training_time_months': 4,
        'training_cost': 8000,
        'market_availability': 'High',
        'criticality': 'Medium'
    },
    'Cybersecurity': {
        'skills': ['Security Frameworks', 'Risk Assessment', 'Compliance', 'Incident Response', 'Encryption'],
        'avg_salary': 115000,
        'training_time_months': 10,
        'training_cost': 18000,
        'market_availability': 'Low',
        'criticality': 'High'
    },
    'Cloud Architecture': {
        'skills': ['AWS/Azure/GCP', 'Infrastructure as Code', 'Microservices', 'DevOps', 'Scalability Design'],
        'avg_salary': 130000,
        'training_time_months': 8,
        'training_cost': 15000,
        'market_availability': 'Medium',
        'criticality': 'High'
    },
    'Product Management': {
        'skills': ['Product Strategy', 'User Experience', 'Agile Methodologies', 'Market Analysis', 'Stakeholder Management'],
        'avg_salary': 125000,
        'training_time_months': 6,
        'training_cost': 10000,
        'market_availability': 'Medium',
        'criticality': 'Medium'
    },
    'Business Intelligence': {
        'skills': ['SQL', 'Data Warehousing', 'Reporting Tools', 'Business Analysis', 'KPI Design'],
        'avg_salary': 85000,
        'training_time_months': 5,
        'training_cost': 8000,
        'market_availability': 'High',
        'criticality': 'Medium'
    }
}

def show_build_buy_analysis():
    """Comprehensive Build vs Buy workforce analysis for AI transformation"""
    
    st.title("🔧 Build vs Buy Analysis")
    st.markdown("**Strategic workforce planning: Build internal capabilities or buy external talent**")
    
    # Check if we have baseline data
    if not hasattr(st.session_state, 'baseline_data') or not st.session_state.baseline_data:
        st.warning("Please configure enterprise functions in Enhanced Function Analysis first.")
        return
    
    # Analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Skills Gap Analysis", 
        "💰 Cost-Benefit Analysis", 
        "📈 Strategic Recommendations", 
        "⏱️ Implementation Planning",
        "📊 Executive Summary"
    ])
    
    with tab1:
        show_skills_gap_analysis()
    
    with tab2:
        show_cost_benefit_analysis()
    
    with tab3:
        show_strategic_recommendations()
    
    with tab4:
        show_implementation_planning()
    
    with tab5:
        show_build_buy_executive_summary()

def show_skills_gap_analysis():
    """Analyze skills gaps across enterprise functions"""
    
    st.subheader("🎯 Skills Gap Analysis")
    
    # Function selector
    functions_list = list(st.session_state.baseline_data.keys())
    selected_function = st.selectbox(
        "Select Function for Skills Analysis:",
        functions_list,
        key="skills_function_selector"
    )
    
    if not selected_function:
        return
    
    # Get function data
    baseline_data = st.session_state.baseline_data[selected_function]
    categories_key = f'categories_{selected_function}'
    categories = getattr(st.session_state, categories_key, {})
    
    # Current workforce overview
    col1, col2, col3 = st.columns(3)
    
    current_headcount = baseline_data.get('headcount', 0)
    current_productivity = baseline_data.get('current_productivity', 0)
    annual_costs = baseline_data.get('annual_costs', 0)
    
    with col1:
        st.metric("Current Headcount", f"{current_headcount:,}")
    with col2:
        st.metric("Productivity Score", f"{current_productivity:.1f}/10")
    with col3:
        avg_salary = annual_costs / max(current_headcount, 1) if current_headcount > 0 else 0
        st.metric("Avg Annual Cost per Employee", f"${avg_salary:,.0f}")
    
    # Analyze required skills based on AI initiatives
    required_skills = analyze_required_skills(categories)
    
    if not required_skills:
        st.info("No AI initiatives configured. Please add AI initiatives to see skills gap analysis.")
        return
    
    # Skills gap assessment
    st.markdown("#### 📋 Required Skills Assessment")
    
    skills_data = []
    for skill_category, details in required_skills.items():
        skill_info = SKILLS_DATABASE.get(skill_category, {})
        
        # Current capability assessment (simulated based on function type and productivity)
        current_capability = estimate_current_capability(selected_function, skill_category, current_productivity)
        required_capability = details['importance_score']
        gap_percentage = max(0, required_capability - current_capability)
        
        skills_data.append({
            'Skill Category': skill_category,
            'Required Level': f"{required_capability}/10",
            'Current Level': f"{current_capability:.1f}/10",
            'Gap': f"{gap_percentage:.1f}/10",
            'Market Availability': skill_info.get('market_availability', 'Unknown'),
            'Avg Salary': f"${skill_info.get('avg_salary', 0):,}",
            'Training Time': f"{skill_info.get('training_time_months', 0)} months",
            'Training Cost': f"${skill_info.get('training_cost', 0):,}",
            'Criticality': skill_info.get('criticality', 'Medium')
        })
    
    df_skills = pd.DataFrame(skills_data)
    st.dataframe(df_skills, use_container_width=True)
    
    # Skills gap visualization
    st.markdown("#### 📊 Skills Gap Visualization")
    
    fig_gap = go.Figure()
    
    skill_categories = [row['Skill Category'] for row in skills_data]
    required_levels = [float(row['Required Level'].split('/')[0]) for row in skills_data]
    current_levels = [float(row['Current Level'].split('/')[0]) for row in skills_data]
    
    fig_gap.add_trace(go.Bar(
        name='Required Level',
        x=skill_categories,
        y=required_levels,
        marker_color='red',
        opacity=0.7
    ))
    
    fig_gap.add_trace(go.Bar(
        name='Current Level', 
        x=skill_categories,
        y=current_levels,
        marker_color='blue',
        opacity=0.7
    ))
    
    fig_gap.update_layout(
        title=f"Skills Gap Analysis - {selected_function}",
        barmode='group',
        yaxis_title="Capability Level (1-10)",
        height=400
    )
    
    st.plotly_chart(fig_gap, use_container_width=True)
    
    # Priority matrix
    st.markdown("#### 🎯 Skills Priority Matrix")
    
    priority_data = []
    for skill_category, details in required_skills.items():
        skill_info = SKILLS_DATABASE.get(skill_category, {})
        current_capability = estimate_current_capability(selected_function, skill_category, current_productivity)
        gap = max(0, details['importance_score'] - current_capability)
        
        # Calculate priority score
        criticality_score = {'Low': 1, 'Medium': 2, 'High': 3}.get(skill_info.get('criticality', 'Medium'), 2)
        availability_score = {'High': 1, 'Medium': 2, 'Low': 3}.get(skill_info.get('market_availability', 'Medium'), 2)
        
        priority_score = (gap * criticality_score * availability_score) / 9 * 10
        
        priority_data.append({
            'Skill Category': skill_category,
            'Skills Gap': gap,
            'Criticality': criticality_score,
            'Market Scarcity': availability_score,
            'Priority Score': priority_score
        })
    
    df_priority = pd.DataFrame(priority_data)
    
    fig_priority = px.scatter(
        df_priority,
        x='Skills Gap',
        y='Priority Score',
        size='Market Scarcity',
        color='Criticality',
        hover_name='Skill Category',
        title="Skills Priority Matrix",
        labels={'Skills Gap': 'Skills Gap (1-10)', 'Priority Score': 'Strategic Priority (1-10)'}
    )
    
    st.plotly_chart(fig_priority, use_container_width=True)

def show_cost_benefit_analysis():
    """Comprehensive cost-benefit analysis for build vs buy decisions"""
    
    st.subheader("💰 Cost-Benefit Analysis")
    
    # Get all functions with skill requirements
    all_skill_requirements = {}
    total_headcount = 0
    
    for func_name in st.session_state.baseline_data.keys():
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_skills = analyze_required_skills(categories)
        if func_skills:
            all_skill_requirements[func_name] = {
                'skills': func_skills,
                'headcount': baseline_data.get('headcount', 0),
                'productivity': baseline_data.get('current_productivity', 0)
            }
            total_headcount += baseline_data.get('headcount', 0)
    
    if not all_skill_requirements:
        st.info("No skills requirements identified. Please configure AI initiatives first.")
        return
    
    # Build vs Buy analysis parameters
    st.markdown("#### ⚙️ Analysis Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hiring_premium = st.slider("External Hiring Premium (%)", 0, 50, 20, 
                                 help="Additional cost premium for external hires vs market rate")
        recruitment_cost = st.slider("Recruitment Cost per Hire ($)", 5000, 50000, 15000,
                                   help="Average cost to recruit and onboard external talent")
    
    with col2:
        training_efficiency = st.slider("Internal Training Efficiency (%)", 50, 100, 80,
                                      help="Effectiveness of internal training programs")
        retention_rate = st.slider("Employee Retention Rate (%)", 70, 95, 85,
                                 help="Expected retention rate for new hires and trained employees")
    
    # Calculate build vs buy scenarios for each skill
    scenarios_data = []
    
    for func_name, func_data in all_skill_requirements.items():
        for skill_category, skill_details in func_data['skills'].items():
            skill_info = SKILLS_DATABASE.get(skill_category, {})
            
            # Estimate number of people needed
            current_capability = estimate_current_capability(func_name, skill_category, func_data['productivity'])
            required_capability = skill_details['importance_score']
            capability_gap = max(0, required_capability - current_capability)
            
            # Rough estimate: 1 point of capability gap = 0.5 FTE needed
            people_needed = max(1, int(capability_gap * 0.8))
            
            # Buy scenario (external hiring)
            market_salary = skill_info.get('avg_salary', 100000)
            buy_annual_cost = market_salary * (1 + hiring_premium/100) * people_needed
            buy_onetime_cost = recruitment_cost * people_needed
            buy_total_3yr = buy_annual_cost * 3 + buy_onetime_cost
            
            # Build scenario (internal training)
            training_cost_per_person = skill_info.get('training_cost', 10000)
            training_time_months = skill_info.get('training_time_months', 6)
            
            # Assume internal employees earn 80% of market rate for this skill initially
            internal_salary = market_salary * 0.8
            training_total_cost = training_cost_per_person * people_needed
            
            # Productivity loss during training (assume 50% productivity during training period)
            productivity_loss_cost = (internal_salary * 0.5 * training_time_months / 12) * people_needed
            
            build_annual_cost = internal_salary * people_needed
            build_onetime_cost = training_total_cost + productivity_loss_cost
            build_total_3yr = build_annual_cost * 3 + build_onetime_cost
            
            # Risk adjustments
            buy_risk_multiplier = 1 + (1 - retention_rate/100) * 0.5  # Higher risk if low retention
            build_risk_multiplier = 1 + (1 - training_efficiency/100) * 0.3  # Risk of training failure
            
            buy_total_3yr_adjusted = buy_total_3yr * buy_risk_multiplier
            build_total_3yr_adjusted = build_total_3yr * build_risk_multiplier
            
            scenarios_data.append({
                'Function': func_name,
                'Skill Category': skill_category,
                'People Needed': people_needed,
                'Buy: Annual Cost': buy_annual_cost,
                'Buy: One-time Cost': buy_onetime_cost,
                'Buy: 3-Year Total': buy_total_3yr_adjusted,
                'Build: Annual Cost': build_annual_cost,
                'Build: One-time Cost': build_onetime_cost,
                'Build: 3-Year Total': build_total_3yr_adjusted,
                'Cost Savings (Build)': buy_total_3yr_adjusted - build_total_3yr_adjusted,
                'Recommendation': 'Build' if build_total_3yr_adjusted < buy_total_3yr_adjusted else 'Buy',
                'Market Availability': skill_info.get('market_availability', 'Medium'),
                'Training Time': training_time_months
            })
    
    # Display scenarios
    st.markdown("#### 📊 Build vs Buy Scenarios")
    
    df_scenarios = pd.DataFrame(scenarios_data)
    
    # Format currency columns
    currency_cols = ['Buy: Annual Cost', 'Buy: One-time Cost', 'Buy: 3-Year Total', 
                    'Build: Annual Cost', 'Build: One-time Cost', 'Build: 3-Year Total', 'Cost Savings (Build)']
    
    df_display = df_scenarios.copy()
    for col in currency_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_display[['Function', 'Skill Category', 'People Needed', 'Recommendation', 
                           'Buy: 3-Year Total', 'Build: 3-Year Total', 'Cost Savings (Build)']], 
                use_container_width=True)
    
    # Summary metrics
    st.markdown("#### 📈 Financial Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_buy_cost = df_scenarios['Buy: 3-Year Total'].sum()
    total_build_cost = df_scenarios['Build: 3-Year Total'].sum()
    total_savings = total_buy_cost - total_build_cost
    savings_percentage = (total_savings / total_buy_cost * 100) if total_buy_cost > 0 else 0
    
    with col1:
        st.metric("Total Buy Cost (3 years)", f"${total_buy_cost:,.0f}")
    with col2:
        st.metric("Total Build Cost (3 years)", f"${total_build_cost:,.0f}")
    with col3:
        st.metric("Potential Savings", f"${total_savings:,.0f}")
    with col4:
        st.metric("Savings Percentage", f"{savings_percentage:.1f}%")
    
    # Cost comparison visualization
    fig_comparison = go.Figure(data=[
        go.Bar(name='Buy Scenario', x=df_scenarios['Skill Category'], y=df_scenarios['Buy: 3-Year Total'], marker_color='red'),
        go.Bar(name='Build Scenario', x=df_scenarios['Skill Category'], y=df_scenarios['Build: 3-Year Total'], marker_color='green')
    ])
    
    fig_comparison.update_layout(
        title='3-Year Cost Comparison: Build vs Buy by Skill Category',
        barmode='group',
        yaxis_title='Total Cost ($)',
        height=400
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

def show_strategic_recommendations():
    """Generate strategic recommendations based on analysis"""
    
    st.subheader("📈 Strategic Recommendations")
    
    # Get analysis data
    all_skill_requirements = {}
    for func_name in st.session_state.baseline_data.keys():
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_skills = analyze_required_skills(categories)
        if func_skills:
            all_skill_requirements[func_name] = {
                'skills': func_skills,
                'headcount': baseline_data.get('headcount', 0),
                'productivity': baseline_data.get('current_productivity', 0)
            }
    
    if not all_skill_requirements:
        st.info("No skills requirements identified. Please configure AI initiatives first.")
        return
    
    # Generate recommendations by category
    recommendations = generate_build_buy_recommendations(all_skill_requirements)
    
    # High-level strategy
    st.markdown("#### 🎯 Recommended Strategy")
    
    build_count = sum(1 for r in recommendations if r['recommendation'] == 'Build')
    buy_count = sum(1 for r in recommendations if r['recommendation'] == 'Buy')
    hybrid_count = sum(1 for r in recommendations if r['recommendation'] == 'Hybrid')
    
    strategy_col1, strategy_col2, strategy_col3 = st.columns(3)
    
    with strategy_col1:
        st.metric("Build Internally", build_count, help="Skills to develop through training")
    with strategy_col2:
        st.metric("Buy Externally", buy_count, help="Skills to acquire through hiring")
    with strategy_col3:
        st.metric("Hybrid Approach", hybrid_count, help="Combination of build and buy")
    
    # Detailed recommendations
    st.markdown("#### 📋 Detailed Recommendations by Skill Category")
    
    for rec in recommendations:
        with st.expander(f"🎯 {rec['skill_category']} - {rec['recommendation']}"):
            st.markdown(f"**Function:** {rec['function']}")
            st.markdown(f"**Strategic Approach:** {rec['recommendation']}")
            st.markdown(f"**Rationale:** {rec['rationale']}")
            st.markdown(f"**Timeline:** {rec['timeline']}")
            st.markdown(f"**Key Actions:**")
            for action in rec['key_actions']:
                st.markdown(f"• {action}")
            
            if rec['risks']:
                st.markdown(f"**Risks to Consider:**")
                for risk in rec['risks']:
                    st.markdown(f"⚠️ {risk}")
    
    # Implementation roadmap
    st.markdown("#### 🗺️ Implementation Roadmap")
    
    # Sort recommendations by priority and timeline
    immediate_actions = [r for r in recommendations if 'immediate' in r['timeline'].lower()]
    short_term_actions = [r for r in recommendations if 'short' in r['timeline'].lower() or '3-6' in r['timeline']]
    long_term_actions = [r for r in recommendations if 'long' in r['timeline'].lower() or '12+' in r['timeline']]
    
    roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)
    
    with roadmap_col1:
        st.markdown("##### 🚀 Immediate (0-3 months)")
        for action in immediate_actions:
            st.markdown(f"• **{action['skill_category']}**: {action['recommendation']}")
    
    with roadmap_col2:
        st.markdown("##### 📈 Short Term (3-12 months)")
        for action in short_term_actions:
            st.markdown(f"• **{action['skill_category']}**: {action['recommendation']}")
    
    with roadmap_col3:
        st.markdown("##### 🎯 Long Term (12+ months)")
        for action in long_term_actions:
            st.markdown(f"• **{action['skill_category']}**: {action['recommendation']}")

def show_implementation_planning():
    """Detailed implementation planning and timeline"""
    
    st.subheader("⏱️ Implementation Planning")
    
    # Get analysis data
    all_skill_requirements = {}
    for func_name in st.session_state.baseline_data.keys():
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_skills = analyze_required_skills(categories)
        if func_skills:
            all_skill_requirements[func_name] = {
                'skills': func_skills,
                'headcount': baseline_data.get('headcount', 0),
                'productivity': baseline_data.get('current_productivity', 0)
            }
    
    if not all_skill_requirements:
        st.info("No skills requirements identified. Please configure AI initiatives first.")
        return
    
    # Implementation timeline
    st.markdown("#### 📅 Implementation Timeline")
    
    timeline_data = []
    current_date = datetime.now()
    
    for func_name, func_data in all_skill_requirements.items():
        for skill_category, skill_details in func_data['skills'].items():
            skill_info = SKILLS_DATABASE.get(skill_category, {})
            
            # Determine implementation approach based on previous analysis
            market_availability = skill_info.get('market_availability', 'Medium')
            training_time = skill_info.get('training_time_months', 6)
            
            if market_availability == 'Low' or training_time <= 6:
                approach = 'Build'
                duration_months = training_time + 2  # Add 2 months for setup
            else:
                approach = 'Buy'
                duration_months = 4  # Recruitment typically takes 3-4 months
            
            start_date = current_date + timedelta(days=30)  # Start next month
            end_date = start_date + timedelta(days=duration_months * 30)
            
            timeline_data.append({
                'Task': f"{skill_category} ({func_name})",
                'Approach': approach,
                'Start': start_date,
                'End': end_date,
                'Duration (months)': duration_months,
                'Resource': skill_info.get('criticality', 'Medium')
            })
    
    # Create Gantt chart
    fig_gantt = go.Figure()
    
    colors = {'Build': 'green', 'Buy': 'blue', 'Hybrid': 'orange'}
    
    for i, row in enumerate(timeline_data):
        fig_gantt.add_trace(go.Scatter(
            x=[row['Start'], row['End']],
            y=[i, i],
            mode='lines',
            line=dict(color=colors.get(row['Approach'], 'gray'), width=20),
            name=row['Approach'],
            showlegend=i == 0 or row['Approach'] not in [prev['Approach'] for prev in timeline_data[:i]]
        ))
        
        # Add task labels
        fig_gantt.add_annotation(
            x=row['Start'] + (row['End'] - row['Start']) / 2,
            y=i,
            text=row['Task'],
            showarrow=False,
            font=dict(color='white', size=10)
        )
    
    fig_gantt.update_layout(
        title='Implementation Timeline - Build vs Buy',
        xaxis_title='Timeline',
        yaxis_title='Skills/Functions',
        height=max(400, len(timeline_data) * 40),
        yaxis=dict(showticklabels=False)
    )
    
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    # Resource allocation planning
    st.markdown("#### 💼 Resource Allocation Planning")
    
    resource_data = []
    total_budget = 0
    
    for func_name, func_data in all_skill_requirements.items():
        for skill_category, skill_details in func_data['skills'].items():
            skill_info = SKILLS_DATABASE.get(skill_category, {})
            
            # Estimate people and budget needed
            capability_gap = max(0, skill_details['importance_score'] - 
                               estimate_current_capability(func_name, skill_category, func_data['productivity']))
            people_needed = max(1, int(capability_gap * 0.8))
            
            # Calculate budget based on build vs buy recommendation
            market_availability = skill_info.get('market_availability', 'Medium')
            if market_availability == 'Low':
                # Build scenario
                budget = skill_info.get('training_cost', 10000) * people_needed
                budget += skill_info.get('avg_salary', 100000) * 0.8 * people_needed  # Annual cost
                approach = 'Build'
            else:
                # Buy scenario
                budget = skill_info.get('avg_salary', 100000) * 1.2 * people_needed  # Include premium
                budget += 15000 * people_needed  # Recruitment cost
                approach = 'Buy'
            
            total_budget += budget
            
            resource_data.append({
                'Function': func_name,
                'Skill Category': skill_category,
                'Approach': approach,
                'People Needed': people_needed,
                'Budget Required': budget,
                'Priority': skill_info.get('criticality', 'Medium'),
                'Timeline': f"{skill_info.get('training_time_months', 6)} months"
            })
    
    # Resource summary
    col1, col2, col3 = st.columns(3)
    
    total_people = sum(r['People Needed'] for r in resource_data)
    build_budget = sum(r['Budget Required'] for r in resource_data if r['Approach'] == 'Build')
    buy_budget = sum(r['Budget Required'] for r in resource_data if r['Approach'] == 'Buy')
    
    with col1:
        st.metric("Total People Needed", total_people)
    with col2:
        st.metric("Build Investment", f"${build_budget:,.0f}")
    with col3:
        st.metric("Buy Investment", f"${buy_budget:,.0f}")
    
    # Resource allocation table
    df_resources = pd.DataFrame(resource_data)
    df_resources['Budget Required'] = df_resources['Budget Required'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_resources, use_container_width=True)

def show_build_buy_executive_summary():
    """Executive summary of build vs buy analysis"""
    
    st.subheader("📊 Executive Summary")
    
    # Get analysis data
    all_skill_requirements = {}
    total_current_headcount = 0
    
    for func_name in st.session_state.baseline_data.keys():
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_skills = analyze_required_skills(categories)
        if func_skills:
            all_skill_requirements[func_name] = {
                'skills': func_skills,
                'headcount': baseline_data.get('headcount', 0),
                'productivity': baseline_data.get('current_productivity', 0)
            }
            total_current_headcount += baseline_data.get('headcount', 0)
    
    if not all_skill_requirements:
        st.info("No skills requirements identified. Please configure AI initiatives first.")
        return
    
    # Calculate executive metrics
    total_skills_identified = sum(len(func_data['skills']) for func_data in all_skill_requirements.values())
    
    # Estimate people and budget requirements
    total_people_needed = 0
    total_build_cost = 0
    total_buy_cost = 0
    high_priority_skills = 0
    
    for func_name, func_data in all_skill_requirements.items():
        for skill_category, skill_details in func_data['skills'].items():
            skill_info = SKILLS_DATABASE.get(skill_category, {})
            
            # People needed
            capability_gap = max(0, skill_details['importance_score'] - 
                               estimate_current_capability(func_name, skill_category, func_data['productivity']))
            people_needed = max(1, int(capability_gap * 0.8))
            total_people_needed += people_needed
            
            # Cost calculations
            market_salary = skill_info.get('avg_salary', 100000)
            training_cost = skill_info.get('training_cost', 10000)
            
            build_cost = (training_cost + market_salary * 0.8) * people_needed
            buy_cost = (market_salary * 1.2 + 15000) * people_needed
            
            total_build_cost += build_cost
            total_buy_cost += buy_cost
            
            if skill_info.get('criticality', 'Medium') == 'High':
                high_priority_skills += 1
    
    # Executive KPIs
    st.markdown("#### 🎯 Key Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Skills Categories Identified", total_skills_identified)
    with col2:
        st.metric("Additional People Needed", total_people_needed)
    with col3:
        workforce_increase = (total_people_needed / max(total_current_headcount, 1)) * 100
        st.metric("Workforce Increase", f"{workforce_increase:.1f}%")
    with col4:
        st.metric("High Priority Skills", high_priority_skills)
    
    # Financial comparison
    st.markdown("#### 💰 Financial Impact")
    
    col1, col2, col3 = st.columns(3)
    
    potential_savings = total_buy_cost - total_build_cost
    savings_percentage = (potential_savings / total_buy_cost * 100) if total_buy_cost > 0 else 0
    
    with col1:
        st.metric("Build Strategy Cost", f"${total_build_cost:,.0f}")
    with col2:
        st.metric("Buy Strategy Cost", f"${total_buy_cost:,.0f}")
    with col3:
        st.metric("Potential Savings (Build)", f"${potential_savings:,.0f}", 
                 delta=f"{savings_percentage:.1f}%")
    
    # Strategic recommendations summary
    st.markdown("#### 🎯 Strategic Recommendations")
    
    recommendations = []
    
    if savings_percentage > 20:
        recommendations.append("💰 Strong financial case for build strategy - invest in internal training programs")
    elif savings_percentage > 10:
        recommendations.append("📈 Moderate savings with build approach - consider hybrid strategy")
    else:
        recommendations.append("🎯 Buy strategy may be more effective - focus on strategic hiring")
    
    if workforce_increase > 20:
        recommendations.append("👥 Significant workforce expansion needed - establish dedicated talent acquisition team")
    
    if high_priority_skills > 3:
        recommendations.append("⚡ High number of critical skills - prioritize these for immediate action")
    
    if total_people_needed > total_current_headcount * 0.1:
        recommendations.append("🏗️ Major capability building required - consider establishing AI Center of Excellence")
    
    for rec in recommendations:
        st.markdown(f"• {rec}")
    
    # Risk assessment
    st.markdown("#### ⚠️ Risk Assessment")
    
    risk_factors = []
    
    # Calculate risk factors based on analysis
    market_scarcity_count = sum(1 for func_data in all_skill_requirements.values() 
                               for skill_cat in func_data['skills'].keys() 
                               if SKILLS_DATABASE.get(skill_cat, {}).get('market_availability') == 'Low')
    
    long_training_count = sum(1 for func_data in all_skill_requirements.values() 
                             for skill_cat in func_data['skills'].keys() 
                             if SKILLS_DATABASE.get(skill_cat, {}).get('training_time_months', 0) > 10)
    
    if market_scarcity_count > 2:
        risk_factors.append("🔴 High market scarcity for key skills - extended recruitment timelines likely")
    
    if long_training_count > 1:
        risk_factors.append("🟡 Extended training periods required - plan for temporary capability gaps")
    
    if workforce_increase > 30:
        risk_factors.append("🔴 Large workforce expansion - significant change management required")
    
    if total_build_cost > total_current_headcount * 50000:
        risk_factors.append("🟡 High training investment - ensure adequate budget allocation and ROI tracking")
    
    if not risk_factors:
        risk_factors.append("🟢 Low risk profile - proceed with recommended strategy")
    
    for risk in risk_factors:
        st.markdown(f"• {risk}")

def analyze_required_skills(categories: Dict) -> Dict[str, Dict]:
    """Analyze required skills based on AI initiatives"""
    
    required_skills = {}
    
    for category_name, category_data in categories.items():
        for init_id, init_data in category_data.get('ai_initiatives', {}).items():
            ai_type = init_data.get('ai_type', '')
            complexity = init_data.get('complexity', 'Medium')
            automation_level = init_data.get('automation_level', 0)
            
            # Map AI types to skill categories
            skill_mapping = {
                'Machine Learning': 'AI/ML Engineering',
                'Natural Language Processing': 'AI/ML Engineering', 
                'Computer Vision': 'AI/ML Engineering',
                'Automation': 'Automation Engineering',
                'Generative AI': 'AI/ML Engineering',
                'Process Automation': 'Automation Engineering',
                'Data Analytics': 'Data Science & Analytics',
                'Business Intelligence': 'Business Intelligence',
                'Predictive Analytics': 'Data Science & Analytics',
                'Risk Management': 'Data Science & Analytics',
                'Cloud Services': 'Cloud Architecture',
                'Digital Transformation': 'Digital Transformation'
            }
            
            # Determine primary skill category
            primary_skill = skill_mapping.get(ai_type, 'Digital Transformation')
            
            # Calculate importance score based on complexity and automation level
            complexity_score = {'Low': 6, 'Medium': 8, 'High': 10}.get(complexity, 8)
            automation_score = min(10, automation_level / 10)
            importance_score = (complexity_score + automation_score) / 2
            
            if primary_skill not in required_skills:
                required_skills[primary_skill] = {
                    'importance_score': importance_score,
                    'initiatives': 1,
                    'complexity_levels': [complexity]
                }
            else:
                # Update with higher importance if found
                required_skills[primary_skill]['importance_score'] = max(
                    required_skills[primary_skill]['importance_score'], 
                    importance_score
                )
                required_skills[primary_skill]['initiatives'] += 1
                required_skills[primary_skill]['complexity_levels'].append(complexity)
            
            # Add secondary skills for complex initiatives
            if complexity == 'High':
                secondary_skills = ['Cybersecurity', 'Product Management']
                for sec_skill in secondary_skills:
                    if sec_skill not in required_skills:
                        required_skills[sec_skill] = {
                            'importance_score': 6,
                            'initiatives': 1,
                            'complexity_levels': ['Medium']
                        }
    
    return required_skills

def estimate_current_capability(function_name: str, skill_category: str, productivity_score: float) -> float:
    """Estimate current capability level for a skill in a function"""
    
    # Base capability based on function type
    function_skill_baseline = {
        'IT': {'AI/ML Engineering': 4, 'Data Science & Analytics': 5, 'Cloud Architecture': 6, 'Cybersecurity': 5},
        'Sales': {'Data Science & Analytics': 3, 'Business Intelligence': 4, 'Digital Transformation': 5},
        'Marketing': {'Data Science & Analytics': 4, 'Digital Transformation': 6, 'Automation Engineering': 3},
        'Operations': {'Automation Engineering': 5, 'Process Automation': 6, 'Business Intelligence': 4},
        'Finance': {'Data Science & Analytics': 5, 'Business Intelligence': 6, 'Risk Management': 5},
        'HR': {'Digital Transformation': 4, 'Business Intelligence': 3, 'Automation Engineering': 2},
        'Customer Service': {'Automation Engineering': 3, 'Digital Transformation': 4, 'AI/ML Engineering': 2},
        'Supply Chain': {'Data Science & Analytics': 4, 'Automation Engineering': 5, 'Business Intelligence': 5},
        'R&D': {'AI/ML Engineering': 6, 'Data Science & Analytics': 7, 'Product Management': 6}
    }
    
    # Get baseline for function-skill combination
    baseline = function_skill_baseline.get(function_name, {}).get(skill_category, 3)
    
    # Adjust based on current productivity score (1-10 scale)
    productivity_multiplier = productivity_score / 10
    
    # Calculate final capability (capped at 8 to show room for improvement)
    current_capability = min(8, baseline * productivity_multiplier)
    
    return current_capability

def generate_build_buy_recommendations(all_skill_requirements: Dict) -> List[Dict]:
    """Generate specific build vs buy recommendations"""
    
    recommendations = []
    
    for func_name, func_data in all_skill_requirements.items():
        for skill_category, skill_details in func_data['skills'].items():
            skill_info = SKILLS_DATABASE.get(skill_category, {})
            
            # Decision factors
            market_availability = skill_info.get('market_availability', 'Medium')
            training_time = skill_info.get('training_time_months', 6)
            criticality = skill_info.get('criticality', 'Medium')
            avg_salary = skill_info.get('avg_salary', 100000)
            
            # Decision logic
            if market_availability == 'Low' and training_time <= 8:
                recommendation = 'Build'
                rationale = f"Low market availability ({market_availability}) makes hiring difficult, while reasonable training time ({training_time} months) makes internal development viable."
                timeline = f"{training_time + 2} months"
                key_actions = [
                    f"Design comprehensive {skill_category.lower()} training program",
                    "Identify high-potential internal candidates",
                    "Establish partnerships with training providers",
                    "Create mentorship programs with external experts"
                ]
                risks = [
                    "Training may not achieve expected proficiency levels",
                    "Key personnel may leave after training investment"
                ]
                
            elif market_availability == 'High' and avg_salary < 120000:
                recommendation = 'Buy'
                rationale = f"High market availability ({market_availability}) and reasonable salary levels (${avg_salary:,}) make external hiring cost-effective."
                timeline = "3-4 months"
                key_actions = [
                    f"Launch targeted recruitment campaign for {skill_category}",
                    "Engage specialized recruitment agencies",
                    "Develop competitive compensation packages",
                    "Streamline onboarding process"
                ]
                risks = [
                    "Extended recruitment timelines in competitive market",
                    "Cultural fit challenges with external hires"
                ]
                
            elif criticality == 'High':
                recommendation = 'Hybrid'
                rationale = f"High criticality requires both immediate capability (hire) and long-term capacity building (train)."
                timeline = "Immediate hire + 6-12 month training program"
                key_actions = [
                    f"Immediately hire 1-2 senior {skill_category.lower()} experts",
                    "Use hired experts to lead internal training programs",
                    "Develop succession planning for critical roles",
                    "Create knowledge transfer protocols"
                ]
                risks = [
                    "High cost of dual approach",
                    "Dependency on key external hires"
                ]
                
            else:
                # Default to build for most scenarios
                recommendation = 'Build'
                rationale = f"Balanced approach favoring internal development for sustainable capability building."
                timeline = f"{training_time} months"
                key_actions = [
                    f"Develop structured {skill_category.lower()} curriculum",
                    "Identify and prepare internal trainers",
                    "Create hands-on project-based learning",
                    "Establish performance assessment criteria"
                ]
                risks = [
                    "Longer time to achieve full capability",
                    "Potential skill gaps during transition"
                ]
            
            recommendations.append({
                'function': func_name,
                'skill_category': skill_category,
                'recommendation': recommendation,
                'rationale': rationale,
                'timeline': timeline,
                'key_actions': key_actions,
                'risks': risks
            })
    
    return recommendations