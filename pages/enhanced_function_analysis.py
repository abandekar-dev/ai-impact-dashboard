import streamlit as st
import pandas as pd
from typing import Dict, List
from utils.category_manager import CategoryManager
from utils.predictive_engine import PredictiveEngine
from datetime import datetime

def show_enhanced_function_analysis(category_manager, db=None):
    """Enhanced function analysis with categories and multiple AI initiatives"""
    
    st.header("🏢 Enhanced Function Analysis")
    st.markdown("**Configure enterprise functions with categories and multiple AI initiatives**")
    
    # Function selector with predefined options
    functions = ["HR & Talent Management", "Finance & Accounting", "Operations & Supply Chain", 
                "Sales & Marketing", "IT & Technology", "Customer Service", "Legal & Compliance", "R&D",
                "Manufacturing & Production", "Quality Assurance", "Business Development", "Strategy & Planning",
                "Risk Management", "Procurement", "Facilities Management", "Data & Analytics"]
    
    selected_function = st.selectbox("Select Enterprise Function", functions)
    
    # Initialize categories for the selected function
    category_manager.initialize_function_categories(selected_function)
    
    st.markdown("---")
    
    # Function baseline metrics (one per function)
    with st.expander("📋 Function Baseline Metrics", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            current_productivity = st.number_input("Current Productivity Index (0-100)", 
                                                 min_value=0.0, max_value=100.0, value=75.0, step=0.1)
            current_headcount = st.number_input("Current Headcount", min_value=1, value=100, step=1)
            current_revenue = st.number_input("Annual Revenue Contribution ($)", 
                                            min_value=0, value=1000000, step=10000)
        
        with col2:
            current_costs = st.number_input("Annual Operating Costs ($)", 
                                          min_value=0, value=500000, step=10000)
            current_satisfaction = st.number_input("Performance Satisfaction (0-100)", 
                                                 min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        
        if st.button("💾 Save Function Baseline"):
            baseline_data = {
                'productivity': current_productivity,
                'headcount': int(current_headcount),
                'revenue': current_revenue,
                'costs': current_costs,
                'satisfaction': current_satisfaction
            }
            st.session_state.baseline_data[selected_function] = baseline_data
            
            if db:
                db.save_function_baseline(selected_function, baseline_data)
            
            st.success("Function baseline saved!")
    
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
    tab1, tab2, tab3 = st.tabs(["📋 Manage Categories", "🤖 AI Initiatives", "📊 Category Analysis"])
    
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
        
        # Select category for initiative
        category_names = list(categories.keys())
        selected_category = st.selectbox("Select Category for AI Initiative", category_names)
        
        # Add new AI initiative
        with st.expander("➕ Create New AI Initiative", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                initiative_name = st.text_input("Initiative Name")
                ai_type = st.selectbox("AI Implementation Type", 
                                      ["Automation", "Augmentation", "Analytics", "Hybrid"])
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