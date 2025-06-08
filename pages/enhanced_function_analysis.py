import streamlit as st
import pandas as pd
from typing import Dict, List
from utils.category_manager import CategoryManager
from utils.predictive_engine import PredictiveEngine
from utils.natural_language_processor import NaturalLanguageProcessor, CrossFunctionAnalyzer
from utils.vector_database import VectorDatabase, SemanticAnalyzer
from datetime import datetime

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
        selected_industry = st.selectbox("Select Industry", list(industries.keys()), 
                                        index=list(industries.keys()).index(saved_industry) if saved_industry in industries else 0)
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
                                               value=existing_data.get('headcount', 100), step=1)
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
                min_value=0, max_value=100, value=existing_data.get('ai_proficiency', 30),
                help="Department's overall AI knowledge and skills"
            )
            
            learning_budget_allocation = st.slider(
                "L&D Budget Allocation (%)",
                min_value=0, max_value=100, value=existing_data.get('learning_budget', 15),
                help="Percentage of department budget allocated to learning"
            )
            
            training_completion_rate = st.slider(
                "Training Completion Rate (%)",
                min_value=0, max_value=100, value=existing_data.get('training_completion', 80)
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
                min_value=0, max_value=100, value=existing_data.get('change_readiness', 70),
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
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Manage Categories", "🤖 AI Initiatives", "📊 Category Analysis", "🔗 Cross-Function Dependencies"])
    
    with tab1:
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
    
    with tab2:
        st.subheader("AI Initiative Management")
        
        if not categories:
            st.warning("Please create at least one category first.")
            return
        
        # Initialize natural language processor
        nlp = NaturalLanguageProcessor()
        
        # Natural language initiative configuration
        with st.expander("🤖 Natural Language Initiative Configuration", expanded=True):
            st.markdown("**Describe your AI initiative in plain language:**")
            
            initiative_description = st.text_area(
                "Initiative Description",
                placeholder="Example: We want to automate our customer support ticket routing using AI to improve response times by analyzing incoming emails and routing them to the right department based on urgency and topic",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                category_names = list(categories.keys())
                target_category = st.selectbox("Target Category", category_names)
            
            with col2:
                if st.button("🚀 Generate AI Initiative", type="primary") and initiative_description:
                    with st.spinner("Analyzing description and generating configuration..."):
                        try:
                            # Parse the description using NLP
                            parsed_config = nlp.parse_initiative_description(
                                initiative_description, 
                                st.session_state.get('selected_industry', 'Technology'),
                                selected_function
                            )
                            
                            # Store the parsed configuration in session state for review
                            st.session_state['parsed_initiative'] = parsed_config
                            st.session_state['parsed_category'] = target_category
                            st.success("AI initiative configuration generated! Review below.")
                            
                        except Exception as e:
                            st.error(f"Error generating configuration: {str(e)}")
        
        # Display and edit parsed configuration
        if 'parsed_initiative' in st.session_state:
            st.markdown("---")
            st.subheader("📋 Review Generated Configuration")
            
            parsed_config = st.session_state['parsed_initiative']
            target_category = st.session_state.get('parsed_category', category_names[0])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Generated Configuration:**")
                edited_name = st.text_input("Initiative Name", value=parsed_config.get('name', ''))
                edited_ai_type = st.selectbox("AI Type", 
                    options=nlp.industry_ai_types.get(st.session_state.get('selected_industry', 'Technology'), []),
                    index=0 if parsed_config.get('ai_type') not in nlp.industry_ai_types.get(st.session_state.get('selected_industry', 'Technology'), []) 
                    else nlp.industry_ai_types.get(st.session_state.get('selected_industry', 'Technology'), []).index(parsed_config.get('ai_type'))
                )
                edited_investment = st.number_input("Investment ($)", value=parsed_config.get('investment', 0), min_value=0)
                edited_automation = st.slider("Automation Level (%)", 0, 100, value=int(parsed_config.get('automation_level', 0)))
                edited_productivity = st.slider("Productivity Gain (%)", 0, 100, value=int(parsed_config.get('productivity_gain', 0)))
            
            with col2:
                st.markdown("**Additional Details:**")
                edited_workforce_reduction = st.slider("Workforce Reduction (%)", 0, 50, value=int(parsed_config.get('workforce_reduction', 0)))
                edited_timeline = st.selectbox("Timeline", 
                    options=['3-6 months', '6-12 months', '12+ months'],
                    index=['3-6 months', '6-12 months', '12+ months'].index(parsed_config.get('timeline', '6-12 months'))
                )
                edited_complexity = st.selectbox("Complexity", 
                    options=['Low', 'Medium', 'High'],
                    index=['Low', 'Medium', 'High'].index(parsed_config.get('complexity', 'Medium'))
                )
                edited_description = st.text_area("Description", value=parsed_config.get('description', ''), height=100)
            
            # Show benefits and implementation steps
            st.markdown("**Key Benefits:**")
            benefits = parsed_config.get('key_benefits', [])
            if isinstance(benefits, list):
                for benefit in benefits:
                    st.markdown(f"• {benefit}")
            
            st.markdown("**Implementation Steps:**")
            steps = parsed_config.get('implementation_steps', [])
            if isinstance(steps, list):
                for i, step in enumerate(steps, 1):
                    st.markdown(f"{i}. {step}")
            
            # Improvement suggestions
            with st.expander("💡 AI-Generated Improvement Suggestions"):
                if st.button("Get Suggestions"):
                    suggestions = nlp.suggest_initiative_improvements(
                        {
                            'name': edited_name,
                            'ai_type': edited_ai_type,
                            'investment': edited_investment,
                            'automation_level': edited_automation,
                            'productivity_gain': edited_productivity
                        },
                        st.session_state.get('selected_industry', 'Technology'),
                        selected_function
                    )
                    
                    for suggestion in suggestions:
                        st.markdown(f"• {suggestion}")
            
            # Save configuration
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Initiative", type="primary"):
                    final_config = {
                        'name': edited_name,
                        'ai_type': edited_ai_type,
                        'investment': edited_investment,
                        'automation_level': edited_automation,
                        'productivity_gain': edited_productivity,
                        'workforce_reduction': edited_workforce_reduction,
                        'timeline': edited_timeline,
                        'complexity': edited_complexity,
                        'description': edited_description,
                        'key_benefits': parsed_config.get('key_benefits', []),
                        'implementation_steps': parsed_config.get('implementation_steps', [])
                    }
                    
                    initiative_id = category_manager.add_ai_initiative(
                        selected_function, target_category, edited_name, final_config
                    )
                    
                    if initiative_id:
                        st.success(f"Initiative '{edited_name}' saved successfully!")
                        
                        # Store in vector database if available
                        if db:
                            try:
                                vector_db = VectorDatabase(db)
                                vector_db.store_initiative_embedding(selected_function, initiative_id, final_config)
                            except Exception:
                                pass  # Vector DB is optional
                        
                        # Clear parsed configuration
                        del st.session_state['parsed_initiative']
                        if 'parsed_category' in st.session_state:
                            del st.session_state['parsed_category']
                        st.rerun()
                    else:
                        st.error("Failed to save initiative.")
            
            with col2:
                if st.button("🔄 Regenerate"):
                    # Clear and regenerate
                    del st.session_state['parsed_initiative']
                    st.rerun()
            
            with col3:
                if st.button("❌ Cancel"):
                    del st.session_state['parsed_initiative']
                    if 'parsed_category' in st.session_state:
                        del st.session_state['parsed_category']
                    st.rerun()
        
        st.markdown("---")
        
        # Manual initiative configuration (existing functionality)
        st.subheader("📝 Manual Initiative Configuration")
        
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
    
    with tab3:
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