import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

def show_comparative_analysis():
    """Comprehensive before/after comparative analysis of AI initiatives vs baseline metrics"""
    
    st.title("📊 Comparative Analysis: Before vs After AI Implementation")
    st.markdown("**Analyze the transformational impact of AI initiatives on enterprise metrics**")
    
    # Check if we have baseline data and AI initiatives
    if not hasattr(st.session_state, 'baseline_data') or not st.session_state.baseline_data:
        st.warning("Please configure enterprise functions in Enhanced Function Analysis first.")
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
        st.info("No AI initiatives configured yet. Please add AI initiatives in Enhanced Function Analysis to see comparative analysis.")
        return
    
    # Analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Metrics Comparison", 
        "💰 Financial Impact", 
        "👥 Workforce Transformation", 
        "⚡ Performance Analytics",
        "📋 Executive Dashboard"
    ])
    
    with tab1:
        show_metrics_comparison(functions_with_ai)
    
    with tab2:
        show_financial_impact_analysis(functions_with_ai)
    
    with tab3:
        show_workforce_transformation_analysis(functions_with_ai)
    
    with tab4:
        show_performance_analytics(functions_with_ai)
    
    with tab5:
        show_executive_dashboard(functions_with_ai)

def show_metrics_comparison(functions_with_ai):
    """Show detailed before/after metrics comparison"""
    
    st.subheader("📈 Key Metrics: Before vs After AI Implementation")
    
    # Function selector
    selected_function = st.selectbox(
        "Select Function for Detailed Analysis:",
        functions_with_ai,
        key="comp_function_selector"
    )
    
    if not selected_function:
        return
    
    # Get baseline and predicted data
    baseline_data = st.session_state.baseline_data[selected_function]
    categories_key = f'categories_{selected_function}'
    categories = getattr(st.session_state, categories_key, {})
    
    # Calculate aggregated predictions
    total_predictions = calculate_total_impact(baseline_data, categories)
    
    # Create comparison metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Current State (Baseline)")
        baseline_metrics = {
            "Annual Revenue": f"${baseline_data.get('annual_revenue', 0):,.0f}",
            "Annual Costs": f"${baseline_data.get('annual_costs', 0):,.0f}",
            "Headcount": f"{baseline_data.get('headcount', 0):,}",
            "Productivity Score": f"{baseline_data.get('current_productivity', 0):.1f}/10",
            "Satisfaction": f"{baseline_data.get('performance_satisfaction', 0):.1f}/10"
        }
        
        for metric, value in baseline_metrics.items():
            st.metric(metric, value)
    
    with col2:
        st.markdown("#### 🚀 Future State (With AI)")
        
        # Calculate future metrics
        future_revenue = baseline_data.get('annual_revenue', 0) * (1 + total_predictions.get('revenue_increase', 0) / 100)
        future_costs = baseline_data.get('annual_costs', 0) * (1 - total_predictions.get('cost_reduction', 0) / 100)
        future_headcount = baseline_data.get('headcount', 0) * (1 - total_predictions.get('workforce_reduction', 0) / 100)
        future_productivity = min(10, baseline_data.get('current_productivity', 0) * (1 + total_predictions.get('productivity_gain', 0) / 100))
        future_satisfaction = min(10, baseline_data.get('performance_satisfaction', 0) * (1 + total_predictions.get('satisfaction_improvement', 0) / 100))
        
        future_metrics = {
            "Annual Revenue": f"${future_revenue:,.0f}",
            "Annual Costs": f"${future_costs:,.0f}",
            "Headcount": f"{future_headcount:,.0f}",
            "Productivity Score": f"{future_productivity:.1f}/10",
            "Satisfaction": f"{future_satisfaction:.1f}/10"
        }
        
        # Calculate deltas
        revenue_delta = future_revenue - baseline_data.get('annual_revenue', 0)
        cost_delta = future_costs - baseline_data.get('annual_costs', 0)
        headcount_delta = future_headcount - baseline_data.get('headcount', 0)
        productivity_delta = future_productivity - baseline_data.get('current_productivity', 0)
        satisfaction_delta = future_satisfaction - baseline_data.get('performance_satisfaction', 0)
        
        st.metric("Annual Revenue", future_metrics["Annual Revenue"], delta=f"${revenue_delta:,.0f}")
        st.metric("Annual Costs", future_metrics["Annual Costs"], delta=f"${cost_delta:,.0f}")
        st.metric("Headcount", future_metrics["Headcount"], delta=f"{headcount_delta:,.0f}")
        st.metric("Productivity Score", future_metrics["Productivity Score"], delta=f"{productivity_delta:+.1f}")
        st.metric("Satisfaction", future_metrics["Satisfaction"], delta=f"{satisfaction_delta:+.1f}")
    
    # Detailed comparison chart
    st.markdown("#### 📊 Visual Comparison")
    
    metrics_data = {
        'Metric': ['Revenue ($M)', 'Costs ($M)', 'Headcount', 'Productivity', 'Satisfaction'],
        'Baseline': [
            baseline_data.get('annual_revenue', 0) / 1000000,
            baseline_data.get('annual_costs', 0) / 1000000,
            baseline_data.get('headcount', 0),
            baseline_data.get('current_productivity', 0),
            baseline_data.get('performance_satisfaction', 0)
        ],
        'With AI': [
            future_revenue / 1000000,
            future_costs / 1000000,
            future_headcount,
            future_productivity,
            future_satisfaction
        ]
    }
    
    df_metrics = pd.DataFrame(metrics_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Baseline',
        x=df_metrics['Metric'],
        y=df_metrics['Baseline'],
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        name='With AI',
        x=df_metrics['Metric'],
        y=df_metrics['With AI'],
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title=f"{selected_function}: Baseline vs AI-Enhanced Metrics",
        barmode='group',
        height=400,
        yaxis_title="Value"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Initiative breakdown
    st.markdown("#### 🎯 AI Initiative Contributions")
    
    initiative_impacts = []
    for category_name, category_data in categories.items():
        for init_id, init_data in category_data.get('ai_initiatives', {}).items():
            if 'predictions' in init_data:
                predictions = init_data['predictions']
                initiative_impacts.append({
                    'Initiative': init_data.get('name', f'Initiative {init_id}'),
                    'Category': category_name,
                    'Investment': init_data.get('investment', 0),
                    'ROI': predictions.get('roi', 0),
                    'Productivity Gain': predictions.get('productivity_gain', 0),
                    'Cost Reduction': predictions.get('cost_reduction', 0)
                })
    
    if initiative_impacts:
        df_initiatives = pd.DataFrame(initiative_impacts)
        st.dataframe(df_initiatives, use_container_width=True)

def show_financial_impact_analysis(functions_with_ai):
    """Show comprehensive financial impact analysis"""
    
    st.subheader("💰 Financial Impact Analysis")
    
    # Calculate enterprise-wide financial impact
    total_investment = 0
    total_roi = 0
    total_cost_savings = 0
    total_revenue_increase = 0
    function_summaries = []
    
    for func_name in functions_with_ai:
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_investment = 0
        func_annual_savings = 0
        func_revenue_increase = 0
        
        for category_name, category_data in categories.items():
            for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                investment = init_data.get('investment', 0)
                func_investment += investment
                
                if 'predictions' in init_data:
                    predictions = init_data['predictions']
                    annual_savings = predictions.get('annual_cost_savings', 0)
                    revenue_boost = predictions.get('annual_revenue_increase', 0)
                    
                    func_annual_savings += annual_savings
                    func_revenue_increase += revenue_boost
        
        total_investment += func_investment
        total_cost_savings += func_annual_savings
        total_revenue_increase += func_revenue_increase
        
        func_roi = ((func_annual_savings + func_revenue_increase - func_investment) / max(func_investment, 1)) * 100
        
        function_summaries.append({
            'Function': func_name,
            'Investment': func_investment,
            'Annual Savings': func_annual_savings,
            'Revenue Increase': func_revenue_increase,
            'Net Annual Benefit': func_annual_savings + func_revenue_increase,
            'ROI (%)': func_roi
        })
    
    # Enterprise summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_annual_benefit = total_cost_savings + total_revenue_increase
    enterprise_roi = ((total_annual_benefit - total_investment) / max(total_investment, 1)) * 100
    payback_period = total_investment / max(total_annual_benefit, 1)
    
    with col1:
        st.metric("Total Investment", f"${total_investment:,.0f}")
    with col2:
        st.metric("Annual Benefit", f"${total_annual_benefit:,.0f}")
    with col3:
        st.metric("Enterprise ROI", f"{enterprise_roi:.1f}%")
    with col4:
        st.metric("Payback Period", f"{payback_period:.1f} years")
    
    # Financial impact by function
    st.markdown("#### 📊 Financial Impact by Function")
    
    if function_summaries:
        df_financial = pd.DataFrame(function_summaries)
        
        # Format currency columns
        currency_cols = ['Investment', 'Annual Savings', 'Revenue Increase', 'Net Annual Benefit']
        for col in currency_cols:
            df_financial[col] = df_financial[col].apply(lambda x: f"${x:,.0f}")
        df_financial['ROI (%)'] = df_financial['ROI (%)'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_financial, use_container_width=True)
        
        # ROI comparison chart
        fig_roi = px.bar(
            pd.DataFrame(function_summaries),
            x='Function',
            y='ROI (%)',
            title="ROI Comparison by Function",
            color='ROI (%)',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # 5-year financial projection
    st.markdown("#### 📈 5-Year Financial Projection")
    
    years = list(range(2024, 2030))
    cumulative_investment = [total_investment if i == 0 else 0 for i in range(6)]
    cumulative_benefits = [total_annual_benefit * (i + 1) for i in range(6)]
    net_value = [cumulative_benefits[i] - sum(cumulative_investment[:i+1]) for i in range(6)]
    
    projection_data = pd.DataFrame({
        'Year': years,
        'Cumulative Investment': [sum(cumulative_investment[:i+1]) for i in range(6)],
        'Cumulative Benefits': cumulative_benefits,
        'Net Value': net_value
    })
    
    fig_projection = go.Figure()
    fig_projection.add_trace(go.Scatter(
        x=projection_data['Year'],
        y=projection_data['Cumulative Investment'],
        mode='lines+markers',
        name='Cumulative Investment',
        line=dict(color='red', width=3)
    ))
    fig_projection.add_trace(go.Scatter(
        x=projection_data['Year'],
        y=projection_data['Cumulative Benefits'],
        mode='lines+markers',
        name='Cumulative Benefits',
        line=dict(color='green', width=3)
    ))
    fig_projection.add_trace(go.Scatter(
        x=projection_data['Year'],
        y=projection_data['Net Value'],
        mode='lines+markers',
        name='Net Value',
        line=dict(color='blue', width=3)
    ))
    
    fig_projection.update_layout(
        title="5-Year Financial Projection",
        xaxis_title="Year",
        yaxis_title="Value ($)",
        height=400
    )
    
    st.plotly_chart(fig_projection, use_container_width=True)

def show_workforce_transformation_analysis(functions_with_ai):
    """Show workforce transformation impact analysis"""
    
    st.subheader("👥 Workforce Transformation Analysis")
    
    # Calculate workforce metrics
    workforce_data = []
    
    for func_name in functions_with_ai:
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        current_headcount = baseline_data.get('headcount', 0)
        total_reduction = 0
        total_upskilling = 0
        total_new_roles = 0
        
        for category_name, category_data in categories.items():
            for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                if 'predictions' in init_data:
                    predictions = init_data['predictions']
                    workforce_reduction = predictions.get('workforce_reduction', 0)
                    upskilling_required = predictions.get('upskilling_required', 0)
                    new_roles_created = predictions.get('new_roles_created', 0)
                    
                    total_reduction += (current_headcount * workforce_reduction / 100)
                    total_upskilling += (current_headcount * upskilling_required / 100)
                    total_new_roles += new_roles_created
        
        future_headcount = current_headcount - total_reduction + total_new_roles
        
        workforce_data.append({
            'Function': func_name,
            'Current Headcount': current_headcount,
            'Workforce Reduction': total_reduction,
            'Upskilling Required': total_upskilling,
            'New Roles Created': total_new_roles,
            'Future Headcount': future_headcount,
            'Net Change': future_headcount - current_headcount,
            'Transformation %': ((total_reduction + total_upskilling) / max(current_headcount, 1)) * 100
        })
    
    # Workforce transformation summary
    col1, col2, col3, col4 = st.columns(4)
    
    total_current = sum(w['Current Headcount'] for w in workforce_data)
    total_reduction = sum(w['Workforce Reduction'] for w in workforce_data)
    total_upskilling = sum(w['Upskilling Required'] for w in workforce_data)
    total_new_roles = sum(w['New Roles Created'] for w in workforce_data)
    
    with col1:
        st.metric("Current Workforce", f"{total_current:,.0f}")
    with col2:
        st.metric("Roles Affected", f"{total_reduction:,.0f}", delta=f"-{(total_reduction/max(total_current,1)*100):.1f}%")
    with col3:
        st.metric("Upskilling Needed", f"{total_upskilling:,.0f}", delta=f"{(total_upskilling/max(total_current,1)*100):.1f}%")
    with col4:
        st.metric("New Roles Created", f"{total_new_roles:,.0f}")
    
    # Workforce transformation by function
    st.markdown("#### 📊 Workforce Impact by Function")
    
    df_workforce = pd.DataFrame(workforce_data)
    st.dataframe(df_workforce.round(1), use_container_width=True)
    
    # Workforce transformation visualization
    fig_workforce = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Current vs Future Headcount', 'Workforce Reduction by Function', 
                       'Upskilling Requirements', 'New Roles Creation'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # Current vs Future headcount
    fig_workforce.add_trace(
        go.Bar(x=df_workforce['Function'], y=df_workforce['Current Headcount'], 
               name='Current', marker_color='lightblue'),
        row=1, col=1
    )
    fig_workforce.add_trace(
        go.Bar(x=df_workforce['Function'], y=df_workforce['Future Headcount'], 
               name='Future', marker_color='darkblue'),
        row=1, col=1
    )
    
    # Workforce reduction
    fig_workforce.add_trace(
        go.Bar(x=df_workforce['Function'], y=df_workforce['Workforce Reduction'], 
               name='Reduction', marker_color='red', showlegend=False),
        row=1, col=2
    )
    
    # Upskilling requirements
    fig_workforce.add_trace(
        go.Bar(x=df_workforce['Function'], y=df_workforce['Upskilling Required'], 
               name='Upskilling', marker_color='orange', showlegend=False),
        row=2, col=1
    )
    
    # New roles
    fig_workforce.add_trace(
        go.Bar(x=df_workforce['Function'], y=df_workforce['New Roles Created'], 
               name='New Roles', marker_color='green', showlegend=False),
        row=2, col=2
    )
    
    fig_workforce.update_layout(height=600, title_text="Workforce Transformation Overview")
    st.plotly_chart(fig_workforce, use_container_width=True)

def show_performance_analytics(functions_with_ai):
    """Show performance analytics and improvement metrics"""
    
    st.subheader("⚡ Performance Analytics")
    
    # Performance metrics analysis
    performance_data = []
    
    for func_name in functions_with_ai:
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        current_productivity = baseline_data.get('current_productivity', 0)
        current_satisfaction = baseline_data.get('performance_satisfaction', 0)
        
        avg_productivity_gain = 0
        avg_accuracy_improvement = 0
        avg_speed_improvement = 0
        automation_level = 0
        initiative_count = 0
        
        for category_name, category_data in categories.items():
            for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                if 'predictions' in init_data:
                    predictions = init_data['predictions']
                    avg_productivity_gain += predictions.get('productivity_gain', 0)
                    avg_accuracy_improvement += predictions.get('accuracy_improvement', 0)
                    avg_speed_improvement += predictions.get('speed_improvement', 0)
                    automation_level += init_data.get('automation_level', 0)
                    initiative_count += 1
        
        if initiative_count > 0:
            avg_productivity_gain /= initiative_count
            avg_accuracy_improvement /= initiative_count
            avg_speed_improvement /= initiative_count
            automation_level /= initiative_count
        
        future_productivity = min(10, current_productivity * (1 + avg_productivity_gain / 100))
        future_satisfaction = min(10, current_satisfaction * 1.2)  # Assume 20% satisfaction improvement
        
        performance_data.append({
            'Function': func_name,
            'Current Productivity': current_productivity,
            'Future Productivity': future_productivity,
            'Productivity Gain (%)': avg_productivity_gain,
            'Accuracy Improvement (%)': avg_accuracy_improvement,
            'Speed Improvement (%)': avg_speed_improvement,
            'Automation Level (%)': automation_level,
            'Current Satisfaction': current_satisfaction,
            'Future Satisfaction': future_satisfaction
        })
    
    # Performance overview
    df_performance = pd.DataFrame(performance_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_productivity_gain = df_performance['Productivity Gain (%)'].mean()
    avg_accuracy_gain = df_performance['Accuracy Improvement (%)'].mean()
    avg_speed_gain = df_performance['Speed Improvement (%)'].mean()
    avg_automation = df_performance['Automation Level (%)'].mean()
    
    with col1:
        st.metric("Avg Productivity Gain", f"{avg_productivity_gain:.1f}%")
    with col2:
        st.metric("Avg Accuracy Improvement", f"{avg_accuracy_gain:.1f}%")
    with col3:
        st.metric("Avg Speed Improvement", f"{avg_speed_gain:.1f}%")
    with col4:
        st.metric("Avg Automation Level", f"{avg_automation:.1f}%")
    
    # Performance comparison table
    st.markdown("#### 📊 Performance Metrics by Function")
    st.dataframe(df_performance.round(1), use_container_width=True)
    
    # Performance improvement radar chart
    st.markdown("#### 🎯 Performance Improvement Overview")
    
    fig_radar = go.Figure()
    
    categories_radar = ['Productivity<br>Gain', 'Accuracy<br>Improvement', 'Speed<br>Improvement', 'Automation<br>Level']
    
    for _, row in df_performance.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row['Productivity Gain (%)'], row['Accuracy Improvement (%)'], 
               row['Speed Improvement (%)'], row['Automation Level (%)']],
            theta=categories_radar,
            fill='toself',
            name=row['Function']
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Performance Improvement by Function"
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

def show_executive_dashboard(functions_with_ai):
    """Show executive-level dashboard with key insights"""
    
    st.subheader("📋 Executive Dashboard")
    
    # Calculate enterprise-wide KPIs
    total_investment = 0
    total_annual_benefit = 0
    total_current_headcount = 0
    total_future_headcount = 0
    weighted_productivity_gain = 0
    initiative_count = 0
    
    function_details = []
    
    for func_name in functions_with_ai:
        baseline_data = st.session_state.baseline_data[func_name]
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        func_investment = 0
        func_benefit = 0
        current_headcount = baseline_data.get('headcount', 0)
        func_productivity_gain = 0
        func_initiatives = 0
        
        for category_name, category_data in categories.items():
            for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                investment = init_data.get('investment', 0)
                func_investment += investment
                func_initiatives += 1
                
                if 'predictions' in init_data:
                    predictions = init_data['predictions']
                    annual_savings = predictions.get('annual_cost_savings', 0)
                    revenue_boost = predictions.get('annual_revenue_increase', 0)
                    productivity_gain = predictions.get('productivity_gain', 0)
                    
                    func_benefit += annual_savings + revenue_boost
                    func_productivity_gain += productivity_gain
        
        if func_initiatives > 0:
            func_productivity_gain /= func_initiatives
        
        # Calculate future headcount (simplified)
        workforce_reduction = func_productivity_gain * 0.3  # Assume 30% of productivity gain translates to workforce reduction
        future_headcount = current_headcount * (1 - workforce_reduction / 100)
        
        total_investment += func_investment
        total_annual_benefit += func_benefit
        total_current_headcount += current_headcount
        total_future_headcount += future_headcount
        weighted_productivity_gain += func_productivity_gain * current_headcount
        initiative_count += func_initiatives
        
        function_details.append({
            'Function': func_name,
            'Investment': func_investment,
            'Annual Benefit': func_benefit,
            'ROI': ((func_benefit - func_investment) / max(func_investment, 1)) * 100,
            'Productivity Gain': func_productivity_gain,
            'Initiative Count': func_initiatives,
            'Risk Level': 'Medium'  # Simplified risk assessment
        })
    
    if total_current_headcount > 0:
        weighted_productivity_gain /= total_current_headcount
    
    # Executive KPIs
    st.markdown("#### 🎯 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    enterprise_roi = ((total_annual_benefit - total_investment) / max(total_investment, 1)) * 100
    payback_period = total_investment / max(total_annual_benefit, 1)
    workforce_impact = ((total_current_headcount - total_future_headcount) / max(total_current_headcount, 1)) * 100
    
    with col1:
        st.metric("Total Investment", f"${total_investment/1000000:.1f}M")
    with col2:
        st.metric("Annual ROI", f"{enterprise_roi:.1f}%")
    with col3:
        st.metric("Payback Period", f"{payback_period:.1f} yrs")
    with col4:
        st.metric("Productivity Gain", f"{weighted_productivity_gain:.1f}%")
    with col5:
        st.metric("Workforce Impact", f"{workforce_impact:.1f}%")
    
    # Function performance summary
    st.markdown("#### 📊 Function Performance Summary")
    
    df_summary = pd.DataFrame(function_details)
    
    # Format currency columns
    df_summary['Investment'] = df_summary['Investment'].apply(lambda x: f"${x/1000000:.1f}M")
    df_summary['Annual Benefit'] = df_summary['Annual Benefit'].apply(lambda x: f"${x/1000000:.1f}M")
    df_summary['ROI'] = df_summary['ROI'].apply(lambda x: f"{x:.1f}%")
    df_summary['Productivity Gain'] = df_summary['Productivity Gain'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(df_summary, use_container_width=True)
    
    # Risk assessment matrix
    st.markdown("#### ⚠️ Risk Assessment Matrix")
    
    risk_data = []
    for func_name in functions_with_ai:
        categories_key = f'categories_{func_name}'
        categories = getattr(st.session_state, categories_key, {})
        
        total_risk = 0
        risk_count = 0
        
        for category_name, category_data in categories.items():
            for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                complexity = init_data.get('complexity', 'Medium')
                investment = init_data.get('investment', 0)
                
                # Simple risk calculation
                complexity_risk = {'Low': 1, 'Medium': 2, 'High': 3}.get(complexity, 2)
                investment_risk = 1 if investment < 100000 else 2 if investment < 500000 else 3
                
                total_risk += (complexity_risk + investment_risk) / 2
                risk_count += 1
        
        if risk_count > 0:
            avg_risk = total_risk / risk_count
            risk_level = 'Low' if avg_risk <= 1.5 else 'Medium' if avg_risk <= 2.5 else 'High'
            
            risk_data.append({
                'Function': func_name,
                'Risk Score': avg_risk,
                'Risk Level': risk_level,
                'Mitigation Priority': 'High' if avg_risk > 2.5 else 'Medium' if avg_risk > 1.5 else 'Low'
            })
    
    if risk_data:
        df_risk = pd.DataFrame(risk_data)
        st.dataframe(df_risk, use_container_width=True)
    
    # Strategic recommendations
    st.markdown("#### 💡 Strategic Recommendations")
    
    recommendations = []
    
    if enterprise_roi > 50:
        recommendations.append("🎯 Excellent ROI potential - consider accelerated implementation timeline")
    elif enterprise_roi > 20:
        recommendations.append("📈 Good ROI potential - proceed with planned implementation")
    else:
        recommendations.append("⚠️ Lower ROI - review and optimize AI initiatives before proceeding")
    
    if payback_period < 2:
        recommendations.append("💰 Fast payback period - prioritize high-impact initiatives")
    elif payback_period > 4:
        recommendations.append("⏰ Extended payback period - consider phased implementation approach")
    
    if workforce_impact > 20:
        recommendations.append("👥 Significant workforce impact - invest heavily in change management and retraining")
    
    if initiative_count > 10:
        recommendations.append("🎯 High initiative volume - establish dedicated AI transformation office")
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

def calculate_total_impact(baseline_data: Dict, categories: Dict) -> Dict:
    """Calculate total impact across all AI initiatives for a function"""
    
    total_impact = {
        'productivity_gain': 0,
        'cost_reduction': 0,
        'revenue_increase': 0,
        'workforce_reduction': 0,
        'satisfaction_improvement': 15  # Default satisfaction improvement
    }
    
    initiative_count = 0
    
    for category_name, category_data in categories.items():
        for init_id, init_data in category_data.get('ai_initiatives', {}).items():
            if 'predictions' in init_data:
                predictions = init_data['predictions']
                total_impact['productivity_gain'] += predictions.get('productivity_gain', 0)
                total_impact['cost_reduction'] += predictions.get('cost_reduction', 0)
                total_impact['revenue_increase'] += predictions.get('revenue_increase', 0)
                total_impact['workforce_reduction'] += predictions.get('workforce_reduction', 0)
                initiative_count += 1
    
    # Average the accumulated values
    if initiative_count > 0:
        total_impact['productivity_gain'] = int(total_impact['productivity_gain'] / initiative_count)
        total_impact['cost_reduction'] = int(total_impact['cost_reduction'] / initiative_count)
        total_impact['revenue_increase'] = int(total_impact['revenue_increase'] / initiative_count)
        total_impact['workforce_reduction'] = int(total_impact['workforce_reduction'] / initiative_count)
    
    return total_impact