import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import streamlit as st

@dataclass
class LearningPersona:
    """AI learning persona definition"""
    persona_id: str
    name: str
    description: str
    department: str
    role_level: str  # Entry, Mid, Senior, Executive
    current_ai_proficiency: float  # 0-100
    learning_style: str  # Visual, Auditory, Kinesthetic, Reading
    time_availability: str  # Limited, Moderate, Flexible
    technical_background: str  # None, Basic, Intermediate, Advanced
    motivation_factors: List[str]
    preferred_learning_format: List[str]
    career_goals: List[str]
    skill_gaps: Dict[str, float]  # skill: gap_level (0-100)

@dataclass
class LearningModule:
    """Individual learning module"""
    module_id: str
    title: str
    description: str
    skill_category: str
    difficulty_level: str  # Beginner, Intermediate, Advanced
    duration_hours: float
    format_type: str  # Video, Interactive, Reading, Hands-on, Workshop
    prerequisites: List[str]
    learning_objectives: List[str]
    assessment_type: str
    completion_criteria: Dict[str, Any]

@dataclass
class DynamicCurriculum:
    """Dynamic curriculum for a persona"""
    curriculum_id: str
    persona_id: str
    title: str
    total_duration: float
    learning_path: List[str]  # module_ids in order
    milestones: Dict[str, Any]
    adaptive_rules: Dict[str, Any]
    progress_tracking: Dict[str, Any]
    completion_timeline: Dict[str, str]

