"""
Enhanced chart styling utilities for professional data visualizations
"""
from typing import Dict, List, Any

# Import dependencies through compatibility layer
try:
    from .compatibility import (
        go, px, pd, PLOTLY_AVAILABLE, PANDAS_AVAILABLE
    )
except ImportError:
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        PLOTLY_AVAILABLE = PANDAS_AVAILABLE = True
    except ImportError:
        PLOTLY_AVAILABLE = PANDAS_AVAILABLE = False

class ChartTheme:
    """Professional chart theming with modern color palettes and styling"""
    
    # Modern color palettes
    PRIMARY_COLORS = [
        '#FF6B6B',  # Coral Red
        '#4ECDC4',  # Turquoise
        '#45B7D1',  # Sky Blue  
        '#96CEB4',  # Mint Green
        '#FFEAA7',  # Warm Yellow
        '#DDA0DD',  # Plum
        '#98D8C8',  # Seafoam
        '#F7DC6F',  # Sunny Yellow
    ]
    
    GRADIENT_COLORS = {
        'blue': ['#667eea', '#764ba2'],
        'green': ['#56CCF2', '#2F80ED'],
        'purple': ['#A8EDEA', '#FED6E3'],
        'orange': ['#FF9A8B', '#F093FB'],
        'teal': ['#4FACFE', '#00F2FE'],
        'pink': ['#FA709A', '#FEE140'],
        'coral': ['#FF6B6B', '#FFE66D'],
        'mint': ['#4ECDC4', '#44A08D'],
        'sunset': ['#FF512F', '#F09819'],
        'ocean': ['#2193b0', '#6dd5ed'],
        'forest': ['#134E5E', '#71B280'],
        'aurora': ['#00C6FF', '#0072FF']
    }
    
    @staticmethod
    def get_layout_theme() -> Dict[str, Any]:
        """Get standard layout theme for all charts - light theme"""
        return {
            'plot_bgcolor': '#ffffff',
            'paper_bgcolor': '#ffffff',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#262730'
            },
            'title': {
                'font': {
                    'size': 18,
                    'family': 'Arial, sans-serif',
                    'color': '#262730'
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            'legend': {
                'bgcolor': 'rgba(255,255,255,0.9)',
                'bordercolor': 'rgba(0,0,0,0.1)',
                'borderwidth': 1,
                'font': {'color': '#262730'}
            },
            'margin': {'t': 60, 'b': 40, 'l': 40, 'r': 40}
        }
    
    @staticmethod
    def get_axis_theme() -> Dict[str, Any]:
        """Get standard axis theme - light theme"""
        return {
            'gridcolor': 'rgba(0,0,0,0.1)',
            'zerolinecolor': 'rgba(0,0,0,0.2)',
            'linecolor': 'rgba(0,0,0,0.2)',
            'tickfont': {'color': '#262730'}
        }

class EnhancedCharts:
    """Enhanced chart creation with professional styling"""
    
    def __init__(self):
        self.theme = ChartTheme()
    
    def create_metric_cards_chart(self, data: Dict[str, float], title: str) -> go.Figure:
        """Create modern metric cards visualization"""
        fig = go.Figure()
        
        categories = list(data.keys())
        values = list(data.values())
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=self.theme.PRIMARY_COLORS[:len(categories)],
            marker_line_color='rgba(255,255,255,0.8)',
            marker_line_width=2,
            text=[f'{v:.1f}%' if v < 100 else f'{v:,.0f}' for v in values],
            textposition='outside',
            textfont={'size': 14, 'color': '#262730'}
        ))
        
        layout = self.theme.get_layout_theme()
        layout['title']['text'] = title
        layout['height'] = 400
        layout['showlegend'] = False
        
        fig.update_layout(**layout)
        fig.update_xaxes(**self.theme.get_axis_theme())
        fig.update_yaxes(**self.theme.get_axis_theme())
        
        return fig
    
    def create_distribution_chart(self, data: List[float], title: str, 
                                color: str = 'blue') -> go.Figure:
        """Create professional distribution histogram"""
        fig = go.Figure()
        
        # Histogram with enhanced styling
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=50,
            marker_color=f'rgba(99, 102, 241, 0.7)',
            marker_line_color='rgba(99, 102, 241, 1.0)',
            marker_line_width=1,
            name='Distribution'
        ))
        
        # Add mean line
        mean_val = sum(data) / len(data)
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_val:.1f}",
            annotation_position="top"
        )
        
        layout = self.theme.get_layout_theme()
        layout['title']['text'] = title
        layout['height'] = 400
        layout['showlegend'] = False
        
        fig.update_layout(**layout)
        fig.update_xaxes(**self.theme.get_axis_theme())
        fig.update_yaxes(**self.theme.get_axis_theme())
        
        return fig
    
    def create_confidence_interval_chart(self, intervals: Dict, metric_name: str) -> go.Figure:
        """Create confidence interval visualization"""
        fig = go.Figure()
        
        confidence_levels = list(intervals.keys())
        lower_bounds = [intervals[level]['lower'] for level in confidence_levels]
        upper_bounds = [intervals[level]['upper'] for level in confidence_levels]
        
        # Create filled area for confidence intervals
        for i, level in enumerate(confidence_levels):
            fig.add_trace(go.Scatter(
                x=[level, level],
                y=[lower_bounds[i], upper_bounds[i]],
                mode='lines+markers',
                line_color=self.theme.PRIMARY_COLORS[i],
                marker_size=8,
                name=level,
                showlegend=True
            ))
        
        layout = self.theme.get_layout_theme()
        layout['title']['text'] = f'{metric_name} Confidence Intervals'
        layout['height'] = 400
        layout['xaxis_title'] = 'Confidence Level'
        layout['yaxis_title'] = metric_name
        
        fig.update_layout(**layout)
        fig.update_xaxes(**self.theme.get_axis_theme())
        fig.update_yaxes(**self.theme.get_axis_theme())
        
        return fig
    
    def create_risk_heatmap(self, risk_data: Dict[str, float]) -> go.Figure:
        """Create risk assessment heatmap"""
        risks = list(risk_data.keys())
        values = list(risk_data.values())
        
        # Create color scale based on risk levels
        colors = []
        for val in values:
            if val < 0.1:
                colors.append('#10b981')  # Green - Low risk
            elif val < 0.3:
                colors.append('#f59e0b')  # Amber - Medium risk
            else:
                colors.append('#ef4444')  # Red - High risk
        
        fig = go.Figure(go.Bar(
            x=values,
            y=risks,
            orientation='h',
            marker_color=colors,
            marker_line_color='rgba(255,255,255,0.8)',
            marker_line_width=2,
            text=[f'{v:.1%}' for v in values],
            textposition='auto',
            textfont={'size': 12, 'color': 'white'}
        ))
        
        layout = self.theme.get_layout_theme()
        layout['title']['text'] = 'Risk Assessment Overview'
        layout['height'] = 400
        layout['showlegend'] = False
        layout['xaxis_title'] = 'Risk Level'
        
        fig.update_layout(**layout)
        fig.update_xaxes(**self.theme.get_axis_theme())
        fig.update_yaxes(**self.theme.get_axis_theme())
        
        return fig
    
    def create_scenario_comparison(self, scenarios: Dict[str, Dict]) -> go.Figure:
        """Create scenario comparison radar chart"""
        categories = ['ROI', 'Risk Level', 'Implementation Speed', 'Value Generation', 'Success Probability']
        
        fig = go.Figure()
        
        for i, (scenario_name, data) in enumerate(scenarios.items()):
            # Normalize values for radar chart (0-1 scale)
            values = [
                data.get('roi', 0) / 100,
                1 - data.get('risk_score', 0.5),  # Invert risk for better visualization
                data.get('implementation_speed', 0.5),
                data.get('value_score', 0.5),
                data.get('success_probability', 0.5)
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],  # Close the polygon
                theta=categories + [categories[0]],
                fill='toself',
                name=scenario_name,
                line_color=self.theme.PRIMARY_COLORS[i],
                fillcolor=f'rgba({",".join(str(int(c[1:3], 16)) for c in [self.theme.PRIMARY_COLORS[i]][:3])}, 0.3)'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(0,0,0,0.1)'
                )
            ),
            title={
                'text': 'Scenario Comparison',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Arial, sans-serif', 'color': '#1f2937'}
            },
            height=500,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Arial, sans-serif', 'color': '#374151'}
        )
        
        return fig

def create_styled_metric_card(value: str, label: str, color_theme: str = 'blue') -> str:
    """Create HTML for styled metric card with vibrant modern design"""
    gradient = ChartTheme.GRADIENT_COLORS.get(color_theme, ChartTheme.GRADIENT_COLORS['blue'])
    
    return f"""
    <div style="background: linear-gradient(135deg, {gradient[0]} 0%, {gradient[1]} 100%); 
                padding: 2rem; border-radius: 20px; color: white; text-align: center;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); margin: 1rem 0;
                transform: scale(1); transition: transform 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.2);">
        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{value}</h2>
        <p style="margin: 0.8rem 0 0 0; opacity: 0.95; font-size: 1.1rem; font-weight: 500; letter-spacing: 0.5px;">{label}</p>
    </div>
    """

def create_styled_card(content: str, title: str = "") -> str:
    """Create HTML for styled content card"""
    title_html = f"<h4 style='margin-top: 0; color: #1f2937;'>{title}</h4>" if title else ""
    
    return f"""
    <div style="background: white; padding: 2rem; border-radius: 12px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border: 1px solid #e5e7eb;
                margin: 1rem 0;">
        {title_html}
        {content}
    </div>
    """