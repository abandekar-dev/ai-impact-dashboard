import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
from datetime import datetime

def show_performance_analysis(category_manager):
    """Performance analysis connecting departmental inputs to corporate objectives"""
    
    st.header("📊 Performance Analysis & Alignment")
    st.markdown("**Analyze how departmental AI initiatives align with corporate objectives and KPIs**")
    
    # Check if required data exists
    has_corporate_objectives = 'corporate_objectives' in st.session_state and st.session_state.corporate_objectives
    has_budget_data = 'budget_resources' in st.session_state and st.session_state.budget_resources
    has_change_data = 'change_management' in st.session_state and st.session_state.change_management
    has_function_data = len(st.session_state.baseline_data) > 0
    
    if not any([has_corporate_objectives, has_budget_data, has_change_data, has_function_data]):
        st.warning("Please configure inputs in the following sections first:")
        st.markdown("- Corporate Objectives & KPIs")
        st.markdown("- Budget & Resource Constraints") 
        st.markdown("- Change Management Readiness")
        st.markdown("- Input by Department/Business")
        return
    
    st.markdown("---")
    
    # Performance Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Objective Alignment", 
        "💰 Investment Analysis", 
        "📈 Gap Analysis", 
        "🚀 Readiness Assessment"
    ])
    
    with tab1:
        show_objective_alignment()
    
    with tab2:
        show_investment_analysis()
    
    with tab3:
        show_gap_analysis(category_manager)
    
    with tab4:
        show_readiness_assessment()

