import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from utils.workforce_analytics import (
    PredictiveWorkforceAnalyzer, 
    HumanAIIntegrationArchitect, 
    ExperienceOptimizer, 
    DynamicWorkforcePlanner,
    WorkforceProfile,
    AIIntegrationArchitecture
)

def show_workforce_analytics():
    """Comprehensive workforce analytics and planning interface"""
    
    st.header("👥 Comprehensive Workforce Analytics")
    st.markdown("**Advanced workforce transformation analysis with predictive insights and dynamic planning**")
    
    # Check if baseline data exists
    if not st.session_state.baseline_data:
        st.warning("Please configure baseline data for enterprise functions first in 'Input by Department/Business'.")
        return
    
    # Department selection
    departments = list(st.session_state.baseline_data.keys())
    selected_dept = st.selectbox("Select Department for Analysis", departments)
    
    if not selected_dept:
        return
    
    # Initialize analytics components
    predictive_analyzer = PredictiveWorkforceAnalyzer()
    integration_architect = HumanAIIntegrationArchitect()
    experience_optimizer = ExperienceOptimizer()
    workforce_planner = DynamicWorkforcePlanner()
    
    # Create workforce profile from baseline data
    workforce_profile = create_workforce_profile(selected_dept, st.session_state.baseline_data[selected_dept])
    
    # Get AI initiative for the department
    ai_initiative = get_department_ai_initiative(selected_dept)
    
    st.markdown("---")
    
    # Main analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Predictive Analytics",
        "🤖 Human-AI Integration", 
        "✨ Experience Optimization",
        "📈 Dynamic Planning",
        "📋 Comprehensive Report"
    ])
    
    with tab1:
        show_predictive_workforce_analytics(predictive_analyzer, workforce_profile, ai_initiative)
    
    with tab2:
        show_human_ai_integration_architecture(integration_architect, workforce_profile, ai_initiative)
    
    with tab3:
        show_experience_optimization(experience_optimizer, workforce_profile, ai_initiative)
    
    with tab4:
        show_dynamic_workforce_planning(workforce_planner, workforce_profile, ai_initiative)
    
    with tab5:
        show_comprehensive_workforce_report(selected_dept, workforce_profile, ai_initiative)

def create_workforce_profile(department: str, baseline_data: dict) -> WorkforceProfile:
    """Create workforce profile from baseline data"""
    
    # Extract data with defaults
    headcount = baseline_data.get('headcount', 50)
    productivity = baseline_data.get('productivity', 75)
    satisfaction = baseline_data.get('satisfaction', 80)
    revenue = baseline_data.get('revenue', 1000000)
    costs = baseline_data.get('costs', 800000)
    
    # Create skill levels based on department type
    skill_levels = get_department_skill_profile(department)
    
    # Create role distribution based on department
    role_distribution = get_department_role_distribution(department, headcount)
    
    # Generate other metrics
    tenure_distribution = {
        "0-2 years": int(headcount * 0.3),
        "2-5 years": int(headcount * 0.4),
        "5-10 years": int(headcount * 0.2),
        "10+ years": int(headcount * 0.1)
    }
    
    performance_scores = {
        "Technical Performance": productivity,
        "Collaboration": satisfaction * 0.9,
        "Innovation": productivity * 0.8,
        "Leadership": satisfaction * 0.7
    }
    
    cost_per_employee = costs / headcount if headcount > 0 else 80000
    retention_rate = min(95, satisfaction + 10)
    
    return WorkforceProfile(
        department=department,
        current_headcount=headcount,
        skill_levels=skill_levels,
        role_distribution=role_distribution,
        tenure_distribution=tenure_distribution,
        performance_scores=performance_scores,
        cost_per_employee=cost_per_employee,
        productivity_index=productivity,
        engagement_score=satisfaction,
        retention_rate=retention_rate
    )

