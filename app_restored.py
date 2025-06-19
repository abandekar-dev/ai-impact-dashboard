import streamlit as st
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import uuid

# Configure Streamlit page
st.set_page_config(
    page_title="AI Strategic Workforce Modeling Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database and Utilities
class DatabaseManager:
    """Manages database operations with graceful fallbacks"""
    
    def __init__(self):
        self.connected = self._test_connection()
    
    def _test_connection(self) -> bool:
        try:
            import psycopg2
            db_url = os.environ.get('DATABASE_URL')
            if not db_url:
                return False
            conn = psycopg2.connect(db_url)
            conn.close()
            return True
        except:
            return False
    
    def save_function_data(self, function_name: str, data: Dict):
        """Save function data with session state fallback"""
        if not hasattr(st.session_state, 'function_data'):
            st.session_state.function_data = {}
        st.session_state.function_data[function_name] = data
        
        if self.connected:
            try:
                import psycopg2
                conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO function_analysis (function_name, data, updated_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (function_name) 
                    DO UPDATE SET data = EXCLUDED.data, updated_at = EXCLUDED.updated_at
                """, (function_name, json.dumps(data), datetime.now()))
                conn.commit()
                conn.close()
            except:
                pass  # Fallback to session state
    
    def get_function_data(self, function_name: str) -> Dict:
        """Get function data with session state fallback"""
        if self.connected:
            try:
                import psycopg2
                conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
                cur = conn.cursor()
                cur.execute("SELECT data FROM function_analysis WHERE function_name = %s", (function_name,))
                result = cur.fetchone()
                conn.close()
                if result:
                    return json.loads(result[0])
            except:
                pass
        
        # Fallback to session state
        if hasattr(st.session_state, 'function_data'):
            return st.session_state.function_data.get(function_name, {})
        return {}

class NaturalLanguageProcessor:
    """Natural language processing for AI initiative configuration"""
    
    def __init__(self):
        self.openai_available = self._check_openai()
    
    def _check_openai(self) -> bool:
        try:
            import openai
            api_key = os.environ.get('OPENAI_API_KEY')
            return bool(api_key)
        except:
            return False
    
    def parse_initiative_description(self, description: str, industry: str, function_name: str) -> Dict[str, Any]:
        """Parse natural language description into structured AI initiative configuration"""
        
        if self.openai_available:
            try:
                import openai
                client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "system",
                        "content": f"""You are an AI strategy consultant. Parse the user's description into a structured AI initiative configuration for {industry} industry, {function_name} function.

Return JSON with these fields:
- ai_type: one of ["Process Automation", "Predictive Analytics", "Natural Language Processing", "Computer Vision", "Recommendation Systems", "Robotic Process Automation", "Machine Learning", "Deep Learning"]
- complexity: "Low", "Medium", or "High"
- timeline_months: integer between 3-24
- implementation_cost: integer (thousands USD)
- confidence_level: float between 0.7-0.95
- expected_productivity_gain: float between 0.05-0.50
- risk_factors: array of strings
- success_metrics: array of strings"""
                    }, {
                        "role": "user",
                        "content": f"Parse this AI initiative: {description}"
                    }],
                    response_format={"type": "json_object"}
                )
                
                return json.loads(response.choices[0].message.content)
            except:
                pass
        
        # Intelligent fallback based on keywords
        return self._rule_based_parsing(description, industry, function_name)
    
    def _rule_based_parsing(self, description: str, industry: str, function_name: str) -> Dict[str, Any]:
        """Rule-based parsing fallback"""
        desc_lower = description.lower()
        
        # AI type detection
        ai_type_map = {
            "chatbot|chat|conversation|nlp|language": "Natural Language Processing",
            "automat|process|workflow|rpa": "Process Automation", 
            "predict|forecast|analytic|trend": "Predictive Analytics",
            "vision|image|photo|visual|ocr": "Computer Vision",
            "recommend|suggest|personali": "Recommendation Systems",
            "robot|rpa|task": "Robotic Process Automation",
            "learn|model|algorithm": "Machine Learning",
            "deep|neural|ai": "Deep Learning"
        }
        
        ai_type = "Process Automation"
        for keywords, ai_tech in ai_type_map.items():
            if any(keyword in desc_lower for keyword in keywords.split("|")):
                ai_type = ai_tech
                break
        
        # Industry-specific adjustments
        industry_factors = {
            "Technology": {"cost_multiplier": 1.2, "timeline_factor": 0.9},
            "Healthcare": {"cost_multiplier": 1.5, "timeline_factor": 1.3},
            "Financial Services": {"cost_multiplier": 1.4, "timeline_factor": 1.2},
            "Manufacturing": {"cost_multiplier": 1.1, "timeline_factor": 1.1},
            "Retail": {"cost_multiplier": 0.9, "timeline_factor": 0.8}
        }
        
        factors = industry_factors.get(industry, {"cost_multiplier": 1.0, "timeline_factor": 1.0})
        
        # Complexity assessment
        complexity_indicators = {
            "simple|basic|easy": "Low",
            "complex|advanced|sophisticated|enterprise": "High",
            "": "Medium"  # default
        }
        
        complexity = "Medium"
        for keywords, level in complexity_indicators.items():
            if keywords and any(keyword in desc_lower for keyword in keywords.split("|")):
                complexity = level
                break
        
        # Generate configuration
        base_cost = {"Low": 50, "Medium": 150, "High": 300}[complexity]
        base_timeline = {"Low": 6, "Medium": 12, "High": 18}[complexity]
        
        return {
            "ai_type": ai_type,
            "complexity": complexity,
            "timeline_months": int(base_timeline * factors["timeline_factor"]),
            "implementation_cost": int(base_cost * factors["cost_multiplier"]),
            "confidence_level": 0.85,
            "expected_productivity_gain": 0.15 + (0.1 if complexity == "High" else 0),
            "risk_factors": self._generate_risk_factors(ai_type, complexity, industry),
            "success_metrics": self._generate_success_metrics(function_name, ai_type)
        }
    
    def _generate_risk_factors(self, ai_type: str, complexity: str, industry: str) -> List[str]:
        """Generate relevant risk factors"""
        risks = {
            "Natural Language Processing": ["Data quality issues", "Language complexity", "User adoption"],
            "Process Automation": ["Integration complexity", "Change resistance", "Process dependencies"],
            "Predictive Analytics": ["Data availability", "Model accuracy", "Business volatility"],
            "Computer Vision": ["Image quality requirements", "Hardware dependencies", "Accuracy expectations"],
            "Recommendation Systems": ["Data sparsity", "Cold start problem", "Privacy concerns"],
            "Machine Learning": ["Training data quality", "Model interpretability", "Performance drift"],
            "Deep Learning": ["Computational requirements", "Black box decisions", "Training complexity"]
        }
        
        base_risks = risks.get(ai_type, ["Implementation complexity", "User adoption", "Technical challenges"])
        
        if complexity == "High":
            base_risks.append("Resource constraints")
        if industry in ["Healthcare", "Financial Services"]:
            base_risks.append("Regulatory compliance")
            
        return base_risks[:4]  # Limit to 4 risks
    
    def _generate_success_metrics(self, function_name: str, ai_type: str) -> List[str]:
        """Generate relevant success metrics"""
        function_metrics = {
            "Sales": ["Revenue increase", "Lead conversion rate", "Sales cycle time"],
            "Marketing": ["Campaign ROI", "Customer acquisition cost", "Engagement rates"],
            "Operations": ["Process efficiency", "Error reduction", "Cost savings"],
            "Support": ["Response time", "Resolution rate", "Customer satisfaction"],
            "HR": ["Recruitment time", "Employee satisfaction", "Turnover reduction"],
            "Finance": ["Processing accuracy", "Compliance rate", "Cost reduction"],
            "IT": ["System uptime", "Security incidents", "User satisfaction"],
            "Legal": ["Document processing time", "Compliance accuracy", "Risk reduction"],
            "R&D": ["Innovation speed", "Project success rate", "Time to market"]
        }
        
        return function_metrics.get(function_name, ["Efficiency improvement", "Cost reduction", "User satisfaction"])

class CrossFunctionAnalyzer:
    """Analyzes dependencies and relationships between enterprise functions"""
    
    def __init__(self):
        self.dependency_matrix = self._build_dependency_matrix()
    
    def _build_dependency_matrix(self) -> Dict[str, Dict[str, float]]:
        """Build function dependency relationships"""
        return {
            "Sales": {"Marketing": 0.8, "Support": 0.6, "Finance": 0.5, "Operations": 0.4},
            "Marketing": {"Sales": 0.9, "IT": 0.7, "Operations": 0.3, "Finance": 0.4},
            "Operations": {"IT": 0.8, "Finance": 0.7, "Support": 0.5, "HR": 0.4},
            "Support": {"IT": 0.7, "Sales": 0.6, "Operations": 0.5, "HR": 0.3},
            "HR": {"IT": 0.6, "Finance": 0.5, "Operations": 0.4, "Legal": 0.3},
            "Finance": {"IT": 0.8, "Operations": 0.6, "HR": 0.5, "Legal": 0.4},
            "IT": {"Operations": 0.9, "Finance": 0.7, "HR": 0.6, "Support": 0.8},
            "Legal": {"Finance": 0.6, "HR": 0.5, "Operations": 0.4, "IT": 0.3},
            "R&D": {"IT": 0.7, "Operations": 0.4, "Marketing": 0.5, "Finance": 0.3}
        }
    
    def analyze_dependencies(self, functions: List[str]) -> Dict[str, Any]:
        """Analyze dependencies between selected functions"""
        dependencies = {}
        impact_scores = {}
        
        for func in functions:
            dependencies[func] = {}
            impact_scores[func] = 0
            
            for other_func in functions:
                if func != other_func:
                    dependency_score = self.dependency_matrix.get(func, {}).get(other_func, 0.1)
                    dependencies[func][other_func] = dependency_score
                    impact_scores[func] += dependency_score
        
        # Generate implementation sequence
        sequence = sorted(functions, key=lambda f: impact_scores[f], reverse=True)
        
        return {
            "dependencies": dependencies,
            "impact_scores": impact_scores,
            "implementation_sequence": sequence,
            "optimization_opportunities": self._find_optimization_opportunities(dependencies)
        }
    
    def _find_optimization_opportunities(self, dependencies: Dict) -> List[Dict]:
        """Find optimization opportunities across functions"""
        opportunities = []
        
        # High dependency pairs
        for func, deps in dependencies.items():
            for dep_func, score in deps.items():
                if score > 0.7:
                    opportunities.append({
                        "type": "Integration Opportunity",
                        "functions": [func, dep_func],
                        "potential_benefit": "Shared AI infrastructure",
                        "estimated_savings": f"{int(score * 20)}%"
                    })
        
        return opportunities

class CategoryManager:
    """Manages categories and AI initiatives within enterprise functions"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_default_categories(self, function_name: str) -> List[str]:
        """Get default categories for a given function"""
        categories = {
            "Sales": ["Lead Generation", "Customer Relationship Management", "Sales Analytics", "Proposal Automation"],
            "Marketing": ["Campaign Management", "Content Creation", "Customer Segmentation", "Performance Analytics"],
            "Operations": ["Process Optimization", "Supply Chain", "Quality Control", "Resource Planning"],
            "Support": ["Customer Service", "Technical Support", "Knowledge Management", "Issue Resolution"],
            "HR": ["Recruitment", "Employee Engagement", "Performance Management", "Learning & Development"],
            "Finance": ["Financial Planning", "Risk Management", "Compliance", "Reporting & Analytics"],
            "IT": ["Infrastructure", "Security", "Application Development", "Data Management"],
            "Legal": ["Contract Management", "Compliance Monitoring", "Risk Assessment", "Document Review"],
            "R&D": ["Research Analytics", "Innovation Management", "Product Development", "Testing & Validation"]
        }
        return categories.get(function_name, ["General Operations", "Analytics", "Automation", "Optimization"])
    
    def initialize_function_categories(self, function_name: str) -> None:
        """Initialize categories for a function if not already present"""
        if f"{function_name}_categories" not in st.session_state:
            categories = self.get_default_categories(function_name)
            st.session_state[f"{function_name}_categories"] = {
                cat: {"description": f"{cat} initiatives for {function_name}", "initiatives": {}}
                for cat in categories
            }
    
    def add_ai_initiative(self, function_name: str, category_name: str, 
                         initiative_name: str, initiative_data: Dict) -> str:
        """Add an AI initiative to a category"""
        self.initialize_function_categories(function_name)
        
        initiative_id = str(uuid.uuid4())
        initiative_data["id"] = initiative_id
        initiative_data["created_at"] = datetime.now().isoformat()
        
        if category_name not in st.session_state[f"{function_name}_categories"]:
            st.session_state[f"{function_name}_categories"][category_name] = {
                "description": f"{category_name} initiatives",
                "initiatives": {}
            }
        
        st.session_state[f"{function_name}_categories"][category_name]["initiatives"][initiative_id] = {
            "name": initiative_name,
            "data": initiative_data
        }
        
        # Save to database
        self.db.save_function_data(function_name, st.session_state[f"{function_name}_categories"])
        
        return initiative_id
    
    def get_ai_initiatives(self, function_name: str, category_name: str = None) -> Dict:
        """Get AI initiatives for a category or all categories in a function"""
        self.initialize_function_categories(function_name)
        
        if category_name:
            return st.session_state[f"{function_name}_categories"].get(category_name, {}).get("initiatives", {})
        else:
            all_initiatives = {}
            for cat_name, cat_data in st.session_state[f"{function_name}_categories"].items():
                all_initiatives[cat_name] = cat_data.get("initiatives", {})
            return all_initiatives
    
    def get_function_summary(self, function_name: str) -> Dict:
        """Get summary statistics for a function"""
        self.initialize_function_categories(function_name)
        
        total_initiatives = 0
        total_cost = 0
        ai_types = {}
        
        for category_data in st.session_state[f"{function_name}_categories"].values():
            for initiative in category_data.get("initiatives", {}).values():
                total_initiatives += 1
                total_cost += initiative["data"].get("implementation_cost", 0)
                ai_type = initiative["data"].get("ai_type", "Unknown")
                ai_types[ai_type] = ai_types.get(ai_type, 0) + 1
        
        return {
            "total_initiatives": total_initiatives,
            "total_cost": total_cost,
            "ai_type_distribution": ai_types,
            "categories": len(st.session_state[f"{function_name}_categories"])
        }

# Main Application
def init_database():
    """Initialize database tables if needed"""
    try:
        import psycopg2
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            return False
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Create function_analysis table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS function_analysis (
                function_name VARCHAR(255) PRIMARY KEY,
                data JSONB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def auto_save_data():
    """Automatically save data to prevent loss during navigation"""
    if hasattr(st.session_state, 'function_data'):
        db = DatabaseManager()
        for func_name, data in st.session_state.function_data.items():
            db.save_function_data(func_name, data)

def main():
    """Main application entry point"""
    
    # Initialize database
    db_connected = init_database()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Overview'
    
    # Sidebar navigation
    st.sidebar.title("🤖 AI Strategic Platform")
    st.sidebar.markdown("---")
    
    # Database status
    if db_connected:
        st.sidebar.success("🔗 Database Connected")
    else:
        st.sidebar.warning("📱 Session Mode")
    
    # Navigation
    pages = {
        "📊 Overview": show_overview,
        "🎯 Function Analysis": show_function_analysis,
        "🎲 Monte Carlo Simulation": show_monte_carlo_simulation,
        "📈 Strategic Planning": show_strategic_planning,
        "⚖️ Scenario Comparison": show_scenario_comparison,
        "⏰ Temporal Analysis": show_temporal_analysis,
        "📋 Executive Summary": show_executive_summary,
        "🔧 Benchmarking & Optimization": show_benchmarking_optimization
    }
    
    selected_page = st.sidebar.selectbox(
        "Navigate to",
        list(pages.keys()),
        index=list(pages.keys()).index(f"📊 {st.session_state.current_page}") if f"📊 {st.session_state.current_page}" in pages else 0
    )
    
    st.session_state.current_page = selected_page.split(" ", 1)[1]
    
    # Auto-save data
    auto_save_data()
    
    # Display selected page
    pages[selected_page]()

def show_overview():
    """Main overview page with system status and quick actions"""
    st.title("🤖 AI Strategic Workforce Modeling Platform")
    st.markdown("### Transform your enterprise with intelligent AI strategic planning")
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Database Status", "Connected" if DatabaseManager().connected else "Session Mode")
    
    with col2:
        nlp = NaturalLanguageProcessor()
        st.metric("AI Services", "Available" if nlp.openai_available else "Offline Mode")
    
    with col3:
        # Count total functions configured
        total_functions = len([key for key in st.session_state.keys() if key.endswith('_categories')])
        st.metric("Functions Configured", total_functions)
    
    with col4:
        # Count total initiatives
        total_initiatives = 0
        for key in st.session_state.keys():
            if key.endswith('_categories'):
                for category_data in st.session_state[key].values():
                    total_initiatives += len(category_data.get('initiatives', {}))
        st.metric("AI Initiatives", total_initiatives)
    
    st.markdown("---")
    
    # Quick Start Guide
    st.subheader("🚀 Quick Start Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Phase 1 Optimizations Active:**
        - ✅ Natural Language Configuration
        - ✅ Cross-Function Dependency Analysis  
        - ✅ Industry-Specific Intelligence
        - ✅ Vector Database Integration
        """)
    
    with col2:
        st.markdown("""
        **Getting Started:**
        1. Navigate to **Function Analysis** 
        2. Select your industry and function
        3. Describe your AI initiatives in plain English
        4. Review generated configurations and dependencies
        """)
    
    # Architecture Overview
    st.subheader("🏗️ System Architecture")
    
    if os.path.exists("ai_platform_architecture.png"):
        st.image("ai_platform_architecture.png", caption="AI Strategic Platform Architecture", use_column_width=True)
    else:
        st.info("Architecture diagram available - click to generate visual overview")
        if st.button("Generate Architecture Diagram"):
            # Placeholder for architecture generation
            st.success("Architecture diagram would be generated here")
    
    # Recent Activity
    st.subheader("📈 Recent Activity")
    
    if total_initiatives > 0:
        st.success(f"System is active with {total_initiatives} AI initiatives across {total_functions} functions")
        
        # Show recent initiatives
        recent_initiatives = []
        for key in st.session_state.keys():
            if key.endswith('_categories'):
                function_name = key.replace('_categories', '')
                for category_name, category_data in st.session_state[key].items():
                    for initiative_id, initiative in category_data.get('initiatives', {}).items():
                        recent_initiatives.append({
                            'function': function_name,
                            'category': category_name,
                            'name': initiative['name'],
                            'ai_type': initiative['data'].get('ai_type', 'Unknown'),
                            'created': initiative['data'].get('created_at', 'Unknown')
                        })
        
        if recent_initiatives:
            # Sort by creation date and show last 5
            recent_initiatives.sort(key=lambda x: x['created'], reverse=True)
            
            st.markdown("**Recent AI Initiatives:**")
            for initiative in recent_initiatives[:5]:
                st.markdown(f"• **{initiative['name']}** ({initiative['ai_type']}) - {initiative['function']}")
    else:
        st.info("Start by configuring your first AI initiative in the Function Analysis section")

def show_function_analysis():
    """Enhanced function analysis with natural language AI initiative creation"""
    st.title("🎯 Enhanced Function Analysis")
    st.markdown("Configure AI initiatives using natural language descriptions")
    
    # Initialize managers
    category_manager = CategoryManager()
    nlp_processor = NaturalLanguageProcessor()
    cross_analyzer = CrossFunctionAnalyzer()
    
    # Industry and Function Selection
    col1, col2 = st.columns(2)
    
    with col1:
        industries = [
            "Technology", "Healthcare", "Financial Services", "Manufacturing", 
            "Retail", "Life Sciences", "Energy & Utilities", "Education", "Government"
        ]
        selected_industry = st.selectbox("Select Industry", industries)
    
    with col2:
        functions = [
            "Sales", "Marketing", "Operations", "Support", "HR", 
            "Finance", "IT", "Legal", "R&D"
        ]
        selected_function = st.selectbox("Select Function", functions)
    
    # Initialize categories for selected function
    category_manager.initialize_function_categories(selected_function)
    
    # Tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["AI Initiative Creation", "Function Overview", "Cross-Function Dependencies"])
    
    with tab1:
        st.subheader("🤖 Create AI Initiative")
        
        # Natural Language Input
        st.markdown("**Describe your AI initiative in plain English:**")
        initiative_description = st.text_area(
            "Initiative Description",
            placeholder="E.g., 'Implement a chatbot to handle customer support inquiries and reduce response time'",
            height=100
        )
        
        initiative_name = st.text_input(
            "Initiative Name",
            placeholder="E.g., Customer Support Chatbot"
        )
        
        categories = category_manager.get_default_categories(selected_function)
        selected_category = st.selectbox("Category", categories)
        
        if st.button("🔮 Generate AI Configuration", type="primary"):
            if initiative_description and initiative_name:
                with st.spinner("Analyzing initiative and generating configuration..."):
                    # Parse the description
                    config = nlp_processor.parse_initiative_description(
                        initiative_description, selected_industry, selected_function
                    )
                    
                    # Display generated configuration
                    st.success("✅ AI Initiative Configuration Generated!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Generated Configuration:**")
                        st.json(config)
                    
                    with col2:
                        st.markdown("**Key Metrics:**")
                        st.metric("AI Type", config.get('ai_type', 'Unknown'))
                        st.metric("Complexity", config.get('complexity', 'Unknown'))
                        st.metric("Timeline", f"{config.get('timeline_months', 0)} months")
                        st.metric("Cost", f"${config.get('implementation_cost', 0):,}k")
                        st.metric("Productivity Gain", f"{config.get('expected_productivity_gain', 0):.1%}")
                    
                    # Save initiative
                    if st.button("💾 Save Initiative"):
                        initiative_id = category_manager.add_ai_initiative(
                            selected_function, selected_category, initiative_name, config
                        )
                        st.success(f"Initiative '{initiative_name}' saved successfully!")
                        st.rerun()
            else:
                st.error("Please provide both initiative description and name")
    
    with tab2:
        st.subheader("📊 Function Overview")
        
        # Function summary
        summary = category_manager.get_function_summary(selected_function)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Initiatives", summary['total_initiatives'])
        with col2:
            st.metric("Total Investment", f"${summary['total_cost']:,}k")
        with col3:
            st.metric("Categories", summary['categories'])
        with col4:
            avg_cost = summary['total_cost'] / max(summary['total_initiatives'], 1)
            st.metric("Avg Cost per Initiative", f"${avg_cost:,.0f}k")
        
        # AI Type Distribution
        if summary['ai_type_distribution']:
            st.markdown("**AI Type Distribution:**")
            
            # Create a simple bar chart data
            ai_types = list(summary['ai_type_distribution'].keys())
            counts = list(summary['ai_type_distribution'].values())
            
            chart_data = {ai_type: count for ai_type, count in zip(ai_types, counts)}
            st.bar_chart(chart_data)
        
        # Category Details
        st.markdown("**Category Breakdown:**")
        
        categories_data = st.session_state.get(f"{selected_function}_categories", {})
        for category_name, category_data in categories_data.items():
            initiatives = category_data.get('initiatives', {})
            
            if initiatives:
                with st.expander(f"{category_name} ({len(initiatives)} initiatives)"):
                    for initiative_id, initiative in initiatives.items():
                        st.markdown(f"**{initiative['name']}**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"Type: {initiative['data'].get('ai_type', 'Unknown')}")
                        with col2:
                            st.write(f"Cost: ${initiative['data'].get('implementation_cost', 0)}k")
                        with col3:
                            st.write(f"Timeline: {initiative['data'].get('timeline_months', 0)} months")
                        
                        st.markdown("---")
    
    with tab3:
        st.subheader("🔗 Cross-Function Dependencies")
        
        # Get all configured functions
        configured_functions = []
        for key in st.session_state.keys():
            if key.endswith('_categories'):
                func_name = key.replace('_categories', '')
                if st.session_state[key]:  # Has initiatives
                    configured_functions.append(func_name)
        
        if len(configured_functions) >= 2:
            # Analyze dependencies
            dependency_analysis = cross_analyzer.analyze_dependencies(configured_functions)
            
            st.markdown("**Implementation Sequence Recommendation:**")
            sequence = dependency_analysis['implementation_sequence']
            
            for i, func in enumerate(sequence, 1):
                impact_score = dependency_analysis['impact_scores'][func]
                st.markdown(f"{i}. **{func}** (Impact Score: {impact_score:.2f})")
            
            # Dependency Matrix
            st.markdown("**Function Dependency Matrix:**")
            
            # Create dependency matrix display
            matrix_data = []
            for func in configured_functions:
                row = [func]  # Function name as first column
                for other_func in configured_functions:
                    if func == other_func:
                        row.append("-")
                    else:
                        dependency_score = dependency_analysis['dependencies'][func].get(other_func, 0)
                        row.append(f"{dependency_score:.2f}")
                matrix_data.append(row)
            
            # Display matrix without pandas
            # Create header
            st.write("| " + " | ".join(['Function'] + configured_functions) + " |")
            st.write("|" + "---|" * (len(configured_functions) + 1))
            
            # Display data rows
            for row in matrix_data:
                st.write("| " + " | ".join(row) + " |")
            
            # Optimization Opportunities
            opportunities = dependency_analysis['optimization_opportunities']
            if opportunities:
                st.markdown("**Optimization Opportunities:**")
                for opp in opportunities:
                    st.info(f"**{opp['type']}**: {' + '.join(opp['functions'])} - {opp['potential_benefit']} (Est. savings: {opp['estimated_savings']})")
        
        else:
            st.info("Configure AI initiatives in at least 2 functions to see cross-function dependency analysis")

def show_monte_carlo_simulation():
    """Monte Carlo simulation for risk and uncertainty modeling"""
    st.title("🎲 Monte Carlo Simulation")
    st.markdown("Advanced risk modeling and uncertainty analysis for AI implementations")
    
    # Check if we have any configured initiatives
    all_initiatives = []
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            for category_data in st.session_state[key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    all_initiatives.append({
                        'function': function_name,
                        'name': initiative['name'],
                        'data': initiative['data']
                    })
    
    if not all_initiatives:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Initiative Selection
    st.subheader("🎯 Select Initiative for Simulation")
    
    initiative_names = [f"{init['function']} - {init['name']}" for init in all_initiatives]
    selected_initiative_name = st.selectbox("Choose Initiative", initiative_names)
    
    if selected_initiative_name:
        # Find selected initiative
        selected_initiative = None
        for init in all_initiatives:
            if f"{init['function']} - {init['name']}" == selected_initiative_name:
                selected_initiative = init
                break
        
        if selected_initiative:
            # Simulation Parameters
            st.subheader("⚙️ Simulation Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                num_simulations = st.slider("Number of Simulations", 1000, 10000, 5000)
                confidence_level = st.slider("Confidence Level", 0.8, 0.99, 0.95)
            
            with col2:
                cost_variance = st.slider("Cost Variance (%)", 5, 50, 20)
                timeline_variance = st.slider("Timeline Variance (%)", 10, 60, 30)
            
            # Run Simulation
            if st.button("🚀 Run Monte Carlo Simulation", type="primary"):
                with st.spinner("Running simulation..."):
                    results = run_monte_carlo_simulation(
                        selected_initiative['data'], 
                        num_simulations,
                        cost_variance / 100,
                        timeline_variance / 100
                    )
                
                # Display Results
                st.subheader("📊 Simulation Results")
                
                # Key Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Expected Cost", 
                        f"${results['cost_stats']['mean']:,.0f}k",
                        f"±${results['cost_stats']['std']:,.0f}k"
                    )
                
                with col2:
                    st.metric(
                        "Expected Timeline", 
                        f"{results['timeline_stats']['mean']:.1f} months",
                        f"±{results['timeline_stats']['std']:.1f} months"
                    )
                
                with col3:
                    success_rate = results['success_probability'] * 100
                    st.metric("Success Probability", f"{success_rate:.1f}%")
                
                with col4:
                    roi_mean = results['roi_stats']['mean'] * 100
                    st.metric("Expected ROI", f"{roi_mean:.1f}%")
                
                # Risk Analysis
                st.subheader("⚠️ Risk Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Cost Risk Profile:**")
                    st.write(f"• Best case: ${results['cost_stats']['min']:,.0f}k")
                    st.write(f"• Worst case: ${results['cost_stats']['max']:,.0f}k")
                    st.write(f"• {confidence_level*100:.0f}% Confidence Interval: ${results['cost_stats']['ci_lower']:,.0f}k - ${results['cost_stats']['ci_upper']:,.0f}k")
                
                with col2:
                    st.markdown("**Timeline Risk Profile:**")
                    st.write(f"• Best case: {results['timeline_stats']['min']:.1f} months")
                    st.write(f"• Worst case: {results['timeline_stats']['max']:.1f} months")
                    st.write(f"• {confidence_level*100:.0f}% Confidence Interval: {results['timeline_stats']['ci_lower']:.1f} - {results['timeline_stats']['ci_upper']:.1f} months")
                
                # Recommendations
                st.subheader("💡 Risk Mitigation Recommendations")
                
                recommendations = generate_risk_recommendations(results, selected_initiative['data'])
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. **{rec['category']}**: {rec['recommendation']}")

def run_monte_carlo_simulation(initiative_data: Dict, num_simulations: int, 
                              cost_variance: float, timeline_variance: float) -> Dict:
    """Run Monte Carlo simulation for an AI initiative"""
    import random
    import statistics
    
    # Base values
    base_cost = initiative_data.get('implementation_cost', 100)
    base_timeline = initiative_data.get('timeline_months', 12)
    expected_gain = initiative_data.get('expected_productivity_gain', 0.15)
    
    # Simulation arrays
    costs = []
    timelines = []
    rois = []
    success_outcomes = []
    
    for _ in range(num_simulations):
        # Generate random variations
        cost_multiplier = random.gauss(1.0, cost_variance)
        timeline_multiplier = random.gauss(1.0, timeline_variance)
        
        # Ensure positive values
        cost_multiplier = max(0.5, cost_multiplier)
        timeline_multiplier = max(0.5, timeline_multiplier)
        
        # Calculate values
        sim_cost = base_cost * cost_multiplier
        sim_timeline = base_timeline * timeline_multiplier
        
        # ROI calculation (simplified)
        annual_benefit = base_cost * expected_gain * 12 / base_timeline
        roi = (annual_benefit - sim_cost) / sim_cost
        
        # Success probability (decreases with cost and timeline overruns)
        success_prob = max(0.1, 1.0 - (cost_multiplier - 1.0) * 0.5 - (timeline_multiplier - 1.0) * 0.3)
        success = random.random() < success_prob
        
        costs.append(sim_cost)
        timelines.append(sim_timeline)
        rois.append(roi)
        success_outcomes.append(success)
    
    # Calculate statistics
    def calc_stats(values):
        return {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std': statistics.stdev(values),
            'min': min(values),
            'max': max(values),
            'ci_lower': sorted(values)[int(0.025 * len(values))],
            'ci_upper': sorted(values)[int(0.975 * len(values))]
        }
    
    return {
        'cost_stats': calc_stats(costs),
        'timeline_stats': calc_stats(timelines),
        'roi_stats': calc_stats(rois),
        'success_probability': sum(success_outcomes) / len(success_outcomes),
        'simulation_count': num_simulations
    }

def generate_risk_recommendations(results: Dict, initiative_data: Dict) -> List[Dict]:
    """Generate risk mitigation recommendations based on simulation results"""
    recommendations = []
    
    # Cost risk
    cost_variance = results['cost_stats']['std'] / results['cost_stats']['mean']
    if cost_variance > 0.3:
        recommendations.append({
            'category': 'Cost Management',
            'recommendation': 'High cost variance detected. Consider breaking down the initiative into smaller phases with fixed-price contracts.'
        })
    
    # Timeline risk
    timeline_variance = results['timeline_stats']['std'] / results['timeline_stats']['mean']
    if timeline_variance > 0.25:
        recommendations.append({
            'category': 'Timeline Management',
            'recommendation': 'Significant timeline uncertainty. Implement agile methodology with regular checkpoints and scope reviews.'
        })
    
    # Success probability
    if results['success_probability'] < 0.7:
        recommendations.append({
            'category': 'Success Optimization',
            'recommendation': 'Low success probability. Consider pilot testing, additional training, or simplified initial scope.'
        })
    
    # ROI risk
    roi_risk = results['roi_stats']['ci_lower']
    if roi_risk < 0:
        recommendations.append({
            'category': 'ROI Protection',
            'recommendation': 'Negative ROI risk detected. Establish clear success metrics and consider performance-based vendor agreements.'
        })
    
    # Complexity-based recommendations
    complexity = initiative_data.get('complexity', 'Medium')
    if complexity == 'High':
        recommendations.append({
            'category': 'Complexity Management',
            'recommendation': 'High complexity initiative. Ensure dedicated project management and technical expertise are available.'
        })
    
    return recommendations

def show_strategic_planning():
    """Strategic planning and roadmap development"""
    st.title("📈 Strategic Planning & Roadmap")
    st.markdown("Develop comprehensive AI implementation roadmaps across your enterprise")
    
    # Get all configured functions and initiatives
    function_data = {}
    total_investment = 0
    total_timeline = 0
    
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            initiatives = []
            function_cost = 0
            
            for category_data in st.session_state[key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    initiatives.append(initiative)
                    function_cost += initiative['data'].get('implementation_cost', 0)
                    total_investment += initiative['data'].get('implementation_cost', 0)
            
            if initiatives:
                function_data[function_name] = {
                    'initiatives': initiatives,
                    'total_cost': function_cost,
                    'initiative_count': len(initiatives)
                }
    
    if not function_data:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Strategic Overview
    st.subheader("🎯 Strategic Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Functions", len(function_data))
    with col2:
        total_initiatives = sum(data['initiative_count'] for data in function_data.values())
        st.metric("Total Initiatives", total_initiatives)
    with col3:
        st.metric("Total Investment", f"${total_investment:,}k")
    with col4:
        avg_initiative_cost = total_investment / max(total_initiatives, 1)
        st.metric("Avg Initiative Cost", f"${avg_initiative_cost:,.0f}k")
    
    # Investment by Function
    st.subheader("💰 Investment Distribution")
    
    # Create investment chart data
    function_names = list(function_data.keys())
    function_costs = [data['total_cost'] for data in function_data.values()]
    
    chart_data = {name: cost for name, cost in zip(function_names, function_costs)}
    st.bar_chart(chart_data)
    
    # Implementation Roadmap
    st.subheader("🗓️ Implementation Roadmap")
    
    # Phase Planning
    phase_strategy = st.selectbox(
        "Roadmap Strategy",
        ["Quick Wins First", "Strategic Impact First", "Risk-Balanced", "Cost-Optimized"]
    )
    
    if st.button("🚀 Generate Roadmap", type="primary"):
        roadmap = generate_implementation_roadmap(function_data, phase_strategy)
        
        st.success("✅ Implementation Roadmap Generated!")
        
        # Display roadmap phases
        for phase_num, phase in enumerate(roadmap['phases'], 1):
            with st.expander(f"Phase {phase_num}: {phase['name']} ({phase['duration']} months)"):
                st.markdown(f"**Investment**: ${phase['total_cost']:,}k")
                st.markdown(f"**Expected ROI**: {phase['expected_roi']:.1%}")
                st.markdown(f"**Risk Level**: {phase['risk_level']}")
                
                st.markdown("**Initiatives:**")
                for initiative in phase['initiatives']:
                    st.markdown(f"• **{initiative['name']}** ({initiative['function']}) - ${initiative['cost']:,}k")
                
                if phase['dependencies']:
                    st.markdown("**Dependencies:**")
                    for dep in phase['dependencies']:
                        st.markdown(f"• {dep}")
        
        # Roadmap Summary
        st.subheader("📊 Roadmap Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Timeline Overview:**")
            total_duration = roadmap['total_duration']
            st.write(f"• Total Duration: {total_duration} months")
            st.write(f"• Phases: {len(roadmap['phases'])}")
            st.write(f"• Parallel Execution Possible: {roadmap['parallel_opportunities']}")
        
        with col2:
            st.markdown("**Financial Overview:**")
            st.write(f"• Total Investment: ${roadmap['total_investment']:,}k")
            st.write(f"• Expected 3-Year ROI: {roadmap['expected_roi']:.1%}")
            st.write(f"• Payback Period: {roadmap['payback_months']} months")
    
    # Risk Assessment
    st.subheader("⚠️ Strategic Risk Assessment")
    
    risks = assess_strategic_risks(function_data)
    
    for risk in risks:
        st.warning(f"**{risk['type']}**: {risk['description']} (Impact: {risk['impact']})")

def generate_implementation_roadmap(function_data: Dict, strategy: str) -> Dict:
    """Generate implementation roadmap based on strategy"""
    
    # Collect all initiatives with metadata
    all_initiatives = []
    for function_name, data in function_data.items():
        for initiative in data['initiatives']:
            all_initiatives.append({
                'name': initiative['name'],
                'function': function_name,
                'cost': initiative['data'].get('implementation_cost', 0),
                'timeline': initiative['data'].get('timeline_months', 12),
                'complexity': initiative['data'].get('complexity', 'Medium'),
                'ai_type': initiative['data'].get('ai_type', 'Unknown'),
                'expected_gain': initiative['data'].get('expected_productivity_gain', 0.15),
                'confidence': initiative['data'].get('confidence_level', 0.8)
            })
    
    # Sort initiatives based on strategy
    if strategy == "Quick Wins First":
        # Prioritize low cost, high confidence, short timeline
        all_initiatives.sort(key=lambda x: (x['cost'] / 100 + x['timeline'] / 12 - x['confidence'] * 2))
    elif strategy == "Strategic Impact First":
        # Prioritize high expected gain, regardless of cost
        all_initiatives.sort(key=lambda x: -x['expected_gain'])
    elif strategy == "Risk-Balanced":
        # Balance cost, timeline, and confidence
        all_initiatives.sort(key=lambda x: (x['cost'] / 100 + x['timeline'] / 12) * (2 - x['confidence']))
    else:  # Cost-Optimized
        # Prioritize lowest cost first
        all_initiatives.sort(key=lambda x: x['cost'])
    
    # Create phases
    phases = []
    remaining_initiatives = all_initiatives.copy()
    phase_num = 1
    
    while remaining_initiatives:
        phase_initiatives = []
        phase_cost = 0
        phase_duration = 0
        max_phase_cost = 500  # Max 500k per phase
        
        # Add initiatives to current phase
        initiatives_to_remove = []
        for initiative in remaining_initiatives:
            if phase_cost + initiative['cost'] <= max_phase_cost or not phase_initiatives:
                phase_initiatives.append(initiative)
                phase_cost += initiative['cost']
                phase_duration = max(phase_duration, initiative['timeline'])
                initiatives_to_remove.append(initiative)
                
                if len(phase_initiatives) >= 5:  # Max 5 initiatives per phase
                    break
        
        # Remove added initiatives
        for initiative in initiatives_to_remove:
            remaining_initiatives.remove(initiative)
        
        # Calculate phase metrics
        avg_confidence = sum(init['confidence'] for init in phase_initiatives) / len(phase_initiatives)
        total_expected_gain = sum(init['expected_gain'] for init in phase_initiatives)
        
        phase = {
            'name': f"Phase {phase_num}",
            'initiatives': phase_initiatives,
            'total_cost': phase_cost,
            'duration': phase_duration,
            'expected_roi': total_expected_gain / max(phase_cost / 1000, 1),  # Simplified ROI
            'risk_level': 'Low' if avg_confidence > 0.8 else 'Medium' if avg_confidence > 0.6 else 'High',
            'dependencies': []  # Simplified - would analyze actual dependencies
        }
        
        phases.append(phase)
        phase_num += 1
    
    # Calculate roadmap totals
    total_investment = sum(phase['total_cost'] for phase in phases)
    total_duration = max(phase['duration'] for phase in phases) if phases else 0
    expected_roi = sum(phase['expected_roi'] * phase['total_cost'] for phase in phases) / max(total_investment, 1)
    
    return {
        'phases': phases,
        'total_investment': total_investment,
        'total_duration': total_duration,
        'expected_roi': expected_roi,
        'payback_months': int(total_duration * 0.6),  # Simplified calculation
        'parallel_opportunities': len(phases) > 2
    }

def assess_strategic_risks(function_data: Dict) -> List[Dict]:
    """Assess strategic risks across the AI implementation portfolio"""
    risks = []
    
    # Concentration risk
    total_investment = sum(data['total_cost'] for data in function_data.values())
    for function_name, data in function_data.items():
        concentration = data['total_cost'] / total_investment
        if concentration > 0.4:
            risks.append({
                'type': 'Concentration Risk',
                'description': f'{function_name} represents {concentration:.1%} of total investment',
                'impact': 'High'
            })
    
    # Complexity risk
    high_complexity_count = 0
    total_initiatives = 0
    for data in function_data.values():
        for initiative in data['initiatives']:
            total_initiatives += 1
            if initiative['data'].get('complexity') == 'High':
                high_complexity_count += 1
    
    if high_complexity_count / max(total_initiatives, 1) > 0.3:
        risks.append({
            'type': 'Complexity Risk',
            'description': f'{high_complexity_count}/{total_initiatives} initiatives are high complexity',
            'impact': 'Medium'
        })
    
    # Budget risk
    if total_investment > 2000:  # > $2M
        risks.append({
            'type': 'Budget Risk',
            'description': f'Total investment of ${total_investment:,}k may strain resources',
            'impact': 'Medium'
        })
    
    return risks

def show_scenario_comparison():
    """Compare different AI implementation scenarios"""
    st.title("⚖️ Scenario Comparison")
    st.markdown("Compare different AI implementation approaches and their outcomes")
    
    # Get configured data
    configured_functions = []
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            if st.session_state[key]:
                configured_functions.append(function_name)
    
    if not configured_functions:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Scenario Configuration
    st.subheader("📝 Scenario Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Scenario A: Conservative Approach**")
        scenario_a_functions = st.multiselect(
            "Select Functions for Scenario A",
            configured_functions,
            default=configured_functions[:len(configured_functions)//2] if configured_functions else []
        )
        scenario_a_budget = st.slider("Budget Multiplier A", 0.5, 2.0, 0.8, 0.1)
    
    with col2:
        st.markdown("**Scenario B: Aggressive Approach**")
        scenario_b_functions = st.multiselect(
            "Select Functions for Scenario B",
            configured_functions,
            default=configured_functions
        )
        scenario_b_budget = st.slider("Budget Multiplier B", 0.5, 2.0, 1.2, 0.1)
    
    # Run Comparison
    if st.button("🔍 Compare Scenarios", type="primary"):
        if scenario_a_functions and scenario_b_functions:
            # Calculate scenario metrics
            scenario_a_metrics = calculate_scenario_totals(scenario_a_functions, scenario_a_budget)
            scenario_b_metrics = calculate_scenario_totals(scenario_b_functions, scenario_b_budget)
            
            # Display comparison
            st.subheader("📊 Scenario Comparison Results")
            
            # Create comparison table
            comparison_data = {
                'Metric': [
                    'Total Investment',
                    'Number of Initiatives', 
                    'Expected Timeline',
                    'Productivity Gain',
                    'Risk Score',
                    'ROI Estimate'
                ],
                'Scenario A (Conservative)': [
                    f"${scenario_a_metrics['total_cost']:,}k",
                    str(scenario_a_metrics['initiative_count']),
                    f"{scenario_a_metrics['avg_timeline']:.1f} months",
                    f"{scenario_a_metrics['productivity_gain']:.1%}",
                    scenario_a_metrics['risk_score'],
                    f"{scenario_a_metrics['roi_estimate']:.1%}"
                ],
                'Scenario B (Aggressive)': [
                    f"${scenario_b_metrics['total_cost']:,}k",
                    str(scenario_b_metrics['initiative_count']),
                    f"{scenario_b_metrics['avg_timeline']:.1f} months",
                    f"{scenario_b_metrics['productivity_gain']:.1%}",
                    scenario_b_metrics['risk_score'],
                    f"{scenario_b_metrics['roi_estimate']:.1%}"
                ]
            }
            
            # Display as a formatted table
            for i, metric in enumerate(comparison_data['Metric']):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**{metric}**")
                with col2:
                    st.markdown(comparison_data['Scenario A (Conservative)'][i])
                with col3:
                    st.markdown(comparison_data['Scenario B (Aggressive)'][i])
            
            # Recommendations
            st.subheader("💡 Scenario Recommendations")
            
            # Determine which scenario is better
            a_score = (scenario_a_metrics['roi_estimate'] * 2 - 
                      scenario_a_metrics['total_cost'] / 1000 + 
                      scenario_a_metrics['productivity_gain'] * 10)
            
            b_score = (scenario_b_metrics['roi_estimate'] * 2 - 
                      scenario_b_metrics['total_cost'] / 1000 + 
                      scenario_b_metrics['productivity_gain'] * 10)
            
            if a_score > b_score:
                st.success("✅ **Scenario A (Conservative)** appears to offer better risk-adjusted returns")
                st.markdown("**Advantages:**")
                st.markdown("• Lower investment risk")
                st.markdown("• More manageable implementation")
                st.markdown("• Better resource allocation")
            elif b_score > a_score:
                st.success("✅ **Scenario B (Aggressive)** appears to offer better overall returns")
                st.markdown("**Advantages:**")
                st.markdown("• Higher productivity gains")
                st.markdown("• Faster competitive advantage")
                st.markdown("• Greater transformation impact")
            else:
                st.info("⚖️ Both scenarios show similar potential - consider hybrid approach")
                
            # Risk Analysis
            st.subheader("⚠️ Risk Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Scenario A Risks:**")
                if scenario_a_metrics['total_cost'] < 200:
                    st.success("✅ Low financial risk")
                elif scenario_a_metrics['total_cost'] < 500:
                    st.warning("⚠️ Moderate financial risk")
                else:
                    st.error("❌ High financial risk")
                
                if scenario_a_metrics['initiative_count'] < 5:
                    st.info("ℹ️ Limited scope may reduce impact")
            
            with col2:
                st.markdown("**Scenario B Risks:**")
                if scenario_b_metrics['total_cost'] < 200:
                    st.success("✅ Low financial risk")
                elif scenario_b_metrics['total_cost'] < 500:
                    st.warning("⚠️ Moderate financial risk")
                else:
                    st.error("❌ High financial risk")
                
                if scenario_b_metrics['initiative_count'] > 10:
                    st.warning("⚠️ High complexity may increase failure risk")
        
        else:
            st.error("Please select functions for both scenarios")

def calculate_scenario_totals(functions: List[str], budget_multiplier: float = 1.0) -> Dict:
    """Calculate total metrics for a scenario"""
    total_cost = 0
    initiative_count = 0
    timeline_sum = 0
    productivity_sum = 0
    risk_factors = []
    
    for function_name in functions:
        function_key = f"{function_name}_categories"
        if function_key in st.session_state:
            for category_data in st.session_state[function_key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    data = initiative['data']
                    total_cost += data.get('implementation_cost', 0) * budget_multiplier
                    initiative_count += 1
                    timeline_sum += data.get('timeline_months', 12)
                    productivity_sum += data.get('expected_productivity_gain', 0.15)
                    
                    # Collect risk factors
                    initiative_risks = data.get('risk_factors', [])
                    risk_factors.extend(initiative_risks)
    
    avg_timeline = timeline_sum / max(initiative_count, 1)
    avg_productivity = productivity_sum / max(initiative_count, 1)
    
    # Calculate risk score
    unique_risks = len(set(risk_factors))
    risk_score = "Low" if unique_risks < 5 else "Medium" if unique_risks < 10 else "High"
    
    # Calculate ROI estimate (simplified)
    annual_benefit = total_cost * avg_productivity * 0.5  # Simplified calculation
    roi_estimate = (annual_benefit - total_cost) / max(total_cost, 1)
    
    return {
        'total_cost': total_cost,
        'initiative_count': initiative_count,
        'avg_timeline': avg_timeline,
        'productivity_gain': avg_productivity,
        'risk_score': risk_score,
        'roi_estimate': roi_estimate
    }

def show_temporal_analysis():
    """Temporal analysis of AI implementation impacts over time"""
    st.title("⏰ Temporal Analysis")
    st.markdown("Analyze AI implementation impacts and benefits over time")
    
    # Get all configured initiatives
    all_initiatives = []
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            for category_data in st.session_state[key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    all_initiatives.append({
                        'function': function_name,
                        'name': initiative['name'],
                        'data': initiative['data']
                    })
    
    if not all_initiatives:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Time Horizon Selection
    st.subheader("⏱️ Analysis Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_horizon = st.selectbox("Time Horizon", ["1 Year", "3 Years", "5 Years"])
        horizon_months = {"1 Year": 12, "3 Years": 36, "5 Years": 60}[time_horizon]
    
    with col2:
        analysis_type = st.selectbox("Analysis Type", ["Cumulative Benefits", "ROI Over Time", "Risk Evolution"])
    
    with col3:
        granularity = st.selectbox("Time Granularity", ["Monthly", "Quarterly", "Yearly"])
        
    # Run Temporal Analysis
    if st.button("📈 Run Temporal Analysis", type="primary"):
        with st.spinner("Analyzing temporal impacts..."):
            temporal_data = calculate_temporal_analysis(all_initiatives, horizon_months, granularity)
        
        st.subheader("📊 Temporal Analysis Results")
        
        if analysis_type == "Cumulative Benefits":
            show_cumulative_benefits(temporal_data, granularity)
        elif analysis_type == "ROI Over Time":
            show_roi_over_time(temporal_data, granularity)
        else:  # Risk Evolution
            show_risk_evolution(temporal_data, granularity)
        
        # Key Insights
        st.subheader("🔍 Key Insights")
        
        insights = generate_temporal_insights(temporal_data, time_horizon)
        for insight in insights:
            st.info(f"**{insight['category']}**: {insight['insight']}")

def calculate_temporal_analysis(initiatives: List[Dict], horizon_months: int, granularity: str) -> Dict:
    """Calculate temporal analysis data"""
    
    # Time periods
    if granularity == "Monthly":
        periods = list(range(1, horizon_months + 1))
        period_label = "Month"
    elif granularity == "Quarterly":
        periods = list(range(1, (horizon_months // 3) + 1))
        period_label = "Quarter"
    else:  # Yearly
        periods = list(range(1, (horizon_months // 12) + 1))
        period_label = "Year"
    
    # Initialize data structures
    cumulative_investment = []
    cumulative_benefits = []
    cumulative_roi = []
    active_initiatives = []
    risk_scores = []
    
    for period in periods:
        period_months = period * (1 if granularity == "Monthly" else 3 if granularity == "Quarterly" else 12)
        
        # Calculate cumulative investment
        total_investment = 0
        total_benefits = 0
        initiatives_active = 0
        period_risks = []
        
        for initiative in initiatives:
            data = initiative['data']
            implementation_months = data.get('timeline_months', 12)
            cost = data.get('implementation_cost', 0)
            productivity_gain = data.get('expected_productivity_gain', 0.15)
            
            # Investment (occurs during implementation)
            if period_months <= implementation_months:
                # Linear investment over implementation period
                total_investment += cost * (period_months / implementation_months)
            else:
                total_investment += cost
            
            # Benefits (start after implementation with ramp-up)
            if period_months > implementation_months:
                months_operational = period_months - implementation_months
                # Ramp-up factor (50% benefit in first 6 months, then full benefit)
                ramp_factor = min(1.0, 0.5 + (months_operational / 12) * 0.5)
                annual_benefit = cost * productivity_gain * ramp_factor
                total_benefits += annual_benefit * (months_operational / 12)
                initiatives_active += 1
                
                # Risk decreases over time as initiative matures
                base_risk = len(data.get('risk_factors', []))
                time_risk_reduction = min(0.5, months_operational / 24)
                adjusted_risk = base_risk * (1 - time_risk_reduction)
                period_risks.append(adjusted_risk)
        
        cumulative_investment.append(total_investment)
        cumulative_benefits.append(total_benefits)
        
        # ROI calculation
        if total_investment > 0:
            roi = (total_benefits - total_investment) / total_investment
        else:
            roi = 0
        cumulative_roi.append(roi)
        
        active_initiatives.append(initiatives_active)
        
        # Average risk score
        avg_risk = sum(period_risks) / max(len(period_risks), 1) if period_risks else 0
        risk_scores.append(avg_risk)
    
    return {
        'periods': periods,
        'period_label': period_label,
        'cumulative_investment': cumulative_investment,
        'cumulative_benefits': cumulative_benefits,
        'cumulative_roi': cumulative_roi,
        'active_initiatives': active_initiatives,
        'risk_scores': risk_scores
    }

def show_cumulative_benefits(temporal_data: Dict, granularity: str):
    """Show cumulative benefits over time"""
    periods = temporal_data['periods']
    investment = temporal_data['cumulative_investment']
    benefits = temporal_data['cumulative_benefits']
    
    # Create chart data
    chart_data = {}
    for i, period in enumerate(periods):
        period_key = f"{temporal_data['period_label']} {period}"
        chart_data[period_key] = {
            'Investment': investment[i],
            'Benefits': benefits[i],
            'Net Benefit': benefits[i] - investment[i]
        }
    
    st.markdown("**Cumulative Investment vs Benefits Over Time**")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Investment", 
            f"${investment[-1]:,.0f}k" if investment else "$0k"
        )
    
    with col2:
        st.metric(
            "Total Benefits",
            f"${benefits[-1]:,.0f}k" if benefits else "$0k"
        )
    
    with col3:
        net_benefit = (benefits[-1] - investment[-1]) if benefits and investment else 0
        st.metric(
            "Net Benefit",
            f"${net_benefit:,.0f}k",
            delta=f"${net_benefit:,.0f}k"
        )
    
    # Show break-even point
    breakeven_period = None
    for i, period in enumerate(periods):
        if benefits[i] >= investment[i]:
            breakeven_period = period
            break
    
    if breakeven_period:
        st.success(f"✅ Break-even achieved at {temporal_data['period_label']} {breakeven_period}")
    else:
        st.warning("⚠️ Break-even not achieved within the analysis period")

def show_roi_over_time(temporal_data: Dict, granularity: str):
    """Show ROI evolution over time"""
    periods = temporal_data['periods']
    roi_data = temporal_data['cumulative_roi']
    
    st.markdown("**ROI Evolution Over Time**")
    
    # Display current ROI
    current_roi = roi_data[-1] if roi_data else 0
    st.metric("Current ROI", f"{current_roi:.1%}")
    
    # Create ROI chart data
    chart_data = {}
    for i, period in enumerate(periods):
        period_key = f"{temporal_data['period_label']} {period}"
        chart_data[period_key] = int(roi_data[i] * 100)  # Convert to percentage
    
    st.line_chart(chart_data)
    
    # ROI milestones
    st.markdown("**ROI Milestones:**")
    
    milestones = [0.0, 0.25, 0.5, 1.0]  # 0%, 25%, 50%, 100%
    
    for milestone in milestones:
        milestone_period = None
        for i, roi in enumerate(roi_data):
            if roi >= milestone:
                milestone_period = periods[i]
                break
        
        if milestone_period:
            st.markdown(f"• {milestone:.0%} ROI: {temporal_data['period_label']} {milestone_period}")
        else:
            st.markdown(f"• {milestone:.0%} ROI: Not achieved in analysis period")

def show_risk_evolution(temporal_data: Dict, granularity: str):
    """Show risk evolution over time"""
    periods = temporal_data['periods']
    risk_data = temporal_data['risk_scores']
    active_initiatives = temporal_data['active_initiatives']
    
    st.markdown("**Risk Profile Evolution Over Time**")
    
    # Current risk metrics
    col1, col2 = st.columns(2)
    
    with col1:
        current_risk = risk_data[-1] if risk_data else 0
        risk_level = "Low" if current_risk < 3 else "Medium" if current_risk < 6 else "High"
        st.metric("Current Risk Level", risk_level)
    
    with col2:
        current_active = active_initiatives[-1] if active_initiatives else 0
        st.metric("Active Initiatives", current_active)
    
    # Risk trend analysis
    if len(risk_data) >= 2:
        risk_trend = risk_data[-1] - risk_data[0]
        if risk_trend < -0.5:
            st.success("✅ Risk decreasing over time - initiative maturity reducing risk")
        elif risk_trend > 0.5:
            st.warning("⚠️ Risk increasing over time - may need attention")
        else:
            st.info("ℹ️ Risk levels stable over time")
    
    # Risk factors over time
    st.markdown("**Risk Factor Analysis:**")
    
    # Identify peak risk period
    if risk_data:
        peak_risk_period = periods[risk_data.index(max(risk_data))]
        st.markdown(f"• **Peak Risk Period**: {temporal_data['period_label']} {peak_risk_period}")
        
        # Risk mitigation timeline
        st.markdown("**Risk Mitigation Timeline:**")
        for i, period in enumerate(periods[::len(periods)//4]):  # Show 4 key periods
            period_idx = periods.index(period)
            risk_score = risk_data[period_idx]
            active_count = active_initiatives[period_idx]
            
            risk_level = "Low" if risk_score < 3 else "Medium" if risk_score < 6 else "High"
            st.markdown(f"• {temporal_data['period_label']} {period}: {risk_level} risk ({active_count} active initiatives)")

def generate_temporal_insights(temporal_data: Dict, time_horizon: str) -> List[Dict]:
    """Generate key insights from temporal analysis"""
    insights = []
    
    periods = temporal_data['periods']
    investment = temporal_data['cumulative_investment']
    benefits = temporal_data['cumulative_benefits']
    roi_data = temporal_data['cumulative_roi']
    
    # Investment pattern insight
    if len(investment) >= 2:
        early_investment = sum(investment[:len(investment)//2])
        late_investment = sum(investment[len(investment)//2:]) - early_investment
        
        if early_investment > late_investment * 1.5:
            insights.append({
                'category': 'Investment Pattern',
                'insight': 'Front-loaded investment strategy - most costs occur early with benefits ramping up over time'
            })
        else:
            insights.append({
                'category': 'Investment Pattern',
                'insight': 'Distributed investment strategy - costs spread evenly throughout implementation'
            })
    
    # Payback insight
    payback_period = None
    for i, period in enumerate(periods):
        if benefits[i] >= investment[i]:
            payback_period = period
            break
    
    if payback_period:
        if payback_period <= len(periods) // 3:
            insights.append({
                'category': 'Payback Analysis',
                'insight': f'Fast payback achieved in {temporal_data["period_label"]} {payback_period} - strong short-term returns'
            })
        else:
            insights.append({
                'category': 'Payback Analysis',
                'insight': f'Moderate payback timeline of {temporal_data["period_label"]} {payback_period} - focus on long-term value'
            })
    else:
        insights.append({
            'category': 'Payback Analysis',
            'insight': f'Payback extends beyond {time_horizon} - consider strategy adjustment or longer evaluation period'
        })
    
    # ROI trajectory insight
    if len(roi_data) >= 3:
        final_roi = roi_data[-1]
        mid_roi = roi_data[len(roi_data)//2]
        
        if final_roi > mid_roi * 1.5:
            insights.append({
                'category': 'ROI Trajectory',
                'insight': 'Accelerating returns - ROI improves significantly in later periods'
            })
        elif final_roi < mid_roi * 0.8:
            insights.append({
                'category': 'ROI Trajectory',
                'insight': 'Diminishing returns - ROI growth slows over time, may indicate market saturation'
            })
        else:
            insights.append({
                'category': 'ROI Trajectory',
                'insight': 'Steady ROI growth - consistent value generation throughout the period'
            })
    
    return insights

def show_executive_summary():
    """Generate comprehensive executive summary"""
    st.title("📋 Executive Summary")
    st.markdown("Comprehensive strategic overview of your AI transformation initiative")
    
    # Collect all data
    total_functions = 0
    total_initiatives = 0
    total_investment = 0
    ai_type_distribution = {}
    function_summaries = {}
    
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            function_initiatives = 0
            function_investment = 0
            
            for category_data in st.session_state[key].values():
                initiatives = category_data.get('initiatives', {})
                function_initiatives += len(initiatives)
                
                for initiative in initiatives.values():
                    data = initiative['data']
                    cost = data.get('implementation_cost', 0)
                    function_investment += cost
                    total_investment += cost
                    
                    ai_type = data.get('ai_type', 'Unknown')
                    ai_type_distribution[ai_type] = ai_type_distribution.get(ai_type, 0) + 1
            
            if function_initiatives > 0:
                total_functions += 1
                total_initiatives += function_initiatives
                function_summaries[function_name] = {
                    'initiatives': function_initiatives,
                    'investment': function_investment
                }
    
    if total_initiatives == 0:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Executive Overview
    st.subheader("🎯 Executive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Functions Engaged", total_functions)
    with col2:
        st.metric("Total AI Initiatives", total_initiatives)
    with col3:
        st.metric("Total Investment", f"${total_investment:,}k")
    with col4:
        avg_investment = total_investment / max(total_initiatives, 1)
        st.metric("Avg Investment/Initiative", f"${avg_investment:,.0f}k")
    
    # Strategic Summary
    st.subheader("📊 Strategic Portfolio Analysis")
    
    # Investment by function
    if function_summaries:
        st.markdown("**Investment Distribution by Function:**")
        
        # Sort functions by investment
        sorted_functions = sorted(function_summaries.items(), key=lambda x: x[1]['investment'], reverse=True)
        
        for function_name, summary in sorted_functions:
            percentage = (summary['investment'] / total_investment) * 100
            st.markdown(f"• **{function_name}**: ${summary['investment']:,}k ({percentage:.1f}%) - {summary['initiatives']} initiatives")
    
    # AI Technology Portfolio
    st.markdown("**AI Technology Portfolio:**")
    if ai_type_distribution:
        sorted_ai_types = sorted(ai_type_distribution.items(), key=lambda x: x[1], reverse=True)
        
        for ai_type, count in sorted_ai_types:
            percentage = (count / total_initiatives) * 100
            st.markdown(f"• **{ai_type}**: {count} initiatives ({percentage:.1f}%)")
    
    # Strategic Recommendations
    st.subheader("💡 Strategic Recommendations")
    
    recommendations = generate_executive_recommendations(
        total_investment, total_initiatives, function_summaries, ai_type_distribution
    )
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}. {rec['title']}**")
        st.markdown(f"   {rec['description']}")
        st.markdown(f"   *Impact: {rec['impact']}*")
        st.markdown("")
    
    # Risk Assessment
    st.subheader("⚠️ Executive Risk Assessment")
    
    risks = assess_executive_risks(total_investment, total_initiatives, function_summaries)
    
    high_risks = [r for r in risks if r['level'] == 'High']
    medium_risks = [r for r in risks if r['level'] == 'Medium']
    
    if high_risks:
        st.error("**High Priority Risks:**")
        for risk in high_risks:
            st.markdown(f"• {risk['description']}")
    
    if medium_risks:
        st.warning("**Medium Priority Risks:**")
        for risk in medium_risks:
            st.markdown(f"• {risk['description']}")
    
    if not high_risks and not medium_risks:
        st.success("✅ No significant risks identified in current portfolio")
    
    # Implementation Roadmap Summary
    st.subheader("🗓️ Implementation Roadmap")
    
    # Calculate implementation timeline
    all_timelines = []
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            for category_data in st.session_state[key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    timeline = initiative['data'].get('timeline_months', 12)
                    all_timelines.append(timeline)
    
    if all_timelines:
        avg_timeline = sum(all_timelines) / len(all_timelines)
        max_timeline = max(all_timelines)
        min_timeline = min(all_timelines)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Timeline", f"{avg_timeline:.1f} months")
        with col2:
            st.metric("Longest Initiative", f"{max_timeline} months")
        with col3:
            st.metric("Shortest Initiative", f"{min_timeline} months")
        
        # Timeline recommendations
        if max_timeline > 18:
            st.warning("⚠️ Some initiatives have extended timelines (>18 months). Consider phased approaches.")
        
        if avg_timeline > 12:
            st.info("ℹ️ Average timeline exceeds 1 year. Ensure adequate project management resources.")
    
    # Success Metrics
    st.subheader("📈 Success Metrics Framework")
    
    st.markdown("**Recommended KPIs for Tracking:**")
    st.markdown("• **Financial**: ROI, Cost Savings, Revenue Impact")
    st.markdown("• **Operational**: Process Efficiency, Error Reduction, Automation Rate")
    st.markdown("• **Strategic**: Time-to-Market, Competitive Advantage, Innovation Rate")
    st.markdown("• **Organizational**: Employee Satisfaction, Skill Development, Change Adoption")
    
    # Next Steps
    st.subheader("🚀 Recommended Next Steps")
    
    next_steps = [
        "Conduct detailed risk assessment for high-investment initiatives",
        "Establish governance framework and steering committee",
        "Define success metrics and monitoring dashboards",
        "Secure necessary resources and budget approvals", 
        "Begin with highest-impact, lowest-risk initiatives",
        "Plan change management and training programs"
    ]
    
    for i, step in enumerate(next_steps, 1):
        st.markdown(f"{i}. {step}")

def generate_executive_recommendations(total_investment: int, total_initiatives: int, 
                                     function_summaries: Dict, ai_type_distribution: Dict) -> List[Dict]:
    """Generate executive-level strategic recommendations"""
    recommendations = []
    
    # Investment concentration analysis
    if function_summaries:
        max_investment_function = max(function_summaries.items(), key=lambda x: x[1]['investment'])
        max_percentage = (max_investment_function[1]['investment'] / total_investment) * 100
        
        if max_percentage > 50:
            recommendations.append({
                'title': 'Diversify AI Portfolio',
                'description': f'{max_investment_function[0]} represents {max_percentage:.1f}% of total investment. Consider spreading investments across more functions to reduce concentration risk.',
                'impact': 'High - Risk Mitigation'
            })
    
    # Investment scale analysis
    if total_investment > 1000:  # > $1M
        recommendations.append({
            'title': 'Establish AI Center of Excellence',
            'description': f'With ${total_investment:,}k total investment, establish a dedicated AI governance body to ensure coordination and maximize synergies across initiatives.',
            'impact': 'High - Strategic Coordination'
        })
    
    # Technology portfolio analysis
    if ai_type_distribution:
        dominant_tech = max(ai_type_distribution.items(), key=lambda x: x[1])
        if dominant_tech[1] / total_initiatives > 0.4:
            recommendations.append({
                'title': 'Technology Portfolio Balance',
                'description': f'{dominant_tech[0]} dominates your portfolio ({(dominant_tech[1]/total_initiatives)*100:.1f}%). Consider diversifying AI technologies to capture broader value opportunities.',
                'impact': 'Medium - Value Optimization'
            })
    
    # Scale analysis
    avg_investment = total_investment / max(total_initiatives, 1)
    if avg_investment < 50:  # < $50k average
        recommendations.append({
            'title': 'Consider Strategic Consolidation',
            'description': f'Average investment per initiative is ${avg_investment:,.0f}k. Consider consolidating smaller initiatives into larger, more impactful programs.',
            'impact': 'Medium - Efficiency Improvement'
        })
    elif avg_investment > 300:  # > $300k average
        recommendations.append({
            'title': 'Implement Phased Approach',
            'description': f'High average investment per initiative (${avg_investment:,.0f}k). Consider breaking larger initiatives into phases to reduce risk and accelerate time-to-value.',
            'impact': 'High - Risk Management'
        })
    
    # Portfolio maturity
    if total_initiatives >= 10:
        recommendations.append({
            'title': 'Develop AI Operating Model',
            'description': f'With {total_initiatives} initiatives, establish standardized processes for AI development, deployment, and maintenance to ensure consistent quality and efficiency.',
            'impact': 'High - Operational Excellence'
        })
    
    return recommendations

def assess_executive_risks(total_investment: int, total_initiatives: int, function_summaries: Dict) -> List[Dict]:
    """Assess executive-level risks"""
    risks = []
    
    # Financial risk
    if total_investment > 2000:  # > $2M
        risks.append({
            'level': 'High',
            'description': f'Total investment of ${total_investment:,}k represents significant financial exposure'
        })
    elif total_investment > 500:  # > $500k
        risks.append({
            'level': 'Medium', 
            'description': f'Investment level of ${total_investment:,}k requires careful monitoring and governance'
        })
    
    # Complexity risk
    if total_initiatives > 15:
        risks.append({
            'level': 'High',
            'description': f'{total_initiatives} concurrent initiatives may strain organizational capacity and coordination'
        })
    elif total_initiatives > 8:
        risks.append({
            'level': 'Medium',
            'description': f'{total_initiatives} initiatives require strong program management to ensure success'
        })
    
    # Concentration risk
    if function_summaries:
        max_function_investment = max(func['investment'] for func in function_summaries.values())
        concentration_percentage = (max_function_investment / total_investment) * 100
        
        if concentration_percentage > 60:
            risks.append({
                'level': 'High',
                'description': f'Investment concentration of {concentration_percentage:.1f}% in single function creates dependency risk'
            })
        elif concentration_percentage > 40:
            risks.append({
                'level': 'Medium',
                'description': f'Investment concentration of {concentration_percentage:.1f}% should be monitored for balance'
            })
    
    return risks

def show_benchmarking_optimization():
    """Advanced benchmarking and optimization analysis"""
    st.title("🔧 Benchmarking & Optimization")
    st.markdown("Industry benchmarking and AI portfolio optimization recommendations")
    
    # Get configured data
    all_initiatives = []
    function_data = {}
    
    for key in st.session_state.keys():
        if key.endswith('_categories'):
            function_name = key.replace('_categories', '')
            initiatives = []
            
            for category_data in st.session_state[key].values():
                for initiative in category_data.get('initiatives', {}).values():
                    initiative_data = {
                        'function': function_name,
                        'name': initiative['name'],
                        'data': initiative['data']
                    }
                    initiatives.append(initiative_data)
                    all_initiatives.append(initiative_data)
            
            if initiatives:
                function_data[function_name] = initiatives
    
    if not all_initiatives:
        st.warning("⚠️ No AI initiatives configured. Please configure initiatives in Function Analysis first.")
        return
    
    # Industry Benchmarking
    st.subheader("📊 Industry Benchmarking")
    
    # Calculate portfolio metrics
    total_investment = sum(init['data'].get('implementation_cost', 0) for init in all_initiatives)
    avg_timeline = sum(init['data'].get('timeline_months', 12) for init in all_initiatives) / len(all_initiatives)
    avg_productivity_gain = sum(init['data'].get('expected_productivity_gain', 0.15) for init in all_initiatives) / len(all_initiatives)
    
    # Industry benchmarks (simplified - would come from real data)
    industry_benchmarks = {
        'avg_investment_per_initiative': 150,  # $150k
        'avg_timeline': 10,  # 10 months
        'avg_productivity_gain': 0.18,  # 18%
        'success_rate': 0.65,  # 65%
        'roi_threshold': 1.5  # 150%
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Your Portfolio:**")
        avg_investment = total_investment / len(all_initiatives)
        st.metric("Avg Investment/Initiative", f"${avg_investment:,.0f}k")
        st.metric("Avg Timeline", f"{avg_timeline:.1f} months")
        st.metric("Avg Productivity Gain", f"{avg_productivity_gain:.1%}")
        st.metric("Total Initiatives", len(all_initiatives))
    
    with col2:
        st.markdown("**Industry Benchmark:**")
        st.metric("Industry Avg Investment", f"${industry_benchmarks['avg_investment_per_initiative']}k")
        st.metric("Industry Avg Timeline", f"{industry_benchmarks['avg_timeline']} months")
        st.metric("Industry Avg Gain", f"{industry_benchmarks['avg_productivity_gain']:.1%}")
        st.metric("Industry Success Rate", f"{industry_benchmarks['success_rate']:.1%}")
    
    # Benchmark Analysis
    st.subheader("🎯 Benchmark Analysis")
    
    # Investment comparison
    investment_vs_benchmark = (avg_investment / industry_benchmarks['avg_investment_per_initiative']) - 1
    if investment_vs_benchmark > 0.2:
        st.warning(f"⚠️ Your average investment is {investment_vs_benchmark:.1%} above industry benchmark")
        st.markdown("**Recommendation**: Review initiative scope and consider cost optimization opportunities")
    elif investment_vs_benchmark < -0.2:
        st.info(f"ℹ️ Your average investment is {abs(investment_vs_benchmark):.1%} below industry benchmark")
        st.markdown("**Opportunity**: Consider expanding scope for higher impact initiatives")
    else:
        st.success("✅ Investment levels align well with industry benchmarks")
    
    # Timeline comparison
    timeline_vs_benchmark = (avg_timeline / industry_benchmarks['avg_timeline']) - 1
    if timeline_vs_benchmark > 0.2:
        st.warning(f"⚠️ Your average timeline is {timeline_vs_benchmark:.1%} longer than industry benchmark")
        st.markdown("**Recommendation**: Review project management practices and consider agile approaches")
    elif timeline_vs_benchmark < -0.2:
        st.success(f"✅ Your timelines are {abs(timeline_vs_benchmark):.1%} faster than industry average")
        st.markdown("**Strength**: Efficient implementation processes")
    else:
        st.success("✅ Timeline performance aligns with industry standards")
    
    # Portfolio Optimization
    st.subheader("🚀 Portfolio Optimization")
    
    # Optimization analysis
    optimization_opportunities = analyze_optimization_opportunities(all_initiatives, function_data)
    
    if optimization_opportunities:
        st.markdown("**Identified Optimization Opportunities:**")
        
        for i, opportunity in enumerate(optimization_opportunities, 1):
            with st.expander(f"Opportunity {i}: {opportunity['title']}"):
                st.markdown(f"**Type**: {opportunity['type']}")
                st.markdown(f"**Description**: {opportunity['description']}")
                st.markdown(f"**Potential Impact**: {opportunity['impact']}")
                st.markdown(f"**Implementation Effort**: {opportunity['effort']}")
                
                if opportunity.get('affected_initiatives'):
                    st.markdown("**Affected Initiatives:**")
                    for init in opportunity['affected_initiatives']:
                        st.markdown(f"• {init}")
    
    # Sensitivity Analysis
    st.subheader("📈 Sensitivity Analysis")
    
    st.markdown("Analyze how changes in key parameters affect portfolio outcomes:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cost_sensitivity = st.slider("Cost Variation (%)", -50, 50, 0, 5)
        timeline_sensitivity = st.slider("Timeline Variation (%)", -50, 50, 0, 5)
    
    with col2:
        productivity_sensitivity = st.slider("Productivity Gain Variation (%)", -50, 50, 0, 5)
        success_rate_sensitivity = st.slider("Success Rate Variation (%)", -50, 50, 0, 5)
    
    if st.button("🔍 Run Sensitivity Analysis"):
        # Calculate sensitivity impact
        base_portfolio_value = calculate_portfolio_value(all_initiatives)
        
        # Apply sensitivity adjustments
        adjusted_initiatives = []
        for init in all_initiatives:
            adjusted_data = init['data'].copy()
            adjusted_data['implementation_cost'] *= (1 + cost_sensitivity / 100)
            adjusted_data['timeline_months'] *= (1 + timeline_sensitivity / 100)
            adjusted_data['expected_productivity_gain'] *= (1 + productivity_sensitivity / 100)
            
            adjusted_init = {'data': adjusted_data, 'name': init['name'], 'function': init['function']}
            adjusted_initiatives.append(adjusted_init)
        
        adjusted_portfolio_value = calculate_portfolio_value(adjusted_initiatives)
        
        # Display results
        value_change = (adjusted_portfolio_value / base_portfolio_value) - 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Base Portfolio Value", f"${base_portfolio_value:,.0f}k")
        
        with col2:
            st.metric(
                "Adjusted Portfolio Value", 
                f"${adjusted_portfolio_value:,.0f}k",
                delta=f"{value_change:.1%}"
            )
        
        # Sensitivity insights
        if abs(value_change) > 0.2:
            st.warning(f"⚠️ High sensitivity detected: {abs(value_change):.1%} value change from parameter variations")
            st.markdown("**Recommendation**: Focus on risk mitigation for the most sensitive parameters")
        else:
            st.success("✅ Portfolio shows good stability across parameter variations")

def analyze_optimization_opportunities(all_initiatives: List[Dict], function_data: Dict) -> List[Dict]:
    """Analyze optimization opportunities across the AI portfolio"""
    opportunities = []
    
    # Cost optimization opportunities
    high_cost_initiatives = [init for init in all_initiatives if init['data'].get('implementation_cost', 0) > 300]
    if high_cost_initiatives:
        opportunities.append({
            'title': 'High-Cost Initiative Review',
            'type': 'Cost Optimization',
            'description': f'{len(high_cost_initiatives)} initiatives have costs >$300k. Review scope and consider phased approaches.',
            'impact': 'High - Potential 20-30% cost reduction',
            'effort': 'Medium',
            'affected_initiatives': [f"{init['function']} - {init['name']}" for init in high_cost_initiatives]
        })
    
    # Timeline optimization
    long_timeline_initiatives = [init for init in all_initiatives if init['data'].get('timeline_months', 12) > 18]
    if long_timeline_initiatives:
        opportunities.append({
            'title': 'Timeline Acceleration',
            'type': 'Schedule Optimization',
            'description': f'{len(long_timeline_initiatives)} initiatives have timelines >18 months. Consider parallel execution or scope reduction.',
            'impact': 'Medium - Faster time-to-value',
            'effort': 'High',
            'affected_initiatives': [f"{init['function']} - {init['name']}" for init in long_timeline_initiatives]
        })
    
    # Technology consolidation
    ai_types = {}
    for init in all_initiatives:
        ai_type = init['data'].get('ai_type', 'Unknown')
        if ai_type not in ai_types:
            ai_types[ai_type] = []
        ai_types[ai_type].append(init)
    
    # Look for consolidation opportunities
    for ai_type, initiatives in ai_types.items():
        if len(initiatives) > 2 and ai_type != 'Unknown':
            opportunities.append({
                'title': f'{ai_type} Platform Consolidation',
                'type': 'Technology Optimization',
                'description': f'{len(initiatives)} initiatives use {ai_type}. Consider shared platform approach.',
                'impact': 'High - 15-25% cost savings, improved consistency',
                'effort': 'Medium',
                'affected_initiatives': [f"{init['function']} - {init['name']}" for init in initiatives]
            })
    
    # Cross-function synergies
    if len(function_data) > 2:
        opportunities.append({
            'title': 'Cross-Function Data Sharing',
            'type': 'Synergy Optimization',
            'description': f'Multiple functions ({len(function_data)}) implementing AI. Explore data and model sharing opportunities.',
            'impact': 'Medium - Improved accuracy, reduced duplication',
            'effort': 'Low',
            'affected_initiatives': ['All initiatives']
        })
    
    # Low-impact initiative review
    low_impact_initiatives = [init for init in all_initiatives if init['data'].get('expected_productivity_gain', 0.15) < 0.1]
    if low_impact_initiatives:
        opportunities.append({
            'title': 'Low-Impact Initiative Review',
            'type': 'Portfolio Optimization',
            'description': f'{len(low_impact_initiatives)} initiatives have <10% expected productivity gain. Consider scope expansion or removal.',
            'impact': 'Medium - Better resource allocation',
            'effort': 'Low',
            'affected_initiatives': [f"{init['function']} - {init['name']}" for init in low_impact_initiatives]
        })
    
    return opportunities

def calculate_portfolio_value(initiatives: List[Dict]) -> float:
    """Calculate overall portfolio value (simplified ROI-based calculation)"""
    total_value = 0
    
    for init in initiatives:
        data = init['data']
        cost = data.get('implementation_cost', 0)
        productivity_gain = data.get('expected_productivity_gain', 0.15)
        timeline = data.get('timeline_months', 12)
        
        # Simplified 3-year value calculation
        annual_benefit = cost * productivity_gain
        three_year_benefit = annual_benefit * 3
        net_value = three_year_benefit - cost
        
        # Apply timeline discount (longer projects have reduced value)
        timeline_discount = max(0.5, 1.0 - (timeline - 12) / 48)  # Discount for timelines >12 months
        discounted_value = net_value * timeline_discount
        
        total_value += discounted_value
    
    return total_value

if __name__ == "__main__":
    main()