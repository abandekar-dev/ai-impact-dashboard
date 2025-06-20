import streamlit as st
import pandas as pd
from typing import Dict, List
from datetime import datetime

def show_budget_resources():
    """Budget & Resource Constraints input page"""
    
    st.header("💰 Budget & Resource Constraints")
    st.markdown("**Define available capital, timeline constraints, and resource limitations**")
    
    # Initialize session state
    if 'budget_resources' not in st.session_state:
        st.session_state.budget_resources = {}
    
    st.markdown("---")
    
    # Budget Overview
    st.subheader("💵 Budget Allocation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Total Available Budget")
        
        total_ai_budget = st.number_input(
            "Total AI Implementation Budget ($)", 
            min_value=0, value=1000000, step=50000,
            help="Total budget allocated for AI initiatives"
        )
        
        annual_budget_limit = st.number_input(
            "Annual Budget Limit ($)", 
            min_value=0, value=500000, step=25000,
            help="Maximum annual spending on AI projects"
        )
        
        emergency_buffer = st.number_input(
            "Emergency Buffer (%)", 
            min_value=0.0, max_value=50.0, value=15.0, step=0.5,
            help="Percentage of budget reserved for unexpected costs"
        )
    
    with col2:
        st.markdown("#### Budget Categories")
        
        technology_budget_pct = st.slider(
            "Technology & Software (%)", 
            min_value=0, max_value=100, value=40,
            help="Percentage allocated to technology and software"
        )
        
        training_budget_pct = st.slider(
            "Training & Development (%)", 
            min_value=0, max_value=100, value=20,
            help="Percentage allocated to employee training"
        )
        
        consulting_budget_pct = st.slider(
            "Consulting & External Services (%)", 
            min_value=0, max_value=100, value=25,
            help="Percentage allocated to external consulting"
        )
        
        infrastructure_budget_pct = st.slider(
            "Infrastructure & Hardware (%)", 
            min_value=0, max_value=100, value=15,
            help="Percentage allocated to infrastructure"
        )
    
    # Budget validation
    total_allocation = technology_budget_pct + training_budget_pct + consulting_budget_pct + infrastructure_budget_pct
    if total_allocation != 100:
        st.warning(f"Budget allocation totals {total_allocation}%. Please adjust to equal 100%.")
    
    st.markdown("---")
    
    # Timeline Constraints
    st.subheader("⏰ Timeline Constraints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Project Timeline")
        
        project_start_date = st.date_input(
            "Project Start Date",
            help="When AI implementation should begin"
        )
        
        first_milestone_months = st.number_input(
            "First Milestone Timeline (months)", 
            min_value=1, max_value=24, value=6, step=1,
            help="Time to achieve first major milestone"
        )
        
        full_implementation_months = st.number_input(
            "Full Implementation Timeline (months)", 
            min_value=6, max_value=60, value=18,
            help="Time to complete full AI implementation"
        )
    
    with col2:
        st.markdown("#### Delivery Constraints")
        
        phased_rollout = st.selectbox(
            "Rollout Strategy",
            ["Single Phase", "2 Phases", "3 Phases", "4+ Phases"],
            index=1,
            help="Number of implementation phases"
        )
        
        critical_deadlines = st.text_area(
            "Critical Business Deadlines",
            height=80,
            placeholder="List any critical business deadlines that impact AI implementation timing..."
        )
        
        seasonal_constraints = st.text_area(
            "Seasonal Constraints",
            height=80,
            placeholder="Describe any seasonal business constraints (peak seasons, budget cycles, etc.)..."
        )
    
    st.markdown("---")
    
    # Human Resources
    st.subheader("👥 Human Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Internal Team")
        
        available_fte = st.number_input(
            "Available FTE for AI Projects", 
            min_value=0.0, max_value=50.0, value=5.0, step=0.5,
            help="Full-time equivalent employees available for AI work"
        )
        
        project_manager_capacity = st.number_input(
            "Project Manager Capacity (%)", 
            min_value=0, max_value=100, value=50,
            help="Percentage of PM time available for AI projects"
        )
        
        technical_leads_available = st.number_input(
            "Technical Leads Available", 
            min_value=0, max_value=10, value=2,
            help="Number of technical leads who can support AI initiatives"
        )
    
    with col2:
        st.markdown("#### Skills & Expertise")
        
        data_science_expertise = st.selectbox(
            "Data Science Expertise Level",
            ["None", "Basic", "Intermediate", "Advanced", "Expert"],
            index=2
        )
        
        ai_ml_expertise = st.selectbox(
            "AI/ML Expertise Level",
            ["None", "Basic", "Intermediate", "Advanced", "Expert"],
            index=1
        )
        
        change_management_expertise = st.selectbox(
            "Change Management Expertise",
            ["None", "Basic", "Intermediate", "Advanced", "Expert"],
            index=2
        )
    
    with col3:
        st.markdown("#### External Resources")
        
        external_consultants_budget = st.number_input(
            "External Consultants Budget ($)", 
            min_value=0, value=200000, step=10000,
            help="Budget for external consulting support"
        )
        
        training_budget_per_employee = st.number_input(
            "Training Budget per Employee ($)", 
            min_value=0, value=5000, step=500,
            help="Training budget per employee"
        )
        
        vendor_relationships = st.multiselect(
            "Existing Vendor Relationships",
            ["Microsoft", "Google", "Amazon", "IBM", "Salesforce", "Oracle", "SAP", "Other"],
            help="Select existing technology vendor relationships"
        )
    
    st.markdown("---")
    
    # Risk & Contingency
    st.subheader("⚠️ Risk & Contingency Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Financial Risk Management")
        
        cost_overrun_tolerance = st.number_input(
            "Cost Overrun Tolerance (%)", 
            min_value=0.0, max_value=50.0, value=10.0, step=0.5,
            help="Acceptable percentage of budget overrun"
        )
        
        roi_failure_threshold = st.number_input(
            "ROI Failure Threshold (%)", 
            min_value=0.0, max_value=20.0, value=5.0, step=0.5,
            help="ROI below which project should be reconsidered"
        )
        
        budget_approval_levels = st.text_area(
            "Budget Approval Process",
            height=80,
            placeholder="Describe the budget approval process and authorization levels..."
        )
    
    with col2:
        st.markdown("#### Operational Risk Management")
        
        resource_unavailability_risk = st.selectbox(
            "Resource Unavailability Risk",
            ["Low", "Medium", "High"],
            index=1,
            help="Risk of key resources becoming unavailable"
        )
        
        technology_obsolescence_risk = st.selectbox(
            "Technology Obsolescence Risk",
            ["Low", "Medium", "High"],
            index=1,
            help="Risk of chosen technology becoming obsolete"
        )
        
        contingency_plans = st.text_area(
            "Contingency Plans",
            height=80,
            placeholder="Describe backup plans for major risks..."
        )
    
    # Save budget and resources
    if st.button("💾 Save Budget & Resource Constraints", type="primary"):
        budget_data = {
            'budget_allocation': {
                'total_ai_budget': total_ai_budget,
                'annual_budget_limit': annual_budget_limit,
                'emergency_buffer': emergency_buffer,
                'technology_budget_pct': technology_budget_pct,
                'training_budget_pct': training_budget_pct,
                'consulting_budget_pct': consulting_budget_pct,
                'infrastructure_budget_pct': infrastructure_budget_pct
            },
            'timeline_constraints': {
                'project_start_date': project_start_date.isoformat(),
                'first_milestone_months': first_milestone_months,
                'full_implementation_months': full_implementation_months,
                'phased_rollout': phased_rollout,
                'critical_deadlines': critical_deadlines,
                'seasonal_constraints': seasonal_constraints
            },
            'human_resources': {
                'available_fte': available_fte,
                'project_manager_capacity': project_manager_capacity,
                'technical_leads_available': technical_leads_available,
                'data_science_expertise': data_science_expertise,
                'ai_ml_expertise': ai_ml_expertise,
                'change_management_expertise': change_management_expertise,
                'external_consultants_budget': external_consultants_budget,
                'training_budget_per_employee': training_budget_per_employee,
                'vendor_relationships': vendor_relationships
            },
            'risk_contingency': {
                'cost_overrun_tolerance': cost_overrun_tolerance,
                'roi_failure_threshold': roi_failure_threshold,
                'budget_approval_levels': budget_approval_levels,
                'resource_unavailability_risk': resource_unavailability_risk,
                'technology_obsolescence_risk': technology_obsolescence_risk,
                'contingency_plans': contingency_plans
            },
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state.budget_resources = budget_data
        st.success("Budget and resource constraints saved successfully!")
    
    # Display current constraints summary
    if 'budget_resources' in st.session_state and st.session_state.budget_resources:
        st.markdown("---")
        st.subheader("📊 Current Constraints Summary")
        
        budget_data = st.session_state.budget_resources
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'budget_allocation' in budget_data:
                budget = budget_data['budget_allocation']
                st.metric("Total AI Budget", f"${budget['total_ai_budget']:,.0f}")
                st.metric("Annual Limit", f"${budget['annual_budget_limit']:,.0f}")
        
        with col2:
            if 'timeline_constraints' in budget_data:
                timeline = budget_data['timeline_constraints']
                st.metric("Implementation Timeline", f"{timeline['full_implementation_months']} months")
                st.metric("Rollout Strategy", timeline['phased_rollout'])
        
        with col3:
            if 'human_resources' in budget_data:
                hr = budget_data['human_resources']
                st.metric("Available FTE", f"{hr['available_fte']}")
                st.metric("Technical Leads", f"{hr['technical_leads_available']}")
        
        with col4:
            if 'risk_contingency' in budget_data:
                risk = budget_data['risk_contingency']
                st.metric("Cost Overrun Tolerance", f"{risk['cost_overrun_tolerance']}%")
                st.metric("ROI Failure Threshold", f"{risk['roi_failure_threshold']}%")
        
        # Budget breakdown chart
        if 'budget_allocation' in budget_data:
            budget = budget_data['budget_allocation']
            budget_breakdown = {
                'Technology & Software': budget['technology_budget_pct'],
                'Training & Development': budget['training_budget_pct'],
                'Consulting & External': budget['consulting_budget_pct'],
                'Infrastructure & Hardware': budget['infrastructure_budget_pct']
            }
            
            import plotly.express as px
            fig = px.pie(
                values=list(budget_breakdown.values()),
                names=list(budget_breakdown.keys()),
                title="Budget Allocation by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Export budget data
        if st.button("📄 Export Budget Data"):
            import json
            budget_json = json.dumps(budget_data, indent=2, default=str)
            
            st.download_button(
                label="Download Budget & Resources Data",
                data=budget_json,
                file_name=f"budget_resources_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )