import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')

from .data_models import MetricsCalculator, TimeSeriesGenerator

class PredictiveEngine:
    """Main engine for predictive modeling of AI implementation impact"""
    
    def __init__(self):
        self.metrics_calc = MetricsCalculator()
        self.ts_generator = TimeSeriesGenerator()
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize machine learning models"""
        self.models = {
            'productivity': RandomForestRegressor(n_estimators=100, random_state=42),
            'value': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'roi': LinearRegression(),
            'risk': RandomForestRegressor(n_estimators=50, random_state=42)
        }
    
    def predict_impact(self, baseline_data: dict, ai_initiative: dict) -> dict:
        """
        Main prediction method that calculates impact across all metrics
        """
        try:
            # Extract key parameters
            baseline_productivity = baseline_data['productivity']
            baseline_revenue = baseline_data['revenue']
            baseline_costs = baseline_data['costs']
            investment = ai_initiative['investment']
            
            # Calculate productivity improvements
            productivity_gain = self._predict_productivity_gain(baseline_data, ai_initiative)
            
            # Calculate value generation
            value_generated = self._predict_value_generation(baseline_data, ai_initiative, productivity_gain)
            
            # Calculate ROI
            roi = self._predict_roi(value_generated, investment, baseline_costs, ai_initiative)
            
            # Calculate payback period
            monthly_value = value_generated / 12
            payback_period = self.metrics_calc.calculate_payback_period(investment, monthly_value)
            
            # Calculate workforce impact
            workforce_impact = self._calculate_workforce_impact(baseline_data, ai_initiative)
            
            # Apply risk adjustments
            risk_factors = {
                'technical_risk': ai_initiative.get('technical_risk', 30),
                'adoption_risk': ai_initiative.get('adoption_risk', 30),
                'integration_risk': ai_initiative.get('integration_risk', 30)
            }
            
            risk_adjusted_roi = self.metrics_calc.apply_risk_adjustment(roi, risk_factors)
            risk_adjusted_value = self.metrics_calc.apply_risk_adjustment(value_generated, risk_factors)
            
            # Calculate confidence intervals
            confidence_interval = self._calculate_confidence_intervals(
                productivity_gain, value_generated, roi, risk_factors
            )
            
            return {
                'productivity_gain': productivity_gain,
                'value_generated': risk_adjusted_value,
                'roi': risk_adjusted_roi,
                'payback_period': payback_period,
                'workforce_impact': workforce_impact,
                'risk_adjusted_roi': risk_adjusted_roi,
                'confidence_interval': confidence_interval,
                'monthly_value': monthly_value,
                'annual_savings': self._calculate_annual_savings(baseline_data, ai_initiative)
            }
            
        except Exception as e:
            # Return default values in case of error
            return {
                'productivity_gain': 0.0,
                'value_generated': 0.0,
                'roi': 0.0,
                'payback_period': float('inf'),
                'workforce_impact': {'reduction': 0, 'upskilling': 0, 'new_roles': 0},
                'risk_adjusted_roi': 0.0,
                'confidence_interval': {'lower': 0, 'upper': 0},
                'monthly_value': 0.0,
                'annual_savings': 0.0,
                'error': str(e)
            }
    
    def _predict_productivity_gain(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Predict productivity gain based on AI implementation"""
        
        # Base productivity calculation using improvement factors
        automation_impact = ai_initiative.get('automation_level', 0) * 0.6
        accuracy_impact = ai_initiative.get('accuracy_improvement', 0) * 0.3
        speed_impact = ai_initiative.get('speed_improvement', 0) * 0.4
        
        # Weight by AI type
        ai_type_multipliers = {
            'Automation': 1.2,
            'Augmentation': 0.9,
            'Analytics': 0.7,
            'Hybrid': 1.1
        }
        
        type_multiplier = ai_type_multipliers.get(ai_initiative.get('type', 'Hybrid'), 1.0)
        
        # Complexity adjustment
        complexity_adjustments = {
            'Low': 1.1,
            'Medium': 1.0,
            'High': 0.85
        }
        
        complexity_adj = complexity_adjustments.get(ai_initiative.get('complexity', 'Medium'), 1.0)
        
        # Calculate base productivity gain
        base_gain = (automation_impact + accuracy_impact + speed_impact) / 3
        adjusted_gain = base_gain * type_multiplier * complexity_adj
        
        # Apply diminishing returns for high baseline productivity
        baseline_factor = 1 - (baseline_data['productivity'] / 100) * 0.3
        final_gain = adjusted_gain * baseline_factor
        
        return min(final_gain, 60.0)  # Cap at 60% gain
    
    def _predict_value_generation(self, baseline_data: dict, ai_initiative: dict, productivity_gain: float) -> float:
        """Predict monetary value generation"""
        
        baseline_revenue = baseline_data['revenue']
        
        # Primary value from productivity improvements
        productivity_value = baseline_revenue * (productivity_gain / 100)
        
        # Additional value streams
        cost_reduction = self._calculate_cost_reduction(baseline_data, ai_initiative)
        revenue_enhancement = self._calculate_revenue_enhancement(baseline_data, ai_initiative)
        
        # Scale by implementation timeline
        timeline_months = self._parse_timeline(ai_initiative.get('timeline', '12 months'))
        timeline_factor = max(0.7, 1 - (timeline_months - 6) / 24)  # Longer implementations have reduced first-year impact
        
        total_value = (productivity_value + cost_reduction + revenue_enhancement) * timeline_factor
        
        return max(total_value, 0)
    
    def _predict_roi(self, value_generated: float, investment: float, baseline_costs: float, ai_initiative: dict) -> float:
        """Predict return on investment"""
        
        # Calculate ongoing costs (maintenance, training, etc.)
        ongoing_costs_factor = {
            'Low': 0.05,    # 5% of investment annually
            'Medium': 0.08,  # 8% of investment annually
            'High': 0.12     # 12% of investment annually
        }
        
        complexity = ai_initiative.get('complexity', 'Medium')
        annual_ongoing_costs = investment * ongoing_costs_factor.get(complexity, 0.08)
        
        # Calculate net value (first year)
        net_value = value_generated - annual_ongoing_costs
        
        if investment == 0:
            return 0
        
        roi = (net_value / investment) * 100
        
        return roi
    
    def _calculate_workforce_impact(self, baseline_data: dict, ai_initiative: dict) -> dict:
        """Calculate detailed workforce impact"""
        
        current_headcount = baseline_data['headcount']
        
        # Direct workforce changes
        workforce_reduction = ai_initiative.get('workforce_reduction', 0)
        new_roles_created = ai_initiative.get('new_roles_created', 0)
        upskilling_required = ai_initiative.get('upskilling_required', 0)
        
        # Calculate absolute numbers
        reduced_positions = int(current_headcount * workforce_reduction / 100)
        new_positions = int(current_headcount * new_roles_created / 100)
        upskilling_count = int(current_headcount * upskilling_required / 100)
        
        # Net headcount change
        net_headcount_change = new_positions - reduced_positions
        
        return {
            'reduction': reduced_positions,
            'new_roles': new_positions,
            'upskilling': upskilling_count,
            'net_change': net_headcount_change,
            'percentage_change': (net_headcount_change / current_headcount) * 100
        }
    
    def _calculate_cost_reduction(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate cost reduction from AI implementation"""
        
        baseline_costs = baseline_data['costs']
        automation_level = ai_initiative.get('automation_level', 0)
        
        # Cost reduction primarily from automation
        direct_cost_reduction = baseline_costs * (automation_level / 100) * 0.3  # 30% of automated costs saved
        
        # Additional savings from accuracy improvements (reduced errors/rework)
        accuracy_improvement = ai_initiative.get('accuracy_improvement', 0)
        error_cost_reduction = baseline_costs * (accuracy_improvement / 100) * 0.1  # 10% of costs from errors
        
        total_cost_reduction = direct_cost_reduction + error_cost_reduction
        
        return total_cost_reduction
    
    def _calculate_revenue_enhancement(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate revenue enhancement from AI implementation"""
        
        baseline_revenue = baseline_data['revenue']
        
        # Revenue enhancement from speed improvements (faster delivery, more capacity)
        speed_improvement = ai_initiative.get('speed_improvement', 0)
        capacity_revenue = baseline_revenue * (speed_improvement / 100) * 0.2  # 20% of speed improvement translates to revenue
        
        # Revenue enhancement from accuracy improvements (better quality, customer satisfaction)
        accuracy_improvement = ai_initiative.get('accuracy_improvement', 0)
        quality_revenue = baseline_revenue * (accuracy_improvement / 100) * 0.15  # 15% of accuracy improvement
        
        total_revenue_enhancement = capacity_revenue + quality_revenue
        
        return total_revenue_enhancement
    
    def _calculate_annual_savings(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate total annual savings"""
        
        cost_reduction = self._calculate_cost_reduction(baseline_data, ai_initiative)
        
        # Labor cost savings from workforce reduction
        workforce_reduction = ai_initiative.get('workforce_reduction', 0)
        avg_salary = baseline_data['costs'] / baseline_data['headcount'] * 0.7  # Assume 70% of costs are labor
        labor_savings = baseline_data['headcount'] * (workforce_reduction / 100) * avg_salary
        
        total_savings = cost_reduction + labor_savings
        
        return total_savings
    
    def _calculate_confidence_intervals(self, productivity_gain: float, value_generated: float, 
                                     roi: float, risk_factors: dict) -> dict:
        """Calculate confidence intervals for predictions"""
        
        # Base uncertainty factors
        base_uncertainty = 0.2  # 20% base uncertainty
        
        # Adjust uncertainty based on risk factors
        avg_risk = (risk_factors['technical_risk'] + risk_factors['adoption_risk'] + 
                   risk_factors['integration_risk']) / 3
        risk_uncertainty = (avg_risk / 100) * 0.3  # Additional 30% uncertainty for high risk
        
        total_uncertainty = base_uncertainty + risk_uncertainty
        
        return {
            'productivity_gain': {
                'lower': productivity_gain * (1 - total_uncertainty),
                'upper': productivity_gain * (1 + total_uncertainty)
            },
            'value_generated': {
                'lower': value_generated * (1 - total_uncertainty),
                'upper': value_generated * (1 + total_uncertainty)
            },
            'roi': {
                'lower': roi * (1 - total_uncertainty),
                'upper': roi * (1 + total_uncertainty)
            }
        }
    
    def _parse_timeline(self, timeline_str: str) -> int:
        """Parse timeline string to months"""
        timeline_map = {
            '3 months': 3,
            '6 months': 6,
            '12 months': 12,
            '18 months': 18,
            '24 months': 24
        }
        return timeline_map.get(timeline_str, 12)
    
    def generate_temporal_projection(self, baseline_data: dict, ai_initiative: dict, 
                                   predictions: dict, months: int) -> dict:
        """Generate month-by-month projections"""
        
        # Get implementation timeline
        impl_months = self._parse_timeline(ai_initiative.get('timeline', '12 months'))
        
        # Generate adoption curve
        adoption_curve = self.ts_generator.generate_adoption_curve(impl_months, "s-curve")
        
        # Extend adoption curve to full timeline
        if months > impl_months:
            full_adoption = [1.0] * (months - impl_months)
            adoption_curve.extend(full_adoption)
        else:
            adoption_curve = adoption_curve[:months]
        
        # Generate monthly projections
        monthly_data = {
            'month': list(range(1, months + 1)),
            'adoption_rate': adoption_curve,
            'monthly_value': [],
            'cumulative_value': [],
            'monthly_roi': [],
            'cumulative_roi': [],
            'productivity_level': [],
            'cost_savings': []
        }
        
        base_monthly_value = predictions['value_generated'] / 12
        cumulative_value = 0
        investment = ai_initiative['investment']
        
        for i, adoption in enumerate(adoption_curve):
            # Calculate monthly value with adoption rate
            monthly_value = base_monthly_value * adoption
            cumulative_value += monthly_value
            
            # Calculate ROI
            if investment > 0:
                monthly_roi = (monthly_value / investment) * 100
                cumulative_roi = ((cumulative_value - investment) / investment) * 100
            else:
                monthly_roi = 0
                cumulative_roi = 0
            
            # Calculate productivity level
            base_productivity = baseline_data['productivity']
            max_gain = predictions['productivity_gain']
            current_productivity = base_productivity + (max_gain * adoption)
            
            # Calculate cost savings
            monthly_savings = predictions.get('annual_savings', 0) / 12 * adoption
            
            monthly_data['monthly_value'].append(monthly_value)
            monthly_data['cumulative_value'].append(cumulative_value)
            monthly_data['monthly_roi'].append(monthly_roi)
            monthly_data['cumulative_roi'].append(cumulative_roi)
            monthly_data['productivity_level'].append(current_productivity)
            monthly_data['cost_savings'].append(monthly_savings)
        
        return monthly_data
    
    def compare_scenarios(self, baseline_scenario: dict, ai_scenarios: list) -> dict:
        """Compare multiple AI implementation scenarios"""
        
        comparison_results = {
            'baseline': baseline_scenario,
            'scenarios': [],
            'best_scenario': None,
            'comparison_metrics': {}
        }
        
        best_roi = -float('inf')
        best_scenario_idx = -1
        
        for i, scenario in enumerate(ai_scenarios):
            scenario_result = self.predict_impact(baseline_scenario, scenario)
            scenario_result['scenario_name'] = f"Scenario {i+1}"
            scenario_result['configuration'] = scenario
            
            comparison_results['scenarios'].append(scenario_result)
            
            # Track best scenario by risk-adjusted ROI
            if scenario_result['risk_adjusted_roi'] > best_roi:
                best_roi = scenario_result['risk_adjusted_roi']
                best_scenario_idx = i
        
        if best_scenario_idx >= 0:
            comparison_results['best_scenario'] = comparison_results['scenarios'][best_scenario_idx]
        
        # Calculate comparison metrics
        comparison_results['comparison_metrics'] = self._calculate_scenario_metrics(
            comparison_results['scenarios']
        )
        
        return comparison_results
    
    def _calculate_scenario_metrics(self, scenarios: list) -> dict:
        """Calculate metrics for scenario comparison"""
        
        if not scenarios:
            return {}
        
        rois = [s['roi'] for s in scenarios]
        values = [s['value_generated'] for s in scenarios]
        paybacks = [s['payback_period'] for s in scenarios if s['payback_period'] != float('inf')]
        
        metrics = {
            'avg_roi': np.mean(rois),
            'max_roi': np.max(rois),
            'min_roi': np.min(rois),
            'total_value': np.sum(values),
            'avg_value': np.mean(values)
        }
        
        if paybacks:
            metrics['avg_payback'] = np.mean(paybacks)
            metrics['min_payback'] = np.min(paybacks)
        
        return metrics
