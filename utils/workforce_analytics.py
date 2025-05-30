import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st
from dataclasses import dataclass
from utils.data_models import MetricsCalculator

@dataclass
class WorkforceProfile:
    """Comprehensive workforce profile for a department"""
    department: str
    current_headcount: int
    skill_levels: Dict[str, float]  # skill_name: proficiency (0-100)
    role_distribution: Dict[str, int]  # role_name: count
    tenure_distribution: Dict[str, int]  # tenure_range: count
    performance_scores: Dict[str, float]  # performance_category: average_score
    cost_per_employee: float
    productivity_index: float
    engagement_score: float
    retention_rate: float

@dataclass
class AIIntegrationArchitecture:
    """Human-AI integration architecture design"""
    department: str
    ai_automation_level: float  # 0-100%
    human_ai_collaboration_model: str  # "Augmentation", "Automation", "Hybrid"
    affected_roles: List[Dict[str, Any]]  # [{"role": str, "impact_type": str, "transformation_level": float}]
    new_roles_created: List[Dict[str, Any]]  # [{"role": str, "skills_required": List[str], "headcount": int}]
    skills_transformation: Dict[str, Dict[str, float]]  # role: {skill: importance_change}
    integration_timeline: Dict[str, str]  # phase: duration
    governance_structure: Dict[str, Any]