def show_objective_alignment():
    """Show how departmental initiatives align with corporate objectives"""
    
    st.subheader("🎯 Corporate Objective Alignment")
    
    if 'corporate_objectives' not in st.session_state:
        st.info("Configure Corporate Objectives & KPIs first to see alignment analysis.")
        return
    
    objectives = st.session_state.corporate_objectives
    
    # Calculate alignment scores for each department
    alignment_data = []
    
    for function_name in st.session_state.baseline_data.keys():
        # Get all AI initiatives for this function
        if f'categories_{function_name}' in st.session_state:
            categories = st.session_state[f'categories_{function_name}']
            
            total_investment = 0
            total_initiatives = 0
            alignment_scores = []
            
            for category_name, category_data in categories.items():
                initiatives = category_data.get('ai_initiatives', {})
                
                for init_id, init_data in initiatives.items():
                    total_investment += init_data.get('investment', 0)
                    total_initiatives += 1
                    
                    # Calculate alignment score based on AI type and objectives
                    alignment_score = calculate_alignment_score(init_data, objectives)
                    alignment_scores.append(alignment_score)
            
            avg_alignment = np.mean(alignment_scores) if alignment_scores else 0
            
            alignment_data.append({
                'Department': function_name,
                'Total Investment': total_investment,
                'AI Initiatives': total_initiatives,
                'Alignment Score': avg_alignment,
                'Investment per Initiative': total_investment / total_initiatives if total_initiatives > 0 else 0
            })
    
    if alignment_data:
        df = pd.DataFrame(alignment_data)
        
        # Display alignment metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_alignment = df['Alignment Score'].mean()
            alignment_color = "green" if avg_alignment > 75 else "orange" if avg_alignment > 50 else "red"
            st.metric("Overall Alignment", f"{avg_alignment:.1f}%")
            st.markdown(f":{alignment_color}[{get_alignment_level(avg_alignment)}]")
        
        with col2:
            total_investment = df['Total Investment'].sum()
            st.metric("Total Investment", f"${total_investment:,.0f}")
        
        with col3:
            total_initiatives = df['AI Initiatives'].sum()
            st.metric("Total AI Initiatives", f"{total_initiatives}")
        
        with col4:
            high_alignment_depts = len(df[df['Alignment Score'] > 75])
            st.metric("High Alignment Depts", f"{high_alignment_depts}")
        
        # Alignment visualization
        fig = px.scatter(
            df, 
            x='Total Investment', 
            y='Alignment Score',
            size='AI Initiatives',
            hover_data=['Department', 'Investment per Initiative'],
            title="Department Alignment vs Investment",
            labels={'Alignment Score': 'Alignment Score (%)', 'Total Investment': 'Total Investment ($)'}
        )
        fig.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="High Alignment Threshold")
        fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Moderate Alignment Threshold")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed alignment table
        st.markdown("#### Department Alignment Details")
        df_display = df.copy()
        df_display['Total Investment'] = df_display['Total Investment'].apply(lambda x: f"${x:,.0f}")
        df_display['Alignment Score'] = df_display['Alignment Score'].apply(lambda x: f"{x:.1f}%")
        df_display['Investment per Initiative'] = df_display['Investment per Initiative'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(df_display, use_container_width=True)
    
    else:
        st.info("No departmental AI initiatives configured yet.")

def show_investment_analysis():
    """Show investment analysis across departments and budget constraints"""
    
    st.subheader("💰 Investment Analysis")
    
    if 'budget_resources' not in st.session_state:
        st.info("Configure Budget & Resource Constraints first to see investment analysis.")
        return
    
    budget_data = st.session_state.budget_resources
    budget_allocation = budget_data.get('budget_allocation', {})
    
    # Calculate actual vs planned investment
    total_budget = budget_allocation.get('total_ai_budget', 0)
    annual_limit = budget_allocation.get('annual_budget_limit', 0)
    
    # Get actual departmental investments
    actual_investment = 0
    investment_by_dept = {}
    
    for function_name in st.session_state.baseline_data.keys():
        if f'categories_{function_name}' in st.session_state:
            categories = st.session_state[f'categories_{function_name}']
            dept_investment = 0
            
            for category_name, category_data in categories.items():
                initiatives = category_data.get('ai_initiatives', {})
                for init_data in initiatives.values():
                    dept_investment += init_data.get('investment', 0)
            
            investment_by_dept[function_name] = dept_investment
            actual_investment += dept_investment
    
    # Display budget utilization
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        budget_utilization = (actual_investment / total_budget * 100) if total_budget > 0 else 0
        util_color = "red" if budget_utilization > 100 else "orange" if budget_utilization > 80 else "green"
        st.metric("Budget Utilization", f"{budget_utilization:.1f}%")
        st.markdown(f":{util_color}[${actual_investment:,.0f} / ${total_budget:,.0f}]")
    
    with col2:
        remaining_budget = total_budget - actual_investment
        st.metric("Remaining Budget", f"${remaining_budget:,.0f}")
    
    with col3:
        annual_utilization = (actual_investment / annual_limit * 100) if annual_limit > 0 else 0
        st.metric("Annual Limit Usage", f"{annual_utilization:.1f}%")
    
    with col4:
        avg_investment = actual_investment / len(investment_by_dept) if investment_by_dept else 0
        st.metric("Avg Dept Investment", f"${avg_investment:,.0f}")
    
    # Investment distribution chart
    if investment_by_dept:
        fig = px.pie(
            values=list(investment_by_dept.values()),
            names=list(investment_by_dept.keys()),
            title="Investment Distribution by Department"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Budget category analysis
    if budget_allocation:
        st.markdown("#### Budget Category Allocation")
        
        planned_categories = {
            'Technology & Software': budget_allocation.get('technology_budget_pct', 0) / 100 * total_budget,
            'Training & Development': budget_allocation.get('training_budget_pct', 0) / 100 * total_budget,
            'Consulting & External': budget_allocation.get('consulting_budget_pct', 0) / 100 * total_budget,
            'Infrastructure & Hardware': budget_allocation.get('infrastructure_budget_pct', 0) / 100 * total_budget
        }
        
        category_df = pd.DataFrame({
            'Category': list(planned_categories.keys()),
            'Planned Budget': list(planned_categories.values()),
            'Planned %': [budget_allocation.get(f'{cat.lower().replace(" & ", "_").replace(" ", "_")}_budget_pct', 0) 
                         for cat in planned_categories.keys()]
        })
        
        fig = px.bar(
            category_df,
            x='Category',
            y='Planned Budget',
            title="Planned Budget by Category",
            text='Planned %'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

def show_gap_analysis(category_manager):
    """Show gap analysis between current state and objectives"""
    
    st.subheader("📈 Gap Analysis")
    
    if not ('corporate_objectives' in st.session_state and st.session_state.baseline_data):
        st.info("Configure Corporate Objectives and departmental data to see gap analysis.")
        return
    
    objectives = st.session_state.corporate_objectives
    strategic_obj = objectives.get('strategic_objectives', {})
    financial_kpis = objectives.get('financial_kpis', {})
    operational_kpis = objectives.get('operational_kpis', {})
    
    # Calculate current performance vs targets
    gap_analysis = []
    
    # Revenue growth analysis
    total_baseline_revenue = sum(data.get('revenue', 0) for data in st.session_state.baseline_data.values())
    total_predicted_value = sum(pred.get('value_generated', 0) for pred in st.session_state.predictions.values())
    
    if total_baseline_revenue > 0:
        actual_revenue_growth = (total_predicted_value / total_baseline_revenue) * 100
        target_revenue_growth = strategic_obj.get('revenue_growth_target', 0)
        revenue_gap = target_revenue_growth - actual_revenue_growth
        
        gap_analysis.append({
            'Metric': 'Revenue Growth',
            'Target': f"{target_revenue_growth:.1f}%",
            'Current Projection': f"{actual_revenue_growth:.1f}%",
            'Gap': f"{revenue_gap:.1f}%",
            'Status': 'On Track' if revenue_gap <= 0 else 'Below Target'
        })
    
    # ROI analysis
    roi_values = [pred.get('roi', 0) for pred in st.session_state.predictions.values()]
    avg_roi = np.mean(roi_values) if roi_values else 0
    target_roi = financial_kpis.get('roi_threshold', 0)
    roi_gap = target_roi - avg_roi
    
    gap_analysis.append({
        'Metric': 'Average ROI',
        'Target': f"{target_roi:.1f}%",
        'Current Projection': f"{avg_roi:.1f}%",
        'Gap': f"{roi_gap:.1f}%",
        'Status': 'Exceeds Target' if roi_gap <= 0 else 'Below Target'
    })
    
    # Productivity analysis
    productivity_values = [pred.get('productivity_gain', 0) for pred in st.session_state.predictions.values()]
    avg_productivity = np.mean(productivity_values) if productivity_values else 0
    target_productivity = strategic_obj.get('productivity_improvement_target', 0)
    productivity_gap = target_productivity - avg_productivity
    
    gap_analysis.append({
        'Metric': 'Productivity Improvement',
        'Target': f"{target_productivity:.1f}%",
        'Current Projection': f"{avg_productivity:.1f}%",
        'Gap': f"{productivity_gap:.1f}%",
        'Status': 'On Track' if productivity_gap <= 0 else 'Below Target'
    })
    
    # Automation target analysis
    automation_values = []
    for function_name in st.session_state.baseline_data.keys():
        if f'categories_{function_name}' in st.session_state:
            categories = st.session_state[f'categories_{function_name}']
            for category_data in categories.values():
                initiatives = category_data.get('ai_initiatives', {})
                for init_data in initiatives.values():
                    automation_values.append(init_data.get('automation_level', 0))
    
    avg_automation = np.mean(automation_values) if automation_values else 0
    target_automation = operational_kpis.get('process_automation_target', 0)
    automation_gap = target_automation - avg_automation
    
    gap_analysis.append({
        'Metric': 'Process Automation',
        'Target': f"{target_automation:.1f}%",
        'Current Projection': f"{avg_automation:.1f}%",
        'Gap': f"{automation_gap:.1f}%",
        'Status': 'On Track' if automation_gap <= 0 else 'Below Target'
    })
    
    # Display gap analysis
    if gap_analysis:
        gap_df = pd.DataFrame(gap_analysis)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        on_track_count = len(gap_df[gap_df['Status'].str.contains('Track|Exceeds')])
        below_target_count = len(gap_df[gap_df['Status'] == 'Below Target'])
        
        with col1:
            st.metric("Metrics On Track", f"{on_track_count}")
        
        with col2:
            st.metric("Metrics Below Target", f"{below_target_count}")
        
        with col3:
            alignment_pct = (on_track_count / len(gap_analysis)) * 100
            st.metric("Target Alignment", f"{alignment_pct:.0f}%")
        
        with col4:
            critical_gaps = len(gap_df[gap_df['Gap'].str.contains('-')])
            st.metric("Critical Gaps", f"{critical_gaps}")
        
        # Gap analysis table
        st.markdown("#### Detailed Gap Analysis")
        
        # Color code the status
        def highlight_status(val):
            if 'On Track' in val or 'Exceeds' in val:
                return 'background-color: lightgreen'
            elif 'Below Target' in val:
                return 'background-color: lightcoral'
            return ''
        
        styled_df = gap_df.style.applymap(highlight_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Gap visualization
        gap_values = []
        metric_names = []
        for _, row in gap_df.iterrows():
            gap_str = row['Gap'].replace('%', '')
            try:
                gap_val = float(gap_str)
                gap_values.append(gap_val)
                metric_names.append(row['Metric'])
            except ValueError:
                continue
        
        if gap_values:
            fig = go.Figure(data=go.Bar(
                x=metric_names,
                y=gap_values,
                marker_color=['red' if x > 0 else 'green' for x in gap_values],
                text=[f"{x:.1f}%" for x in gap_values],
                textposition='auto'
            ))
            fig.update_layout(
                title="Performance Gaps (Positive = Below Target)",
                yaxis_title="Gap (%)",
                xaxis_title="Metrics"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            st.plotly_chart(fig, use_container_width=True)

def show_readiness_assessment():
    """Show overall readiness assessment combining all inputs"""
    
    st.subheader("🚀 Overall Readiness Assessment")
    
    readiness_scores = {}
    
    # Corporate objectives readiness
    if 'corporate_objectives' in st.session_state:
        objectives = st.session_state.corporate_objectives
        obj_score = calculate_objectives_readiness(objectives)
        readiness_scores['Strategic Clarity'] = obj_score
    
    # Budget readiness
    if 'budget_resources' in st.session_state:
        budget = st.session_state.budget_resources
        budget_score = calculate_budget_readiness(budget)
        readiness_scores['Budget Readiness'] = budget_score
    
    # Change readiness
    if 'change_management' in st.session_state:
        change = st.session_state.change_management
        change_score = calculate_change_readiness_score(change)
        readiness_scores['Change Readiness'] = change_score
    
    # Implementation readiness
    if st.session_state.baseline_data:
        impl_score = calculate_implementation_readiness()
        readiness_scores['Implementation Readiness'] = impl_score
    
    if readiness_scores:
        overall_readiness = np.mean(list(readiness_scores.values()))
        
        # Display readiness metrics
        cols = st.columns(len(readiness_scores) + 1)
        
        for i, (category, score) in enumerate(readiness_scores.items()):
            with cols[i]:
                color = "green" if score > 75 else "orange" if score > 50 else "red"
                st.metric(category, f"{score:.0f}%")
        
        with cols[-1]:
            overall_color = "green" if overall_readiness > 75 else "orange" if overall_readiness > 50 else "red"
            st.metric("Overall Readiness", f"{overall_readiness:.0f}%")
            st.markdown(f":{overall_color}[{get_readiness_level(overall_readiness)}]")
        
        # Readiness radar chart
        categories = list(readiness_scores.keys())
        values = list(readiness_scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Readiness'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="AI Implementation Readiness Assessment"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations based on readiness
        st.markdown("#### Readiness Recommendations")
        
        recommendations = []
        
        for category, score in readiness_scores.items():
            if score < 50:
                recommendations.append(f"🔴 **{category}**: Critical attention needed (Score: {score:.0f}%)")
            elif score < 75:
                recommendations.append(f"🟡 **{category}**: Improvement recommended (Score: {score:.0f}%)")
            else:
                recommendations.append(f"🟢 **{category}**: Well prepared (Score: {score:.0f}%)")
        
        for rec in recommendations:
            st.markdown(rec)
    
    else:
        st.info("Configure input sections to see comprehensive readiness assessment.")

def calculate_alignment_score(initiative_data, objectives):
    """Calculate how well an AI initiative aligns with corporate objectives"""
    score = 50  # Base score
    
    ai_type = initiative_data.get('ai_type', '')
    automation_level = initiative_data.get('automation_level', 0)
    investment = initiative_data.get('investment', 0)
    
    strategic_obj = objectives.get('strategic_objectives', {})
    
    # Alignment based on AI type and objectives
    if 'Automation' in ai_type and strategic_obj.get('productivity_improvement_target', 0) > 20:
        score += 20
    
    if 'Analytics' in ai_type and strategic_obj.get('revenue_growth_target', 0) > 10:
        score += 15
    
    if 'Generative' in ai_type and strategic_obj.get('innovation_index_target', '') in ['Industry Leader', 'Industry Pioneer']:
        score += 25
    
    # Automation level alignment
    target_automation = objectives.get('operational_kpis', {}).get('process_automation_target', 0)
    if automation_level >= target_automation:
        score += 15
    
    return min(score, 100)

def calculate_objectives_readiness(objectives):
    """Calculate strategic objectives readiness score"""
    score = 0
    
    strategic = objectives.get('strategic_objectives', {})
    financial = objectives.get('financial_kpis', {})
    operational = objectives.get('operational_kpis', {})
    
    # Strategic objectives completeness
    if strategic.get('revenue_growth_target', 0) > 0:
        score += 20
    if strategic.get('cost_reduction_target', 0) > 0:
        score += 15
    if strategic.get('productivity_improvement_target', 0) > 0:
        score += 15
    
    # Financial KPIs completeness
    if financial.get('roi_threshold', 0) > 0:
        score += 20
    if financial.get('payback_period_max', 0) > 0:
        score += 15
    
    # Operational KPIs completeness
    if operational.get('process_automation_target', 0) > 0:
        score += 15
    
    return min(score, 100)

def calculate_budget_readiness(budget_data):
    """Calculate budget readiness score"""
    score = 0
    
    allocation = budget_data.get('budget_allocation', {})
    timeline = budget_data.get('timeline_constraints', {})
    hr = budget_data.get('human_resources', {})
    
    # Budget allocation
    if allocation.get('total_ai_budget', 0) > 0:
        score += 30
    
    # Timeline planning
    if timeline.get('full_implementation_months', 0) > 0:
        score += 20
    
    # Human resources
    if hr.get('available_fte', 0) > 0:
        score += 25
    
    # Risk management
    if budget_data.get('risk_contingency', {}).get('cost_overrun_tolerance', 0) > 0:
        score += 25
    
    return min(score, 100)

def calculate_change_readiness_score(change_data):
    """Calculate change management readiness score"""
    culture = change_data.get('organizational_culture', {})
    leadership = change_data.get('leadership_sponsorship', {})
    employee = change_data.get('employee_readiness', {})
    
    culture_score = 70  # Default moderate score
    leadership_score = 70
    employee_score = 70
    
    # Calculate based on actual data if available
    if culture:
        culture_factors = ['innovation_appetite', 'learning_orientation', 'cross_functional_collaboration']
        culture_values = [culture.get(factor, 'Moderate') for factor in culture_factors]
        # Simple scoring based on positive indicators
        culture_score = sum(50 + (i * 10) for i, val in enumerate(culture_values) 
                          if val in ['Innovative', 'Continuous', 'Strong', 'Seamless']) / len(culture_values) * 100
    
    return (culture_score + leadership_score + employee_score) / 3

def calculate_implementation_readiness():
    """Calculate implementation readiness based on configured departments"""
    score = 0
    
    total_functions = len(st.session_state.baseline_data)
    if total_functions > 0:
        score += min(total_functions * 10, 40)  # Up to 40 points for functions
    
    total_initiatives = 0
    for function_name in st.session_state.baseline_data.keys():
        if f'categories_{function_name}' in st.session_state:
            categories = st.session_state[f'categories_{function_name}']
            for category_data in categories.values():
                total_initiatives += len(category_data.get('ai_initiatives', {}))
    
    if total_initiatives > 0:
        score += min(total_initiatives * 5, 40)  # Up to 40 points for initiatives
    
    if st.session_state.predictions:
        score += 20  # 20 points for having predictions
    
    return min(score, 100)

def get_alignment_level(score):
    """Get alignment level description"""
    if score >= 80:
        return "Excellent Alignment"
    elif score >= 60:
        return "Good Alignment"
    elif score >= 40:
        return "Moderate Alignment"
    else:
        return "Poor Alignment"

def get_readiness_level(score):
    """Get readiness level description"""
    if score >= 80:
        return "High Readiness"
    elif score >= 60:
        return "Moderate Readiness"
    elif score >= 40:
        return "Low Readiness"
    else:
        return "Very Low Readiness"