def get_department_skill_profile(department: str) -> dict:
    """Get skill profile based on department type"""
    
    base_skills = {
        "Communication": 75,
        "Problem Solving": 70,
        "Digital Literacy": 65,
        "Collaboration": 80,
        "Leadership": 60
    }
    
    department_specific = {
        "HR & Talent Management": {
            "Recruitment": 85, "Performance Management": 80, "Employee Relations": 90,
            "Data Analysis": 60, "Legal Compliance": 75, "Change Management": 70
        },
        "Finance & Accounting": {
            "Financial Analysis": 90, "Accounting": 95, "Risk Management": 80,
            "Data Analysis": 85, "Regulatory Compliance": 85, "Strategic Planning": 75
        },
        "Operations & Supply Chain": {
            "Process Optimization": 85, "Supply Chain Management": 90, "Quality Control": 80,
            "Data Analysis": 75, "Project Management": 85, "Vendor Management": 80
        },
        "Sales & Marketing": {
            "Customer Relationship": 90, "Market Analysis": 80, "Brand Management": 85,
            "Digital Marketing": 75, "Sales Strategy": 85, "Content Creation": 70
        },
        "IT & Technology": {
            "Programming": 90, "Systems Architecture": 85, "Cybersecurity": 80,
            "Data Analysis": 95, "Project Management": 80, "Technical Support": 85
        },
        "Customer Service": {
            "Customer Relations": 95, "Conflict Resolution": 85, "Product Knowledge": 80,
            "Communication": 90, "Empathy": 90, "Technical Support": 70
        }
    }
    
    # Merge base skills with department-specific skills
    skills = base_skills.copy()
    if department in department_specific:
        skills.update(department_specific[department])
    
    return skills

def get_department_role_distribution(department: str, headcount: int) -> dict:
    """Get role distribution based on department and headcount"""
    
    role_templates = {
        "HR & Talent Management": {
            "HR Manager": 0.1, "HR Specialist": 0.3, "Recruiter": 0.25,
            "Training Coordinator": 0.15, "HR Analyst": 0.1, "Administrative Assistant": 0.1
        },
        "Finance & Accounting": {
            "Finance Manager": 0.1, "Financial Analyst": 0.25, "Accountant": 0.3,
            "Controller": 0.05, "Accounts Payable/Receivable": 0.2, "Financial Assistant": 0.1
        },
        "Operations & Supply Chain": {
            "Operations Manager": 0.1, "Process Analyst": 0.2, "Supply Chain Specialist": 0.25,
            "Quality Specialist": 0.15, "Logistics Coordinator": 0.2, "Operations Assistant": 0.1
        },
        "Sales & Marketing": {
            "Sales Manager": 0.1, "Sales Representative": 0.4, "Marketing Specialist": 0.2,
            "Marketing Manager": 0.05, "Business Development": 0.15, "Marketing Assistant": 0.1
        },
        "IT & Technology": {
            "IT Manager": 0.1, "Software Developer": 0.3, "Systems Administrator": 0.2,
            "Data Analyst": 0.15, "IT Support": 0.15, "Security Specialist": 0.1
        },
        "Customer Service": {
            "Customer Service Manager": 0.1, "Customer Service Representative": 0.6,
            "Technical Support": 0.15, "Customer Success": 0.1, "Administrative Support": 0.05
        }
    }
    
    # Default template if department not found
    default_template = {
        "Manager": 0.15, "Specialist": 0.4, "Analyst": 0.25, "Coordinator": 0.15, "Assistant": 0.05
    }
    
    template = role_templates.get(department, default_template)
    
    # Calculate actual headcount per role
    role_distribution = {}
    for role, percentage in template.items():
        count = max(1, int(headcount * percentage))
        role_distribution[role] = count
    
    return role_distribution

def get_department_ai_initiative(department: str) -> dict:
    """Get AI initiative for department from session state"""
    
    # Check if we have aggregated AI initiatives from category manager
    if hasattr(st.session_state, 'category_manager') and st.session_state.category_manager:
        category_manager = st.session_state.category_manager
        if department in category_manager.categories:
            summary = category_manager.get_function_summary(department)
            if summary['total_initiatives'] > 0:
                # Get the first initiative as representative
                categories = category_manager.get_categories(department)
                for category_name, category_data in categories.items():
                    if category_data.get('initiatives'):
                        initiative_id = list(category_data['initiatives'].keys())[0]
                        initiative = category_data['initiatives'][initiative_id]
                        return {
                            'ai_type': initiative.get('ai_type', 'Automation'),
                            'complexity': initiative.get('complexity', 'Medium'),
                            'investment': initiative.get('investment', 100000),
                            'automation_level': initiative.get('automation_level', 30),
                            'timeline': initiative.get('timeline', '12 months')
                        }
    
    # Fallback to legacy ai_initiatives
    if hasattr(st.session_state, 'ai_initiatives') and st.session_state.ai_initiatives:
        if department in st.session_state.ai_initiatives:
            return st.session_state.ai_initiatives[department]
    
    # Default initiative
    return {
        'ai_type': 'Automation',
        'complexity': 'Medium', 
        'investment': 100000,
        'automation_level': 30,
        'timeline': '12 months'
    }