class PredictiveWorkforceAnalyzer:
    """Advanced predictive analytics for workforce transformation"""
    
    def __init__(self):
        self.skill_categories = {
            "Technical": ["Programming", "Data Analysis", "AI/ML Knowledge", "Systems Architecture", "Cybersecurity"],
            "Cognitive": ["Problem Solving", "Critical Thinking", "Creativity", "Decision Making", "Strategic Thinking"],
            "Social": ["Communication", "Leadership", "Collaboration", "Emotional Intelligence", "Negotiation"],
            "Digital": ["Digital Literacy", "Process Automation", "Digital Innovation", "Technology Adoption", "Digital Strategy"]
        }
        
    def analyze_workforce_transformation(self, baseline_profile: WorkforceProfile, 
                                       ai_initiative: Dict[str, Any], 
                                       timeline_months: int = 24) -> Dict[str, Any]:
        """Comprehensive workforce transformation analysis"""
        
        # Automation impact analysis
        automation_impact = self._calculate_automation_impact(baseline_profile, ai_initiative)
        
        # Skill evolution prediction
        skill_evolution = self._predict_skill_evolution(baseline_profile, ai_initiative, timeline_months)
        
        # Role transformation analysis
        role_transformation = self._analyze_role_transformation(baseline_profile, ai_initiative)
        
        # Productivity and performance predictions
        performance_predictions = self._predict_performance_changes(baseline_profile, ai_initiative)
        
        # Cost and efficiency analysis
        cost_efficiency = self._analyze_cost_efficiency(baseline_profile, ai_initiative, timeline_months)
        
        # Risk assessment
        transformation_risks = self._assess_transformation_risks(baseline_profile, ai_initiative)
        
        return {
            "automation_impact": automation_impact,
            "skill_evolution": skill_evolution,
            "role_transformation": role_transformation,
            "performance_predictions": performance_predictions,
            "cost_efficiency": cost_efficiency,
            "transformation_risks": transformation_risks,
            "timeline_analysis": self._create_timeline_analysis(baseline_profile, ai_initiative, timeline_months)
        }
    
    def _calculate_automation_impact(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed automation impact on workforce"""
        
        automation_level = ai_initiative.get('automation_level', 30) / 100
        complexity_factor = {"Low": 0.8, "Medium": 1.0, "High": 1.3}.get(ai_initiative.get('complexity', 'Medium'), 1.0)
        
        # Calculate role-specific automation impact
        role_impacts = {}
        for role, count in profile.role_distribution.items():
            # Different roles have different automation susceptibility
            susceptibility = self._get_role_automation_susceptibility(role)
            impact_level = automation_level * susceptibility * complexity_factor
            
            affected_positions = int(count * impact_level)
            transformation_type = self._determine_transformation_type(impact_level)
            
            role_impacts[role] = {
                "current_count": count,
                "affected_positions": affected_positions,
                "impact_percentage": impact_level * 100,
                "transformation_type": transformation_type,
                "timeline_months": self._estimate_transformation_timeline(transformation_type)
            }
        
        # Calculate overall impact metrics
        total_affected = sum(impact["affected_positions"] for impact in role_impacts.values())
        displacement_risk = total_affected / profile.current_headcount * 100
        
        return {
            "role_impacts": role_impacts,
            "total_affected_positions": total_affected,
            "displacement_risk_percentage": displacement_risk,
            "net_headcount_change": self._calculate_net_headcount_change(role_impacts, ai_initiative),
            "retraining_requirements": self._calculate_retraining_needs(role_impacts, profile)
        }
    
    def _predict_skill_evolution(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any], 
                               timeline_months: int) -> Dict[str, Any]:
        """Predict how skill requirements will evolve"""
        
        current_skills = profile.skill_levels.copy()
        ai_type = ai_initiative.get('ai_type', 'Automation')
        
        # Define skill importance changes based on AI type
        skill_transformations = self._get_skill_transformation_matrix(ai_type)
        
        # Project skill evolution over timeline
        skill_projections = {}
        for month in range(0, timeline_months + 1, 3):  # Quarterly projections
            monthly_skills = {}
            
            for skill, current_level in current_skills.items():
                transformation_rate = skill_transformations.get(skill, 0)
                # Apply S-curve adoption pattern
                progress_factor = 1 - np.exp(-month / 12)  # 12-month adoption curve
                
                new_importance = current_level + (transformation_rate * progress_factor)
                new_importance = max(0, min(100, new_importance))  # Bound between 0-100
                
                monthly_skills[skill] = new_importance
            
            skill_projections[f"Month_{month}"] = monthly_skills
        
        # Identify critical skill gaps
        skill_gaps = self._identify_skill_gaps(current_skills, skill_transformations)
        
        # Training recommendations
        training_recommendations = self._generate_training_recommendations(skill_gaps, timeline_months)
        
        return {
            "skill_projections": skill_projections,
            "critical_skill_gaps": skill_gaps,
            "training_recommendations": training_recommendations,
            "skill_investment_priority": self._prioritize_skill_investments(skill_gaps)
        }
    
    def _analyze_role_transformation(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how roles will transform with AI implementation"""
        
        role_transformations = {}
        new_roles = []
        
        for role, count in profile.role_distribution.items():
            transformation_analysis = self._analyze_individual_role_transformation(role, ai_initiative)
            role_transformations[role] = transformation_analysis
            
            # Identify potential new roles
            if transformation_analysis["creates_new_roles"]:
                new_roles.extend(transformation_analysis["new_roles"])
        
        # Analyze role evolution patterns
        evolution_patterns = self._identify_role_evolution_patterns(role_transformations)
        
        # Calculate organizational structure changes
        structure_changes = self._analyze_organizational_structure_changes(role_transformations, profile)
        
        return {
            "role_transformations": role_transformations,
            "new_roles": new_roles,
            "evolution_patterns": evolution_patterns,
            "organizational_structure_changes": structure_changes,
            "management_layer_impact": self._assess_management_impact(role_transformations)
        }
    
    def _predict_performance_changes(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any]) -> Dict[str, Any]:
        """Predict changes in workforce performance metrics"""
        
        baseline_productivity = profile.productivity_index
        baseline_engagement = profile.engagement_score
        
        # Calculate productivity improvements
        productivity_factors = self._calculate_productivity_factors(ai_initiative)
        projected_productivity = baseline_productivity * productivity_factors["multiplier"]
        
        # Calculate engagement impact
        engagement_factors = self._calculate_engagement_factors(ai_initiative, profile)
        projected_engagement = baseline_engagement + engagement_factors["change"]
        
        # Performance distribution analysis
        performance_distribution = self._analyze_performance_distribution_changes(profile, ai_initiative)
        
        # Quality metrics prediction
        quality_metrics = self._predict_quality_metrics(profile, ai_initiative)
        
        return {
            "productivity_improvement": {
                "baseline": baseline_productivity,
                "projected": projected_productivity,
                "improvement_percentage": ((projected_productivity - baseline_productivity) / baseline_productivity) * 100
            },
            "engagement_impact": {
                "baseline": baseline_engagement,
                "projected": max(0, min(100, projected_engagement)),
                "factors": engagement_factors
            },
            "performance_distribution": performance_distribution,
            "quality_metrics": quality_metrics,
            "innovation_capacity": self._assess_innovation_capacity_change(profile, ai_initiative)
        }
    
    def _analyze_cost_efficiency(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any], 
                               timeline_months: int) -> Dict[str, Any]:
        """Analyze cost and efficiency implications"""
        
        # Current cost baseline
        current_annual_cost = profile.current_headcount * profile.cost_per_employee
        
        # Implementation costs
        implementation_costs = self._calculate_implementation_costs(profile, ai_initiative, timeline_months)
        
        # Ongoing cost changes
        ongoing_cost_changes = self._calculate_ongoing_cost_changes(profile, ai_initiative)
        
        # Efficiency gains
        efficiency_gains = self._calculate_efficiency_gains(profile, ai_initiative, timeline_months)
        
        # ROI calculation
        roi_analysis = self._calculate_workforce_roi(implementation_costs, ongoing_cost_changes, 
                                                   efficiency_gains, timeline_months)
        
        return {
            "current_annual_cost": current_annual_cost,
            "implementation_costs": implementation_costs,
            "ongoing_cost_changes": ongoing_cost_changes,
            "efficiency_gains": efficiency_gains,
            "roi_analysis": roi_analysis,
            "payback_period_months": self._calculate_payback_period(implementation_costs, efficiency_gains)
        }
    
    def _assess_transformation_risks(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks associated with workforce transformation"""
        
        risks = {
            "change_resistance": self._assess_change_resistance_risk(profile, ai_initiative),
            "skill_gap": self._assess_skill_gap_risk(profile, ai_initiative),
            "retention": self._assess_retention_risk(profile, ai_initiative),
            "performance_disruption": self._assess_performance_disruption_risk(profile, ai_initiative),
            "cultural_alignment": self._assess_cultural_alignment_risk(profile, ai_initiative)
        }
        
        # Calculate overall risk score
        risk_weights = {"change_resistance": 0.25, "skill_gap": 0.25, "retention": 0.2, 
                       "performance_disruption": 0.15, "cultural_alignment": 0.15}
        
        overall_risk = sum(risks[risk_type]["score"] * weight for risk_type, weight in risk_weights.items())
        
        # Mitigation strategies
        mitigation_strategies = self._generate_risk_mitigation_strategies(risks)
        
        return {
            "individual_risks": risks,
            "overall_risk_score": overall_risk,
            "risk_level": self._categorize_risk_level(overall_risk),
            "mitigation_strategies": mitigation_strategies,
            "monitoring_metrics": self._define_risk_monitoring_metrics(risks)
        }
    
    def _create_timeline_analysis(self, profile: WorkforceProfile, ai_initiative: Dict[str, Any], 
                                timeline_months: int) -> Dict[str, Any]:
        """Create detailed timeline analysis for workforce transformation"""
        
        phases = self._define_transformation_phases(ai_initiative, timeline_months)
        
        timeline_analysis = {}
        for phase_name, phase_info in phases.items():
            timeline_analysis[phase_name] = {
                "duration_months": phase_info["duration"],
                "workforce_changes": self._calculate_phase_workforce_changes(profile, ai_initiative, phase_info),
                "skill_development": self._calculate_phase_skill_development(profile, phase_info),
                "cost_impact": self._calculate_phase_cost_impact(profile, ai_initiative, phase_info),
                "risk_factors": self._identify_phase_risks(phase_info),
                "success_metrics": self._define_phase_success_metrics(phase_info)
            }
        
        return timeline_analysis
    
    # Helper methods for detailed calculations
    def _get_role_automation_susceptibility(self, role: str) -> float:
        """Get automation susceptibility for different roles"""
        susceptibility_map = {
            "Data Entry Clerk": 0.9,
            "Administrative Assistant": 0.7,
            "Analyst": 0.6,
            "Manager": 0.3,
            "Creative Professional": 0.2,
            "Customer Service": 0.6,
            "Sales Representative": 0.4,
            "Engineer": 0.5,
            "Developer": 0.3,
            "Consultant": 0.2
        }
        
        # Find closest match or use default
        for role_key, susceptibility in susceptibility_map.items():
            if role_key.lower() in role.lower():
                return susceptibility
        
        return 0.5  # Default moderate susceptibility
    
    def _determine_transformation_type(self, impact_level: float) -> str:
        """Determine type of transformation based on impact level"""
        if impact_level < 0.2:
            return "Minimal Change"
        elif impact_level < 0.4:
            return "Role Enhancement"
        elif impact_level < 0.6:
            return "Significant Transformation"
        elif impact_level < 0.8:
            return "Role Redefinition"
        else:
            return "Potential Displacement"
    
    def _estimate_transformation_timeline(self, transformation_type: str) -> int:
        """Estimate timeline for different transformation types"""
        timeline_map = {
            "Minimal Change": 3,
            "Role Enhancement": 6,
            "Significant Transformation": 12,
            "Role Redefinition": 18,
            "Potential Displacement": 24
        }
        return timeline_map.get(transformation_type, 12)
    
    def _get_skill_transformation_matrix(self, ai_type: str) -> Dict[str, float]:
        """Get skill importance changes based on AI type"""
        
        base_transformations = {
            "Programming": 20,
            "Data Analysis": 25,
            "AI/ML Knowledge": 40,
            "Problem Solving": 15,
            "Critical Thinking": 20,
            "Creativity": 25,
            "Communication": 10,
            "Leadership": 15,
            "Digital Literacy": 30,
            "Process Automation": 35
        }
        
        # Adjust based on AI type
        if ai_type == "Generative AI":
            base_transformations["Creativity"] += 20
            base_transformations["Critical Thinking"] += 15
        elif ai_type == "Predictive Analytics":
            base_transformations["Data Analysis"] += 15
            base_transformations["Statistical Knowledge"] = 30
        elif ai_type == "Process Automation":
            base_transformations["Process Automation"] += 20
            base_transformations["Systems Thinking"] = 25
        
        return base_transformations
    
    def _identify_skill_gaps(self, current_skills: Dict[str, float], 
                           transformations: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify critical skill gaps"""
        gaps = []
        
        for skill, importance_change in transformations.items():
            current_level = current_skills.get(skill, 50)  # Default moderate level
            future_importance = current_level + importance_change
            
            if future_importance > 80 and current_level < 60:
                gap_severity = "Critical"
            elif future_importance > 70 and current_level < 50:
                gap_severity = "High"
            elif future_importance > 60 and current_level < 40:
                gap_severity = "Medium"
            else:
                gap_severity = "Low"
            
            if gap_severity in ["Critical", "High", "Medium"]:
                gaps.append({
                    "skill": skill,
                    "current_level": current_level,
                    "required_level": future_importance,
                    "gap_size": future_importance - current_level,
                    "severity": gap_severity,
                    "training_priority": self._calculate_training_priority(gap_severity, importance_change)
                })
        
        return sorted(gaps, key=lambda x: x["gap_size"], reverse=True)
    
    def _calculate_training_priority(self, severity: str, importance_change: float) -> int:
        """Calculate training priority score"""
        severity_scores = {"Critical": 100, "High": 75, "Medium": 50, "Low": 25}
        base_score = severity_scores.get(severity, 25)
        importance_factor = min(importance_change / 50, 1.0)  # Normalize to 0-1
        
        return int(base_score * (1 + importance_factor))

class HumanAIIntegrationArchitect:
    """Design human-AI integration architectures"""
    
    def __init__(self):
        self.integration_models = {
            "Augmentation": "AI enhances human capabilities",
            "Automation": "AI replaces human tasks",
            "Hybrid": "Dynamic collaboration between humans and AI",
            "Oversight": "Humans supervise AI operations",
            "Creative Partnership": "Humans and AI co-create solutions"
        }
    
    def design_integration_architecture(self, workforce_profile: WorkforceProfile, 
                                      ai_initiative: Dict[str, Any]) -> AIIntegrationArchitecture:
        """Design comprehensive human-AI integration architecture"""
        
        # Determine optimal integration model
        integration_model = self._select_optimal_integration_model(workforce_profile, ai_initiative)
        
        # Analyze role impacts
        affected_roles = self._analyze_role_impacts(workforce_profile, ai_initiative, integration_model)
        
        # Design new roles
        new_roles = self._design_new_roles(workforce_profile, ai_initiative, integration_model)
        
        # Plan skills transformation
        skills_transformation = self._plan_skills_transformation(workforce_profile, ai_initiative)
        
        # Create implementation timeline
        integration_timeline = self._create_integration_timeline(ai_initiative, integration_model)
        
        # Design governance structure
        governance_structure = self._design_governance_structure(workforce_profile, ai_initiative)
        
        return AIIntegrationArchitecture(
            department=workforce_profile.department,
            ai_automation_level=ai_initiative.get('automation_level', 30),
            human_ai_collaboration_model=integration_model,
            affected_roles=affected_roles,
            new_roles_created=new_roles,
            skills_transformation=skills_transformation,
            integration_timeline=integration_timeline,
            governance_structure=governance_structure
        )
    
    def _select_optimal_integration_model(self, profile: WorkforceProfile, 
                                        ai_initiative: Dict[str, Any]) -> str:
        """Select the most appropriate integration model"""
        
        complexity = ai_initiative.get('complexity', 'Medium')
        ai_type = ai_initiative.get('ai_type', 'Automation')
        automation_level = ai_initiative.get('automation_level', 30)
        
        # Decision matrix based on various factors
        if automation_level > 70:
            return "Automation"
        elif ai_type == "Generative AI":
            return "Creative Partnership"
        elif complexity == "High" and profile.skill_levels.get("Problem Solving", 50) > 70:
            return "Hybrid"
        elif automation_level < 30:
            return "Augmentation"
        else:
            return "Oversight"

class ExperienceOptimizer:
    """Optimize workforce experience during AI transformation"""
    
    def __init__(self):
        self.experience_dimensions = [
            "Job Satisfaction",
            "Learning Opportunities", 
            "Career Progression",
            "Work-Life Balance",
            "Autonomy",
            "Purpose Alignment",
            "Social Connection",
            "Recognition",
            "Growth Mindset",
            "Innovation Engagement"
        ]
    
    def optimize_transformation_experience(self, workforce_profile: WorkforceProfile,
                                         transformation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workforce experience during transformation"""
        
        # Analyze current experience baseline
        experience_baseline = self._assess_experience_baseline(workforce_profile)
        
        # Predict transformation impact on experience
        experience_impact = self._predict_experience_impact(workforce_profile, transformation_plan)
        
        # Design experience optimization strategies
        optimization_strategies = self._design_optimization_strategies(experience_baseline, experience_impact)
        
        # Create experience journey map
        journey_map = self._create_experience_journey_map(transformation_plan, optimization_strategies)
        
        # Define success metrics
        success_metrics = self._define_experience_success_metrics(experience_baseline)
        
        return {
            "experience_baseline": experience_baseline,
            "transformation_impact": experience_impact,
            "optimization_strategies": optimization_strategies,
            "experience_journey_map": journey_map,
            "success_metrics": success_metrics,
            "monitoring_framework": self._create_experience_monitoring_framework()
        }

class DynamicWorkforcePlanner:
    """Dynamic workforce planning and modeling"""
    
    def __init__(self):
        self.planning_horizons = ["Short-term (3-6 months)", "Medium-term (6-18 months)", "Long-term (18+ months)"]
        self.scenario_types = ["Conservative", "Moderate", "Aggressive", "Disruptive"]
    
    def create_dynamic_workforce_model(self, baseline_profile: WorkforceProfile,
                                     ai_initiatives: List[Dict[str, Any]],
                                     planning_horizon: str = "Medium-term") -> Dict[str, Any]:
        """Create dynamic workforce planning model"""
        
        # Multi-scenario workforce projections
        scenario_projections = self._create_scenario_projections(baseline_profile, ai_initiatives, planning_horizon)
        
        # Resource allocation optimization
        resource_optimization = self._optimize_resource_allocation(baseline_profile, ai_initiatives)
        
        # Capacity planning
        capacity_planning = self._create_capacity_planning_model(baseline_profile, ai_initiatives)
        
        # Succession planning
        succession_planning = self._create_succession_planning_framework(baseline_profile, ai_initiatives)
        
        # Contingency planning
        contingency_plans = self._create_contingency_plans(baseline_profile, ai_initiatives)
        
        return {
            "scenario_projections": scenario_projections,
            "resource_optimization": resource_optimization,
            "capacity_planning": capacity_planning,
            "succession_planning": succession_planning,
            "contingency_plans": contingency_plans,
            "adaptive_strategies": self._design_adaptive_strategies(baseline_profile, ai_initiatives)
        }