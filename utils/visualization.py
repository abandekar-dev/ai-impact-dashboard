from typing import Dict, List

# Import dependencies through compatibility layer
try:
    from .compatibility import (
        go, px, make_subplots, pd, np,
        PLOTLY_AVAILABLE, PANDAS_AVAILABLE, NUMPY_AVAILABLE
    )
except ImportError:
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots
        import pandas as pd
        import numpy as np
        PLOTLY_AVAILABLE = PANDAS_AVAILABLE = NUMPY_AVAILABLE = True
    except ImportError:
        # Use fallback visualizations
        PLOTLY_AVAILABLE = PANDAS_AVAILABLE = NUMPY_AVAILABLE = False

class DashboardVisualizer:
    """Visualization utilities for the AI impact dashboard"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#8c564b',
            'dark': '#e377c2'
        }
    
    def create_impact_summary(self, predictions: Dict, function_name: str) -> go.Figure:
        """Create a summary chart showing key impact metrics"""
        
        # Prepare data for radar chart
        categories = ['Productivity Gain', 'ROI', 'Value Score', 'Risk Level', 'Payback Score']
        
        # Normalize values to 0-100 scale for comparison
        productivity_norm = min(predictions['productivity_gain'] * 2, 100)  # Scale productivity gain
        roi_norm = min(max(predictions['roi'], 0), 100)  # Cap ROI at 100
        value_norm = min((predictions['value_generated'] / 1000000) * 50, 100)  # Scale value
        
        # Risk level (inverse - lower risk is better)
        if 'confidence_interval' in predictions:
            risk_level = 100 - (predictions.get('confidence_interval', {}).get('productivity_gain', {}).get('lower', 50))
        else:
            risk_level = 70  # Default moderate risk
        
        # Payback score (inverse of payback period)
        payback_score = max(0, 100 - (predictions['payback_period'] * 2)) if predictions['payback_period'] != float('inf') else 0
        
        values = [productivity_norm, roi_norm, value_norm, risk_level, payback_score]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=function_name,
            line_color=self.color_palette['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f"AI Impact Assessment - {function_name}",
            font=dict(size=12),
            height=500
        )
        
        return fig
    
    def create_scenario_comparison(self, baseline_totals: Dict, ai_totals: Dict) -> go.Figure:
        """Create comparison chart between baseline and AI scenarios"""
        
        categories = ['Revenue', 'Costs', 'Productivity', 'Headcount']
        
        baseline_values = [
            baseline_totals['revenue'],
            baseline_totals['costs'],
            baseline_totals['productivity'],
            baseline_totals['headcount']
        ]
        
        ai_values = [
            ai_totals['revenue'],
            ai_totals['costs'],
            ai_totals['productivity'],
            ai_totals['headcount']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Baseline Scenario',
            x=categories,
            y=baseline_values,
            marker_color=self.color_palette['secondary']
        ))
        
        fig.add_trace(go.Bar(
            name='AI-Enabled Scenario',
            x=categories,
            y=ai_values,
            marker_color=self.color_palette['primary']
        ))
        
        fig.update_layout(
            barmode='group',
            title='Scenario Comparison: Baseline vs AI-Enabled',
            xaxis_title='Metrics',
            yaxis_title='Values',
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    def create_temporal_analysis(self, temporal_data: Dict, years: int) -> go.Figure:
        """Create temporal analysis chart showing projections over time"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Cumulative Value Generation', 'Monthly ROI Trends', 
                          'Productivity Evolution', 'Cost Savings Progression'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        colors = [self.color_palette['primary'], self.color_palette['secondary'], 
                 self.color_palette['success'], self.color_palette['warning']]
        
        color_idx = 0
        
        for func_name, data in temporal_data.items():
            color = colors[color_idx % len(colors)]
            
            # Cumulative Value Generation
            fig.add_trace(
                go.Scatter(x=data['month'], y=data['cumulative_value'], 
                          name=f'{func_name} - Cumulative Value',
                          line=dict(color=color, width=2)),
                row=1, col=1
            )
            
            # Monthly ROI
            fig.add_trace(
                go.Scatter(x=data['month'], y=data['monthly_roi'], 
                          name=f'{func_name} - Monthly ROI',
                          line=dict(color=color, width=2, dash='dot')),
                row=1, col=2
            )
            
            # Productivity Level
            fig.add_trace(
                go.Scatter(x=data['month'], y=data['productivity_level'], 
                          name=f'{func_name} - Productivity',
                          line=dict(color=color, width=2, dash='dash')),
                row=2, col=1
            )
            
            # Cost Savings
            fig.add_trace(
                go.Scatter(x=data['month'], y=data['cost_savings'], 
                          name=f'{func_name} - Cost Savings',
                          line=dict(color=color, width=2, dash='dashdot')),
                row=2, col=2
            )
            
            color_idx += 1
        
        fig.update_layout(
            height=800,
            title_text=f"Temporal Analysis - {years} Year Projection",
            showlegend=True,
            font=dict(size=10)
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Month", row=1, col=1)
        fig.update_xaxes(title_text="Month", row=1, col=2)
        fig.update_xaxes(title_text="Month", row=2, col=1)
        fig.update_xaxes(title_text="Month", row=2, col=2)
        
        fig.update_yaxes(title_text="Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="ROI (%)", row=1, col=2)
        fig.update_yaxes(title_text="Productivity Index", row=2, col=1)
        fig.update_yaxes(title_text="Savings ($)", row=2, col=2)
        
        return fig
    
    def create_individual_temporal_analysis(self, temporal_data: Dict, function_name: str) -> go.Figure:
        """Create detailed temporal analysis for individual function"""
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                f'{function_name} - Value Generation Over Time',
                f'{function_name} - ROI Progression', 
                f'{function_name} - Adoption & Productivity'
            ),
            specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]]
        )
        
        months = temporal_data['month']
        
        # Value Generation (Primary and Secondary Y-axis)
        fig.add_trace(
            go.Scatter(x=months, y=temporal_data['monthly_value'], 
                      name='Monthly Value', line=dict(color=self.color_palette['primary'])),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=months, y=temporal_data['cumulative_value'], 
                      name='Cumulative Value', line=dict(color=self.color_palette['secondary'])),
            row=1, col=1, secondary_y=True
        )
        
        # ROI Progression
        fig.add_trace(
            go.Scatter(x=months, y=temporal_data['monthly_roi'], 
                      name='Monthly ROI', line=dict(color=self.color_palette['success'])),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=months, y=temporal_data['cumulative_roi'], 
                      name='Cumulative ROI', line=dict(color=self.color_palette['warning'])),
            row=2, col=1, secondary_y=True
        )
        
        # Adoption and Productivity
        fig.add_trace(
            go.Scatter(x=months, y=[a*100 for a in temporal_data['adoption_rate']], 
                      name='Adoption Rate (%)', line=dict(color=self.color_palette['info'])),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=months, y=temporal_data['productivity_level'], 
                      name='Productivity Level', line=dict(color=self.color_palette['dark'])),
            row=3, col=1, secondary_y=True
        )
        
        # Update layout
        fig.update_layout(height=900, showlegend=True, font=dict(size=10))
        
        # Update axis labels
        fig.update_xaxes(title_text="Month", row=3, col=1)
        fig.update_yaxes(title_text="Monthly Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="Cumulative Value ($)", row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Monthly ROI (%)", row=2, col=1)
        fig.update_yaxes(title_text="Cumulative ROI (%)", row=2, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Adoption Rate (%)", row=3, col=1)
        fig.update_yaxes(title_text="Productivity Level", row=3, col=1, secondary_y=True)
        
        return fig
    
    def create_portfolio_overview(self, predictions: Dict) -> go.Figure:
        """Create portfolio overview showing all functions"""
        
        if not predictions:
            return go.Figure().add_annotation(
                text="No data available. Please configure functions first.",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        # Prepare data
        functions = list(predictions.keys())
        roi_values = [predictions[f]['roi'] for f in functions]
        value_values = [predictions[f]['value_generated'] for f in functions]
        productivity_values = [predictions[f]['productivity_gain'] for f in functions]
        
        # Create bubble chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=roi_values,
            y=value_values,
            mode='markers+text',
            marker=dict(
                size=[p*2 for p in productivity_values],  # Size based on productivity gain
                color=productivity_values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Productivity Gain (%)")
            ),
            text=functions,
            textposition="middle center",
            name="Functions"
        ))
        
        fig.update_layout(
            title="AI Implementation Portfolio Overview",
            xaxis_title="ROI (%)",
            yaxis_title="Value Generated ($)",
            height=500,
            font=dict(size=12)
        )
        
        # Add quadrant lines
        if roi_values and value_values:
            avg_roi = np.mean(roi_values)
            avg_value = np.mean(value_values)
            
            fig.add_hline(y=avg_value, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=avg_roi, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
    
    def create_risk_heatmap(self, ai_initiatives: Dict) -> go.Figure:
        """Create risk assessment heatmap"""
        
        if not ai_initiatives:
            return go.Figure().add_annotation(
                text="No data available. Please configure functions first.",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        functions = list(ai_initiatives.keys())
        risk_categories = ['Technical Risk', 'Adoption Risk', 'Integration Risk']
        
        # Prepare risk matrix
        risk_matrix = []
        for func in functions:
            initiative = ai_initiatives[func]
            risk_row = [
                initiative.get('technical_risk', 30),
                initiative.get('adoption_risk', 30),
                initiative.get('integration_risk', 30)
            ]
            risk_matrix.append(risk_row)
        
        fig = go.Figure(data=go.Heatmap(
            z=risk_matrix,
            x=risk_categories,
            y=functions,
            colorscale='RdYlGn_r',  # Red-Yellow-Green (reversed)
            colorbar=dict(title="Risk Level (0-100)")
        ))
        
        fig.update_layout(
            title="Risk Assessment Heatmap",
            xaxis_title="Risk Categories",
            yaxis_title="Functions",
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    def create_investment_breakdown(self, ai_initiatives: Dict) -> go.Figure:
        """Create investment breakdown by function"""
        
        if not ai_initiatives:
            return go.Figure().add_annotation(
                text="No data available. Please configure functions first.",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        functions = list(ai_initiatives.keys())
        investments = [ai_initiatives[f]['investment'] for f in functions]
        
        fig = go.Figure(data=[go.Pie(
            labels=functions,
            values=investments,
            hole=0.3,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Investment Distribution by Function",
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    def create_waterfall_chart(self, baseline_value: float, improvements: Dict) -> go.Figure:
        """Create waterfall chart showing value creation breakdown"""
        
        categories = ['Baseline'] + list(improvements.keys()) + ['Total']
        values = [baseline_value] + list(improvements.values())
        total_value = baseline_value + sum(improvements.values())
        values.append(total_value)
        
        # Calculate cumulative values for waterfall
        cumulative = [baseline_value]
        for improvement in improvements.values():
            cumulative.append(cumulative[-1] + improvement)
        
        fig = go.Figure()
        
        # Add baseline bar
        fig.add_trace(go.Bar(
            name='Baseline',
            x=[categories[0]],
            y=[baseline_value],
            marker_color=self.color_palette['secondary']
        ))
        
        # Add improvement bars
        for i, (cat, val) in enumerate(zip(categories[1:-1], improvements.values()), 1):
            fig.add_trace(go.Bar(
                name=cat,
                x=[cat],
                y=[val],
                base=cumulative[i-1],
                marker_color=self.color_palette['success'] if val > 0 else self.color_palette['warning']
            ))
        
        # Add total bar
        fig.add_trace(go.Bar(
            name='Total',
            x=[categories[-1]],
            y=[total_value],
            marker_color=self.color_palette['primary']
        ))
        
        fig.update_layout(
            title="Value Creation Waterfall",
            xaxis_title="Components",
            yaxis_title="Value ($)",
            showlegend=False,
            height=500,
            font=dict(size=12)
        )
        
        return fig
