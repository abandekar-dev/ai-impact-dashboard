from typing import Dict, List, Tuple
import streamlit as st

# Import dependencies through compatibility layer
try:
    from .compatibility import (
        np, pd, NUMPY_AVAILABLE, PANDAS_AVAILABLE
    )
except ImportError:
    try:
        import numpy as np
        import pandas as pd
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = PANDAS_AVAILABLE = False
from .monte_carlo import MonteCarloSimulator, ScenarioModeler

class StrategicScenarioPlanner:
    """Strategic scenario planning for AI implementation based on business value questions"""
    
    def __init__(self):
        self.scenario_modeler = ScenarioModeler()
        self.business_value_scenarios = {}
        
    def create_business_value_scenarios(self, baseline_data: dict) -> Dict[str, dict]:
        """Create scenarios based on where AI will create real business value in next 12 months"""
        
        scenarios = {
            "Value Chain Optimization": {
                "name": "Value Chain Optimization",
                "description": "Focus on bottlenecked processes with high human throughput requirements",
                "ai_initiative": {
                    "ai_type": "Automation",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.08,  # 8% of revenue
                    "timeline": "6-12 months",
                    "change_management": "Phased",
                    "automation_level": 70,
                    "accuracy_improvement": 35,
                    "speed_improvement": 60,
                    "workforce_reduction": 20,
                    "upskilling_required": 40,
                    "new_roles_created": 8,
                    "technical_risk": 0.25,
                    "adoption_risk": 0.30,
                    "integration_risk": 0.20
                },
                "uncertainty_parameters": {
                    "automation_level": {"distribution": "normal", "std_pct": 0.25},
                    "speed_improvement": {"distribution": "normal", "std_pct": 0.30}
                }
            },
            
            "Data Insight Monetization": {
                "name": "Data Insight Monetization", 
                "description": "Leverage rich but under-utilized data for predictive insights",
                "ai_initiative": {
                    "ai_type": "Analytics",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.06,  # 6% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Gradual",
                    "automation_level": 40,
                    "accuracy_improvement": 50,
                    "speed_improvement": 35,
                    "workforce_reduction": 5,
                    "upskilling_required": 70,
                    "new_roles_created": 15,
                    "technical_risk": 0.35,
                    "adoption_risk": 0.25,
                    "integration_risk": 0.30
                },
                "uncertainty_parameters": {
                    "accuracy_improvement": {"distribution": "normal", "std_pct": 0.35},
                    "technical_risk": {"distribution": "beta", "alpha": 3, "beta": 4}
                }
            },
            
            "Customer Experience Enhancement": {
                "name": "Customer Experience Enhancement",
                "description": "Proactive and predictive customer touchpoints",
                "ai_initiative": {
                    "ai_type": "Augmentation",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.05,  # 5% of revenue
                    "timeline": "6-12 months",
                    "change_management": "Phased",
                    "automation_level": 50,
                    "accuracy_improvement": 40,
                    "speed_improvement": 45,
                    "workforce_reduction": 10,
                    "upskilling_required": 60,
                    "new_roles_created": 12,
                    "technical_risk": 0.20,
                    "adoption_risk": 0.35,
                    "integration_risk": 0.25
                },
                "uncertainty_parameters": {
                    "adoption_risk": {"distribution": "beta", "alpha": 2, "beta": 5},
                    "accuracy_improvement": {"distribution": "normal", "std_pct": 0.20}
                }
            }
        }
        
        return scenarios
    
    def create_integration_depth_scenarios(self, baseline_data: dict) -> Dict[str, dict]:
        """Scenarios for building AI into business vs layering on top"""
        
        scenarios = {
            "Surface Layer AI": {
                "name": "Surface Layer AI",
                "description": "Tool-based add-ons with minimal workflow integration",
                "ai_initiative": {
                    "ai_type": "Augmentation",
                    "complexity": "Low",
                    "investment": baseline_data['revenue'] * 0.03,  # 3% of revenue
                    "timeline": "3-6 months",
                    "change_management": "Gradual",
                    "automation_level": 25,
                    "accuracy_improvement": 20,
                    "speed_improvement": 30,
                    "workforce_reduction": 0,
                    "upskilling_required": 30,
                    "new_roles_created": 3,
                    "technical_risk": 0.15,
                    "adoption_risk": 0.20,
                    "integration_risk": 0.10
                }
            },
            
            "Deep Integration AI": {
                "name": "Deep Integration AI", 
                "description": "AI embedded in core decision points and workflows",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.12,  # 12% of revenue
                    "timeline": "18+ months",
                    "change_management": "Big Bang",
                    "automation_level": 65,
                    "accuracy_improvement": 55,
                    "speed_improvement": 70,
                    "workforce_reduction": 25,
                    "upskilling_required": 80,
                    "new_roles_created": 20,
                    "technical_risk": 0.40,
                    "adoption_risk": 0.45,
                    "integration_risk": 0.50
                }
            },
            
            "Progressive Integration": {
                "name": "Progressive Integration",
                "description": "Balanced approach with selective deep integration",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.07,  # 7% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Phased",
                    "automation_level": 50,
                    "accuracy_improvement": 40,
                    "speed_improvement": 50,
                    "workforce_reduction": 15,
                    "upskilling_required": 65,
                    "new_roles_created": 15,
                    "technical_risk": 0.25,
                    "adoption_risk": 0.30,
                    "integration_risk": 0.25
                }
            }
        }
        
        return scenarios
    
    def create_talent_readiness_scenarios(self, baseline_data: dict) -> Dict[str, dict]:
        """Scenarios based on talent and managerial readiness for AI"""
        
        scenarios = {
            "Leadership-Led Transformation": {
                "name": "Leadership-Led Transformation",
                "description": "High leadership AI fluency driving organization-wide adoption",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.09,  # 9% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Phased",
                    "automation_level": 55,
                    "accuracy_improvement": 45,
                    "speed_improvement": 55,
                    "workforce_reduction": 12,
                    "upskilling_required": 75,
                    "new_roles_created": 18,
                    "technical_risk": 0.20,
                    "adoption_risk": 0.25,
                    "integration_risk": 0.20
                }
            },
            
            "Grassroots Innovation": {
                "name": "Grassroots Innovation",
                "description": "Bottom-up AI adoption with varying leadership support",
                "ai_initiative": {
                    "ai_type": "Augmentation", 
                    "complexity": "Low",
                    "investment": baseline_data['revenue'] * 0.04,  # 4% of revenue
                    "timeline": "6-12 months",
                    "change_management": "Gradual",
                    "automation_level": 35,
                    "accuracy_improvement": 30,
                    "speed_improvement": 40,
                    "workforce_reduction": 5,
                    "upskilling_required": 50,
                    "new_roles_created": 8,
                    "technical_risk": 0.25,
                    "adoption_risk": 0.40,
                    "integration_risk": 0.35
                }
            },
            
            "Skill Gap Bridging": {
                "name": "Skill Gap Bridging",
                "description": "Intensive reskilling focus with strategic hiring",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.11,  # 11% of revenue
                    "timeline": "18+ months",
                    "change_management": "Phased",
                    "automation_level": 45,
                    "accuracy_improvement": 35,
                    "speed_improvement": 45,
                    "workforce_reduction": 20,
                    "upskilling_required": 85,
                    "new_roles_created": 25,
                    "technical_risk": 0.30,
                    "adoption_risk": 0.35,
                    "integration_risk": 0.25
                }
            }
        }
        
        return scenarios
    
    def create_risk_governance_scenarios(self, baseline_data: dict) -> Dict[str, dict]:
        """Scenarios based on AI risk management and governance approaches"""
        
        scenarios = {
            "Conservative Governance": {
                "name": "Conservative Governance",
                "description": "Strong oversight with extensive human controls",
                "ai_initiative": {
                    "ai_type": "Augmentation",
                    "complexity": "Low",
                    "investment": baseline_data['revenue'] * 0.05,  # 5% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Gradual",
                    "automation_level": 30,
                    "accuracy_improvement": 35,
                    "speed_improvement": 25,
                    "workforce_reduction": 3,
                    "upskilling_required": 60,
                    "new_roles_created": 10,
                    "technical_risk": 0.15,
                    "adoption_risk": 0.20,
                    "integration_risk": 0.15,
                    "regulatory_risk": 0.10,
                    "data_risk": 0.15
                }
            },
            
            "Balanced Risk Management": {
                "name": "Balanced Risk Management",
                "description": "Moderate oversight with smart automation boundaries",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.07,  # 7% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Phased",
                    "automation_level": 50,
                    "accuracy_improvement": 40,
                    "speed_improvement": 50,
                    "workforce_reduction": 15,
                    "upskilling_required": 65,
                    "new_roles_created": 15,
                    "technical_risk": 0.25,
                    "adoption_risk": 0.30,
                    "integration_risk": 0.25,
                    "regulatory_risk": 0.20,
                    "data_risk": 0.25
                }
            },
            
            "Aggressive Innovation": {
                "name": "Aggressive Innovation",
                "description": "Rapid deployment with iterative risk management",
                "ai_initiative": {
                    "ai_type": "Automation",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.10,  # 10% of revenue
                    "timeline": "6-12 months",
                    "change_management": "Big Bang",
                    "automation_level": 70,
                    "accuracy_improvement": 50,
                    "speed_improvement": 75,
                    "workforce_reduction": 25,
                    "upskilling_required": 50,
                    "new_roles_created": 12,
                    "technical_risk": 0.40,
                    "adoption_risk": 0.35,
                    "integration_risk": 0.40,
                    "regulatory_risk": 0.35,
                    "data_risk": 0.40
                }
            }
        }
        
        return scenarios
    
    def create_competitive_advantage_scenarios(self, baseline_data: dict) -> Dict[str, dict]:
        """Scenarios for building sustainable AI competitive advantage"""
        
        scenarios = {
            "Data Moat Strategy": {
                "name": "Data Moat Strategy",
                "description": "Focus on proprietary data and learning loops",
                "ai_initiative": {
                    "ai_type": "Analytics",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.08,  # 8% of revenue
                    "timeline": "18+ months",
                    "change_management": "Gradual",
                    "automation_level": 45,
                    "accuracy_improvement": 60,
                    "speed_improvement": 40,
                    "workforce_reduction": 8,
                    "upskilling_required": 80,
                    "new_roles_created": 22,
                    "technical_risk": 0.30,
                    "adoption_risk": 0.25,
                    "integration_risk": 0.35
                }
            },
            
            "Platform Ecosystem": {
                "name": "Platform Ecosystem",
                "description": "Building systems that get smarter with usage",
                "ai_initiative": {
                    "ai_type": "Hybrid",
                    "complexity": "High",
                    "investment": baseline_data['revenue'] * 0.12,  # 12% of revenue
                    "timeline": "18+ months",
                    "change_management": "Phased",
                    "automation_level": 60,
                    "accuracy_improvement": 45,
                    "speed_improvement": 65,
                    "workforce_reduction": 18,
                    "upskilling_required": 75,
                    "new_roles_created": 25,
                    "technical_risk": 0.35,
                    "adoption_risk": 0.30,
                    "integration_risk": 0.40
                }
            },
            
            "Human-AI Fluency": {
                "name": "Human-AI Fluency",
                "description": "Building internal AI capability and cultural advantage",
                "ai_initiative": {
                    "ai_type": "Augmentation",
                    "complexity": "Medium",
                    "investment": baseline_data['revenue'] * 0.06,  # 6% of revenue
                    "timeline": "12-18 months",
                    "change_management": "Gradual",
                    "automation_level": 40,
                    "accuracy_improvement": 35,
                    "speed_improvement": 45,
                    "workforce_reduction": 5,
                    "upskilling_required": 90,
                    "new_roles_created": 20,
                    "technical_risk": 0.20,
                    "adoption_risk": 0.20,
                    "integration_risk": 0.20
                }
            }
        }
        
        return scenarios
    
    def run_comprehensive_scenario_analysis(self, baseline_data: dict, 
                                          scenario_categories: List[str] = None) -> dict:
        """Run comprehensive analysis across multiple scenario categories"""
        
        if scenario_categories is None:
            scenario_categories = [
                "business_value", "integration_depth", "talent_readiness", 
                "risk_governance", "competitive_advantage"
            ]
        
        all_scenarios = {}
        scenario_results = {}
        
        # Generate scenarios for each category
        for category in scenario_categories:
            if category == "business_value":
                scenarios = self.create_business_value_scenarios(baseline_data)
            elif category == "integration_depth":
                scenarios = self.create_integration_depth_scenarios(baseline_data)
            elif category == "talent_readiness":
                scenarios = self.create_talent_readiness_scenarios(baseline_data)
            elif category == "risk_governance":
                scenarios = self.create_risk_governance_scenarios(baseline_data)
            elif category == "competitive_advantage":
                scenarios = self.create_competitive_advantage_scenarios(baseline_data)
            
            all_scenarios[category] = scenarios
            
            # Run scenario comparison
            scenario_configs = list(scenarios.values())
            comparison_results = self.scenario_modeler.compare_multiple_scenarios(
                baseline_data, scenario_configs
            )
            scenario_results[category] = comparison_results
        
        return {
            "scenarios": all_scenarios,
            "analysis_results": scenario_results,
            "strategic_recommendations": self._generate_strategic_recommendations(scenario_results)
        }
    
    def _generate_strategic_recommendations(self, scenario_results: dict) -> dict:
        """Generate strategic recommendations based on scenario analysis"""
        
        recommendations = {
            "short_term": [],
            "medium_term": [],
            "long_term": [],
            "risk_mitigation": [],
            "investment_priorities": []
        }
        
        # Analyze results across categories
        for category, results in scenario_results.items():
            if 'comparative_analysis' in results:
                comparison = results['comparative_analysis']
                
                # Find best performing scenarios
                if 'summary_table' in comparison:
                    best_scenarios = sorted(
                        comparison['summary_table'].items(),
                        key=lambda x: x[1]['expected_roi'],
                        reverse=True
                    )
                    
                    if best_scenarios:
                        best_scenario = best_scenarios[0]
                        scenario_name = best_scenario[0]
                        metrics = best_scenario[1]
                        
                        if metrics['expected_roi'] > 25:
                            recommendations["investment_priorities"].append(
                                f"High priority: {scenario_name} in {category} (Expected ROI: {metrics['expected_roi']:.1f}%)"
                            )
                        elif metrics['expected_roi'] > 15:
                            recommendations["medium_term"].append(
                                f"Consider: {scenario_name} in {category} (Expected ROI: {metrics['expected_roi']:.1f}%)"
                            )
                
                # Risk analysis recommendations
                if 'risk_comparison' in comparison:
                    high_risk_scenarios = [
                        name for name, risk_data in comparison['risk_comparison'].items()
                        if risk_data['probability_positive_roi'] < 0.7
                    ]
                    
                    if high_risk_scenarios:
                        recommendations["risk_mitigation"].extend([
                            f"High risk scenario in {category}: {scenario}" 
                            for scenario in high_risk_scenarios
                        ])
        
        # Add strategic timing recommendations
        recommendations["short_term"].append("Focus on low-complexity, high-impact scenarios first")
        recommendations["medium_term"].append("Build capabilities for deeper AI integration")
        recommendations["long_term"].append("Develop proprietary AI advantages and data moats")
        
        return recommendations