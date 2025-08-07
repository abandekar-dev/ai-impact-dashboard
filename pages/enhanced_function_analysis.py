import streamlit as st
import pandas as pd
from typing import Dict, List
from utils.category_manager import CategoryManager
from utils.predictive_engine import PredictiveEngine
from datetime import datetime

def generate_ai_recommendations(assessment_data: Dict, function_name: str) -> List[Dict]:
    """Generate AI initiative recommendations based on business problem assessment"""
    
    # AI initiative templates mapped to business problems and impact areas
    ai_templates = {
        # Generative AI Templates
        "content_generation": {
            "name": "AI Content Generation Assistant",
            "ai_type": "🤖 Generative AI - Content Generation (emails, presentations, training)",
            "category": "Content & Communication",
            "complexity": "Medium",
            "timeline": "6 months",
            "estimated_roi": 180,
            "triggers": ["Content creation and documentation", "Communication and collaboration"],
            "problems": ["Manual processes are too slow and error-prone", "Knowledge management and retention problems"],
            "benefits": "Automate document creation, standardize communications, accelerate content production"
        },
        "conversation_ai": {
            "name": "Intelligent Customer Assistant",
            "ai_type": "🤖 Generative AI - Conversation / Dialogue (chatbots, assistants)",
            "category": "Customer Experience",
            "complexity": "Medium",
            "timeline": "9 months",
            "estimated_roi": 240,
            "triggers": ["Customer interaction and personalization", "Communication and collaboration"],
            "problems": ["Poor customer experience and satisfaction", "Slow response times to customer requests"],
            "benefits": "24/7 customer support, consistent service quality, reduced response times"
        },
        "document_summarization": {
            "name": "Document Intelligence System",
            "ai_type": "🤖 Generative AI - Summarization (documents, transcripts, calls)",
            "category": "Knowledge Management",
            "complexity": "Low",
            "timeline": "3 months",
            "estimated_roi": 160,
            "triggers": ["Data analysis and insights generation", "Training and knowledge sharing"],
            "problems": ["Difficulty accessing and analyzing data insights", "Knowledge management and retention problems"],
            "benefits": "Quick information extraction, automated summaries, improved knowledge accessibility"
        },
        
        # Predictive AI Templates
        "demand_forecasting": {
            "name": "Predictive Analytics Engine",
            "ai_type": "🔶 Predictive AI - Forecasting / Prediction (churn, demand, attrition)",
            "category": "Analytics & Forecasting",
            "complexity": "High",
            "timeline": "12 months",
            "estimated_roi": 320,
            "triggers": ["Predictive analytics and forecasting", "Data analysis and insights generation"],
            "problems": ["Difficulty accessing and analyzing data insights", "Inefficient resource allocation"],
            "benefits": "Accurate demand prediction, optimized inventory, reduced waste"
        },
        "recommendation_engine": {
            "name": "AI Recommendation System",
            "ai_type": "🔶 Predictive AI - Recommendation (next best action, skill path)",
            "category": "Decision Support",
            "complexity": "Medium",
            "timeline": "9 months",
            "estimated_roi": 210,
            "triggers": ["Decision support and recommendations", "Customer interaction and personalization"],
            "problems": ["Inconsistent decision-making across teams", "Poor customer experience and satisfaction"],
            "benefits": "Personalized recommendations, improved decision consistency, enhanced user experience"
        },
        "classification_system": {
            "name": "Intelligent Classification System",
            "ai_type": "🔶 Predictive AI - Classification / Tagging (documents, risks, intent)",
            "category": "Process Automation",
            "complexity": "Medium",
            "timeline": "6 months",
            "estimated_roi": 190,
            "triggers": ["Process efficiency and automation", "Quality assurance and monitoring"],
            "problems": ["Manual processes are too slow and error-prone", "Quality control and consistency issues"],
            "benefits": "Automated categorization, consistent tagging, reduced manual effort"
        },
        
        # Agentic AI Templates
        "workflow_automation": {
            "name": "Autonomous Workflow Agent",
            "ai_type": "🔸 Agentic AI - Autonomous Task Execution (multi-step workflows)",
            "category": "Process Automation",
            "complexity": "High",
            "timeline": "12 months",
            "estimated_roi": 280,
            "triggers": ["Process efficiency and automation", "Decision support and recommendations"],
            "problems": ["Manual processes are too slow and error-prone", "Complex approval and workflow processes"],
            "benefits": "End-to-end automation, reduced manual intervention, consistent process execution"
        },
        "planning_agent": {
            "name": "Strategic Planning Assistant",
            "ai_type": "🔸 Agentic AI - Goal-Oriented Planning (task decomposition)",
            "category": "Strategic Planning",
            "complexity": "High",
            "timeline": "18 months",
            "estimated_roi": 250,
            "triggers": ["Decision support and recommendations", "Process efficiency and automation"],
            "problems": ["Inconsistent decision-making across teams", "Scaling operations without proportional cost increase"],
            "benefits": "Automated task breakdown, optimized resource allocation, strategic guidance"
        },
        "monitoring_agent": {
            "name": "Proactive Monitoring System",
            "ai_type": "🔸 Agentic AI - Monitoring + Proactive Alerting (triggered actions)",
            "category": "Operations & Monitoring",
            "complexity": "Medium",
            "timeline": "9 months",
            "estimated_roi": 200,
            "triggers": ["Quality assurance and monitoring", "Risk assessment and compliance"],
            "problems": ["Lack of real-time visibility and monitoring", "Lack of proactive problem identification"],
            "benefits": "Real-time issue detection, automated responses, reduced downtime"
        },
        
        # Data AI Templates
        "data_extraction": {
            "name": "Intelligent Data Extraction",
            "ai_type": "🔹 Data AI - Data Extraction / Structuring (OCR, unstructured data)",
            "category": "Data Processing",
            "complexity": "Medium",
            "timeline": "6 months",
            "estimated_roi": 170,
            "triggers": ["Data analysis and insights generation", "Process efficiency and automation"],
            "problems": ["Manual data entry and processing", "Difficulty accessing and analyzing data insights"],
            "benefits": "Automated data capture, structured information, reduced data entry errors"
        },
        "knowledge_retrieval": {
            "name": "AI Knowledge Assistant",
            "ai_type": "🔹 Data AI - Knowledge Retention / Retrieval (memory-enabled responses)",
            "category": "Knowledge Management",
            "complexity": "Medium",
            "timeline": "9 months",
            "estimated_roi": 185,
            "triggers": ["Training and knowledge sharing", "Decision support and recommendations"],
            "problems": ["Knowledge management and retention problems", "Difficulty finding relevant information quickly"],
            "benefits": "Instant knowledge access, contextual information retrieval, improved learning"
        },
        
        # Classical ML Templates
        "computer_vision": {
            "name": "Quality Inspection System",
            "ai_type": "⚙️ Classical ML - Computer Vision (image inspection, recognition)",
            "category": "Quality Assurance",
            "complexity": "High",
            "timeline": "12 months",
            "estimated_roi": 230,
            "triggers": ["Quality assurance and monitoring", "Process efficiency and automation"],
            "problems": ["Quality control and consistency issues", "Manual processes are too slow and error-prone"],
            "benefits": "Automated quality inspection, consistent standards, defect detection"
        },
        "nlp_analysis": {
            "name": "Text Analytics Platform",
            "ai_type": "⚙️ Classical ML - Natural Language Processing (text analysis)",
            "category": "Analytics & Insights",
            "complexity": "Medium",
            "timeline": "9 months",
            "estimated_roi": 195,
            "triggers": ["Data analysis and insights generation", "Customer interaction and personalization"],
            "problems": ["Difficulty accessing and analyzing data insights", "Poor customer experience and satisfaction"],
            "benefits": "Sentiment analysis, content insights, customer intelligence"
        }
    }
    
    # Score each template based on assessment
    scored_recommendations = []
    
    for template_id, template in ai_templates.items():
        score = 0
        reasoning_parts = []
        
        # Score based on impact area match
        if assessment_data['impact_area'] in template['triggers']:
            score += 40
            reasoning_parts.append(f"Directly addresses your focus on {assessment_data['impact_area'].lower()}")
        
        # Score based on primary challenge match
        if assessment_data['primary_challenge'] in template['problems']:
            score += 30
            reasoning_parts.append(f"Solves your primary challenge: {assessment_data['primary_challenge'].lower()}")
        
        # Score based on pain points overlap
        pain_point_matches = 0
        for pain_point in assessment_data['pain_points']:
            if any(keyword in pain_point.lower() for keyword in template['name'].lower().split()):
                pain_point_matches += 1
        if pain_point_matches > 0:
            score += min(pain_point_matches * 10, 20)
            reasoning_parts.append(f"Addresses {pain_point_matches} of your pain points")
        
        # Adjust score based on readiness level
        readiness_complexity_match = {
            "Just starting - need simple, low-risk solutions": {"Low": 20, "Medium": 5, "High": -10},
            "Some experience - ready for moderate complexity": {"Low": 10, "Medium": 20, "High": 5},
            "Experienced - can handle advanced implementations": {"Low": 5, "Medium": 15, "High": 20},
            "AI-native - looking for cutting-edge solutions": {"Low": 0, "Medium": 10, "High": 25}
        }
        
        if assessment_data['readiness_level'] in readiness_complexity_match:
            complexity_bonus = readiness_complexity_match[assessment_data['readiness_level']].get(template['complexity'], 0)
            score += complexity_bonus
            if complexity_bonus > 0:
                reasoning_parts.append(f"Matches your {assessment_data['readiness_level'].lower()}")
        
        # Create recommendation object
        if score > 0:  # Only include relevant recommendations
            recommendation = {
                'name': template['name'],
                'ai_type': template['ai_type'],
                'category': template['category'],
                'complexity': template['complexity'],
                'timeline': template['timeline'],
                'estimated_roi': template['estimated_roi'],
                'match_score': min(score, 100),
                'reasoning': '; '.join(reasoning_parts) if reasoning_parts else "General fit for your requirements",
                'benefits': template['benefits'],
                'approach': f"Implement as {template['complexity'].lower()} complexity solution over {template['timeline']}"
            }
            scored_recommendations.append(recommendation)
    
    # Sort by score and return top 5
    scored_recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return scored_recommendations[:5]

