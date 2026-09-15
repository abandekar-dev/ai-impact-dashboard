import streamlit as st
import pandas as pd
from typing import Dict, List
from datetime import datetime

def show_corporate_objectives():
    """Corporate Objectives & KPIs input page"""
    
    st.header("🎯 Corporate Objectives & KPIs")
    st.markdown("**Define strategic goals and success metrics for AI implementation**")
    
    # Initialize session state for corporate objectives
    if 'corporate_objectives' not in st.session_state:
        st.session_state.corporate_objectives = {}
    
    st.markdown("---")
    
    # Strategic Objectives
    st.subheader("📈 Strategic Objectives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Primary Business Goals")
        
        revenue_growth_target = st.number_input(
            "Revenue Growth Target (%)", 
            min_value=0.0, max_value=100.0, value=15.0, step=0.1,
            help="Target annual revenue growth from AI initiatives"
        )
        
        cost_reduction_target = st.number_input(
            "Cost Reduction Target (%)", 
            min_value=0.0, max_value=50.0, value=10.0, step=0.1,
            help="Target cost savings across operations"
        )
        
        productivity_improvement_target = st.number_input(
            "Productivity Improvement Target (%)", 
            min_value=0.0, max_value=100.0, value=25.0, step=0.1,
            help="Target improvement in workforce productivity"
        )
        
        customer_satisfaction_target = st.number_input(
            "Customer Satisfaction Target (1-10)", 
            min_value=1.0, max_value=10.0, value=8.5, step=0.1,
            help="Target customer satisfaction score"
        )
    
    with col2:
        st.markdown("#### Innovation & Market Position")
        
        market_share_target = st.number_input(
            "Market Share Growth Target (%)", 
            min_value=0.0, max_value=50.0, value=5.0, step=0.1,
            help="Target increase in market share"
        )
        
        time_to_market_improvement = st.number_input(
            "Time-to-Market Improvement (%)", 
            min_value=0.0, max_value=80.0, value=30.0, step=0.1,
            help="Target reduction in product/service launch time"
        )
        
        innovation_index_target = st.selectbox(
            "Innovation Index Target",
            ["Industry Follower", "Industry Average", "Industry Leader", "Industry Pioneer"],
            index=2,
            help="Target position in industry innovation rankings"
        )
        
        digital_transformation_maturity = st.selectbox(
            "Digital Transformation Maturity Target",
            ["Basic", "Intermediate", "Advanced", "Leading Edge"],
            index=2,
            help="Target level of digital transformation"
        )
    
    st.markdown("---")
    
    # Key Performance Indicators
    st.subheader("📊 Key Performance Indicators (KPIs)")
    
    # Financial KPIs
    with st.expander("💰 Financial KPIs", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            roi_threshold = st.number_input(
                "Minimum ROI Threshold (%)", 
                min_value=0.0, max_value=100.0, value=20.0, step=0.5,
                help="Minimum acceptable return on AI investments"
            )
            
            payback_period_max = st.number_input(
                "Maximum Payback Period (months)", 
                min_value=1, max_value=60, value=18, step=1,
                help="Maximum acceptable time to recover investment"
            )
        
        with col2:
            ebitda_improvement = st.number_input(
                "EBITDA Improvement Target (%)", 
                min_value=0.0, max_value=50.0, value=12.0, step=0.5,
                help="Target improvement in earnings before interest, taxes, depreciation, and amortization"
            )
            
            cash_flow_improvement = st.number_input(
                "Cash Flow Improvement Target (%)", 
                min_value=0.0, max_value=50.0, value=15.0, step=0.5,
                help="Target improvement in operating cash flow"
            )
        
        with col3:
            capital_efficiency = st.number_input(
                "Capital Efficiency Target (Revenue/Capital)", 
                min_value=0.0, max_value=10.0, value=2.5, step=0.1,
                help="Target ratio of revenue to invested capital"
            )
            
            working_capital_optimization = st.number_input(
                "Working Capital Optimization (%)", 
                min_value=0.0, max_value=30.0, value=8.0, step=0.5,
                help="Target reduction in working capital requirements"
            )
    
    # Operational KPIs
    with st.expander("⚙️ Operational KPIs"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            process_automation_target = st.number_input(
                "Process Automation Target (%)", 
                min_value=0.0, max_value=100.0, value=40.0, step=1.0,
                help="Target percentage of processes to be automated"
            )
            
            error_reduction_target = st.number_input(
                "Error Reduction Target (%)", 
                min_value=0.0, max_value=95.0, value=60.0, step=1.0,
                help="Target reduction in operational errors"
            )
        
        with col2:
            cycle_time_reduction = st.number_input(
                "Cycle Time Reduction Target (%)", 
                min_value=0.0, max_value=80.0, value=35.0, step=1.0,
                help="Target reduction in process cycle times"
            )
            
            quality_improvement = st.number_input(
                "Quality Improvement Target (%)", 
                min_value=0.0, max_value=50.0, value=20.0, step=1.0,
                help="Target improvement in output quality metrics"
            )
        
        with col3:
            resource_utilization = st.number_input(
                "Resource Utilization Target (%)", 
                min_value=50.0, max_value=95.0, value=85.0, step=1.0,
                help="Target efficiency of resource utilization"
            )
            
            capacity_expansion = st.number_input(
                "Capacity Expansion Target (%)", 
                min_value=0.0, max_value=100.0, value=25.0, step=1.0,
                help="Target increase in operational capacity"
            )
    
    # Customer & Market KPIs
    with st.expander("👥 Customer & Market KPIs"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_acquisition_improvement = st.number_input(
                "Customer Acquisition Improvement (%)", 
                min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                help="Target improvement in customer acquisition rate"
            )
            
            customer_retention_target = st.number_input(
                "Customer Retention Target (%)", 
                min_value=50.0, max_value=98.0, value=90.0, step=0.5,
                help="Target customer retention rate"
            )
            
            nps_score_target = st.number_input(
                "Net Promoter Score Target", 
                min_value=-100, max_value=100, value=50, step=1,
                help="Target Net Promoter Score"
            )
        
        with col2:
            customer_lifetime_value_increase = st.number_input(
                "Customer Lifetime Value Increase (%)", 
                min_value=0.0, max_value=100.0, value=25.0, step=1.0,
                help="Target increase in customer lifetime value"
            )
            
            response_time_improvement = st.number_input(
                "Response Time Improvement (%)", 
                min_value=0.0, max_value=90.0, value=50.0, step=1.0,
                help="Target improvement in customer response times"
            )
            
            personalization_score = st.number_input(
                "Personalization Score Target (1-10)", 
                min_value=1.0, max_value=10.0, value=8.0, step=0.1,
                help="Target level of customer experience personalization"
            )
    
    st.markdown("---")
    
    # Strategic Timeline
    st.subheader("📅 Strategic Timeline")
    
    col1, col2 = st.columns(2)
    
    with col1:
        short_term_goals = st.text_area(
            "Short-term Goals (6-12 months)",
            height=100,
            placeholder="List key objectives for the next 6-12 months..."
        )
        
        medium_term_goals = st.text_area(
            "Medium-term Goals (1-2 years)",
            height=100,
            placeholder="List key objectives for 1-2 years..."
        )
    
    with col2:
        long_term_vision = st.text_area(
            "Long-term Vision (3-5 years)",
            height=100,
            placeholder="Describe the long-term vision and strategic outcomes..."
        )
        
        success_metrics = st.text_area(
            "Success Metrics & Measurement",
            height=100,
            placeholder="How will success be measured and evaluated..."
        )
    
    # Save corporate objectives
    if st.button("💾 Save Corporate Objectives", type="primary"):
        objectives_data = {
            'strategic_objectives': {
                'revenue_growth_target': revenue_growth_target,
                'cost_reduction_target': cost_reduction_target,
                'productivity_improvement_target': productivity_improvement_target,
                'customer_satisfaction_target': customer_satisfaction_target,
                'market_share_target': market_share_target,
                'time_to_market_improvement': time_to_market_improvement,
                'innovation_index_target': innovation_index_target,
                'digital_transformation_maturity': digital_transformation_maturity
            },
            'financial_kpis': {
                'roi_threshold': roi_threshold,
                'payback_period_max': payback_period_max,
                'ebitda_improvement': ebitda_improvement,
                'cash_flow_improvement': cash_flow_improvement,
                'capital_efficiency': capital_efficiency,
                'working_capital_optimization': working_capital_optimization
            },
            'operational_kpis': {
                'process_automation_target': process_automation_target,
                'error_reduction_target': error_reduction_target,
                'cycle_time_reduction': cycle_time_reduction,
                'quality_improvement': quality_improvement,
                'resource_utilization': resource_utilization,
                'capacity_expansion': capacity_expansion
            },
            'customer_market_kpis': {
                'customer_acquisition_improvement': customer_acquisition_improvement,
                'customer_retention_target': customer_retention_target,
                'nps_score_target': nps_score_target,
                'customer_lifetime_value_increase': customer_lifetime_value_increase,
                'response_time_improvement': response_time_improvement,
                'personalization_score': personalization_score
            },
            'strategic_timeline': {
                'short_term_goals': short_term_goals,
                'medium_term_goals': medium_term_goals,
                'long_term_vision': long_term_vision,
                'success_metrics': success_metrics
            },
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state.corporate_objectives = objectives_data
        st.success("Corporate objectives and KPIs saved successfully!")
    
    # Display saved objectives summary
    if 'corporate_objectives' in st.session_state and st.session_state.corporate_objectives:
        st.markdown("---")
        st.subheader("📋 Current Objectives Summary")
        
        objectives = st.session_state.corporate_objectives
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'strategic_objectives' in objectives:
                st.metric("Revenue Growth Target", f"{objectives['strategic_objectives']['revenue_growth_target']:.1f}%")
                st.metric("Market Share Growth", f"{objectives['strategic_objectives']['market_share_target']:.1f}%")
        
        with col2:
            if 'financial_kpis' in objectives:
                st.metric("Min ROI Threshold", f"{objectives['financial_kpis']['roi_threshold']:.1f}%")
                st.metric("Max Payback Period", f"{objectives['financial_kpis']['payback_period_max']} months")
        
        with col3:
            if 'operational_kpis' in objectives:
                st.metric("Automation Target", f"{objectives['operational_kpis']['process_automation_target']:.0f}%")
                st.metric("Error Reduction", f"{objectives['operational_kpis']['error_reduction_target']:.0f}%")
        
        with col4:
            if 'customer_market_kpis' in objectives:
                st.metric("Customer Retention", f"{objectives['customer_market_kpis']['customer_retention_target']:.1f}%")
                st.metric("NPS Target", f"{objectives['customer_market_kpis']['nps_score_target']}")
        
        # Export objectives
        if st.button("📄 Export Objectives"):
            import json
            objectives_json = json.dumps(objectives, indent=2, default=str)
            
            st.download_button(
                label="Download Corporate Objectives",
                data=objectives_json,
                file_name=f"corporate_objectives_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )