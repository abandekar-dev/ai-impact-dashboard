import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import time
from datetime import datetime, timedelta

class DynamicOutputsVisualizer:
    """Dynamic visualization utilities for outputs section"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#4F46E5',
            'secondary': '#06B6D4',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#8B5CF6',
            'gradient_blue': ['#667eea', '#764ba2'],
            'gradient_green': ['#56CCF2', '#2F80ED'],
            'gradient_purple': ['#A8EDEA', '#FED6E3']
        }
    
    def create_real_time_metrics_dashboard(self, functions_data: Dict) -> go.Figure:
        """Create a real-time metrics dashboard with animated elements"""
        
        if not functions_data:
            return self._create_empty_dashboard()
        
        # Prepare data for visualization
        functions = list(functions_data.keys())
        roi_values = []
        productivity_gains = []
        value_generated = []
        risk_scores = []
        
        for func, data in functions_data.items():
            predictions = data.get('predictions', {})
            roi_values.append(predictions.get('roi', 0))
            productivity_gains.append(predictions.get('productivity_gain', 0))
            value_generated.append(predictions.get('value_generated', 0))
            
            # Calculate composite risk score
            baseline = data.get('baseline', {})
            risk_score = (
                baseline.get('technical_risk', 30) + 
                baseline.get('adoption_risk', 40) + 
                baseline.get('integration_risk', 35)
            ) / 3
            risk_scores.append(100 - risk_score)  # Invert for better visualization
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('ROI Performance', 'Productivity Impact', 'Value Generation', 'Risk Assessment'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "polar"}]]
        )
        
        # ROI Bar Chart with gradient
        fig.add_trace(
            go.Bar(
                x=functions,
                y=roi_values,
                name='ROI %',
                marker=dict(
                    color=roi_values,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="ROI %", x=0.45)
                ),
                text=[f'{val:.1f}%' for val in roi_values],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Productivity Scatter Plot
        fig.add_trace(
            go.Scatter(
                x=functions,
                y=productivity_gains,
                mode='markers+lines',
                marker=dict(
                    size=[max(10, val/5) for val in productivity_gains],
                    color=self.color_palette['secondary'],
                    line=dict(width=2, color='white')
                ),
                line=dict(color=self.color_palette['secondary'], width=3),
                name='Productivity Gain %'
            ),
            row=1, col=2
        )
        
        # Value Generation Funnel
        value_normalized = [val/1000000 for val in value_generated]  # Convert to millions
        fig.add_trace(
            go.Bar(
                x=functions,
                y=value_normalized,
                name='Value (M$)',
                marker=dict(
                    color=self.color_palette['success'],
                    pattern=dict(shape="x", solidity=0.3)
                ),
                text=[f'${val:.1f}M' for val in value_normalized],
                textposition='outside'
            ),
            row=2, col=1
        )
        
        # Risk Assessment Polar Chart
        fig.add_trace(
            go.Scatterpolar(
                r=risk_scores,
                theta=functions,
                fill='toself',
                name='Risk Score',
                line=dict(color=self.color_palette['warning'], width=2),
                fillcolor=f'{self.color_palette["warning"]}40'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="AI Implementation Impact Dashboard",
                x=0.5,
                font=dict(size=24, color='#1f2937')
            ),
            height=800,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Arial, sans-serif', color='#374151')
        )
        
        # Update polar subplot
        fig.update_polars(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%'),
            angularaxis=dict(tickmode='array', tickvals=list(range(len(functions))), ticktext=functions)
        )
        
        return fig
    
    def create_temporal_trend_visualization(self, temporal_data: Dict) -> go.Figure:
        """Create animated temporal trend visualization"""
        
        if not temporal_data:
            return self._create_empty_timeline()
        
        fig = go.Figure()
        
        # Create timeline data
        months = list(range(1, 25))  # 24 months
        colors = px.colors.qualitative.Set3
        
        for i, (func, data) in enumerate(temporal_data.items()):
            if 'timeline' in data:
                timeline = data['timeline']
                
                # Revenue projection
                fig.add_trace(go.Scatter(
                    x=months[:len(timeline['revenue'])],
                    y=timeline['revenue'],
                    mode='lines+markers',
                    name=f'{func} - Revenue',
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8),
                    hovertemplate=f'<b>{func}</b><br>Month: %{{x}}<br>Revenue: $%{{y:,.0f}}<extra></extra>'
                ))
        
        # Add trend annotations
        current_time = datetime.now()
        fig.add_vline(
            x=6, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Expected Break-even"
        )
        
        fig.add_vline(
            x=12, 
            line_dash="dash", 
            line_color="green",
            annotation_text="Full ROI Realization"
        )
        
        fig.update_layout(
            title="AI Implementation Revenue Timeline",
            xaxis_title="Months from Implementation",
            yaxis_title="Revenue Impact ($)",
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_interactive_scenario_matrix(self, scenarios_data: Dict) -> go.Figure:
        """Create interactive scenario comparison matrix"""
        
        if not scenarios_data:
            return self._create_empty_matrix()
        
        # Create heatmap data
        functions = list(scenarios_data.keys())
        metrics = ['ROI', 'Risk', 'Timeline', 'Investment']
        
        z_values = []
        text_values = []
        
        for metric in metrics:
            row_values = []
            row_text = []
            
            for func in functions:
                data = scenarios_data[func]
                
                if metric == 'ROI':
                    val = data.get('predictions', {}).get('roi', 0)
                    row_values.append(min(val, 200))  # Cap at 200%
                    row_text.append(f'{val:.1f}%')
                elif metric == 'Risk':
                    baseline = data.get('baseline', {})
                    risk = (baseline.get('technical_risk', 30) + 
                           baseline.get('adoption_risk', 40)) / 2
                    row_values.append(100 - risk)  # Invert for color scale
                    row_text.append(f'{risk:.0f}')
                elif metric == 'Timeline':
                    timeline = data.get('ai_initiative', {}).get('implementation_timeline', '12 months')
                    months = int(timeline.split()[0])
                    row_values.append(25 - months)  # Invert for color scale
                    row_text.append(f'{months}m')
                else:  # Investment
                    investment = data.get('ai_initiative', {}).get('investment_amount', 100000)
                    row_values.append(min(investment / 10000, 100))  # Scale and cap
                    row_text.append(f'${investment/1000:.0f}K')
            
            z_values.append(row_values)
            text_values.append(row_text)
        
        fig = go.Figure(data=go.Heatmap(
            z=z_values,
            x=functions,
            y=metrics,
            text=text_values,
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Performance Score")
        ))
        
        fig.update_layout(
            title="AI Initiative Performance Matrix",
            height=400,
            font=dict(family='Arial, sans-serif')
        )
        
        return fig
    
    def create_kpi_gauge_cluster(self, aggregate_data: Dict) -> go.Figure:
        """Create cluster of KPI gauges"""
        
        if not aggregate_data:
            return self._create_empty_gauges()
        
        # Calculate aggregate KPIs
        total_roi = aggregate_data.get('total_roi', 0)
        avg_productivity = aggregate_data.get('avg_productivity_gain', 0)
        total_value = aggregate_data.get('total_value_generated', 0) / 1000000  # Millions
        implementation_readiness = aggregate_data.get('readiness_score', 70)
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=('Portfolio ROI', 'Avg Productivity Gain', 'Total Value (M$)', 'Implementation Readiness')
        )
        
        # ROI Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=total_roi,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Portfolio ROI (%)"},
            delta={'reference': 150, 'position': "top"},
            gauge={
                'axis': {'range': [None, 300]},
                'bar': {'color': self.color_palette['primary']},
                'steps': [
                    {'range': [0, 100], 'color': "#ffebee"},
                    {'range': [100, 200], 'color': "#e8f5e8"},
                    {'range': [200, 300], 'color': "#c8e6c9"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 150
                }
            }
        ), row=1, col=1)
        
        # Productivity Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=avg_productivity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Avg Productivity (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette['secondary']},
                'steps': [
                    {'range': [0, 25], 'color': "#ffebee"},
                    {'range': [25, 50], 'color': "#fff3e0"},
                    {'range': [50, 75], 'color': "#e8f5e8"},
                    {'range': [75, 100], 'color': "#c8e6c9"}
                ]
            }
        ), row=1, col=2)
        
        # Value Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=total_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Total Value (M$)"},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': self.color_palette['success']},
                'steps': [
                    {'range': [0, 10], 'color': "#ffebee"},
                    {'range': [10, 25], 'color': "#e8f5e8"},
                    {'range': [25, 50], 'color': "#c8e6c9"}
                ]
            }
        ), row=2, col=1)
        
        # Readiness Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=implementation_readiness,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Readiness Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_palette['info']},
                'steps': [
                    {'range': [0, 40], 'color': "#ffebee"},
                    {'range': [40, 70], 'color': "#fff3e0"},
                    {'range': [70, 85], 'color': "#e8f5e8"},
                    {'range': [85, 100], 'color': "#c8e6c9"}
                ]
            }
        ), row=2, col=2)
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title=dict(
                text="AI Implementation KPI Dashboard",
                x=0.5,
                font=dict(size=20)
            )
        )
        
        return fig
    
    def _create_empty_dashboard(self) -> go.Figure:
        """Create empty dashboard placeholder"""
        fig = go.Figure()
        fig.add_annotation(
            text="Configure AI initiatives to see dynamic visualizations",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    def _create_empty_timeline(self) -> go.Figure:
        """Create empty timeline placeholder"""
        fig = go.Figure()
        fig.add_annotation(
            text="Temporal data will appear here after running predictions",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300, showlegend=False)
        return fig
    
    def _create_empty_matrix(self) -> go.Figure:
        """Create empty matrix placeholder"""
        fig = go.Figure()
        fig.add_annotation(
            text="Scenario comparison matrix will load with data",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300, showlegend=False)
        return fig
    
    def _create_empty_gauges(self) -> go.Figure:
        """Create empty gauges placeholder"""
        fig = go.Figure()
        fig.add_annotation(
            text="KPI gauges will populate with aggregated data",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=400, showlegend=False)
        return fig

def show_dynamic_outputs():
    """Display dynamic outputs visualization page"""
    st.header("📊 Dynamic AI Impact Visualizations")
    
    visualizer = DynamicOutputsVisualizer()
    
    # Auto-refresh toggle
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**Real-time Dashboard Updates**")
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
    with col3:
        refresh_interval = st.selectbox("Interval", [5, 10, 30, 60], index=1)
    
    # Collect data from session state
    functions_data = {}
    for func_name in st.session_state.get('baseline_data', {}):
        functions_data[func_name] = {
            'baseline': st.session_state.baseline_data.get(func_name, {}),
            'ai_initiative': st.session_state.ai_initiatives.get(func_name, {}),
            'predictions': st.session_state.predictions.get(func_name, {})
        }
    
    # Main dashboard
    st.subheader("🎯 Real-Time Metrics Dashboard")
    if functions_data:
        fig_dashboard = visualizer.create_real_time_metrics_dashboard(functions_data)
        st.plotly_chart(fig_dashboard, use_container_width=True)
    else:
        st.info("Configure AI initiatives in the Functions Analysis section to see dynamic visualizations.")
    
    # KPI Gauges
    st.subheader("📈 Portfolio KPI Gauges")
    if functions_data:
        # Calculate aggregate data
        total_roi = sum(data['predictions'].get('roi', 0) for data in functions_data.values()) / len(functions_data)
        avg_productivity = sum(data['predictions'].get('productivity_gain', 0) for data in functions_data.values()) / len(functions_data)
        total_value = sum(data['predictions'].get('value_generated', 0) for data in functions_data.values())
        
        aggregate_data = {
            'total_roi': total_roi,
            'avg_productivity_gain': avg_productivity,
            'total_value_generated': total_value,
            'readiness_score': 75  # This could be calculated from actual readiness data
        }
        
        fig_gauges = visualizer.create_kpi_gauge_cluster(aggregate_data)
        st.plotly_chart(fig_gauges, use_container_width=True)
    
    # Scenario Matrix
    st.subheader("🔄 Interactive Scenario Matrix")
    if functions_data:
        fig_matrix = visualizer.create_interactive_scenario_matrix(functions_data)
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Temporal Trends
    st.subheader("📅 Temporal Implementation Trends")
    if functions_data:
        # Generate sample temporal data for demonstration
        temporal_data = {}
        for func_name, data in functions_data.items():
            if data['predictions']:
                # Create sample timeline
                base_revenue = data['baseline'].get('current_revenue', 1000000)
                roi = data['predictions'].get('roi', 0) / 100
                
                revenue_timeline = []
                for month in range(1, 25):
                    # Progressive implementation
                    implementation_factor = min(month / 12, 1.0)
                    monthly_revenue = base_revenue * (1 + roi * implementation_factor)
                    revenue_timeline.append(monthly_revenue)
                
                temporal_data[func_name] = {
                    'timeline': {'revenue': revenue_timeline}
                }
        
        if temporal_data:
            fig_temporal = visualizer.create_temporal_trend_visualization(temporal_data)
            st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Auto-refresh functionality
    if auto_refresh and functions_data:
        time.sleep(refresh_interval)
        st.rerun()