def show_enhanced_function_analysis(category_manager, db=None):
    """Enhanced function analysis with categories and multiple AI initiatives"""
    
    st.header("🏢 Enhanced Function Analysis")
    st.markdown("**Configure enterprise functions with categories and multiple AI initiatives**")
    
    # Industry selector
    industries = {
        "Technology": ["IT & Technology", "Data & Analytics", "Product Development", "Customer Support", 
                      "Sales & Marketing", "HR & Talent Management", "Finance & Accounting", "Legal & Compliance"],
        "Retail": ["Store Operations", "E-commerce", "Supply Chain & Logistics", "Merchandising", 
                  "Customer Experience", "Marketing & Promotions", "Finance & Accounting", "HR & Talent Management"],
        "Manufacturing": ["Production & Assembly", "Quality Control", "Plant Operations", "Supply Chain Management", 
                         "R&D & Engineering", "Maintenance & Facilities", "Safety & Compliance", "Finance & Accounting"],
        "Healthcare": ["Patient Care", "Clinical Operations", "Medical Records", "Pharmacy", "Laboratory Services", 
                      "Administrative Services", "Finance & Billing", "Compliance & Risk Management"],
        "Financial Services": ["Investment Management", "Loan Processing", "Risk Assessment", "Customer Service", 
                              "Compliance & Regulatory", "Trading Operations", "Wealth Management", "Operations & Technology"],
        "Life Sciences": ["R&D & Discovery", "Clinical Trials", "Regulatory Affairs", "Manufacturing & Production", 
                         "Quality Assurance", "Medical Affairs", "Commercial Operations", "Supply Chain"],
        "Energy & Utilities": ["Operations & Maintenance", "Grid Management", "Customer Service", "Safety & Compliance", 
                              "Asset Management", "Trading & Risk", "Environmental Management", "Engineering"],
        "Education": ["Academic Affairs", "Student Services", "Research & Development", "Administration", 
                     "IT & Technology", "Facilities Management", "Finance & Budgeting", "Human Resources"],
        "Government": ["Public Services", "Policy Development", "Regulatory Oversight", "Citizen Services", 
                      "Administrative Operations", "Finance & Budgeting", "IT & Digital Services", "Human Resources"]
    }
    
    # Load saved industry if available
    saved_industry = st.session_state.get('selected_industry', 'Technology')
    
    col1, col2 = st.columns([1, 2])
    with col1:
        industry_keys = list(industries.keys())
        default_index = industry_keys.index(saved_industry) if saved_industry and saved_industry in industry_keys else 0
        selected_industry = st.selectbox("Select Industry", industry_keys, index=default_index)
        st.session_state.selected_industry = selected_industry
    
    with col2:
        st.info(f"Functions customized for {selected_industry} industry")
    
    # Get industry-specific functions
    functions = industries[selected_industry]
    
    selected_function = st.selectbox("Select Enterprise Function", functions)
    
    # Initialize categories for the selected function
    category_manager.initialize_function_categories(selected_function)
    
    st.markdown("---")
    
    # Function baseline metrics (one per function)
    with st.expander("📋 Function Baseline Metrics", expanded=True):
        
        # Load existing data if available
        existing_data = st.session_state.baseline_data.get(selected_function, {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_productivity = st.number_input("Current Productivity Index (0-100)", 
                                                 min_value=0.0, max_value=100.0, 
                                                 value=existing_data.get('productivity', 75.0), step=0.1)
            current_headcount = st.number_input("Current Headcount", min_value=1, 
                                               value=int(existing_data.get('headcount', 100)), step=1)
            current_revenue = st.number_input("Annual Revenue Contribution ($)", 
                                            min_value=0.0, value=float(existing_data.get('revenue', 1000000)), step=10000.0)
        
        with col2:
            current_costs = st.number_input("Annual Operating Costs ($)", 
                                          min_value=0.0, value=float(existing_data.get('costs', 500000)), step=10000.0)
            current_satisfaction = st.number_input("Performance Satisfaction (0-100)", 
                                                 min_value=0.0, max_value=100.0, 
                                                 value=existing_data.get('satisfaction', 80.0), step=0.1)
        
        # Learning & Development Profile
        st.markdown("#### 🎓 Learning & Development Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_ai_proficiency = st.slider(
                "Current AI Proficiency Level (%)",
                min_value=0, max_value=100, value=int(existing_data.get('ai_proficiency', 30)),
                help="Department's overall AI knowledge and skills"
            )
            
            learning_budget_allocation = st.slider(
                "L&D Budget Allocation (%)",
                min_value=0, max_value=100, value=int(existing_data.get('learning_budget', 15)),
                help="Percentage of department budget allocated to learning"
            )
            
            training_completion_rate = st.slider(
                "Training Completion Rate (%)",
                min_value=0, max_value=100, value=int(existing_data.get('training_completion', 80))
            )
        
        with col2:
            preferred_learning_formats = st.multiselect(
                "Preferred Learning Formats",
                ["Self-paced Online", "Live Virtual Sessions", "In-person Workshops", 
                 "Hands-on Labs", "Mentorship Programs", "Micro-learning", 
                 "Project-based Learning", "Peer Learning Groups"],
                default=existing_data.get('preferred_formats', ["Self-paced Online", "Live Virtual Sessions"])
            )
            
            time_options = ["Limited (1-2 hours/week)", "Moderate (3-5 hours/week)", "Flexible (6+ hours/week)"]
            existing_time = existing_data.get('time_availability', "Moderate (3-5 hours/week)")
            time_index = time_options.index(existing_time) if existing_time in time_options else 1
            
            learning_time_availability = st.selectbox(
                "Time Availability for Learning",
                time_options,
                index=time_index
            )
            
            change_readiness_score = st.slider(
                "Change Readiness Score (%)",
                min_value=0, max_value=100, value=int(existing_data.get('change_readiness', 70)),
                help="Department's openness to adopting new technologies"
            )

        # Auto-save data as user inputs it
        baseline_data = {
            'productivity': current_productivity,
            'headcount': int(current_headcount),
            'revenue': current_revenue,
            'costs': current_costs,
            'satisfaction': current_satisfaction,
            # Learning & Development data
            'ai_proficiency': current_ai_proficiency,
            'learning_budget': learning_budget_allocation,
            'training_completion': training_completion_rate,
            'preferred_formats': preferred_learning_formats,
            'time_availability': learning_time_availability,
            'change_readiness': change_readiness_score
        }
        
        # Always save to session state immediately
        st.session_state.baseline_data[selected_function] = baseline_data
        
        # Save button for explicit confirmation
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 Save Function Baseline"):
                success_db = False
                
                if db:
                    try:
                        db.save_function_baseline(selected_function, baseline_data)
                        success_db = True
                    except Exception as e:
                        st.warning(f"Database save failed, but data is preserved locally")
                
                if success_db:
                    st.success("Function baseline saved to database!")
                else:
                    st.success("Function baseline saved locally!")
        
        with col2:
            if selected_function in st.session_state.baseline_data:
                st.info(f"✓ Data for {selected_function} is preserved in your session")
    
    st.markdown("---")
    
    # Categories and AI Initiatives Management
    st.subheader("📂 Categories & AI Initiatives")
    
    categories = category_manager.get_categories(selected_function)
    
    # Function summary
    function_summary = category_manager.get_function_summary(selected_function)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Categories", function_summary['total_categories'])
    with col2:
        st.metric("Total AI Initiatives", function_summary['total_initiatives'])
    with col3:
        st.metric("Total Investment", f"${function_summary['total_investment']:,.0f}")
    with col4:
        ai_types = function_summary['ai_type_distribution']
        if ai_types:
            most_common = max(ai_types.items(), key=lambda x: x[1])
            st.metric("Most Common AI Type", most_common[0])
        else:
            st.metric("Most Common AI Type", "None")
    
    # Category management
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Business Problem Assessment", "📋 Manage Categories", "🤖 AI Initiatives", "📊 Category Analysis"])
    
    with tab1:
        st.subheader("🎯 Business Problem Assessment")
        st.markdown("**Answer these questions to get personalized AI initiative recommendations**")
        
        # Business problem assessment form
        with st.form("business_problem_assessment"):
            st.markdown("#### 📋 Business Challenge Analysis")
            
            # Question 1: Primary business challenge
            q1 = st.selectbox(
                "1. What is your primary business challenge in this function?",
                [
                    "Select a challenge...",
                    "Manual processes are too slow and error-prone",
                    "Inconsistent decision-making across teams",
                    "Poor customer experience and satisfaction",
                    "High operational costs and resource waste",
                    "Difficulty accessing and analyzing data insights",
                    "Compliance and risk management issues",
                    "Scaling operations without proportional cost increase",
                    "Lack of real-time visibility and monitoring",
                    "Knowledge management and retention problems",
                    "Quality control and consistency issues"
                ],
                help="Select the most critical business problem your organization faces"
            )
            
            # Question 2: Impact area
            q2 = st.selectbox(
                "2. Which area would benefit most from improvement?",
                [
                    "Select an area...",
                    "Process efficiency and automation",
                    "Data analysis and insights generation",
                    "Customer interaction and personalization",
                    "Content creation and documentation",
                    "Predictive analytics and forecasting",
                    "Quality assurance and monitoring",
                    "Decision support and recommendations",
                    "Communication and collaboration",
                    "Training and knowledge sharing",
                    "Risk assessment and compliance"
                ],
                help="Choose the functional area where AI could have the biggest impact"
            )
            
            # Question 3: Current pain points
            q3 = st.multiselect(
                "3. What are your biggest operational pain points? (Select all that apply)",
                [
                    "Too much time spent on repetitive tasks",
                    "Inconsistent results and quality",
                    "Difficulty finding relevant information quickly",
                    "Poor coordination between teams",
                    "Manual data entry and processing",
                    "Slow response times to customer requests",
                    "Lack of proactive problem identification",
                    "Inefficient resource allocation",
                    "Complex approval and workflow processes",
                    "Limited real-time performance visibility"
                ],
                help="Select all pain points that apply to your current operations"
            )
            
            # Question 4: Success metrics
            q4 = st.selectbox(
                "4. What success metric matters most to your organization?",
                [
                    "Select a metric...",
                    "Reducing processing time and cycle time",
                    "Improving accuracy and reducing errors",
                    "Increasing customer satisfaction scores",
                    "Lowering operational costs",
                    "Generating more revenue per employee",
                    "Improving compliance and risk scores",
                    "Enhancing employee productivity",
                    "Accelerating decision-making speed",
                    "Improving data quality and insights",
                    "Increasing automation coverage"
                ],
                help="Choose the key performance indicator you want to improve"
            )
            
            # Question 5: Implementation readiness
            q5 = st.selectbox(
                "5. How would you describe your organization's AI readiness?",
                [
                    "Select readiness level...",
                    "Just starting - need simple, low-risk solutions",
                    "Some experience - ready for moderate complexity",
                    "Experienced - can handle advanced implementations",
                    "AI-native - looking for cutting-edge solutions"
                ],
                help="Assess your team's current AI knowledge and implementation capability"
            )
            
            # Additional context
            additional_context = st.text_area(
                "📝 Additional Context (Optional)",
                placeholder="Describe any specific requirements, constraints, or goals...",
                help="Provide any additional context that might help us recommend the best AI initiatives"
            )
            
            submitted = st.form_submit_button("🔍 Get AI Initiative Recommendations", type="primary")
            
            if submitted and q1 != "Select a challenge..." and q2 != "Select an area...":
                # Store assessment data
                assessment_data = {
                    'primary_challenge': q1,
                    'impact_area': q2,
                    'pain_points': q3,
                    'success_metric': q4,
                    'readiness_level': q5,
                    'additional_context': additional_context,
                    'timestamp': datetime.now()
                }
                
                # Store in session state
                if 'business_assessments' not in st.session_state:
                    st.session_state.business_assessments = {}
                st.session_state.business_assessments[selected_function] = assessment_data
                
                # Generate recommendations
                recommendations = generate_ai_recommendations(assessment_data, selected_function)
                
                # Display recommendations
                st.markdown("---")
                st.subheader("🎯 Recommended AI Initiatives")
                st.success(f"Based on your assessment, here are the top AI initiatives for {selected_function}:")
                
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"🥇 Recommendation {i}: {rec['name']}", expanded=i==1):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**AI Type:** {rec['ai_type']}")
                            st.markdown(f"**Why this fits:** {rec['reasoning']}")
                            st.markdown(f"**Expected Benefits:** {rec['benefits']}")
                            st.markdown(f"**Implementation Approach:** {rec['approach']}")
                        
                        with col2:
                            st.metric("Match Score", f"{rec['match_score']}%")
                            st.metric("Estimated ROI", f"{rec['estimated_roi']}%")
                            st.metric("Complexity", rec['complexity'])
                            st.metric("Timeline", rec['timeline'])
                        
                        if st.button(f"📝 Create Initiative from Recommendation {i}", key=f"create_from_rec_{i}"):
                            # Auto-populate the AI initiative form
                            st.session_state.auto_populate_initiative = rec
                            st.session_state.selected_tab = "🤖 AI Initiatives"
                            st.success(f"Ready to create '{rec['name']}' - switch to AI Initiatives tab!")
                
                # Quick action buttons
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📋 Create Category for Top Recommendation"):
                        top_rec = recommendations[0]
                        category_name = f"{top_rec['category']}"
                        if category_manager.add_category(selected_function, category_name, f"Auto-created for {top_rec['name']}"):
                            st.success(f"Category '{category_name}' created!")
                        else:
                            st.info("Category already exists or similar category found")
                
                with col2:
                    if st.button("📊 View Assessment Summary"):
                        st.session_state.show_assessment_summary = True
                
                with col3:
                    if st.button("🔄 Retake Assessment"):
                        if selected_function in st.session_state.business_assessments:
                            del st.session_state.business_assessments[selected_function]
                        st.rerun()
            
            elif submitted:
                st.warning("Please answer at least the first two questions to get recommendations.")
        
        # Show previous assessment if exists
        if selected_function in st.session_state.get('business_assessments', {}):
            with st.expander("📋 Previous Assessment Results", expanded=False):
                prev_assessment = st.session_state.business_assessments[selected_function]
                st.write(f"**Assessment Date:** {prev_assessment['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Primary Challenge:** {prev_assessment['primary_challenge']}")
                st.write(f"**Impact Area:** {prev_assessment['impact_area']}")
                st.write(f"**Success Metric:** {prev_assessment['success_metric']}")
                if prev_assessment['pain_points']:
                    st.write(f"**Pain Points:** {', '.join(prev_assessment['pain_points'])}")

    with tab2:
        st.subheader("Category Management")
        
        # Add new category
        with st.expander("➕ Add New Category"):
            new_category_name = st.text_input("Category Name")
            new_category_desc = st.text_area("Category Description (optional)")
            
            if st.button("Create Category") and new_category_name:
                if category_manager.add_category(selected_function, new_category_name, new_category_desc):
                    st.success(f"Category '{new_category_name}' created!")
                    st.rerun()
                else:
                    st.error("Category already exists or creation failed.")
        
        # Display existing categories
        st.markdown("#### Current Categories")
        for category_name, category_data in categories.items():
            with st.expander(f"📁 {category_name}"):
                st.write(f"**Description:** {category_data.get('description', 'No description')}")
                
                initiatives = category_data.get('ai_initiatives', {})
                st.write(f"**AI Initiatives:** {len(initiatives)}")
                
                if initiatives:
                    for init_id, init_data in initiatives.items():
                        st.write(f"• {init_data.get('name', 'Unnamed Initiative')} ({init_data.get('ai_type', 'Unknown')})")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📊 View Details", key=f"details_{category_name}"):
                        st.session_state[f'show_category_details_{category_name}'] = True
                
                with col2:
                    if st.button(f"🗑️ Delete Category", key=f"delete_{category_name}"):
                        if category_manager.remove_category(selected_function, category_name):
                            st.success(f"Category '{category_name}' deleted!")
                            st.rerun()
    
    with tab3:
        st.subheader("AI Initiative Management")
        
        if not categories:
            st.warning("Please create at least one category first.")
            return
        
        # Select category for initiative
        category_names = list(categories.keys())
        selected_category = st.selectbox("Select Category for AI Initiative", category_names)
        
        # Add new AI initiative
        with st.expander("➕ Create New AI Initiative", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                initiative_name = st.text_input("Initiative Name")
                ai_type = st.selectbox("AI Implementation Type", [
                    "🤖 Generative AI - Summarization (documents, transcripts, calls)",
                    "🤖 Generative AI - Content Generation (emails, presentations, training)",
                    "🤖 Generative AI - Conversation / Dialogue (chatbots, assistants)",
                    "🔶 Predictive AI - Forecasting / Prediction (churn, demand, attrition)",
                    "🔶 Predictive AI - Recommendation (next best action, skill path)",
                    "🔶 Predictive AI - Classification / Tagging (documents, risks, intent)",
                    "🔶 Predictive AI - Sentiment & Emotion Analysis",
                    "🔸 Agentic AI - Autonomous Task Execution (multi-step workflows)",
                    "🔸 Agentic AI - Goal-Oriented Planning (task decomposition)",
                    "🔸 Agentic AI - Reasoning Across Contexts (decision chaining)",
                    "🔸 Agentic AI - Multi-Agent Collaboration (coordination)",
                    "🔸 Agentic AI - System Orchestration / Tool Use (APIs, apps)",
                    "🔸 Agentic AI - Monitoring + Proactive Alerting (triggered actions)",
                    "🔹 Data AI - Data Extraction / Structuring (OCR, unstructured data)",
                    "🔹 Data AI - Knowledge Retention / Retrieval (memory-enabled responses)",
                    "🔹 Data AI - AutoML & Pattern Discovery (insight generation)",
                    "⚙️ Classical ML - Regression and Time Series Forecasting",
                    "⚙️ Classical ML - Classification and Clustering (segmentation, fraud)",
                    "⚙️ Classical ML - Computer Vision (image inspection, recognition)",
                    "⚙️ Classical ML - Natural Language Processing (text analysis)",
                    "⚙️ Classical ML - Deep Neural Networks (pattern recognition)"
                ])
                implementation_complexity = st.selectbox("Implementation Complexity", 
                                                        ["Low", "Medium", "High"])
                investment_amount = st.number_input("Investment Amount ($)", 
                                                  min_value=0, value=50000, step=5000)
                implementation_timeline = st.selectbox("Implementation Timeline", 
                                                     ["3 months", "6 months", "12 months", "18 months", "24 months"])
            
            with col2:
                change_management = st.selectbox("Change Management Approach", 
                                               ["Gradual", "Phased", "Big Bang"])
                automation_level = st.slider("Automation Level (%)", 0, 100, 50)
                accuracy_improvement = st.slider("Expected Accuracy Improvement (%)", 0, 100, 25)
                speed_improvement = st.slider("Expected Speed Improvement (%)", 0, 100, 40)
                workforce_reduction = st.slider("Workforce Reduction (%)", 0, 50, 10)
            
            # Advanced parameters - using markdown header instead of nested expander
            st.markdown("#### 🔧 Advanced Risk & Impact Parameters")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                technical_risk = st.slider("Technical Risk", 0, 100, 30)
                adoption_risk = st.slider("Adoption Risk", 0, 100, 40)
                integration_risk = st.slider("Integration Risk", 0, 100, 35)
            
            with col2:
                regulatory_risk = st.slider("Regulatory Risk", 0, 100, 25)
                competitive_risk = st.slider("Competitive Risk", 0, 100, 20)
                data_risk = st.slider("Data Quality Risk", 0, 100, 30)
            
            with col3:
                upskilling_required = st.slider("Upskilling Required (%)", 0, 100, 60)
                new_roles_created = st.slider("New Roles Created (%)", 0, 30, 5)
            
            if st.button("🚀 Create AI Initiative", type="primary") and initiative_name:
                initiative_data = {
                    'ai_type': ai_type,
                    'complexity': implementation_complexity,
                    'investment': investment_amount,
                    'timeline': implementation_timeline,
                    'change_management': change_management,
                    'automation_level': automation_level,
                    'accuracy_improvement': accuracy_improvement,
                    'speed_improvement': speed_improvement,
                    'workforce_reduction': workforce_reduction,
                    'upskilling_required': upskilling_required,
                    'new_roles_created': new_roles_created,
                    'technical_risk': technical_risk,
                    'adoption_risk': adoption_risk,
                    'integration_risk': integration_risk,
                    'regulatory_risk': regulatory_risk,
                    'competitive_risk': competitive_risk,
                    'data_risk': data_risk
                }
                
                initiative_id = category_manager.add_ai_initiative(
                    selected_function, selected_category, initiative_name, initiative_data
                )
                
                if initiative_id:
                    st.success(f"AI Initiative '{initiative_name}' created in category '{selected_category}'!")
                    
                    # Run prediction for this initiative if baseline exists
                    if selected_function in st.session_state.baseline_data:
                        baseline_data = st.session_state.baseline_data[selected_function]
                        engine = PredictiveEngine()
                        predictions = engine.predict_impact(baseline_data, initiative_data)
                        
                        # Store prediction in initiative data
                        initiative_data['predictions'] = predictions
                        initiative_data['predicted_roi'] = predictions.get('roi', 0)
                        
                        category_manager.update_ai_initiative(
                            selected_function, selected_category, initiative_id, initiative_data
                        )
                        
                        st.success("Predictions generated and saved!")
                    
                    st.rerun()
                else:
                    st.error("Failed to create AI initiative.")
        
        # Display existing initiatives in selected category
        if selected_category:
            st.markdown(f"#### AI Initiatives in '{selected_category}'")
            initiatives = category_manager.get_ai_initiatives(selected_function, selected_category)
            
            if initiatives:
                for init_id, init_data in initiatives.items():
                    with st.expander(f"🤖 {init_data.get('name', 'Unnamed Initiative')}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Type:** {init_data.get('ai_type', 'Unknown')}")
                            st.write(f"**Investment:** ${init_data.get('investment', 0):,.0f}")
                            st.write(f"**Timeline:** {init_data.get('timeline', 'Unknown')}")
                        
                        with col2:
                            st.write(f"**Automation Level:** {init_data.get('automation_level', 0)}%")
                            st.write(f"**Workforce Reduction:** {init_data.get('workforce_reduction', 0)}%")
                            st.write(f"**Complexity:** {init_data.get('complexity', 'Unknown')}")
                        
                        with col3:
                            if 'predictions' in init_data:
                                pred = init_data['predictions']
                                st.write(f"**Predicted ROI:** {pred.get('roi', 0):.1f}%")
                                st.write(f"**Value Generated:** ${pred.get('value_generated', 0):,.0f}")
                                st.write(f"**Payback Period:** {pred.get('payback_period', 0):.1f} months")
                            else:
                                st.write("**Predictions:** Not generated")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"🔄 Regenerate Predictions", key=f"regen_{init_id}"):
                                if selected_function in st.session_state.baseline_data:
                                    baseline_data = st.session_state.baseline_data[selected_function]
                                    engine = PredictiveEngine()
                                    predictions = engine.predict_impact(baseline_data, init_data)
                                    
                                    init_data['predictions'] = predictions
                                    init_data['predicted_roi'] = predictions.get('roi', 0)
                                    
                                    category_manager.update_ai_initiative(
                                        selected_function, selected_category, init_id, init_data
                                    )
                                    st.success("Predictions updated!")
                                    st.rerun()
                        
                        with col2:
                            if st.button(f"📊 View Details", key=f"view_{init_id}"):
                                st.session_state[f'show_initiative_details_{init_id}'] = True
                        
                        with col3:
                            if st.button(f"🗑️ Delete", key=f"del_{init_id}"):
                                if category_manager.remove_ai_initiative(selected_function, selected_category, init_id):
                                    st.success("Initiative deleted!")
                                    st.rerun()
            else:
                st.info(f"No AI initiatives in '{selected_category}' yet.")
    
    with tab4:
        st.subheader("Category Analysis & Comparison")
        
        if not categories:
            st.warning("No categories configured yet.")
            return
        
        # Category comparison
        comparison_data = []
        for category_name in categories.keys():
            totals = category_manager.calculate_category_totals(selected_function, category_name)
            comparison_data.append({
                'Category': category_name,
                'AI Initiatives': totals['total_initiatives'],
                'Total Investment': f"${totals['total_investment']:,.0f}",
                'Avg Automation Level': f"{totals['avg_automation_level']:.1f}%",
                'Expected ROI': f"{totals['avg_expected_roi']:.1f}%",
                'Workforce Impact': f"{totals['total_workforce_impact']:.1f}%"
            })
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            # Investment distribution chart
            if len(comparison_data) > 1:
                import plotly.express as px
                
                investment_data = []
                for row in comparison_data:
                    investment_str = row['Total Investment'].replace('$', '').replace(',', '')
                    investment_data.append({
                        'Category': row['Category'],
                        'Investment': float(investment_str)
                    })
                
                fig = px.pie(investment_data, values='Investment', names='Category',
                           title="Investment Distribution by Category")
                st.plotly_chart(fig, use_container_width=True)
        
        # Export function data
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export Function Data"):
                export_data = category_manager.export_function_data(selected_function)
                
                import json
                export_json = json.dumps(export_data, indent=2, default=str)
                
                st.download_button(
                    label="Download Function Export",
                    data=export_json,
                    file_name=f"function_export_{selected_function}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Run All Predictions"):
                if selected_function in st.session_state.baseline_data:
                    baseline_data = st.session_state.baseline_data[selected_function]
                    engine = PredictiveEngine()
                    
                    updated_count = 0
                    for category_name, category_data in categories.items():
                        for init_id, init_data in category_data.get('ai_initiatives', {}).items():
                            predictions = engine.predict_impact(baseline_data, init_data)
                            init_data['predictions'] = predictions
                            init_data['predicted_roi'] = predictions.get('roi', 0)
                            
                            category_manager.update_ai_initiative(
                                selected_function, category_name, init_id, init_data
                            )
                            updated_count += 1
                    
                    st.success(f"Updated predictions for {updated_count} initiatives!")
                    st.rerun()
                else:
                    st.error("Please save function baseline first.")