class LearningPersonaAnalyzer:
    """Analyze and create AI learning personas across the enterprise"""
    
    def __init__(self):
        self.ai_skill_categories = {
            "Foundation": ["AI Literacy", "Digital Transformation", "Data Basics", "Ethics in AI"],
            "Technical": ["Machine Learning", "Data Science", "Programming", "AI Tools", "Analytics"],
            "Application": ["Process Automation", "Decision Support", "Customer Experience", "Operations"],
            "Leadership": ["AI Strategy", "Change Management", "Team Leadership", "Innovation"],
            "Specialized": ["Natural Language Processing", "Computer Vision", "Robotics", "Advanced Analytics"]
        }
        
        self.learning_formats = [
            "Self-paced Online",
            "Live Virtual Sessions", 
            "In-person Workshops",
            "Hands-on Labs",
            "Mentorship Programs",
            "Micro-learning",
            "Project-based Learning",
            "Peer Learning Groups"
        ]
    
    def analyze_enterprise_personas(self, departments_data: Dict[str, Any], workforce_analytics_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze personas across all departments using baseline data and workforce analytics"""
        
        enterprise_personas = []
        department_personas = {}
        
        for dept_name, dept_data in departments_data.items():
            # Get workforce analytics data for this department if available
            workforce_data = workforce_analytics_data.get(dept_name, {}) if workforce_analytics_data else {}
            
            # Create department-specific personas
            dept_personas = self._create_department_personas(dept_name, dept_data, workforce_data)
            department_personas[dept_name] = dept_personas
            enterprise_personas.extend(dept_personas)
        
        # Analyze persona patterns across enterprise
        persona_analysis = self._analyze_persona_patterns(enterprise_personas)
        
        # Create enterprise-level personas
        enterprise_level_personas = self._create_enterprise_level_personas(enterprise_personas)
        
        return {
            "enterprise_personas": enterprise_level_personas,
            "department_personas": department_personas,
            "persona_analysis": persona_analysis,
            "learning_pathways": self._design_learning_pathways(enterprise_personas),
            "skill_gap_analysis": self._analyze_skill_gaps(enterprise_personas)
        }
    
    def _create_department_personas(self, department: str, dept_data: Dict[str, Any], workforce_data: Dict[str, Any] = None) -> List[LearningPersona]:
        """Create personas specific to a department using baseline and workforce data"""
        
        personas = []
        headcount = dept_data.get('headcount', 50)
        
        # Get department-specific role distribution
        role_levels = self._get_department_role_levels(department, headcount)
        
        for role_level, count in role_levels.items():
            if count > 0:
                persona = self._create_persona_for_role(department, role_level, dept_data, workforce_data)
                personas.append(persona)
        
        return personas
    
    def _create_persona_for_role(self, department: str, role_level: str, dept_data: Dict[str, Any], workforce_data: Dict[str, Any] = None) -> LearningPersona:
        """Create a specific persona for a role level in a department using actual data"""
        
        persona_id = f"{department}_{role_level}".replace(" ", "_").lower()
        
        # Use actual AI proficiency from department data if available
        if 'ai_proficiency' in dept_data:
            base_proficiency = dept_data['ai_proficiency']
        else:
            # Fallback to role-based estimates
            role_base = {"Entry": 20, "Mid": 35, "Senior": 50, "Executive": 30}
            dept_adjustments = {
                "IT & Technology": 25, "Finance & Accounting": 10, "HR & Talent Management": 5,
                "Operations & Supply Chain": 15, "Sales & Marketing": 12, "Customer Service": 8
            }
            base_proficiency = role_base.get(role_level, 30) + dept_adjustments.get(department, 0)
        
        # Adjust by role level
        role_multipliers = {"Entry": 0.8, "Mid": 1.0, "Senior": 1.2, "Executive": 0.9}
        current_proficiency = min(100, max(0, base_proficiency * role_multipliers.get(role_level, 1.0)))
        
        # Generate skill gaps based on department and role
        skill_gaps = self._generate_skill_gaps(department, role_level)
        
        # Use actual learning preferences from department data if available
        if 'preferred_formats' in dept_data and dept_data['preferred_formats']:
            preferred_formats = dept_data['preferred_formats']
        else:
            preferred_formats = self._get_preferred_formats(role_level)
        
        if 'time_availability' in dept_data:
            time_availability = dept_data['time_availability']
        else:
            time_availability = {"Entry": "Moderate", "Mid": "Limited", "Senior": "Limited", "Executive": "Limited"}.get(role_level, "Moderate")
        
        # Determine learning style and motivation factors
        learning_style, motivation_factors = self._determine_learning_style_and_motivation(role_level)
        
        persona = LearningPersona(
            persona_id=persona_id,
            name=f"{department} {role_level} Professional",
            description=f"{role_level} level professional in {department} seeking AI upskilling",
            department=department,
            role_level=role_level,
            current_ai_proficiency=current_proficiency,
            learning_style=learning_style,
            time_availability=time_availability,
            technical_background=self._get_technical_background(department, role_level),
            motivation_factors=motivation_factors,
            preferred_learning_format=preferred_formats,
            career_goals=self._get_career_goals(department, role_level),
            skill_gaps=skill_gaps
        )
        
        return persona
    
    def _generate_skill_gaps(self, department: str, role_level: str) -> Dict[str, float]:
        """Generate skill gaps for a specific department and role"""
        
        # Base gaps by department
        dept_skill_priorities = {
            "IT & Technology": {
                "Machine Learning": 60, "Programming": 40, "Data Science": 70,
                "AI Tools": 50, "Process Automation": 45
            },
            "Finance & Accounting": {
                "Data Analytics": 65, "Process Automation": 70, "AI Ethics": 45,
                "Decision Support": 60, "Risk Management AI": 55
            },
            "HR & Talent Management": {
                "People Analytics": 70, "AI Ethics": 60, "Recruitment AI": 65,
                "Performance AI": 55, "Learning AI": 50
            },
            "Operations & Supply Chain": {
                "Predictive Analytics": 65, "Process Optimization": 70, "IoT Integration": 60,
                "Supply Chain AI": 75, "Quality AI": 50
            },
            "Sales & Marketing": {
                "Customer Analytics": 70, "Marketing AI": 65, "CRM AI": 60,
                "Content AI": 55, "Sales Forecasting": 65
            },
            "Customer Service": {
                "Chatbot Development": 75, "Sentiment Analysis": 60, "Service AI": 70,
                "Knowledge Management": 55, "Customer Insights": 65
            }
        }
        
        base_gaps = dept_skill_priorities.get(department, {
            "AI Literacy": 50, "Data Basics": 45, "Process Automation": 40
        })
        
        # Adjust by role level
        role_multipliers = {
            "Entry": 1.2,
            "Mid": 1.0,
            "Senior": 0.8,
            "Executive": 0.6
        }
        
        multiplier = role_multipliers.get(role_level, 1.0)
        
        adjusted_gaps = {}
        for skill, gap in base_gaps.items():
            adjusted_gaps[skill] = min(100, gap * multiplier)
        
        return adjusted_gaps
    
    def _determine_learning_preferences(self, role_level: str) -> Tuple[str, str, List[str]]:
        """Determine learning preferences based on role level"""
        
        preferences = {
            "Entry": {
                "style": "Visual",
                "time": "Moderate",
                "motivation": ["Career Growth", "Skill Development", "Job Security"]
            },
            "Mid": {
                "style": "Kinesthetic", 
                "time": "Limited",
                "motivation": ["Professional Development", "Efficiency", "Leadership Growth"]
            },
            "Senior": {
                "style": "Reading",
                "time": "Limited", 
                "motivation": ["Strategic Advantage", "Team Development", "Innovation"]
            },
            "Executive": {
                "style": "Auditory",
                "time": "Limited",
                "motivation": ["Business Transformation", "Competitive Edge", "Strategic Vision"]
            }
        }
        
        pref = preferences.get(role_level, preferences["Mid"])
        return pref["style"], pref["time"], pref["motivation"]
    
    def _get_technical_background(self, department: str, role_level: str) -> str:
        """Get technical background level"""
        
        tech_depts = ["IT & Technology"]
        
        if department in tech_depts:
            return {"Entry": "Basic", "Mid": "Intermediate", "Senior": "Advanced", "Executive": "Intermediate"}.get(role_level, "Basic")
        else:
            return {"Entry": "None", "Mid": "Basic", "Senior": "Basic", "Executive": "None"}.get(role_level, "None")
    
    def _get_preferred_formats(self, role_level: str) -> List[str]:
        """Get preferred learning formats by role level"""
        
        format_preferences = {
            "Entry": ["Self-paced Online", "Hands-on Labs", "Peer Learning Groups"],
            "Mid": ["Live Virtual Sessions", "Project-based Learning", "Micro-learning"],
            "Senior": ["In-person Workshops", "Mentorship Programs", "Case Studies"],
            "Executive": ["Executive Briefings", "Strategic Workshops", "Peer Networks"]
        }
        
        return format_preferences.get(role_level, ["Self-paced Online", "Live Virtual Sessions"])
    
    def _get_career_goals(self, department: str, role_level: str) -> List[str]:
        """Get career goals for persona"""
        
        base_goals = {
            "Entry": ["Build foundational AI skills", "Understand AI applications", "Prepare for advancement"],
            "Mid": ["Lead AI projects", "Become department AI champion", "Develop specialized expertise"],
            "Senior": ["Drive AI strategy", "Mentor teams in AI adoption", "Innovate with AI solutions"],
            "Executive": ["Transform business with AI", "Set AI vision", "Lead digital transformation"]
        }
        
        return base_goals.get(role_level, ["Develop AI capabilities"])
    
    def _get_department_role_levels(self, department: str, headcount: int) -> Dict[str, int]:
        """Get role level distribution for department"""
        
        # Standard distribution across role levels
        distribution = {
            "Entry": 0.35,
            "Mid": 0.40, 
            "Senior": 0.20,
            "Executive": 0.05
        }
        
        role_counts = {}
        for level, percentage in distribution.items():
            role_counts[level] = max(1, int(headcount * percentage))
        
        return role_counts
    
    def _analyze_persona_patterns(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Analyze patterns across all personas"""
        
        if not personas:
            return {}
        
        # Proficiency distribution
        proficiency_levels = [p.current_ai_proficiency for p in personas]
        avg_proficiency = np.mean(proficiency_levels)
        
        # Learning style distribution
        learning_styles = {}
        for persona in personas:
            style = persona.learning_style
            learning_styles[style] = learning_styles.get(style, 0) + 1
        
        # Time availability patterns
        time_patterns = {}
        for persona in personas:
            time = persona.time_availability
            time_patterns[time] = time_patterns.get(time, 0) + 1
        
        # Common skill gaps
        all_gaps = {}
        for persona in personas:
            for skill, gap in persona.skill_gaps.items():
                if skill not in all_gaps:
                    all_gaps[skill] = []
                all_gaps[skill].append(gap)
        
        common_gaps = {skill: np.mean(gaps) for skill, gaps in all_gaps.items()}
        top_gaps = sorted(common_gaps.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_personas": len(personas),
            "average_proficiency": avg_proficiency,
            "proficiency_distribution": {
                "Beginner (0-30)": len([p for p in proficiency_levels if p <= 30]),
                "Intermediate (31-60)": len([p for p in proficiency_levels if 31 <= p <= 60]),
                "Advanced (61-100)": len([p for p in proficiency_levels if p > 60])
            },
            "learning_style_distribution": learning_styles,
            "time_availability_patterns": time_patterns,
            "top_skill_gaps": top_gaps
        }
    
    def _create_enterprise_level_personas(self, personas: List[LearningPersona]) -> List[LearningPersona]:
        """Create enterprise-level personas based on common patterns"""
        
        if not personas:
            return []
        
        enterprise_personas = []
        
        # Group personas by similar characteristics
        persona_groups = self._group_personas_by_characteristics(personas)
        
        for group_name, group_personas in persona_groups.items():
            enterprise_persona = self._create_enterprise_persona(group_name, group_personas)
            enterprise_personas.append(enterprise_persona)
        
        return enterprise_personas
    
    def _group_personas_by_characteristics(self, personas: List[LearningPersona]) -> Dict[str, List[LearningPersona]]:
        """Group personas by similar learning characteristics"""
        
        groups = {
            "Tech-Savvy Innovators": [],
            "Business-Focused Adopters": [],
            "Cautious Learners": [],
            "Strategic Leaders": []
        }
        
        for persona in personas:
            if persona.role_level == "Executive":
                groups["Strategic Leaders"].append(persona)
            elif persona.technical_background in ["Intermediate", "Advanced"]:
                groups["Tech-Savvy Innovators"].append(persona)
            elif persona.current_ai_proficiency < 30:
                groups["Cautious Learners"].append(persona)
            else:
                groups["Business-Focused Adopters"].append(persona)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _create_enterprise_persona(self, group_name: str, group_personas: List[LearningPersona]) -> LearningPersona:
        """Create an enterprise-level persona from a group"""
        
        if not group_personas:
            return None
        
        # Calculate averages and common characteristics
        avg_proficiency = np.mean([p.current_ai_proficiency for p in group_personas])
        
        # Most common characteristics
        learning_styles = [p.learning_style for p in group_personas]
        most_common_style = max(set(learning_styles), key=learning_styles.count)
        
        time_availability = [p.time_availability for p in group_personas]
        most_common_time = max(set(time_availability), key=time_availability.count)
        
        # Aggregate skill gaps
        all_gaps = {}
        for persona in group_personas:
            for skill, gap in persona.skill_gaps.items():
                if skill not in all_gaps:
                    all_gaps[skill] = []
                all_gaps[skill].append(gap)
        
        avg_gaps = {skill: np.mean(gaps) for skill, gaps in all_gaps.items()}
        
        # Common motivation factors
        all_motivations = []
        for persona in group_personas:
            all_motivations.extend(persona.motivation_factors)
        
        top_motivations = list(set(all_motivations))[:3]
        
        enterprise_persona = LearningPersona(
            persona_id=f"enterprise_{group_name.lower().replace(' ', '_').replace('-', '_')}",
            name=group_name,
            description=f"Enterprise-level persona representing {group_name} across departments",
            department="Enterprise",
            role_level="Mixed",
            current_ai_proficiency=avg_proficiency,
            learning_style=most_common_style,
            time_availability=most_common_time,
            technical_background="Mixed",
            motivation_factors=top_motivations,
            preferred_learning_format=self._aggregate_preferred_formats(group_personas),
            career_goals=self._aggregate_career_goals(group_personas),
            skill_gaps=avg_gaps
        )
        
        return enterprise_persona
    
    def _aggregate_preferred_formats(self, personas: List[LearningPersona]) -> List[str]:
        """Aggregate preferred learning formats"""
        all_formats = []
        for persona in personas:
            all_formats.extend(persona.preferred_learning_format)
        
        # Get top 3 most common formats
        format_counts = {}
        for fmt in all_formats:
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
        
        sorted_formats = sorted(format_counts.items(), key=lambda x: x[1], reverse=True)
        return [fmt for fmt, _ in sorted_formats[:3]]
    
    def _aggregate_career_goals(self, personas: List[LearningPersona]) -> List[str]:
        """Aggregate career goals"""
        all_goals = []
        for persona in personas:
            all_goals.extend(persona.career_goals)
        
        # Get top 3 most common goals
        goal_counts = {}
        for goal in all_goals:
            goal_counts[goal] = goal_counts.get(goal, 0) + 1
        
        sorted_goals = sorted(goal_counts.items(), key=lambda x: x[1], reverse=True)
        return [goal for goal, _ in sorted_goals[:3]]
    
    def _design_learning_pathways(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Design learning pathways for different persona types"""
        
        pathways = {}
        
        # Group personas by proficiency level
        beginner_personas = [p for p in personas if p.current_ai_proficiency <= 30]
        intermediate_personas = [p for p in personas if 30 < p.current_ai_proficiency <= 60]
        advanced_personas = [p for p in personas if p.current_ai_proficiency > 60]
        
        if beginner_personas:
            pathways["Foundation Track"] = self._create_foundation_pathway(beginner_personas)
        
        if intermediate_personas:
            pathways["Application Track"] = self._create_application_pathway(intermediate_personas)
        
        if advanced_personas:
            pathways["Innovation Track"] = self._create_innovation_pathway(advanced_personas)
        
        return pathways
    
    def _create_foundation_pathway(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Create foundation learning pathway"""
        return {
            "name": "AI Foundation Track",
            "description": "Building fundamental AI literacy and understanding",
            "duration_weeks": 12,
            "modules": [
                "AI Fundamentals",
                "Digital Transformation Basics", 
                "Data Literacy",
                "AI Ethics and Responsibility",
                "AI in Your Industry",
                "Hands-on AI Tools"
            ],
            "learning_formats": ["Self-paced Online", "Virtual Workshops", "Peer Groups"],
            "assessment": "Portfolio of practical applications",
            "target_personas": len(personas)
        }
    
    def _create_application_pathway(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Create application learning pathway"""
        return {
            "name": "AI Application Track", 
            "description": "Applying AI solutions to business challenges",
            "duration_weeks": 16,
            "modules": [
                "Advanced AI Concepts",
                "Process Automation with AI",
                "Data Analytics and Insights",
                "AI Project Management", 
                "Industry-Specific Applications",
                "Implementation Strategies"
            ],
            "learning_formats": ["Project-based Learning", "Case Studies", "Mentorship"],
            "assessment": "Real-world project implementation",
            "target_personas": len(personas)
        }
    
    def _create_innovation_pathway(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Create innovation learning pathway"""
        return {
            "name": "AI Innovation Track",
            "description": "Leading AI innovation and strategic transformation", 
            "duration_weeks": 20,
            "modules": [
                "AI Strategy and Vision",
                "Advanced AI Technologies",
                "Innovation Management",
                "Change Leadership",
                "AI Governance and Ethics",
                "Future of AI"
            ],
            "learning_formats": ["Executive Programs", "Innovation Labs", "Peer Networks"],
            "assessment": "Strategic AI transformation plan",
            "target_personas": len(personas)
        }
    
    def _analyze_skill_gaps(self, personas: List[LearningPersona]) -> Dict[str, Any]:
        """Analyze skill gaps across all personas"""
        
        if not personas:
            return {}
        
        # Aggregate all skill gaps
        skill_gap_data = {}
        for persona in personas:
            for skill, gap in persona.skill_gaps.items():
                if skill not in skill_gap_data:
                    skill_gap_data[skill] = []
                skill_gap_data[skill].append(gap)
        
        # Calculate statistics
        gap_analysis = {}
        for skill, gaps in skill_gap_data.items():
            gap_analysis[skill] = {
                "average_gap": np.mean(gaps),
                "max_gap": np.max(gaps),
                "personas_affected": len(gaps),
                "priority_level": self._calculate_priority_level(np.mean(gaps), len(gaps))
            }
        
        # Sort by priority
        prioritized_gaps = sorted(gap_analysis.items(), 
                                key=lambda x: (x[1]["priority_level"], x[1]["average_gap"]), 
                                reverse=True)
        
        return {
            "total_skills_analyzed": len(gap_analysis),
            "skill_gap_analysis": gap_analysis,
            "prioritized_skill_gaps": prioritized_gaps[:10],
            "enterprise_skill_priorities": self._identify_enterprise_priorities(prioritized_gaps)
        }
    
    def _calculate_priority_level(self, avg_gap: float, personas_affected: int) -> float:
        """Calculate priority level for skill gaps"""
        # Higher gap and more personas affected = higher priority
        return (avg_gap * 0.7) + (personas_affected * 2)
    
    def _identify_enterprise_priorities(self, prioritized_gaps: List[Tuple[str, Dict]]) -> List[str]:
        """Identify top enterprise skill priorities"""
        top_priorities = []
        
        for skill, data in prioritized_gaps[:5]:
            if data["average_gap"] > 50 and data["personas_affected"] > 2:
                top_priorities.append(skill)
        
        return top_priorities

class DynamicCurriculumBuilder:
    """Build dynamic, personalized curricula for learning personas"""
    
    def __init__(self):
        self.module_library = self._create_module_library()
    
    def build_curriculum_for_persona(self, persona: LearningPersona) -> DynamicCurriculum:
        """Build a dynamic curriculum for a specific persona"""
        
        # Select appropriate modules based on persona characteristics
        selected_modules = self._select_modules_for_persona(persona)
        
        # Sequence modules based on dependencies and learning path
        learning_path = self._sequence_modules(selected_modules, persona)
        
        # Create adaptive rules
        adaptive_rules = self._create_adaptive_rules(persona)
        
        # Define milestones
        milestones = self._define_milestones(learning_path, persona)
        
        # Calculate total duration
        total_duration = sum(self.module_library[mod_id].duration_hours for mod_id in learning_path)
        
        curriculum = DynamicCurriculum(
            curriculum_id=f"curriculum_{persona.persona_id}",
            persona_id=persona.persona_id,
            title=f"AI Learning Path for {persona.name}",
            total_duration=total_duration,
            learning_path=learning_path,
            milestones=milestones,
            adaptive_rules=adaptive_rules,
            progress_tracking=self._create_progress_tracking(learning_path),
            completion_timeline=self._estimate_completion_timeline(learning_path, persona)
        )
        
        return curriculum
    
    def _create_module_library(self) -> Dict[str, LearningModule]:
        """Create a comprehensive library of learning modules"""
        
        modules = {}
        
        # Foundation modules
        foundation_modules = [
            ("ai_fundamentals", "AI Fundamentals", "Introduction to artificial intelligence concepts", 
             "Foundation", "Beginner", 8, "Video", [], 
             ["Understand what AI is", "Identify AI applications", "Recognize AI limitations"]),
            ("digital_transformation", "Digital Transformation", "Understanding digital change in business",
             "Foundation", "Beginner", 6, "Interactive", [],
             ["Grasp digital transformation", "Identify opportunities", "Understand challenges"]),
            ("data_literacy", "Data Literacy", "Working with data effectively",
             "Foundation", "Beginner", 10, "Hands-on", [],
             ["Read data visualizations", "Understand data quality", "Make data-driven decisions"]),
            ("ai_ethics", "AI Ethics", "Responsible AI development and deployment",
             "Foundation", "Beginner", 4, "Reading", [],
             ["Understand AI bias", "Apply ethical frameworks", "Ensure responsible AI use"])
        ]
        
        # Technical modules
        technical_modules = [
            ("machine_learning", "Machine Learning Basics", "Introduction to ML algorithms",
             "Technical", "Intermediate", 16, "Hands-on", ["ai_fundamentals"],
             ["Understand ML concepts", "Apply basic algorithms", "Evaluate model performance"]),
            ("data_science", "Data Science Fundamentals", "Data analysis and modeling",
             "Technical", "Intermediate", 20, "Hands-on", ["data_literacy"],
             ["Perform data analysis", "Build predictive models", "Interpret results"]),
            ("ai_tools", "AI Tools and Platforms", "Working with AI development tools",
             "Technical", "Intermediate", 12, "Hands-on", ["machine_learning"],
             ["Use AI platforms", "Build AI applications", "Deploy AI solutions"])
        ]
        
        # Application modules
        application_modules = [
            ("process_automation", "Process Automation", "Automating business processes with AI",
             "Application", "Intermediate", 14, "Project-based", ["ai_fundamentals"],
             ["Identify automation opportunities", "Design automated workflows", "Implement solutions"]),
            ("customer_analytics", "Customer Analytics", "AI for customer insights",
             "Application", "Intermediate", 12, "Case-study", ["data_literacy"],
             ["Analyze customer data", "Predict customer behavior", "Personalize experiences"]),
            ("decision_support", "AI Decision Support", "AI-powered decision making",
             "Application", "Intermediate", 10, "Workshop", ["ai_fundamentals"],
             ["Build decision frameworks", "Use AI for insights", "Implement decision systems"])
        ]
        
        # Leadership modules
        leadership_modules = [
            ("ai_strategy", "AI Strategy", "Developing organizational AI strategy", 
             "Leadership", "Advanced", 16, "Workshop", ["ai_fundamentals"],
             ["Create AI vision", "Develop strategy", "Lead transformation"]),
            ("change_management", "Change Management for AI", "Leading AI adoption",
             "Leadership", "Advanced", 12, "Workshop", [],
             ["Manage AI change", "Build buy-in", "Overcome resistance"]),
            ("innovation_leadership", "Innovation Leadership", "Leading AI innovation",
             "Leadership", "Advanced", 14, "Mentorship", ["ai_strategy"],
             ["Foster innovation", "Build innovation culture", "Lead innovation teams"])
        ]
        
        all_modules = foundation_modules + technical_modules + application_modules + leadership_modules
        
        for module_data in all_modules:
            module = LearningModule(
                module_id=module_data[0],
                title=module_data[1],
                description=module_data[2],
                skill_category=module_data[3],
                difficulty_level=module_data[4],
                duration_hours=module_data[5],
                format_type=module_data[6],
                prerequisites=module_data[7],
                learning_objectives=module_data[8],
                assessment_type="Quiz and Practical",
                completion_criteria={"min_score": 80, "practical_completion": True}
            )
            modules[module.module_id] = module
        
        return modules
    
    def _select_modules_for_persona(self, persona: LearningPersona) -> List[str]:
        """Select appropriate modules for a persona"""
        
        selected_modules = []
        
        # Always include foundation modules for lower proficiency
        if persona.current_ai_proficiency < 40:
            selected_modules.extend(["ai_fundamentals", "digital_transformation", "data_literacy", "ai_ethics"])
        
        # Add modules based on skill gaps
        for skill, gap in persona.skill_gaps.items():
            if gap > 50:  # Significant gap
                module_id = self._map_skill_to_module(skill)
                if module_id and module_id not in selected_modules:
                    selected_modules.append(module_id)
        
        # Add role-specific modules
        role_modules = self._get_role_specific_modules(persona.role_level)
        for module_id in role_modules:
            if module_id not in selected_modules:
                selected_modules.append(module_id)
        
        # Add department-specific modules
        dept_modules = self._get_department_specific_modules(persona.department)
        for module_id in dept_modules:
            if module_id not in selected_modules:
                selected_modules.append(module_id)
        
        return selected_modules
    
    def _map_skill_to_module(self, skill: str) -> Optional[str]:
        """Map skill gaps to appropriate modules"""
        
        skill_module_mapping = {
            "Machine Learning": "machine_learning",
            "Data Science": "data_science", 
            "AI Tools": "ai_tools",
            "Process Automation": "process_automation",
            "Customer Analytics": "customer_analytics",
            "Decision Support": "decision_support",
            "AI Strategy": "ai_strategy",
            "Change Management": "change_management",
            "Data Analytics": "data_science",
            "AI Ethics": "ai_ethics"
        }
        
        return skill_module_mapping.get(skill)
    
    def _get_role_specific_modules(self, role_level: str) -> List[str]:
        """Get modules specific to role level"""
        
        role_modules = {
            "Entry": ["ai_fundamentals", "data_literacy"],
            "Mid": ["process_automation", "customer_analytics"],
            "Senior": ["decision_support", "change_management"],
            "Executive": ["ai_strategy", "innovation_leadership"]
        }
        
        return role_modules.get(role_level, [])
    
    def _get_department_specific_modules(self, department: str) -> List[str]:
        """Get modules specific to department"""
        
        dept_modules = {
            "IT & Technology": ["machine_learning", "ai_tools", "data_science"],
            "Finance & Accounting": ["data_science", "decision_support", "process_automation"],
            "HR & Talent Management": ["customer_analytics", "ai_ethics", "change_management"],
            "Operations & Supply Chain": ["process_automation", "decision_support", "data_science"],
            "Sales & Marketing": ["customer_analytics", "data_science", "ai_tools"],
            "Customer Service": ["customer_analytics", "process_automation", "ai_tools"]
        }
        
        return dept_modules.get(department, [])
    
    def _sequence_modules(self, module_ids: List[str], persona: LearningPersona) -> List[str]:
        """Sequence modules based on prerequisites and learning path"""
        
        sequenced = []
        remaining = module_ids.copy()
        
        while remaining:
            # Find modules with no unfulfilled prerequisites
            available = []
            for mod_id in remaining:
                module = self.module_library[mod_id]
                if all(prereq in sequenced for prereq in module.prerequisites):
                    available.append(mod_id)
            
            if not available:
                # If no modules are available, add the first one (break circular dependencies)
                available = [remaining[0]]
            
            # Sort available modules by difficulty and persona preferences
            available.sort(key=lambda x: self._get_module_priority(x, persona))
            
            # Add the highest priority module
            next_module = available[0]
            sequenced.append(next_module)
            remaining.remove(next_module)
        
        return sequenced
    
    def _get_module_priority(self, module_id: str, persona: LearningPersona) -> int:
        """Get priority score for module based on persona"""
        
        module = self.module_library[module_id]
        priority = 0
        
        # Prefer modules that match persona's preferred format
        if module.format_type in persona.preferred_learning_format:
            priority += 10
        
        # Prefer modules that address bigger skill gaps
        for skill, gap in persona.skill_gaps.items():
            if skill.lower() in module.title.lower():
                priority += int(gap / 10)
        
        # Prefer foundation modules for beginners
        if persona.current_ai_proficiency < 40 and module.skill_category == "Foundation":
            priority += 20
        
        return priority
    
    def _create_adaptive_rules(self, persona: LearningPersona) -> Dict[str, Any]:
        """Create adaptive rules for curriculum"""
        
        return {
            "pace_adjustment": {
                "slow_learner": "Extend deadlines by 25% if assessment scores < 70%",
                "fast_learner": "Provide advanced materials if completing ahead of schedule"
            },
            "format_adaptation": {
                "preferred_format": persona.preferred_learning_format[0] if persona.preferred_learning_format else "Self-paced Online",
                "alternative_formats": persona.preferred_learning_format[1:] if len(persona.preferred_learning_format) > 1 else []
            },
            "difficulty_scaling": {
                "increase_difficulty": "Add advanced modules if consistently scoring > 90%",
                "decrease_difficulty": "Provide additional support if struggling"
            },
            "engagement_rules": {
                "motivation_factors": persona.motivation_factors,
                "engagement_triggers": "Peer collaboration for social learners, individual challenges for independent learners"
            }
        }
    
    def _define_milestones(self, learning_path: List[str], persona: LearningPersona) -> Dict[str, Any]:
        """Define learning milestones"""
        
        milestones = {}
        total_modules = len(learning_path)
        
        milestone_points = [0.25, 0.5, 0.75, 1.0]
        milestone_names = ["Foundation Complete", "Midpoint Achievement", "Advanced Skills", "Mastery Achieved"]
        
        for i, (point, name) in enumerate(zip(milestone_points, milestone_names)):
            module_index = int(total_modules * point) - 1
            if module_index >= 0 and module_index < total_modules:
                milestones[name] = {
                    "module_index": module_index,
                    "module_id": learning_path[module_index],
                    "completion_percentage": point * 100,
                    "reward": "Certificate" if point == 1.0 else "Badge",
                    "assessment_required": True
                }
        
        return milestones
    
    def _create_progress_tracking(self, learning_path: List[str]) -> Dict[str, Any]:
        """Create progress tracking structure"""
        
        return {
            "total_modules": len(learning_path),
            "completed_modules": 0,
            "current_module": learning_path[0] if learning_path else None,
            "module_progress": {mod_id: {"status": "not_started", "score": None, "completion_date": None} 
                             for mod_id in learning_path},
            "overall_progress_percentage": 0,
            "estimated_completion_date": None,
            "time_spent": 0
        }
    
    def _estimate_completion_timeline(self, learning_path: List[str], persona: LearningPersona) -> Dict[str, str]:
        """Estimate completion timeline based on persona characteristics"""
        
        total_hours = sum(self.module_library[mod_id].duration_hours for mod_id in learning_path)
        
        # Adjust based on time availability
        weekly_hours = {
            "Limited": 2,
            "Moderate": 4, 
            "Flexible": 8
        }
        
        hours_per_week = weekly_hours.get(persona.time_availability, 4)
        total_weeks = max(1, int(total_hours / hours_per_week))
        
        # Create timeline
        timeline = {}
        current_week = 0
        
        for i, module_id in enumerate(learning_path):
            module = self.module_library[module_id]
            module_weeks = max(1, int(module.duration_hours / hours_per_week))
            
            start_week = current_week
            end_week = current_week + module_weeks
            
            timeline[module_id] = f"Week {start_week + 1}-{end_week}"
            current_week = end_week
        
        return timeline