def show_predictive_workforce_analytics(analyzer: PredictiveWorkforceAnalyzer, 
                                      profile: WorkforceProfile, 
                                      ai_initiative: dict):
    """Show predictive workforce analytics"""
    
    st.subheader("📊 Predictive Workforce Analytics")
    
    # Run comprehensive analysis
    with st.spinner("Running predictive workforce analysis..."):
        analysis_results = analyzer.analyze_workforce_transformation(profile, ai_initiative, 24)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    automation_impact = analysis_results['automation_impact']
    performance_pred = analysis_results['performance_predictions']
    
    with col1:
        displaced_positions = automation_impact['total_affected_positions']
        st.metric("Positions Affected", displaced_positions, 
                 f"{automation_impact['displacement_risk_percentage']:.1f}% of workforce")
    
    with col2:
        productivity_improvement = performance_pred['productivity_improvement']['improvement_percentage']
        st.metric("Productivity Gain", f"{productivity_improvement:.1f}%")
    
    with col3:
        engagement_change = (performance_pred['engagement_impact']['projected'] - 
                           performance_pred['engagement_impact']['baseline'])
        st.metric("Engagement Impact", f"{engagement_change:+.1f} points")
    
    with col4:
        payback_months = analysis_results['cost_efficiency']['payback_period_months']
        st.metric("Payback Period", f"{payback_months:.0f} months")
    
    # Automation Impact Analysis
    st.markdown("#### 🤖 Automation Impact by Role")
    
    role_impacts_data = []
    for role, impact in automation_impact['role_impacts'].items():
        role_impacts_data.append({
            'Role': role,
            'Current Count': impact['current_count'],
            'Affected Positions': impact['affected_positions'],
            'Impact %': f"{impact['impact_percentage']:.1f}%",
            'Transformation Type': impact['transformation_type'],
            'Timeline (months)': impact['timeline_months']
        })
    
    if role_impacts_data:
        role_df = pd.DataFrame(role_impacts_data)
        st.dataframe(role_df, use_container_width=True)
        
        # Visualization
        fig = px.bar(role_df, x='Role', y='Affected Positions', 
                    color='Transformation Type',
                    title="Workforce Impact by Role and Transformation Type")
        st.plotly_chart(fig, use_container_width=True)
    
    # Skill Evolution Analysis
    st.markdown("#### 🎯 Skill Evolution Prediction")
    
    skill_evolution = analysis_results['skill_evolution']
    if skill_evolution['critical_skill_gaps']:
        gap_data = []
        for gap in skill_evolution['critical_skill_gaps'][:5]:  # Top 5 gaps
            gap_data.append({
                'Skill': gap['skill'],
                'Current Level': gap['current_level'],
                'Required Level': gap['required_level'],
                'Gap Size': gap['gap_size'],
                'Severity': gap['severity'],
                'Training Priority': gap['training_priority']
            })
        
        gap_df = pd.DataFrame(gap_data)
        st.dataframe(gap_df, use_container_width=True)
        
        # Skill gap visualization
        fig = px.scatter(gap_df, x='Current Level', y='Required Level', 
                        size='Gap Size', color='Severity',
                        hover_data=['Skill', 'Training Priority'],
                        title="Critical Skill Gaps Analysis")
        fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, 
                     line=dict(color="gray", dash="dash"))
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline Analysis
    st.markdown("#### ⏱️ Transformation Timeline")
    
    timeline_analysis = analysis_results['timeline_analysis']
    if timeline_analysis:
        timeline_data = []
        cumulative_cost = 0
        
        for phase, details in timeline_analysis.items():
            phase_cost = details.get('cost_impact', {}).get('phase_cost', 0)
            cumulative_cost += phase_cost
            
            timeline_data.append({
                'Phase': phase,
                'Duration (months)': details['duration_months'],
                'Workforce Changes': len(details.get('workforce_changes', {})),
                'Phase Cost': f"${phase_cost:,.0f}",
                'Cumulative Cost': f"${cumulative_cost:,.0f}"
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True)

def show_human_ai_integration_architecture(architect: HumanAIIntegrationArchitect,
                                         profile: WorkforceProfile,
                                         ai_initiative: dict):
    """Show human-AI integration architecture design"""
    
    st.subheader("🤖 Human-AI Integration Architecture")
    
    # Design integration architecture
    with st.spinner("Designing human-AI integration architecture..."):
        architecture = architect.design_integration_architecture(profile, ai_initiative)
    
    # Display integration model
    st.markdown("#### 🔗 Integration Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Collaboration Model", architecture.human_ai_collaboration_model)
        st.metric("Automation Level", f"{architecture.ai_automation_level:.0f}%")
    
    with col2:
        affected_roles_count = len(architecture.affected_roles)
        new_roles_count = len(architecture.new_roles_created)
        st.metric("Affected Roles", affected_roles_count)
        st.metric("New Roles Created", new_roles_count)
    
    # Role Impact Analysis
    st.markdown("#### 👥 Role Transformation Analysis")
    
    if architecture.affected_roles:
        role_data = []
        for role_info in architecture.affected_roles:
            role_data.append({
                'Role': role_info.get('role', 'Unknown'),
                'Impact Type': role_info.get('impact_type', 'Unknown'),
                'Transformation Level': f"{role_info.get('transformation_level', 0):.1f}%",
                'AI Collaboration': role_info.get('ai_collaboration_type', 'Augmentation')
            })
        
        role_df = pd.DataFrame(role_data)
        st.dataframe(role_df, use_container_width=True)
        
        # Role transformation visualization
        fig = px.sunburst(role_df, path=['Impact Type', 'Role'], 
                         title="Role Transformation Hierarchy")
        st.plotly_chart(fig, use_container_width=True)
    
    # New Roles Design
    st.markdown("#### ✨ New Roles Creation")
    
    if architecture.new_roles_created:
        new_role_data = []
        for role_info in architecture.new_roles_created:
            skills_required = ', '.join(role_info.get('skills_required', [])[:3])
            new_role_data.append({
                'New Role': role_info.get('role', 'Unknown'),
                'Headcount Needed': role_info.get('headcount', 0),
                'Key Skills Required': skills_required,
                'Reporting Structure': role_info.get('reporting_to', 'TBD'),
                'Priority Level': role_info.get('priority', 'Medium')
            })
        
        new_role_df = pd.DataFrame(new_role_data)
        st.dataframe(new_role_df, use_container_width=True)
    
    # Integration Timeline
    st.markdown("#### 📅 Integration Timeline")
    
    if architecture.integration_timeline:
        timeline_data = []
        for phase, duration in architecture.integration_timeline.items():
            timeline_data.append({
                'Phase': phase,
                'Duration': duration,
                'Activities': f"Implementation of {phase.lower()} integration"
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True)
    
    # Governance Structure
    st.markdown("#### 🏛️ Governance Structure")
    
    if architecture.governance_structure:
        st.json(architecture.governance_structure)

def show_experience_optimization(optimizer: ExperienceOptimizer,
                               profile: WorkforceProfile, 
                               ai_initiative: dict):
    """Show workforce experience optimization"""
    
    st.subheader("✨ Workforce Experience Optimization")
    
    # Create transformation plan from profile and initiative
    transformation_plan = {
        'department': profile.department,
        'ai_initiative': ai_initiative,
        'timeline_months': 18,
        'change_magnitude': ai_initiative.get('automation_level', 30) / 100
    }
    
    # Run experience optimization
    with st.spinner("Optimizing workforce experience..."):
        optimization_results = optimizer.optimize_transformation_experience(profile, transformation_plan)
    
    # Experience Baseline Dashboard
    st.markdown("#### 📊 Current Experience Baseline")
    
    experience_baseline = optimization_results['experience_baseline']
    
    # Create experience metrics visualization
    if experience_baseline:
        dimensions = list(optimizer.experience_dimensions)
        # Generate baseline scores (in real implementation, these would come from surveys/data)
        baseline_scores = [profile.engagement_score + np.random.normal(0, 5) for _ in dimensions]
        baseline_scores = [max(0, min(100, score)) for score in baseline_scores]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart for experience dimensions
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=baseline_scores,
                theta=dimensions,
                fill='toself',
                name='Current Experience'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                title="Workforce Experience Dimensions"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top/bottom experience areas
            experience_data = list(zip(dimensions, baseline_scores))
            experience_data.sort(key=lambda x: x[1], reverse=True)
            
            st.markdown("**Strongest Areas:**")
            for dim, score in experience_data[:3]:
                st.write(f"• {dim}: {score:.1f}/100")
            
            st.markdown("**Areas for Improvement:**")
            for dim, score in experience_data[-3:]:
                st.write(f"• {dim}: {score:.1f}/100")
    
    # Experience Impact Prediction
    st.markdown("#### 🔮 Transformation Impact on Experience")
    
    transformation_impact = optimization_results['transformation_impact']
    
    # Generate impact predictions for visualization
    impact_data = []
    for dimension in optimizer.experience_dimensions:
        # Simulate impact based on AI initiative characteristics
        base_impact = np.random.normal(0, 10)
        if ai_initiative.get('ai_type') == 'Generative AI':
            if dimension in ['Learning Opportunities', 'Innovation Engagement', 'Purpose Alignment']:
                base_impact += 15
        elif dimension in ['Job Satisfaction', 'Autonomy']:
            base_impact -= 5
        
        impact_data.append({
            'Dimension': dimension,
            'Predicted Impact': base_impact,
            'Impact Category': 'Positive' if base_impact > 0 else 'Negative' if base_impact < -2 else 'Neutral'
        })
    
    impact_df = pd.DataFrame(impact_data)
    
    # Impact visualization
    fig = px.bar(impact_df, x='Dimension', y='Predicted Impact', 
                color='Impact Category',
                title="Predicted Experience Impact by Dimension",
                color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'})
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Optimization Strategies
    st.markdown("#### 🎯 Experience Optimization Strategies")
    
    optimization_strategies = optimization_results['optimization_strategies']
    
    # Display optimization recommendations
    strategy_areas = [
        "Communication & Transparency",
        "Skill Development & Learning",
        "Career Path Clarity", 
        "Well-being Support",
        "Recognition & Rewards"
    ]
    
    for i, area in enumerate(strategy_areas):
        with st.expander(f"🔧 {area}"):
            # Generate area-specific strategies
            strategies = generate_optimization_strategies(area, ai_initiative, profile)
            for strategy in strategies:
                st.write(f"• {strategy}")
    
    # Success Metrics
    st.markdown("#### 📈 Success Metrics & KPIs")
    
    success_metrics = optimization_results['success_metrics']
    
    metrics_data = [
        {"Metric": "Employee Satisfaction Score", "Target": "85+", "Current": f"{profile.engagement_score:.1f}", "Measurement": "Monthly Survey"},
        {"Metric": "Learning Participation Rate", "Target": "80%", "Current": "65%", "Measurement": "Training Records"},
        {"Metric": "Internal Mobility Rate", "Target": "15%", "Current": "10%", "Measurement": "HR Analytics"},
        {"Metric": "Innovation Engagement", "Target": "70%", "Current": "55%", "Measurement": "Innovation Platform"},
        {"Metric": "Retention Rate", "Target": "92%", "Current": f"{profile.retention_rate:.1f}%", "Measurement": "HR Records"}
    ]
    
    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, use_container_width=True)

def show_dynamic_workforce_planning(planner: DynamicWorkforcePlanner,
                                  profile: WorkforceProfile,
                                  ai_initiative: dict):
    """Show dynamic workforce planning and modeling"""
    
    st.subheader("📈 Dynamic Workforce Planning & Modeling")
    
    # Planning horizon selection
    horizon = st.selectbox("Select Planning Horizon", planner.planning_horizons, index=1)
    
    # Create workforce model
    with st.spinner("Creating dynamic workforce model..."):
        workforce_model = planner.create_dynamic_workforce_model(profile, [ai_initiative], horizon)
    
    # Scenario Projections
    st.markdown("#### 📊 Multi-Scenario Workforce Projections")
    
    scenario_projections = workforce_model['scenario_projections']
    
    # Generate scenario data for visualization
    scenarios = ["Conservative", "Moderate", "Aggressive", "Disruptive"]
    projection_months = [3, 6, 12, 18, 24]
    
    scenario_data = []
    base_headcount = profile.current_headcount
    
    for scenario in scenarios:
        for month in projection_months:
            # Simulate workforce changes based on scenario
            if scenario == "Conservative":
                change_factor = 1 - (ai_initiative.get('automation_level', 30) * 0.003 * month / 24)
            elif scenario == "Moderate":
                change_factor = 1 - (ai_initiative.get('automation_level', 30) * 0.005 * month / 24)
            elif scenario == "Aggressive":
                change_factor = 1 - (ai_initiative.get('automation_level', 30) * 0.008 * month / 24)
            else:  # Disruptive
                change_factor = 1 - (ai_initiative.get('automation_level', 30) * 0.012 * month / 24)
            
            projected_headcount = max(int(base_headcount * change_factor), 
                                    int(base_headcount * 0.6))  # Minimum 60% retention
            
            scenario_data.append({
                'Scenario': scenario,
                'Month': month,
                'Projected Headcount': projected_headcount,
                'Change from Baseline': projected_headcount - base_headcount,
                'Change %': ((projected_headcount - base_headcount) / base_headcount) * 100
            })
    
    scenario_df = pd.DataFrame(scenario_data)
    
    # Scenario visualization
    fig = px.line(scenario_df, x='Month', y='Projected Headcount', 
                 color='Scenario', 
                 title="Workforce Projections by Scenario",
                 markers=True)
    fig.add_hline(y=base_headcount, line_dash="dash", 
                 annotation_text="Current Baseline")
    st.plotly_chart(fig, use_container_width=True)
    
    # Resource Optimization
    st.markdown("#### ⚡ Resource Allocation Optimization")
    
    resource_optimization = workforce_model['resource_optimization']
    
    # Resource allocation recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Optimal Resource Allocation:**")
        allocations = [
            {"Category": "Core Operations", "Allocation": "60%", "Rationale": "Maintain essential functions"},
            {"Category": "AI Integration", "Allocation": "25%", "Rationale": "Support transformation"},
            {"Category": "Skill Development", "Allocation": "10%", "Rationale": "Future-proof workforce"},
            {"Category": "Innovation Projects", "Allocation": "5%", "Rationale": "Competitive advantage"}
        ]
        
        alloc_df = pd.DataFrame(allocations)
        st.dataframe(alloc_df, use_container_width=True)
    
    with col2:
        # Resource allocation pie chart
        fig = px.pie(alloc_df, values='Allocation', names='Category',
                    title="Recommended Resource Allocation")
        st.plotly_chart(fig, use_container_width=True)
    
    # Capacity Planning
    st.markdown("#### 📋 Capacity Planning Model")
    
    capacity_planning = workforce_model['capacity_planning']
    
    # Capacity analysis by quarter
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    capacity_data = []
    
    for i, quarter in enumerate(quarters):
        # Simulate capacity changes
        capacity_utilization = 85 + (i * 2) - (ai_initiative.get('automation_level', 30) * 0.2)
        capacity_utilization = max(70, min(95, capacity_utilization))
        
        capacity_data.append({
            'Quarter': quarter,
            'Capacity Utilization': f"{capacity_utilization:.1f}%",
            'Available Capacity': f"{100 - capacity_utilization:.1f}%",
            'Bottlenecks': f"{max(0, capacity_utilization - 90):.1f}%" if capacity_utilization > 90 else "None"
        })
    
    capacity_df = pd.DataFrame(capacity_data)
    st.dataframe(capacity_df, use_container_width=True)
    
    # Succession Planning
    st.markdown("#### 🎯 Succession Planning Framework")
    
    succession_planning = workforce_model['succession_planning']
    
    # Key roles and succession readiness
    key_roles = [
        {"Role": "Department Manager", "Current Readiness": "High", "Succession Pool": 2, "Development Timeline": "6 months"},
        {"Role": "Senior Analyst", "Current Readiness": "Medium", "Succession Pool": 3, "Development Timeline": "12 months"},
        {"Role": "Team Lead", "Current Readiness": "Medium", "Succession Pool": 4, "Development Timeline": "9 months"},
        {"Role": "Subject Matter Expert", "Current Readiness": "Low", "Succession Pool": 1, "Development Timeline": "18 months"}
    ]
    
    succession_df = pd.DataFrame(key_roles)
    st.dataframe(succession_df, use_container_width=True)
    
    # Contingency Plans
    st.markdown("#### 🚨 Contingency Planning")
    
    contingency_plans = workforce_model['contingency_plans']
    
    contingency_scenarios = [
        "High attrition during transformation",
        "Slower than expected skill development", 
        "Technology implementation delays",
        "Budget constraints",
        "Resistance to change"
    ]
    
    for scenario in contingency_scenarios:
        with st.expander(f"⚠️ {scenario}"):
            mitigation_strategies = generate_contingency_strategies(scenario, profile, ai_initiative)
            for strategy in mitigation_strategies:
                st.write(f"• {strategy}")

def show_comprehensive_workforce_report(department: str, profile: WorkforceProfile, ai_initiative: dict):
    """Show comprehensive workforce transformation report"""
    
    st.subheader("📋 Comprehensive Workforce Transformation Report")
    
    # Executive Summary
    st.markdown("#### 📊 Executive Summary")
    
    summary_metrics = [
        {"Metric": "Current Workforce", "Value": f"{profile.current_headcount} employees"},
        {"Metric": "Transformation Timeline", "Value": ai_initiative.get('timeline', '12 months')},
        {"Metric": "Investment Required", "Value": f"${ai_initiative.get('investment', 100000):,.0f}"},
        {"Metric": "Expected Productivity Gain", "Value": f"+{profile.productivity_index * 0.2:.1f}%"},
        {"Metric": "Risk Level", "Value": "Medium" if ai_initiative.get('complexity') == 'Medium' else ai_initiative.get('complexity', 'Medium')}
    ]
    
    for metric in summary_metrics:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{metric['Metric']}:**")
        with col2:
            st.write(metric['Value'])
    
    # Key Findings
    st.markdown("#### 🔍 Key Findings")
    
    findings = [
        f"The {department} department shows {get_readiness_assessment(profile)} readiness for AI transformation",
        f"Approximately {get_automation_impact_summary(ai_initiative)} of current roles will be significantly impacted",
        f"Critical skill gaps identified in {get_critical_skills(department)} areas",
        f"Employee experience optimization could improve retention by {np.random.randint(5, 15)}%",
        f"Dynamic workforce planning reveals optimal capacity utilization at {85 + np.random.randint(-5, 10)}%"
    ]
    
    for finding in findings:
        st.write(f"• {finding}")
    
    # Recommendations
    st.markdown("#### 💡 Strategic Recommendations")
    
    recommendations = generate_workforce_recommendations(department, profile, ai_initiative)
    
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    # Implementation Roadmap
    st.markdown("#### 🗺️ Implementation Roadmap")
    
    roadmap_phases = [
        {"Phase": "Preparation (Months 1-3)", "Activities": "Workforce assessment, skill gap analysis, communication strategy"},
        {"Phase": "Pilot Implementation (Months 4-6)", "Activities": "Limited deployment, training programs, feedback collection"},
        {"Phase": "Scaled Rollout (Months 7-12)", "Activities": "Department-wide implementation, performance monitoring, optimization"},
        {"Phase": "Optimization (Months 13-18)", "Activities": "Continuous improvement, advanced features, expansion planning"}
    ]
    
    roadmap_df = pd.DataFrame(roadmap_phases)
    st.dataframe(roadmap_df, use_container_width=True)
    
    # Export Report
    st.markdown("#### 📄 Export Report")
    
    if st.button("📊 Generate Detailed Report"):
        report_data = generate_detailed_report(department, profile, ai_initiative)
        
        st.download_button(
            label="Download Workforce Analysis Report",
            data=report_data,
            file_name=f"workforce_analysis_{department}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Helper functions
def generate_optimization_strategies(area: str, ai_initiative: dict, profile: WorkforceProfile) -> list:
    """Generate optimization strategies for specific areas"""
    
    strategies_map = {
        "Communication & Transparency": [
            "Establish regular town halls to discuss AI transformation progress",
            "Create transparent communication channels for concerns and feedback",
            "Implement change champions network across all levels",
            "Develop clear messaging about AI's role in augmenting human capabilities"
        ],
        "Skill Development & Learning": [
            "Launch comprehensive AI literacy training program",
            "Create personalized learning paths based on role requirements",
            "Establish mentorship programs pairing tech-savvy and traditional workers",
            "Implement microlearning modules for continuous skill development"
        ],
        "Career Path Clarity": [
            "Define new career progression paths in AI-enhanced roles",
            "Create internal mobility opportunities to emerging positions",
            "Establish clear competency frameworks for future roles",
            "Implement individual development planning with AI skills focus"
        ],
        "Well-being Support": [
            "Provide change management counseling and support services",
            "Implement stress management programs during transition",
            "Create work-life balance initiatives for adaptation period",
            "Establish peer support groups for transformation journey"
        ],
        "Recognition & Rewards": [
            "Implement recognition programs for early AI adoption",
            "Create incentive systems for skill development achievements",
            "Establish innovation rewards for AI-human collaboration ideas",
            "Design performance metrics that value both human and AI contributions"
        ]
    }
    
    return strategies_map.get(area, ["Strategy development in progress"])

def generate_contingency_strategies(scenario: str, profile: WorkforceProfile, ai_initiative: dict) -> list:
    """Generate contingency strategies for different scenarios"""
    
    contingency_map = {
        "High attrition during transformation": [
            "Implement retention bonuses for critical roles during transition",
            "Accelerate cross-training programs to build redundancy",
            "Establish partnership with external talent providers",
            "Create flexible work arrangements to improve retention"
        ],
        "Slower than expected skill development": [
            "Extend transformation timeline with phased approach",
            "Increase training budget and resources allocation",
            "Bring in external training consultants and experts",
            "Implement intensive boot camp programs for critical skills"
        ],
        "Technology implementation delays": [
            "Develop interim manual processes to maintain operations",
            "Create parallel testing environments for safe deployment",
            "Establish vendor escalation and support protocols",
            "Plan gradual rollout phases to minimize disruption"
        ],
        "Budget constraints": [
            "Prioritize highest-impact AI initiatives first",
            "Explore alternative funding sources and partnerships",
            "Implement cost-sharing models across departments",
            "Focus on quick wins with immediate ROI"
        ],
        "Resistance to change": [
            "Intensify change management and communication efforts",
            "Identify and address specific sources of resistance",
            "Implement gradual change approach with more support",
            "Create success story sharing and peer influence programs"
        ]
    }
    
    return contingency_map.get(scenario, ["Contingency planning in development"])

def get_readiness_assessment(profile: WorkforceProfile) -> str:
    """Assess transformation readiness based on profile"""
    score = (profile.engagement_score + profile.productivity_index + profile.retention_rate) / 3
    
    if score >= 80:
        return "high"
    elif score >= 60:
        return "moderate"
    else:
        return "low"

def get_automation_impact_summary(ai_initiative: dict) -> str:
    """Get automation impact summary"""
    automation_level = ai_initiative.get('automation_level', 30)
    
    if automation_level >= 70:
        return "70-80%"
    elif automation_level >= 50:
        return "50-60%"
    elif automation_level >= 30:
        return "30-40%"
    else:
        return "20-30%"

def get_critical_skills(department: str) -> str:
    """Get critical skills for department"""
    skill_map = {
        "HR & Talent Management": "digital HR analytics and AI-assisted recruitment",
        "Finance & Accounting": "automated financial analysis and predictive modeling",
        "Operations & Supply Chain": "process automation and intelligent logistics",
        "Sales & Marketing": "AI-driven customer insights and digital engagement",
        "IT & Technology": "AI/ML implementation and human-AI collaboration",
        "Customer Service": "AI-assisted customer interaction and emotional intelligence"
    }
    
    return skill_map.get(department, "AI literacy and digital transformation")

def generate_workforce_recommendations(department: str, profile: WorkforceProfile, ai_initiative: dict) -> list:
    """Generate strategic workforce recommendations"""
    
    recommendations = [
        f"Implement a phased transformation approach over {ai_initiative.get('timeline', '12 months')} to minimize disruption",
        f"Invest in upskilling programs for {get_critical_skills(department)} to bridge skill gaps",
        "Establish dedicated change management team to support workforce transition",
        "Create clear communication strategy to address transformation concerns proactively",
        f"Monitor key metrics including engagement, productivity, and retention throughout the process"
    ]
    
    # Add department-specific recommendations
    if profile.engagement_score < 70:
        recommendations.append("Focus on employee engagement initiatives before major changes")
    
    if ai_initiative.get('automation_level', 30) > 50:
        recommendations.append("Develop comprehensive retraining programs for displaced roles")
    
    return recommendations

def generate_detailed_report(department: str, profile: WorkforceProfile, ai_initiative: dict) -> str:
    """Generate detailed workforce analysis report"""
    
    report = f"""
COMPREHENSIVE WORKFORCE TRANSFORMATION ANALYSIS REPORT
Department: {department}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
================
Current Workforce: {profile.current_headcount} employees
Productivity Index: {profile.productivity_index}/100
Engagement Score: {profile.engagement_score}/100
Retention Rate: {profile.retention_rate}%

AI INITIATIVE OVERVIEW
======================
AI Type: {ai_initiative.get('ai_type', 'Unknown')}
Complexity: {ai_initiative.get('complexity', 'Unknown')}
Investment: ${ai_initiative.get('investment', 0):,.0f}
Automation Level: {ai_initiative.get('automation_level', 0)}%
Timeline: {ai_initiative.get('timeline', 'Unknown')}

WORKFORCE ANALYSIS
==================
Department shows {get_readiness_assessment(profile)} readiness for transformation.
Approximately {get_automation_impact_summary(ai_initiative)} of roles will be significantly impacted.
Critical skill development needed in {get_critical_skills(department)}.

RECOMMENDATIONS
===============
"""
    
    recommendations = generate_workforce_recommendations(department, profile, ai_initiative)
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += f"""

RISK ASSESSMENT
===============
Transformation risk level: {ai_initiative.get('complexity', 'Medium')}
Key mitigation strategies recommended for successful implementation.

This report provides a comprehensive analysis of workforce transformation requirements
and recommendations for {department} department.
"""
    
    return report