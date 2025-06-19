import streamlit as st
import openai
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class NaturalLanguageProcessor:
    """Natural language processing for AI initiative configuration"""
    
    def __init__(self):
        # Use environment variable for OpenAI API key
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = openai.OpenAI(api_key=api_key)
        else:
            self.openai_client = None
        
        # Industry-specific AI types mapping
        self.industry_ai_types = {
            'Technology': ['Machine Learning', 'Natural Language Processing', 'Computer Vision', 'Automation', 'Generative AI'],
            'Healthcare': ['Medical AI', 'Diagnostic Automation', 'Patient Care AI', 'Clinical Decision Support', 'Medical Imaging AI'],
            'Financial Services': ['Fraud Detection', 'Risk Assessment AI', 'Trading Algorithms', 'Customer Service AI', 'Compliance Automation'],
            'Retail': ['Recommendation Systems', 'Inventory Optimization', 'Customer Analytics', 'Price Optimization', 'Supply Chain AI'],
            'Manufacturing': ['Predictive Maintenance', 'Quality Control AI', 'Production Optimization', 'Safety Monitoring', 'Supply Chain AI'],
            'Life Sciences': ['Drug Discovery AI', 'Clinical Trial Optimization', 'Research Analytics', 'Regulatory Compliance AI', 'Lab Automation'],
            'Energy & Utilities': ['Grid Optimization', 'Predictive Maintenance', 'Demand Forecasting', 'Safety Monitoring', 'Asset Management AI'],
            'Education': ['Adaptive Learning', 'Student Analytics', 'Content Generation', 'Assessment Automation', 'Learning Path Optimization'],
            'Government': ['Citizen Services AI', 'Compliance Monitoring', 'Data Analytics', 'Security Systems', 'Process Automation']
        }
    
    def parse_initiative_description(self, description: str, industry: str, function_name: str) -> Dict[str, Any]:
        """Parse natural language description into structured AI initiative configuration"""
        
        if not self.openai_client:
            st.warning("OpenAI API key not configured. Using rule-based parsing.")
            return self._rule_based_parsing(description, industry, function_name)
        
        industry_types = self.industry_ai_types.get(industry, self.industry_ai_types['Technology'])
        
        prompt = f"""
        Parse the following AI initiative description into a structured configuration for a {industry} company's {function_name} function.

        Description: "{description}"

        Available AI types for {industry}: {', '.join(industry_types)}

        Return a JSON object with these exact fields:
        {{
            "name": "Brief descriptive name for the initiative",
            "ai_type": "One of the available AI types that best matches",
            "investment": "Estimated investment amount in USD (number only)",
            "automation_level": "Percentage of process automation (0-100)",
            "productivity_gain": "Expected productivity improvement percentage (0-100)",
            "workforce_reduction": "Expected workforce reduction percentage (0-50)",
            "timeline": "Implementation timeline (3-6 months, 6-12 months, 12+ months)",
            "complexity": "Implementation complexity (Low, Medium, High)",
            "description": "Detailed description of the initiative",
            "key_benefits": "List of 3-5 key expected benefits",
            "implementation_steps": "List of 3-5 high-level implementation steps"
        }}

        Base estimates on industry standards for {industry} and realistic {function_name} implementations.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an AI strategy expert specializing in enterprise AI implementations. Provide realistic, industry-appropriate estimates."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content or "{}")
            
            # Validate and clean the result
            cleaned_result = self._validate_and_clean_config(result, industry_types)
            
            return cleaned_result
            
        except Exception as e:
            st.warning(f"AI parsing failed, using rule-based approach: {str(e)}")
            return self._rule_based_parsing(description, industry, function_name)
    
    def suggest_initiative_improvements(self, initiative_config: Dict[str, Any], industry: str, function_name: str) -> List[str]:
        """Suggest improvements to an existing AI initiative configuration"""
        
        if not self.openai_client:
            return self._rule_based_improvements(initiative_config, industry, function_name)
        
        prompt = f"""
        Analyze this AI initiative configuration for a {industry} company's {function_name} function and suggest 3-5 specific improvements:

        Configuration:
        - Name: {initiative_config.get('name', 'Unknown')}
        - AI Type: {initiative_config.get('ai_type', 'Unknown')}
        - Investment: ${initiative_config.get('investment', 0):,.0f}
        - Automation Level: {initiative_config.get('automation_level', 0)}%
        - Expected Productivity Gain: {initiative_config.get('productivity_gain', 0)}%

        Provide specific, actionable suggestions to:
        1. Optimize investment allocation
        2. Improve implementation approach
        3. Enhance expected outcomes
        4. Reduce risks
        5. Better align with {industry} best practices

        Return only a JSON array of improvement suggestions as strings.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an AI implementation consultant specializing in {industry} industry optimizations."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            
            result = json.loads(response.choices[0].message.content or "{}")
            return result.get('suggestions', [])
            
        except Exception as e:
            return self._rule_based_improvements(initiative_config, industry, function_name)
    
    def generate_category_suggestions(self, function_name: str, industry: str, existing_categories: List[str]) -> List[str]:
        """Generate AI category suggestions based on function and industry"""
        
        if not self.openai_client:
            return self._rule_based_categories(function_name, industry, existing_categories)
        
        prompt = f"""
        For a {industry} company's {function_name} function, suggest 5-7 AI initiative categories that would be most valuable.

        Existing categories: {', '.join(existing_categories) if existing_categories else 'None'}

        Focus on:
        1. Industry-specific opportunities
        2. Function-specific pain points
        3. Emerging AI applications in {industry}
        4. Categories not already covered

        Return a JSON object with category names as keys and brief descriptions as values.
        """
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an AI strategy consultant specializing in {industry} industry transformations."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                if content:
                    result = json.loads(content)
                    return list(result.keys()) if result else self._rule_based_categories(function_name, industry, existing_categories)
            
            return self._rule_based_categories(function_name, industry, existing_categories)
            
        except Exception as e:
            return self._rule_based_categories(function_name, industry, existing_categories)
    
    def _rule_based_categories(self, function_name: str, industry: str, existing_categories: List[str]) -> List[str]:
        """Generate categories using rule-based logic"""
        base_categories = [
            "Process Automation",
            "Data Analytics & Insights", 
            "Customer Experience Enhancement",
            "Operational Efficiency",
            "Risk Management"
        ]
        
        # Add industry-specific categories
        industry_categories = {
            'Healthcare': ["Clinical Decision Support", "Patient Care Optimization"],
            'Financial Services': ["Fraud Detection", "Algorithmic Trading"],
            'Retail': ["Inventory Optimization", "Personalization Engine"],
            'Manufacturing': ["Predictive Maintenance", "Quality Control"],
            'Technology': ["Code Generation", "Performance Optimization"]
        }
        
        if industry in industry_categories:
            base_categories.extend(industry_categories[industry])
        
        # Filter out existing categories
        new_categories = [cat for cat in base_categories if cat not in existing_categories]
        
        return new_categories[:7]
    
    def _validate_and_clean_config(self, config: Dict[str, Any], valid_ai_types: List[str]) -> Dict[str, Any]:
        """Validate and clean the parsed configuration"""
        
        cleaned = {}
        
        # Clean and validate fields
        cleaned['name'] = str(config.get('name', 'AI Initiative'))[:100]
        
        # Validate AI type
        ai_type = config.get('ai_type', '')
        if ai_type not in valid_ai_types:
            # Find closest match
            cleaned['ai_type'] = self._find_closest_ai_type(ai_type, valid_ai_types)
        else:
            cleaned['ai_type'] = ai_type
        
        # Validate numeric fields
        cleaned['investment'] = self._clean_number(config.get('investment'), 10000, 10000000)
        cleaned['automation_level'] = self._clean_percentage(config.get('automation_level'))
        cleaned['productivity_gain'] = self._clean_percentage(config.get('productivity_gain'))
        cleaned['workforce_reduction'] = self._clean_percentage(config.get('workforce_reduction'), max_val=50)
        
        # Validate categorical fields
        cleaned['timeline'] = self._validate_timeline(config.get('timeline', '6-12 months'))
        cleaned['complexity'] = self._validate_complexity(config.get('complexity', 'Medium'))
        
        # Keep text fields as-is
        cleaned['description'] = str(config.get('description', ''))
        cleaned['key_benefits'] = config.get('key_benefits', [])
        cleaned['implementation_steps'] = config.get('implementation_steps', [])
        
        return cleaned
    
    def _clean_number(self, value: Any, min_val: float = 0, max_val: float = float('inf')) -> float:
        """Clean and validate numeric values"""
        try:
            # Extract number from string if needed
            if isinstance(value, str):
                # Remove currency symbols and commas
                cleaned = re.sub(r'[,$]', '', value)
                value = float(cleaned)
            else:
                value = float(value)
            
            return max(min_val, min(max_val, value))
        except (ValueError, TypeError):
            return min_val
    
    def _rule_based_parsing(self, description: str, industry: str, function_name: str) -> Dict[str, Any]:
        """Rule-based parsing when OpenAI API is not available"""
        
        industry_types = self.industry_ai_types.get(industry, self.industry_ai_types['Technology'])
        description_lower = description.lower()
        
        # Extract AI type based on keywords
        ai_type = industry_types[0]  # Default
        for ai_type_option in industry_types:
            if any(word in description_lower for word in ai_type_option.lower().split()):
                ai_type = ai_type_option
                break
        
        # Estimate investment based on keywords
        investment = 100000  # Default
        if any(word in description_lower for word in ['large', 'enterprise', 'comprehensive']):
            investment = 500000
        elif any(word in description_lower for word in ['pilot', 'small', 'basic']):
            investment = 50000
        elif any(word in description_lower for word in ['medium', 'standard']):
            investment = 200000
        
        # Estimate automation level
        automation = 30  # Default
        if any(word in description_lower for word in ['automate', 'automation', 'replace']):
            automation = 70
        elif any(word in description_lower for word in ['assist', 'support', 'enhance']):
            automation = 40
        
        # Estimate productivity gain
        productivity = 20  # Default
        if any(word in description_lower for word in ['dramatically', 'significantly', 'major']):
            productivity = 50
        elif any(word in description_lower for word in ['improve', 'enhance', 'optimize']):
            productivity = 30
        
        return {
            'name': f"{function_name} AI Initiative",
            'ai_type': ai_type,
            'investment': investment,
            'automation_level': automation,
            'productivity_gain': productivity,
            'workforce_reduction': max(0, automation // 10),
            'timeline': '6-12 months',
            'complexity': 'Medium',
            'description': description,
            'key_benefits': [
                'Improved operational efficiency',
                'Enhanced decision-making capabilities',
                'Reduced manual workload',
                'Better resource utilization'
            ],
            'implementation_steps': [
                'Assess current processes and requirements',
                'Design and prototype AI solution',
                'Conduct pilot implementation',
                'Scale to full deployment',
                'Monitor and optimize performance'
            ]
        }
    
    def _rule_based_improvements(self, initiative_config: Dict[str, Any], industry: str, function_name: str) -> List[str]:
        """Generate improvement suggestions using rule-based logic"""
        
        suggestions = []
        investment = initiative_config.get('investment', 0)
        automation = initiative_config.get('automation_level', 0)
        productivity = initiative_config.get('productivity_gain', 0)
        
        # Investment-based suggestions
        if investment > 500000:
            suggestions.append("Consider phased implementation to reduce initial investment risk")
        elif investment < 50000:
            suggestions.append("Ensure adequate budget allocation for comprehensive implementation")
        
        # Automation-based suggestions
        if automation > 80:
            suggestions.append("Plan comprehensive change management for high automation levels")
        elif automation < 20:
            suggestions.append("Explore opportunities for higher automation to maximize ROI")
        
        # Productivity-based suggestions
        if productivity > 50:
            suggestions.append("Validate ambitious productivity targets with pilot testing")
        elif productivity < 15:
            suggestions.append("Consider more impactful AI applications to increase productivity gains")
        
        # Industry-specific suggestions
        industry_suggestions = {
            'Healthcare': "Ensure compliance with HIPAA and medical device regulations",
            'Financial Services': "Address regulatory requirements and risk management protocols",
            'Manufacturing': "Focus on safety protocols and quality control integration",
            'Retail': "Consider seasonal variations and customer experience impact",
            'Technology': "Leverage existing technical infrastructure and expertise"
        }
        
        if industry in industry_suggestions:
            suggestions.append(industry_suggestions[industry])
        
        # Ensure we have at least 3 suggestions
        while len(suggestions) < 3:
            suggestions.extend([
                "Establish clear success metrics and monitoring framework",
                "Plan adequate training and upskilling for affected employees",
                "Consider integration with existing systems and workflows"
            ])
        
        return suggestions[:5]  # Return top 5
    
    def _clean_percentage(self, value: Any, max_val: float = 100) -> float:
        """Clean and validate percentage values"""
        try:
            if isinstance(value, str):
                # Remove percentage symbol
                cleaned = value.replace('%', '')
                value = float(cleaned)
            else:
                value = float(value)
            
            return max(0, min(max_val, value))
        except (ValueError, TypeError):
            return 0
    
    def _find_closest_ai_type(self, target: str, valid_types: List[str]) -> str:
        """Find the closest matching AI type"""
        target_lower = target.lower()
        
        # Simple keyword matching
        for ai_type in valid_types:
            if any(word in target_lower for word in ai_type.lower().split()):
                return ai_type
        
        # Default fallback
        return valid_types[0] if valid_types else 'Machine Learning'
    
    def _validate_timeline(self, timeline: str) -> str:
        """Validate timeline values"""
        valid_timelines = ['3-6 months', '6-12 months', '12+ months']
        
        if timeline in valid_timelines:
            return timeline
        
        # Try to map based on keywords
        timeline_lower = str(timeline).lower()
        if any(word in timeline_lower for word in ['short', 'quick', '3', '6']):
            return '3-6 months'
        elif any(word in timeline_lower for word in ['medium', 'year', '12']):
            return '6-12 months'
        else:
            return '12+ months'
    
    def _validate_complexity(self, complexity: str) -> str:
        """Validate complexity values"""
        valid_complexities = ['Low', 'Medium', 'High']
        
        if complexity in valid_complexities:
            return complexity
        
        # Try to map based on keywords
        complexity_lower = str(complexity).lower()
        if any(word in complexity_lower for word in ['low', 'simple', 'easy']):
            return 'Low'
        elif any(word in complexity_lower for word in ['high', 'complex', 'difficult']):
            return 'High'
        else:
            return 'Medium'
    
    def _generate_default_config(self, description: str, industry: str, function_name: str) -> Dict[str, Any]:
        """Generate a default configuration when parsing fails"""
        
        industry_types = self.industry_ai_types.get(industry, self.industry_ai_types['Technology'])
        
        return {
            'name': f"{function_name} AI Initiative",
            'ai_type': industry_types[0],
            'investment': 100000,
            'automation_level': 30,
            'productivity_gain': 15,
            'workforce_reduction': 5,
            'timeline': '6-12 months',
            'complexity': 'Medium',
            'description': description,
            'key_benefits': [
                'Improved operational efficiency',
                'Enhanced decision-making capabilities',
                'Reduced manual workload'
            ],
            'implementation_steps': [
                'Assess current processes',
                'Design AI solution',
                'Pilot implementation',
                'Full deployment',
                'Monitor and optimize'
            ]
        }

class CrossFunctionAnalyzer:
    """Analyze dependencies and relationships between enterprise functions"""
    
    def __init__(self):
        pass
    
    def analyze_function_dependencies(self, baseline_data: Dict[str, Dict], categories_data: Dict[str, Dict]) -> Dict[str, Any]:
        """Analyze dependencies between configured functions"""
        
        functions = list(baseline_data.keys())
        
        if len(functions) < 2:
            return {
                'dependencies': {},
                'impact_matrix': {},
                'optimization_opportunities': [],
                'implementation_sequence': functions
            }
        
        # Calculate dependency relationships
        dependencies = self._calculate_dependencies(functions, baseline_data, categories_data)
        
        # Create impact matrix
        impact_matrix = self._create_impact_matrix(functions, dependencies, baseline_data)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(
            functions, dependencies, baseline_data, categories_data
        )
        
        # Suggest implementation sequence
        implementation_sequence = self._suggest_implementation_sequence(
            functions, dependencies, impact_matrix
        )
        
        return {
            'dependencies': dependencies,
            'impact_matrix': impact_matrix,
            'optimization_opportunities': optimization_opportunities,
            'implementation_sequence': implementation_sequence
        }
    
    def _calculate_dependencies(self, functions: List[str], baseline_data: Dict, categories_data: Dict) -> Dict[str, List[Dict]]:
        """Calculate dependency relationships between functions"""
        
        dependencies = {}
        
        # Define common dependency patterns
        dependency_patterns = {
            # Customer-facing functions
            ('Sales Operations', 'Customer Service'): 0.8,
            ('Customer Service', 'Sales Operations'): 0.6,
            ('Marketing Operations', 'Sales Operations'): 0.7,
            
            # Operations dependencies
            ('Supply Chain Management', 'Manufacturing Operations'): 0.9,
            ('Manufacturing Operations', 'Quality Control'): 0.8,
            ('Inventory Management', 'Supply Chain Management'): 0.7,
            
            # Support function dependencies
            ('Human Resources', 'Learning & Development'): 0.8,
            ('Finance & Accounting', 'Procurement'): 0.6,
            ('IT Operations', 'Data Management'): 0.9,
            
            # Healthcare dependencies
            ('Patient Care', 'Clinical Operations'): 0.9,
            ('Clinical Operations', 'Medical Records Management'): 0.8,
            
            # Financial services
            ('Risk Management', 'Compliance'): 0.8,
            ('Trading Operations', 'Risk Management'): 0.7,
            
            # Generic patterns
            ('Operations', 'Management'): 0.6,
            ('Analytics', 'Operations'): 0.5
        }
        
        for func1 in functions:
            dependencies[func1] = []
            
            for func2 in functions:
                if func1 != func2:
                    # Calculate dependency strength
                    strength = self._calculate_dependency_strength(
                        func1, func2, dependency_patterns, baseline_data, categories_data
                    )
                    
                    if strength > 0.3:  # Only include significant dependencies
                        dependencies[func1].append({
                            'target_function': func2,
                            'dependency_strength': strength,
                            'dependency_type': self._classify_dependency_type(func1, func2, strength)
                        })
        
        return dependencies
    
    def _calculate_dependency_strength(self, func1: str, func2: str, patterns: Dict, 
                                     baseline_data: Dict, categories_data: Dict) -> float:
        """Calculate the strength of dependency between two functions"""
        
        # Check for exact pattern matches
        if (func1, func2) in patterns:
            base_strength = patterns[(func1, func2)]
        else:
            # Check for partial keyword matches
            base_strength = 0
            for (pattern_func1, pattern_func2), strength in patterns.items():
                if (any(word in func1.lower() for word in pattern_func1.lower().split()) and
                    any(word in func2.lower() for word in pattern_func2.lower().split())):
                    base_strength = max(base_strength, strength * 0.7)  # Reduce for partial matches
        
        # Adjust based on relative sizes and importance
        if func1 in baseline_data and func2 in baseline_data:
            func1_data = baseline_data[func1]
            func2_data = baseline_data[func2]
            
            # Larger functions tend to have more dependencies
            size_factor = min(func1_data.get('headcount', 1), func2_data.get('headcount', 1)) / 100
            base_strength += size_factor * 0.1
            
            # Revenue-generating functions have higher interdependencies
            revenue_factor = (func1_data.get('revenue', 0) + func2_data.get('revenue', 0)) / 2000000
            base_strength += revenue_factor * 0.05
        
        return min(1.0, base_strength)
    
    def _classify_dependency_type(self, func1: str, func2: str, strength: float) -> str:
        """Classify the type of dependency between functions"""
        
        if strength > 0.7:
            return 'Critical'
        elif strength > 0.5:
            return 'High'
        elif strength > 0.3:
            return 'Medium'
        else:
            return 'Low'
    
    def _create_impact_matrix(self, functions: List[str], dependencies: Dict, baseline_data: Dict) -> Dict[str, Dict[str, float]]:
        """Create impact matrix showing how AI implementations affect other functions"""
        
        impact_matrix = {}
        
        for func1 in functions:
            impact_matrix[func1] = {}
            
            for func2 in functions:
                if func1 == func2:
                    impact_matrix[func1][func2] = 1.0  # Self-impact
                else:
                    # Calculate impact based on dependencies and relative importance
                    impact_score = 0
                    
                    # Check if func1 depends on func2
                    func1_deps = dependencies.get(func1, [])
                    for dep in func1_deps:
                        if dep['target_function'] == func2:
                            impact_score += dep['dependency_strength'] * 0.6
                    
                    # Check if func2 depends on func1 (reverse impact)
                    func2_deps = dependencies.get(func2, [])
                    for dep in func2_deps:
                        if dep['target_function'] == func1:
                            impact_score += dep['dependency_strength'] * 0.4
                    
                    # Adjust based on function sizes
                    if func1 in baseline_data and func2 in baseline_data:
                        func1_revenue = baseline_data[func1].get('revenue', 0)
                        func2_revenue = baseline_data[func2].get('revenue', 0)
                        
                        if func1_revenue > 0 and func2_revenue > 0:
                            revenue_ratio = min(func1_revenue, func2_revenue) / max(func1_revenue, func2_revenue)
                            impact_score *= (0.5 + revenue_ratio * 0.5)
                    
                    impact_matrix[func1][func2] = min(1.0, impact_score)
        
        return impact_matrix
    
    def _identify_optimization_opportunities(self, functions: List[str], dependencies: Dict, 
                                          baseline_data: Dict, categories_data: Dict) -> List[Dict[str, Any]]:
        """Identify cross-function optimization opportunities"""
        
        opportunities = []
        
        # Opportunity 1: Shared AI Infrastructure
        ai_types_by_function = {}
        for func in functions:
            if f'categories_{func}' in categories_data:
                categories = categories_data[f'categories_{func}']
                ai_types = set()
                for category_data in categories.values():
                    initiatives = category_data.get('ai_initiatives', {})
                    for init_data in initiatives.values():
                        ai_types.add(init_data.get('ai_type', 'Unknown'))
                ai_types_by_function[func] = ai_types
        
        # Find functions with overlapping AI types
        for i, func1 in enumerate(functions):
            for func2 in functions[i+1:]:
                if func1 in ai_types_by_function and func2 in ai_types_by_function:
                    overlap = ai_types_by_function[func1] & ai_types_by_function[func2]
                    if overlap:
                        opportunities.append({
                            'type': 'Shared AI Infrastructure',
                            'functions': [func1, func2],
                            'ai_types': list(overlap),
                            'potential_savings': '15-30%',
                            'description': f'Share AI infrastructure for {", ".join(overlap)} between {func1} and {func2}'
                        })
        
        # Opportunity 2: Sequential Implementation Benefits
        for func1 in functions:
            func1_deps = dependencies.get(func1, [])
            high_deps = [dep for dep in func1_deps if dep['dependency_strength'] > 0.6]
            
            if high_deps:
                opportunities.append({
                    'type': 'Sequential Implementation',
                    'functions': [func1] + [dep['target_function'] for dep in high_deps],
                    'dependency_strength': max(dep['dependency_strength'] for dep in high_deps),
                    'potential_benefit': 'Reduced implementation risk and enhanced outcomes',
                    'description': f'Implement AI in {func1} after dependent functions for optimal results'
                })
        
        # Opportunity 3: Data Synergy
        for func1 in functions:
            for func2 in functions:
                if func1 != func2 and func1 in baseline_data and func2 in baseline_data:
                    # Functions with similar revenue patterns might benefit from shared analytics
                    func1_revenue = baseline_data[func1].get('revenue', 0)
                    func2_revenue = baseline_data[func2].get('revenue', 0)
                    
                    if abs(func1_revenue - func2_revenue) / max(func1_revenue, func2_revenue, 1) < 0.3:
                        opportunities.append({
                            'type': 'Data Synergy',
                            'functions': [func1, func2],
                            'similarity_score': 1 - abs(func1_revenue - func2_revenue) / max(func1_revenue, func2_revenue, 1),
                            'potential_benefit': 'Enhanced analytics through combined datasets',
                            'description': f'Combine data analytics initiatives between {func1} and {func2}'
                        })
        
        return opportunities[:10]  # Limit to top 10 opportunities
    
    def _suggest_implementation_sequence(self, functions: List[str], dependencies: Dict, 
                                       impact_matrix: Dict[str, Dict[str, float]]) -> List[str]:
        """Suggest optimal implementation sequence based on dependencies"""
        
        # Calculate dependency scores for each function
        dependency_scores = {}
        
        for func in functions:
            # Score based on how many functions depend on this one
            incoming_dependencies = 0
            outgoing_dependencies = len(dependencies.get(func, []))
            
            for other_func in functions:
                other_deps = dependencies.get(other_func, [])
                for dep in other_deps:
                    if dep['target_function'] == func:
                        incoming_dependencies += dep['dependency_strength']
            
            # Functions with high incoming dependencies should be implemented first
            # Functions with high outgoing dependencies should be implemented later
            dependency_scores[func] = incoming_dependencies - (outgoing_dependencies * 0.5)
        
        # Sort by dependency score (highest first)
        sorted_functions = sorted(functions, key=lambda f: dependency_scores[f], reverse=True)
        
        return sorted_functions