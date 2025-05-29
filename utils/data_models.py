from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta

@dataclass
class EnterpriseFunction:
    """Data model for enterprise function baseline metrics"""
    name: str
    current_productivity: float  # 0-100 scale
    headcount: int
    annual_revenue: float
    annual_costs: float
    performance_satisfaction: float  # 0-100 scale
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'productivity': self.current_productivity,
            'headcount': self.headcount,
            'revenue': self.annual_revenue,
            'costs': self.annual_costs,
            'satisfaction': self.performance_satisfaction
        }

@dataclass
class AIInitiative:
    """Data model for AI initiative configuration"""
    function_name: str
    ai_type: str  # Automation, Augmentation, Analytics, Hybrid
    complexity: str  # Low, Medium, High
    investment: float
    timeline: str  # Implementation timeline
    change_management: str  # Gradual, Phased, Big Bang
    
    # Risk factors (0-100)
    technical_risk: float
    adoption_risk: float
    integration_risk: float
    
    # Expected improvements (0-100%)
    automation_level: float
    accuracy_improvement: float
    speed_improvement: float
    
    # Workforce impact
    workforce_reduction: float  # 0-50%
    upskilling_required: float  # 0-100%
    new_roles_created: float  # 0-30%
    
    def get_risk_score(self) -> float:
        """Calculate overall risk score"""
        return (self.technical_risk + self.adoption_risk + self.integration_risk) / 3
    
    def get_improvement_score(self) -> float:
        """Calculate overall improvement potential"""
        return (self.automation_level + self.accuracy_improvement + self.speed_improvement) / 3
    
    def to_dict(self) -> Dict:
        return {
            'function': self.function_name,
            'type': self.ai_type,
            'complexity': self.complexity,
            'investment': self.investment,
            'timeline': self.timeline,
            'change_management': self.change_management,
            'risk_score': self.get_risk_score(),
            'improvement_score': self.get_improvement_score(),
            'workforce_impact': {
                'reduction': self.workforce_reduction,
                'upskilling': self.upskilling_required,
                'new_roles': self.new_roles_created
            }
        }

@dataclass
class PredictionResult:
    """Data model for prediction results"""
    function_name: str
    productivity_gain: float
    value_generated: float
    roi: float
    payback_period: float  # in months
    workforce_impact: Dict
    risk_adjusted_roi: float
    confidence_interval: Dict
    
    def to_dict(self) -> Dict:
        return {
            'function': self.function_name,
            'productivity_gain': self.productivity_gain,
            'value_generated': self.value_generated,
            'roi': self.roi,
            'payback_period': self.payback_period,
            'workforce_impact': self.workforce_impact,
            'risk_adjusted_roi': self.risk_adjusted_roi,
            'confidence_interval': self.confidence_interval
        }

class DataValidator:
    """Utility class for data validation"""
    
    @staticmethod
    def validate_baseline_metrics(data: Dict) -> List[str]:
        """Validate baseline metrics data"""
        errors = []
        
        required_fields = ['productivity', 'headcount', 'revenue', 'costs', 'satisfaction']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if 'productivity' in data and not (0 <= data['productivity'] <= 100):
            errors.append("Productivity must be between 0 and 100")
        
        if 'headcount' in data and data['headcount'] <= 0:
            errors.append("Headcount must be positive")
        
        if 'revenue' in data and data['revenue'] < 0:
            errors.append("Revenue cannot be negative")
        
        if 'costs' in data and data['costs'] < 0:
            errors.append("Costs cannot be negative")
        
        if 'satisfaction' in data and not (0 <= data['satisfaction'] <= 100):
            errors.append("Satisfaction must be between 0 and 100")
        
        return errors
    
    @staticmethod
    def validate_ai_initiative(data: Dict) -> List[str]:
        """Validate AI initiative data"""
        errors = []
        
        required_fields = ['type', 'complexity', 'investment', 'timeline']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if 'investment' in data and data['investment'] <= 0:
            errors.append("Investment must be positive")
        
        # Validate risk factors
        risk_fields = ['technical_risk', 'adoption_risk', 'integration_risk']
        for field in risk_fields:
            if field in data and not (0 <= data[field] <= 100):
                errors.append(f"{field} must be between 0 and 100")
        
        # Validate improvement factors
        improvement_fields = ['automation_level', 'accuracy_improvement', 'speed_improvement']
        for field in improvement_fields:
            if field in data and not (0 <= data[field] <= 100):
                errors.append(f"{field} must be between 0 and 100")
        
        # Validate workforce impact
        if 'workforce_reduction' in data and not (0 <= data['workforce_reduction'] <= 50):
            errors.append("Workforce reduction must be between 0 and 50%")
        
        return errors

