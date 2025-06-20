from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import dependencies through compatibility layer
try:
    from .compatibility import (
        np, pd, go, px, make_subplots,
        NUMPY_AVAILABLE, PANDAS_AVAILABLE, PLOTLY_AVAILABLE
    )
except ImportError:
    try:
        import numpy as np
        import pandas as pd
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = PLOTLY_AVAILABLE = False

try:
    from scipy import stats as scipy_stats
except ImportError:
    scipy_stats = None

from .predictive_engine import PredictiveEngine
from .data_models import MetricsCalculator

class MonteCarloSimulator:
    """Monte Carlo simulation engine for multi-scenario AI impact modeling"""
    
    def __init__(self, n_simulations: int = 1000):
        self.n_simulations = n_simulations
        self.engine = PredictiveEngine()
        self.metrics_calc = MetricsCalculator()
        self.simulation_results = {}
        
    def run_simulation(self, baseline_data: dict, ai_initiative: dict, 
                      uncertainty_parameters: dict = None) -> dict:
        """
        Run Monte Carlo simulation with uncertainty in key parameters
        
        Args:
            baseline_data: Base enterprise function data
            ai_initiative: AI initiative configuration
            uncertainty_parameters: Distribution parameters for uncertain variables
        """
        
        # Define default uncertainty parameters if not provided
        if uncertainty_parameters is None:
            uncertainty_parameters = self._get_default_uncertainty_params()
        
        # Ensure we have a valid dictionary
        if not isinstance(uncertainty_parameters, dict):
            uncertainty_parameters = self._get_default_uncertainty_params()
        
        # Storage for simulation results
        results = {
            'productivity_gain': [],
            'value_generated': [],
            'roi': [],
            'payback_period': [],
            'risk_adjusted_roi': [],
            'net_cost_impact': [],
            'implementation_success_probability': [],
            'simulation_parameters': []
        }
        
        # Run simulations
        for i in range(self.n_simulations):
            # Generate random parameter values
            sim_baseline, sim_initiative = self._generate_random_parameters(
                baseline_data, ai_initiative, uncertainty_parameters
            )
            
            # Calculate implementation success probability
            success_prob = self._calculate_implementation_success(sim_initiative)
            
            # Run prediction with simulated parameters
            try:
                prediction = self.engine.predict_impact(sim_baseline, sim_initiative)
                
                # Apply success probability to results
                adjusted_productivity = prediction['productivity_gain'] * success_prob
                adjusted_value = prediction['value_generated'] * success_prob
                adjusted_roi = prediction['roi'] * success_prob
                
                # Store results
                results['productivity_gain'].append(adjusted_productivity)
                results['value_generated'].append(adjusted_value)
                results['roi'].append(adjusted_roi)
                results['payback_period'].append(prediction['payback_period'])
                results['risk_adjusted_roi'].append(prediction['risk_adjusted_roi'] * success_prob)
                results['net_cost_impact'].append(
                    prediction['workforce_impact'].get('net_cost_impact', 0)
                )
                results['implementation_success_probability'].append(success_prob)
                results['simulation_parameters'].append({
                    'investment_variation': sim_initiative['investment'] / ai_initiative['investment'],
                    'productivity_baseline': sim_baseline['productivity'],
                    'automation_level': sim_initiative['automation_level'],
                    'market_conditions': sim_baseline.get('market_factor', 1.0)
                })
                
            except Exception as e:
                # Handle failed simulations by using conservative estimates
                results['productivity_gain'].append(0)
                results['value_generated'].append(0)
                results['roi'].append(-10)
                results['payback_period'].append(999)
                results['risk_adjusted_roi'].append(-10)
                results['net_cost_impact'].append(ai_initiative['investment'])
                results['implementation_success_probability'].append(0.1)
                results['simulation_parameters'].append({})
        
        # Calculate statistical summaries
        summary_stats = self._calculate_summary_statistics(results)
        
        # Calculate risk metrics
        risk_metrics = self._calculate_risk_metrics(results)
        
        # Generate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(results)
        
        # Perform sensitivity analysis
        sensitivity_analysis = self._perform_sensitivity_analysis(results)
        
        return {
            'simulation_results': results,
            'summary_statistics': summary_stats,
            'risk_metrics': risk_metrics,
            'confidence_intervals': confidence_intervals,
            'sensitivity_analysis': sensitivity_analysis,
            'simulation_parameters': {
                'n_simulations': self.n_simulations,
                'uncertainty_parameters': uncertainty_parameters
            }
        }
    
    def _get_default_uncertainty_params(self) -> dict:
        """Define default uncertainty parameters for key variables"""
        return {
            'investment': {'distribution': 'normal', 'std_pct': 0.15},  # 15% standard deviation
            'productivity_baseline': {'distribution': 'normal', 'std_pct': 0.10},  # 10% std dev
            'automation_level': {'distribution': 'normal', 'std_pct': 0.20},  # 20% std dev
            'accuracy_improvement': {'distribution': 'normal', 'std_pct': 0.25},  # 25% std dev
            'speed_improvement': {'distribution': 'normal', 'std_pct': 0.20},  # 20% std dev
            'technical_risk': {'distribution': 'beta', 'alpha': 2, 'beta': 5},  # Beta distribution
            'adoption_risk': {'distribution': 'beta', 'alpha': 2, 'beta': 4},
            'integration_risk': {'distribution': 'beta', 'alpha': 3, 'beta': 4},
            'market_conditions': {'distribution': 'normal', 'std_pct': 0.12},  # Market volatility
            'competitive_pressure': {'distribution': 'uniform', 'low': 0.8, 'high': 1.2}
        }
    
    def _generate_random_parameters(self, baseline_data: dict, ai_initiative: dict, 
                                  uncertainty_params: dict) -> Tuple[dict, dict]:
        """Generate random parameter values based on uncertainty distributions"""
        
        sim_baseline = baseline_data.copy()
        sim_initiative = ai_initiative.copy()
        
        # Generate random values for each uncertain parameter
        for param, config in uncertainty_params.items():
            if param == 'investment':
                std = ai_initiative['investment'] * config['std_pct']
                sim_initiative['investment'] = max(10000, 
                    np.random.normal(ai_initiative['investment'], std))
            
            elif param == 'productivity_baseline':
                std = baseline_data['productivity'] * config['std_pct']
                sim_baseline['productivity'] = np.clip(
                    np.random.normal(baseline_data['productivity'], std), 10, 95)
            
            elif param == 'automation_level':
                std = ai_initiative['automation_level'] * config['std_pct']
                sim_initiative['automation_level'] = np.clip(
                    np.random.normal(ai_initiative['automation_level'], std), 0, 100)
            
            elif param == 'accuracy_improvement':
                std = ai_initiative['accuracy_improvement'] * config['std_pct']
                sim_initiative['accuracy_improvement'] = max(0,
                    np.random.normal(ai_initiative['accuracy_improvement'], std))
            
            elif param == 'speed_improvement':
                std = ai_initiative['speed_improvement'] * config['std_pct']
                sim_initiative['speed_improvement'] = max(0,
                    np.random.normal(ai_initiative['speed_improvement'], std))
            
            elif param == 'technical_risk':
                if config['distribution'] == 'beta':
                    sim_initiative['technical_risk'] = np.random.beta(
                        config['alpha'], config['beta'])
            
            elif param == 'adoption_risk':
                if config['distribution'] == 'beta':
                    sim_initiative['adoption_risk'] = np.random.beta(
                        config['alpha'], config['beta'])
            
            elif param == 'integration_risk':
                if config['distribution'] == 'beta':
                    sim_initiative['integration_risk'] = np.random.beta(
                        config['alpha'], config['beta'])
            
            elif param == 'market_conditions':
                std = config['std_pct']
                market_factor = np.clip(np.random.normal(1.0, std), 0.5, 1.5)
                sim_baseline['market_factor'] = market_factor
                # Apply market factor to revenue
                sim_baseline['revenue'] = baseline_data['revenue'] * market_factor
            
            elif param == 'competitive_pressure':
                comp_factor = np.random.uniform(config['low'], config['high'])
                sim_initiative['competitive_factor'] = comp_factor
        
        return sim_baseline, sim_initiative
    
    def _calculate_implementation_success(self, ai_initiative: dict) -> float:
        """Calculate probability of successful implementation based on risk factors"""
        
        # Base success probability
        base_success = 0.85
        
        # Risk factors that affect success probability
        technical_risk = ai_initiative.get('technical_risk', 0.3)
        adoption_risk = ai_initiative.get('adoption_risk', 0.3)
        integration_risk = ai_initiative.get('integration_risk', 0.3)
        
        # Complexity penalty
        complexity = ai_initiative.get('complexity', 'Medium')
        complexity_penalty = {'Low': 0.05, 'Medium': 0.10, 'High': 0.20}.get(complexity, 0.10)
        
        # Timeline factor (rushed implementations are riskier)
        timeline = ai_initiative.get('timeline', '6-12 months')
        timeline_penalty = {'3-6 months': 0.15, '6-12 months': 0.05, 
                           '12-18 months': 0.02, '18+ months': 0.0}.get(timeline, 0.05)
        
        # Calculate final success probability
        risk_penalty = (technical_risk + adoption_risk + integration_risk) * 0.2
        total_penalty = risk_penalty + complexity_penalty + timeline_penalty
        
        success_probability = max(0.2, base_success - total_penalty)
        
        return success_probability
    
    def _calculate_summary_statistics(self, results: dict) -> dict:
        """Calculate summary statistics for simulation results"""
        
        stats = {}
        
        for metric, values in results.items():
            if metric == 'simulation_parameters':
                continue
                
            values = np.array(values)
            
            stats[metric] = {
                'mean': np.mean(values),
                'median': np.median(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'q25': np.percentile(values, 25),
                'q75': np.percentile(values, 75),
                'skewness': float(scipy_stats.skew(values)) if len(values) > 2 else 0.0,
                'kurtosis': float(scipy_stats.kurtosis(values)) if len(values) > 3 else 0.0
            }
        
        return stats
    
    def _calculate_risk_metrics(self, results: dict) -> dict:
        """Calculate risk-specific metrics"""
        
        roi_values = np.array(results['roi'])
        value_values = np.array(results['value_generated'])
        payback_values = np.array(results['payback_period'])
        
        return {
            'probability_positive_roi': np.mean(roi_values > 0),
            'probability_roi_above_15': np.mean(roi_values > 15),
            'probability_roi_above_25': np.mean(roi_values > 25),
            'probability_payback_under_24_months': np.mean(payback_values < 24),
            'probability_payback_under_36_months': np.mean(payback_values < 36),
            'value_at_risk_5': np.percentile(value_values, 5),  # 5% VaR
            'value_at_risk_10': np.percentile(value_values, 10),  # 10% VaR
            'expected_shortfall_5': np.mean(value_values[value_values <= np.percentile(value_values, 5)]),
            'maximum_loss': np.min(value_values),
            'probability_of_loss': np.mean(value_values < 0)
        }
    
    def _calculate_confidence_intervals(self, results: dict, confidence_levels: List[float] = [0.90, 0.95, 0.99]) -> dict:
        """Calculate confidence intervals for key metrics"""
        
        intervals = {}
        
        for metric in ['productivity_gain', 'value_generated', 'roi', 'payback_period']:
            values = np.array(results[metric])
            intervals[metric] = {}
            
            for conf_level in confidence_levels:
                alpha = 1 - conf_level
                lower = np.percentile(values, (alpha/2) * 100)
                upper = np.percentile(values, (1 - alpha/2) * 100)
                
                intervals[metric][f'{conf_level:.0%}'] = {
                    'lower': lower,
                    'upper': upper,
                    'range': upper - lower
                }
        
        return intervals
    
    def _perform_sensitivity_analysis(self, results: dict) -> dict:
        """Perform sensitivity analysis on simulation parameters"""
        
        # Convert simulation parameters to DataFrame for analysis
        param_data = []
        roi_values = results['roi']
        
        for i, params in enumerate(results['simulation_parameters']):
            if params:  # Skip empty parameter sets
                param_row = params.copy()
                param_row['roi'] = roi_values[i]
                param_data.append(param_row)
        
        if not param_data:
            return {}
        
        df = pd.DataFrame(param_data)
        
        # Calculate correlations
        correlations = {}
        if 'roi' in df.columns:
            for col in df.columns:
                if col != 'roi' and df[col].dtype in ['float64', 'int64']:
                    correlation = df['roi'].corr(df[col])
                    correlations[col] = correlation
        
        # Rank parameters by sensitivity
        sensitivity_ranking = sorted(correlations.items(), 
                                   key=lambda x: abs(x[1]), reverse=True)
        
        return {
            'correlations': correlations,
            'sensitivity_ranking': sensitivity_ranking,
            'most_sensitive_parameter': sensitivity_ranking[0][0] if sensitivity_ranking else None,
            'parameter_statistics': df.describe().to_dict() if len(df) > 0 else {}
        }
    
    def create_simulation_visualizations(self, simulation_data: dict) -> Dict[str, go.Figure]:
        """Create comprehensive visualizations for simulation results"""
        
        results = simulation_data['simulation_results']
        summary_stats = simulation_data['summary_statistics']
        
        visualizations = {}
        
        # 1. Distribution plots for key metrics
        visualizations['distributions'] = self._create_distribution_plots(results, summary_stats)
        
        # 2. Risk analysis charts
        visualizations['risk_analysis'] = self._create_risk_analysis_charts(simulation_data)
        
        # 3. Sensitivity analysis
        visualizations['sensitivity'] = self._create_sensitivity_charts(simulation_data)
        
        # 4. Scenario comparison
        visualizations['scenario_comparison'] = self._create_scenario_comparison(simulation_data)
        
        # 5. Confidence intervals
        visualizations['confidence_intervals'] = self._create_confidence_interval_chart(simulation_data)
        
        return visualizations
    
    def _create_distribution_plots(self, results: dict, summary_stats: dict) -> go.Figure:
        """Create distribution plots for key metrics"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['ROI Distribution', 'Value Generated Distribution', 
                          'Productivity Gain Distribution', 'Payback Period Distribution'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        metrics = [
            ('roi', 'ROI (%)', 1, 1),
            ('value_generated', 'Value ($)', 1, 2),
            ('productivity_gain', 'Productivity Gain (%)', 2, 1),
            ('payback_period', 'Payback (months)', 2, 2)
        ]
        
        for metric, title, row, col in metrics:
            values = results[metric]
            
            # Histogram
            fig.add_trace(
                go.Histogram(x=values, name=f'{metric}_hist', 
                           opacity=0.7, showlegend=False),
                row=row, col=col
            )
            
            # Add mean line
            mean_val = summary_stats[metric]['mean']
            fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                         annotation_text=f"Mean: {mean_val:.1f}",
                         row=row, col=col)
        
        fig.update_layout(height=600, title_text="Monte Carlo Simulation Results - Distributions")
        return fig
    
    def _create_risk_analysis_charts(self, simulation_data: dict) -> go.Figure:
        """Create risk analysis visualization"""
        
        risk_metrics = simulation_data['risk_metrics']
        
        # Probability chart
        probabilities = [
            ('Positive ROI', risk_metrics['probability_positive_roi']),
            ('ROI > 15%', risk_metrics['probability_roi_above_15']),
            ('ROI > 25%', risk_metrics['probability_roi_above_25']),
            ('Payback < 24mo', risk_metrics['probability_payback_under_24_months']),
            ('Payback < 36mo', risk_metrics['probability_payback_under_36_months'])
        ]
        
        fig = go.Figure()
        
        labels, values = zip(*probabilities)
        
        fig.add_trace(go.Bar(
            x=labels,
            y=values,
            text=[f'{v:.1%}' for v in values],
            textposition='auto',
            name='Probability'
        ))
        
        fig.update_layout(
            title="Risk Analysis - Success Probabilities",
            xaxis_title="Outcome",
            yaxis_title="Probability",
            yaxis=dict(tickformat='.0%')
        )
        
        return fig
    
    def _create_sensitivity_charts(self, simulation_data: dict) -> go.Figure:
        """Create sensitivity analysis chart"""
        
        sensitivity = simulation_data['sensitivity_analysis']
        
        if not sensitivity.get('sensitivity_ranking'):
            return go.Figure().add_annotation(text="No sensitivity data available")
        
        params, correlations = zip(*sensitivity['sensitivity_ranking'])
        
        fig = go.Figure()
        
        colors = ['red' if c < 0 else 'green' for c in correlations]
        
        fig.add_trace(go.Bar(
            x=correlations,
            y=params,
            orientation='h',
            marker_color=colors,
            text=[f'{c:.3f}' for c in correlations],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Sensitivity Analysis - Parameter Impact on ROI",
            xaxis_title="Correlation with ROI",
            yaxis_title="Parameters"
        )
        
        return fig
    
    def _create_scenario_comparison(self, simulation_data: dict) -> go.Figure:
        """Create scenario comparison chart"""
        
        summary_stats = simulation_data['summary_statistics']
        
        metrics = ['roi', 'value_generated', 'productivity_gain']
        scenarios = ['Pessimistic (Q25)', 'Expected (Mean)', 'Optimistic (Q75)']
        
        fig = go.Figure()
        
        for metric in metrics:
            values = [
                summary_stats[metric]['q25'],
                summary_stats[metric]['mean'],
                summary_stats[metric]['q75']
            ]
            
            fig.add_trace(go.Scatter(
                x=scenarios,
                y=values,
                mode='lines+markers',
                name=metric.replace('_', ' ').title(),
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Scenario Comparison - Key Metrics",
            xaxis_title="Scenario",
            yaxis_title="Value"
        )
        
        return fig
    
    def _create_confidence_interval_chart(self, simulation_data: dict) -> go.Figure:
        """Create confidence interval visualization"""
        
        confidence_intervals = simulation_data['confidence_intervals']
        
        fig = go.Figure()
        
        metrics = ['roi', 'value_generated', 'productivity_gain']
        
        for metric in metrics:
            if metric in confidence_intervals:
                ci_95 = confidence_intervals[metric]['95%']
                
                fig.add_trace(go.Scatter(
                    x=[metric],
                    y=[ci_95['lower']],
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[ci_95['upper'] - ci_95['lower']],
                        arrayminus=[0]
                    ),
                    mode='markers',
                    name=f'{metric} 95% CI',
                    marker=dict(size=10)
                ))
        
        fig.update_layout(
            title="95% Confidence Intervals",
            xaxis_title="Metrics",
            yaxis_title="Value Range"
        )
        
        return fig

class ScenarioModeler:
    """Advanced scenario modeling with Monte Carlo capabilities"""
    
    def __init__(self):
        self.monte_carlo = MonteCarloSimulator()
        
    def compare_multiple_scenarios(self, baseline_data: dict, 
                                 scenario_configs: List[dict]) -> dict:
        """Compare multiple AI implementation scenarios using Monte Carlo"""
        
        scenario_results = {}
        
        for i, config in enumerate(scenario_configs):
            scenario_name = config.get('name', f'Scenario {i+1}')
            
            # Run Monte Carlo simulation for this scenario
            simulation_result = self.monte_carlo.run_simulation(
                baseline_data, 
                config['ai_initiative'],
                config.get('uncertainty_parameters')
            )
            
            scenario_results[scenario_name] = simulation_result
        
        # Create comparative analysis
        comparison = self._create_scenario_comparison(scenario_results)
        
        return {
            'individual_scenarios': scenario_results,
            'comparative_analysis': comparison
        }
    
    def _create_scenario_comparison(self, scenario_results: dict) -> dict:
        """Create comparative analysis across scenarios"""
        
        comparison = {
            'summary_table': {},
            'risk_comparison': {},
            'recommendations': []
        }
        
        # Summary statistics comparison
        for scenario_name, results in scenario_results.items():
            summary = results['summary_statistics']
            comparison['summary_table'][scenario_name] = {
                'expected_roi': summary['roi']['mean'],
                'roi_std': summary['roi']['std'],
                'expected_value': summary['value_generated']['mean'],
                'value_std': summary['value_generated']['std'],
                'probability_success': results['risk_metrics']['probability_positive_roi']
            }
        
        # Risk comparison
        for scenario_name, results in scenario_results.items():
            risk_metrics = results['risk_metrics']
            comparison['risk_comparison'][scenario_name] = {
                'value_at_risk_5': risk_metrics['value_at_risk_5'],
                'probability_positive_roi': risk_metrics['probability_positive_roi'],
                'maximum_loss': risk_metrics['maximum_loss']
            }
        
        # Generate recommendations
        comparison['recommendations'] = self._generate_recommendations(comparison)
        
        return comparison
    
    def _generate_recommendations(self, comparison: dict) -> List[str]:
        """Generate strategic recommendations based on scenario analysis"""
        
        recommendations = []
        
        summary_table = comparison['summary_table']
        risk_comparison = comparison['risk_comparison']
        
        # Find best performing scenario
        best_roi_scenario = max(summary_table.keys(), 
                               key=lambda x: summary_table[x]['expected_roi'])
        
        best_risk_scenario = max(risk_comparison.keys(),
                                key=lambda x: risk_comparison[x]['probability_positive_roi'])
        
        recommendations.append(f"Highest expected ROI: {best_roi_scenario}")
        recommendations.append(f"Lowest risk profile: {best_risk_scenario}")
        
        # Risk-return analysis
        for scenario, metrics in summary_table.items():
            roi = metrics['expected_roi']
            risk = metrics['roi_std']
            prob_success = comparison['risk_comparison'][scenario]['probability_positive_roi']
            
            if roi > 20 and prob_success > 0.8:
                recommendations.append(f"{scenario}: High return, high confidence - Recommended")
            elif roi > 15 and prob_success > 0.7:
                recommendations.append(f"{scenario}: Moderate return, good confidence - Consider")
            elif prob_success < 0.6:
                recommendations.append(f"{scenario}: High risk - Proceed with caution")
        
        return recommendations