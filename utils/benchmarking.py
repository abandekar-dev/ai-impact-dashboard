from typing import Dict, List, Optional

# Import dependencies through compatibility layer
try:
    from .compatibility import (
        np, pd, go, make_subplots,
        NUMPY_AVAILABLE, PANDAS_AVAILABLE, PLOTLY_AVAILABLE
    )
except ImportError:
    try:
        import pandas as pd
        import numpy as np
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = False

class IndustryBenchmarking:
    """Industry benchmarking and comparative analysis utilities"""
    
    def __init__(self):
        # Industry benchmark data based on research and market studies
        self.industry_benchmarks = {
            'Technology': {
                'ai_adoption_rate': 65,
                'avg_roi': 150,
                'avg_payback_months': 8,
                'automation_potential': 45,
                'productivity_gain': 25
            },
            'Financial Services': {
                'ai_adoption_rate': 58,
                'avg_roi': 180,
                'avg_payback_months': 10,
                'automation_potential': 55,
                'productivity_gain': 30
            },
            'Manufacturing': {
                'ai_adoption_rate': 45,
                'avg_roi': 120,
                'avg_payback_months': 12,
                'automation_potential': 60,
                'productivity_gain': 35
            },
            'Healthcare': {
                'ai_adoption_rate': 35,
                'avg_roi': 140,
                'avg_payback_months': 15,
                'automation_potential': 40,
                'productivity_gain': 20
            },
            'Retail': {
                'ai_adoption_rate': 50,
                'avg_roi': 110,
                'avg_payback_months': 14,
                'automation_potential': 50,
                'productivity_gain': 22
            },
            'General': {
                'ai_adoption_rate': 45,
                'avg_roi': 135,
                'avg_payback_months': 12,
                'automation_potential': 48,
                'productivity_gain': 25
            }
        }
        
        self.function_benchmarks = {
            'HR & Talent Management': {'automation_potential': 45, 'typical_roi': 120},
            'Finance & Accounting': {'automation_potential': 65, 'typical_roi': 180},
            'Operations & Supply Chain': {'automation_potential': 55, 'typical_roi': 150},
            'Sales & Marketing': {'automation_potential': 40, 'typical_roi': 140},
            'IT & Technology': {'automation_potential': 70, 'typical_roi': 200},
            'Customer Service': {'automation_potential': 60, 'typical_roi': 160},
            'Legal & Compliance': {'automation_potential': 35, 'typical_roi': 110},
            'R&D': {'automation_potential': 30, 'typical_roi': 130},
            'Manufacturing & Production': {'automation_potential': 75, 'typical_roi': 170},
            'Quality Assurance': {'automation_potential': 65, 'typical_roi': 155},
            'Business Development': {'automation_potential': 25, 'typical_roi': 125},
            'Strategy & Planning': {'automation_potential': 35, 'typical_roi': 140},
            'Risk Management': {'automation_potential': 50, 'typical_roi': 145},
            'Procurement': {'automation_potential': 55, 'typical_roi': 135},
            'Facilities Management': {'automation_potential': 45, 'typical_roi': 115},
            'Data & Analytics': {'automation_potential': 80, 'typical_roi': 220}
        }
    
    def get_industry_comparison(self, industry: str, predictions: Dict) -> Dict:
        """Compare predictions against industry benchmarks"""
        
        benchmark = self.industry_benchmarks.get(industry, self.industry_benchmarks['General'])
        
        # Calculate portfolio metrics
        avg_roi = np.mean([p['roi'] for p in predictions.values()])
        avg_payback = np.mean([p['payback_period'] for p in predictions.values() 
                              if p['payback_period'] != float('inf')])
        avg_productivity = np.mean([p['productivity_gain'] for p in predictions.values()])
        
        comparison = {
            'industry': industry,
            'benchmark': benchmark,
            'your_metrics': {
                'avg_roi': avg_roi,
                'avg_payback_months': avg_payback,
                'avg_productivity_gain': avg_productivity
            },
            'performance': {
                'roi_vs_benchmark': (avg_roi - benchmark['avg_roi']) / benchmark['avg_roi'] * 100,
                'payback_vs_benchmark': (benchmark['avg_payback_months'] - avg_payback) / benchmark['avg_payback_months'] * 100,
                'productivity_vs_benchmark': (avg_productivity - benchmark['productivity_gain']) / benchmark['productivity_gain'] * 100
            }
        }
        
        return comparison
    
    def create_benchmark_comparison_chart(self, comparison: Dict) -> go.Figure:
        """Create benchmark comparison visualization"""
        
        categories = ['ROI (%)', 'Payback (months)', 'Productivity Gain (%)']
        
        your_values = [
            comparison['your_metrics']['avg_roi'],
            comparison['your_metrics']['avg_payback_months'],
            comparison['your_metrics']['avg_productivity_gain']
        ]
        
        benchmark_values = [
            comparison['benchmark']['avg_roi'],
            comparison['benchmark']['avg_payback_months'],
            comparison['benchmark']['productivity_gain']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Your Portfolio',
            x=categories,
            y=your_values,
            marker_color='#1f77b4'
        ))
        
        fig.add_trace(go.Bar(
            name=f'{comparison["industry"]} Benchmark',
            x=categories,
            y=benchmark_values,
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            title=f'Performance vs {comparison["industry"]} Industry Benchmark',
            barmode='group',
            height=400,
            yaxis_title='Values'
        )
        
        return fig
    
    def get_function_benchmark(self, function_name: str, prediction: Dict) -> Dict:
        """Get function-specific benchmark comparison"""
        
        benchmark = self.function_benchmarks.get(function_name, {'automation_potential': 50, 'typical_roi': 135})
        
        comparison = {
            'function': function_name,
            'your_roi': prediction['roi'],
            'benchmark_roi': benchmark['typical_roi'],
            'your_automation': prediction.get('automation_level', 0),
            'benchmark_automation': benchmark['automation_potential'],
            'roi_percentile': self._calculate_percentile(prediction['roi'], benchmark['typical_roi']),
            'automation_percentile': self._calculate_percentile(prediction.get('automation_level', 0), benchmark['automation_potential'])
        }
        
        return comparison
    
    def _calculate_percentile(self, value: float, benchmark: float) -> str:
        """Calculate performance percentile"""
        ratio = value / benchmark if benchmark > 0 else 0
        
        if ratio >= 1.3:
            return "Top 10%"
        elif ratio >= 1.15:
            return "Top 25%"
        elif ratio >= 0.85:
            return "Average"
        elif ratio >= 0.7:
            return "Below Average"
        else:
            return "Bottom 25%"

class SensitivityAnalysis:
    """Sensitivity analysis for AI implementation scenarios"""
    
    def __init__(self):
        self.sensitivity_factors = [
            'investment', 'automation_level', 'accuracy_improvement', 
            'speed_improvement', 'technical_risk', 'adoption_risk'
        ]
    
    def run_sensitivity_analysis(self, baseline_data: Dict, ai_initiative: Dict, 
                                predictions: Dict, factor: str, 
                                variation_range: float = 0.3) -> Dict:
        """Run sensitivity analysis on a specific factor"""
        
        from .predictive_engine import PredictiveEngine
        engine = PredictiveEngine()
        
        base_value = ai_initiative.get(factor, 0)
        variations = []
        results = []
        
        # Test variations from -30% to +30%
        for i in range(-3, 4):
            variation = i * (variation_range / 3)
            variations.append(variation * 100)
            
            # Create modified initiative
            modified_initiative = ai_initiative.copy()
            
            if factor in ['investment']:
                modified_initiative[factor] = base_value * (1 + variation)
            elif factor in ['automation_level', 'accuracy_improvement', 'speed_improvement']:
                modified_initiative[factor] = min(100, base_value * (1 + variation))
            elif factor in ['technical_risk', 'adoption_risk', 'integration_risk']:
                modified_initiative[factor] = min(100, base_value * (1 + variation))
            
            # Run prediction with modified values
            result = engine.predict_impact(baseline_data, modified_initiative)
            results.append(result)
        
        return {
            'factor': factor,
            'variations': variations,
            'roi_results': [r['roi'] for r in results],
            'value_results': [r['value_generated'] for r in results],
            'payback_results': [r['payback_period'] for r in results]
        }
    
    def create_sensitivity_chart(self, sensitivity_data: Dict) -> go.Figure:
        """Create sensitivity analysis visualization"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('ROI Sensitivity', 'Value Generation Sensitivity', 
                          'Payback Period Sensitivity', 'Risk vs Return'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        variations = sensitivity_data['variations']
        
        # ROI sensitivity
        fig.add_trace(
            go.Scatter(x=variations, y=sensitivity_data['roi_results'], 
                      name='ROI', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Value sensitivity
        fig.add_trace(
            go.Scatter(x=variations, y=sensitivity_data['value_results'], 
                      name='Value', line=dict(color='green')),
            row=1, col=2
        )
        
        # Payback sensitivity
        capped_payback = [min(p, 100) for p in sensitivity_data['payback_results']]
        fig.add_trace(
            go.Scatter(x=variations, y=capped_payback, 
                      name='Payback', line=dict(color='red')),
            row=2, col=1
        )
        
        # Risk vs Return scatter
        fig.add_trace(
            go.Scatter(x=variations, y=sensitivity_data['roi_results'], 
                      mode='markers', name='Risk-Return', 
                      marker=dict(color='purple', size=8)),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text=f"Sensitivity Analysis: {sensitivity_data['factor'].replace('_', ' ').title()}"
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Variation (%)", row=2, col=1)
        fig.update_xaxes(title_text="Variation (%)", row=2, col=2)
        
        return fig

class ScenarioOptimization:
    """Scenario optimization and what-if analysis"""
    
    def __init__(self):
        self.optimization_targets = ['roi', 'payback_period', 'value_generated', 'risk_adjusted_roi']
    
    def optimize_scenario(self, baseline_data: Dict, ai_initiative: Dict, 
                         target_metric: str = 'roi') -> Dict:
        """Optimize AI initiative parameters for target metric"""
        
        from .predictive_engine import PredictiveEngine
        engine = PredictiveEngine()
        
        best_result = None
        best_score = -float('inf') if target_metric != 'payback_period' else float('inf')
        best_config = None
        
        # Test different parameter combinations
        automation_levels = [30, 40, 50, 60, 70, 80]
        investment_multipliers = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
        complexity_levels = ['Low', 'Medium', 'High']
        
        optimization_results = []
        
        for automation in automation_levels:
            for inv_mult in investment_multipliers:
                for complexity in complexity_levels:
                    # Create test configuration
                    test_config = ai_initiative.copy()
                    test_config['automation_level'] = automation
                    test_config['investment'] = ai_initiative['investment'] * inv_mult
                    test_config['complexity'] = complexity
                    
                    # Adjust other parameters based on automation level
                    test_config['accuracy_improvement'] = min(100, automation * 0.8)
                    test_config['speed_improvement'] = min(100, automation * 0.9)
                    
                    # Run prediction
                    result = engine.predict_impact(baseline_data, test_config)
                    
                    score = result[target_metric]
                    if target_metric == 'payback_period':
                        score = -score if score != float('inf') else -1000
                    
                    optimization_results.append({
                        'config': test_config,
                        'result': result,
                        'score': score
                    })
                    
                    # Track best result
                    if target_metric == 'payback_period':
                        if score > best_score:
                            best_score = score
                            best_result = result
                            best_config = test_config
                    else:
                        if score > best_score:
                            best_score = score
                            best_result = result
                            best_config = test_config
        
        return {
            'target_metric': target_metric,
            'best_config': best_config,
            'best_result': best_result,
            'improvement': self._calculate_improvement(ai_initiative, best_config, target_metric),
            'all_results': sorted(optimization_results, key=lambda x: x['score'], reverse=True)[:10]
        }
    
    def _calculate_improvement(self, original: Dict, optimized: Dict, metric: str) -> Dict:
        """Calculate improvement from optimization"""
        
        from .predictive_engine import PredictiveEngine
        engine = PredictiveEngine()
        
        # This would need baseline_data, but for simplicity we'll return parameter changes
        changes = {}
        for key in ['automation_level', 'investment', 'complexity']:
            if key in original and key in optimized:
                if key == 'investment':
                    changes[key] = f"{((optimized[key] - original[key]) / original[key] * 100):.1f}%"
                elif key == 'automation_level':
                    changes[key] = f"{optimized[key] - original[key]:.1f} points"
                else:
                    changes[key] = f"{original[key]} → {optimized[key]}"
        
        return changes