class MetricsCalculator:
    """Utility class for metrics calculations"""
    
    @staticmethod
    def calculate_productivity_index(baseline: float, improvements: Dict) -> float:
        """Calculate productivity index based on improvements"""
        automation_factor = improvements.get('automation_level', 0) * 0.4
        accuracy_factor = improvements.get('accuracy_improvement', 0) * 0.3
        speed_factor = improvements.get('speed_improvement', 0) * 0.3
        
        total_improvement = (automation_factor + accuracy_factor + speed_factor) / 100
        new_productivity = baseline * (1 + total_improvement)
        
        return min(new_productivity, 100.0)  # Cap at 100
    
    @staticmethod
    def calculate_value_generation(baseline_revenue: float, productivity_gain: float, 
                                 efficiency_improvements: Dict) -> float:
        """Calculate value generation from AI implementation"""
        # Base value from productivity improvements
        productivity_value = baseline_revenue * (productivity_gain / 100)
        
        # Additional value from specific improvements
        automation_value = baseline_revenue * (efficiency_improvements.get('automation_level', 0) / 100) * 0.15
        accuracy_value = baseline_revenue * (efficiency_improvements.get('accuracy_improvement', 0) / 100) * 0.10
        
        total_value = productivity_value + automation_value + accuracy_value
        
        return total_value
    
    @staticmethod
    def calculate_roi(value_generated: float, investment: float, 
                     ongoing_costs: float = 0, time_period: int = 12) -> float:
        """Calculate ROI over specified time period (months)"""
        total_value = value_generated * (time_period / 12)  # Annualized value
        total_costs = investment + (ongoing_costs * time_period / 12)
        
        if total_costs == 0:
            return 0
        
        roi = ((total_value - total_costs) / total_costs) * 100
        return roi
    
    @staticmethod
    def calculate_payback_period(investment: float, monthly_value: float) -> float:
        """Calculate payback period in months"""
        if monthly_value <= 0:
            return float('inf')  # Never pays back
        
        return investment / monthly_value
    
    @staticmethod
    def apply_risk_adjustment(base_value: float, risk_factors: Dict) -> float:
        """Apply risk adjustment to base calculations"""
        technical_risk = risk_factors.get('technical_risk', 0) / 100
        adoption_risk = risk_factors.get('adoption_risk', 0) / 100
        integration_risk = risk_factors.get('integration_risk', 0) / 100
        
        # Calculate overall risk multiplier
        risk_multiplier = 1 - ((technical_risk + adoption_risk + integration_risk) / 3) * 0.3
        
        return base_value * risk_multiplier

class TimeSeriesGenerator:
    """Utility class for generating time-series data"""
    
    @staticmethod
    def generate_adoption_curve(months: int, curve_type: str = "s-curve") -> List[float]:
        """Generate adoption curve over time"""
        import numpy as np
        
        time_points = np.linspace(0, months, months)
        
        if curve_type == "s-curve":
            # S-curve adoption pattern
            adoption = 1 / (1 + np.exp(-0.3 * (time_points - months/2)))
        elif curve_type == "linear":
            # Linear adoption
            adoption = time_points / months
        elif curve_type == "exponential":
            # Exponential adoption
            adoption = 1 - np.exp(-0.1 * time_points)
        else:
            # Default to S-curve
            adoption = 1 / (1 + np.exp(-0.3 * (time_points - months/2)))
        
        return adoption.tolist()
    
    @staticmethod
    def generate_value_progression(base_value: float, months: int, 
                                 adoption_curve: List[float]) -> List[float]:
        """Generate value progression over time"""
        value_progression = []
        
        for i, adoption_rate in enumerate(adoption_curve):
            # Account for learning curve and optimization over time
            learning_factor = min(1.0 + (i / months) * 0.2, 1.3)  # Up to 30% improvement
            monthly_value = base_value * adoption_rate * learning_factor / 12
            value_progression.append(monthly_value)
        
        return value_progression
    
    @staticmethod
    def add_uncertainty_bands(values: List[float], confidence_level: float = 0.95) -> Dict:
        """Add confidence intervals to predictions"""
        import numpy as np
        
        # Calculate standard deviation based on typical AI project variability
        std_dev = np.std(values) * 0.3  # 30% variability assumption
        
        confidence_factor = 1.96 if confidence_level == 0.95 else 2.58  # 99% confidence
        
        upper_bound = [v + confidence_factor * std_dev for v in values]
        lower_bound = [max(0, v - confidence_factor * std_dev) for v in values]
        
        return {
            'values': values,
            'upper_bound': upper_bound,
            'lower_bound': lower_bound,
            'confidence_level': confidence_level
        }
