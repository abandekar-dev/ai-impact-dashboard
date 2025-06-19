import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any

# Minimal version without numpy/pandas dependencies
def main():
    st.title("🎯 Analytics and Insights Engine")
    st.markdown("**Executive Platform for Strategic AI Implementation and Workforce Transformation Analytics**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Overview"
    
    # Navigation buttons
    if st.sidebar.button("🏠 Overview", use_container_width=True, 
                        type="primary" if st.session_state.selected_page == "Overview" else "secondary"):
        st.session_state.selected_page = "Overview"
        st.rerun()
    
    if st.sidebar.button("🔧 Build vs Buy Analysis", use_container_width=True,
                        type="primary" if st.session_state.selected_page == "Build Buy Analysis" else "secondary"):
        st.session_state.selected_page = "Build Buy Analysis"
        st.rerun()
    
    # Page routing
    page = st.session_state.selected_page
    
    if page == "Overview":
        show_overview()
    elif page == "Build Buy Analysis":
        show_build_buy_minimal()

def show_overview():
    st.markdown("""
    ## 🌟 AI-Powered Strategic Modeling Platform
    
    Welcome to the comprehensive enterprise AI transformation analytics platform.
    
    ### Key Capabilities:
    - **Build vs Buy Analysis**: Strategic workforce planning for AI transformation
    - **Skills Gap Assessment**: Identify capability gaps and training needs
    - **Cost-Benefit Modeling**: Financial analysis of hiring vs training decisions
    - **Implementation Planning**: Timeline and resource allocation strategies
    
    ### Current Status:
    The platform is operational with core analytics capabilities. Navigate to Build vs Buy Analysis to explore workforce strategy planning.
    """)
    
    # Show some basic metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Skill Categories", "8", help="AI/ML, Data Science, Automation, etc.")
    with col2:
        st.metric("Analysis Types", "5", help="Skills Gap, Cost-Benefit, Strategic, etc.")
    with col3:
        st.metric("Industries Supported", "9", help="Technology, Healthcare, Finance, etc.")

def show_build_buy_minimal():
    st.title("🔧 Build vs Buy Analysis")
    st.markdown("**Strategic workforce planning: Build internal capabilities or buy external talent**")
    
    # Skills database (simplified version)
    skills_db = {
        'AI/ML Engineering': {'salary': 140000, 'training_months': 12, 'training_cost': 25000, 'availability': 'Low'},
        'Data Science & Analytics': {'salary': 120000, 'training_months': 8, 'training_cost': 15000, 'availability': 'Medium'},
        'Automation Engineering': {'salary': 95000, 'training_months': 6, 'training_cost': 12000, 'availability': 'Medium'},
        'Digital Transformation': {'salary': 110000, 'training_months': 4, 'training_cost': 8000, 'availability': 'High'},
        'Cybersecurity': {'salary': 115000, 'training_months': 10, 'training_cost': 18000, 'availability': 'Low'},
        'Cloud Architecture': {'salary': 130000, 'training_months': 8, 'training_cost': 15000, 'availability': 'Medium'},
        'Product Management': {'salary': 125000, 'training_months': 6, 'training_cost': 10000, 'availability': 'Medium'},
        'Business Intelligence': {'salary': 85000, 'training_months': 5, 'training_cost': 8000, 'availability': 'High'}
    }
    
    # Analysis parameters
    st.markdown("#### ⚙️ Analysis Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_headcount = st.number_input("Current Workforce Size", min_value=1, value=100)
        hiring_premium = st.slider("External Hiring Premium (%)", 0, 50, 20)
    
    with col2:
        skill_gap_percentage = st.slider("Estimated Skills Gap (%)", 10, 50, 25)
        training_efficiency = st.slider("Internal Training Efficiency (%)", 50, 100, 80)
    
    # Skill selection
    st.markdown("#### 🎯 Required Skills Selection")
    selected_skills = st.multiselect(
        "Select skills needed for AI transformation:",
        list(skills_db.keys()),
        default=['AI/ML Engineering', 'Data Science & Analytics', 'Automation Engineering']
    )
    
    if selected_skills:
        # Calculate analysis
        st.markdown("#### 📊 Analysis Results")
        
        total_buy_cost = 0
        total_build_cost = 0
        recommendations = []
        
        for skill in selected_skills:
            skill_info = skills_db[skill]
            
            # Estimate people needed (simplified calculation)
            people_needed = max(1, int((current_headcount * skill_gap_percentage / 100) / len(selected_skills)))
            
            # Buy scenario
            market_salary = skill_info['salary']
            buy_annual_cost = market_salary * (1 + hiring_premium/100) * people_needed
            buy_onetime_cost = 15000 * people_needed  # Recruitment cost
            buy_3yr_total = buy_annual_cost * 3 + buy_onetime_cost
            
            # Build scenario
            training_cost = skill_info['training_cost'] * people_needed
            internal_salary = market_salary * 0.8 * people_needed
            productivity_loss = (internal_salary * 0.5 * skill_info['training_months'] / 12)
            build_3yr_total = internal_salary * 3 + training_cost + productivity_loss
            
            total_buy_cost += buy_3yr_total
            total_build_cost += build_3yr_total
            
            # Generate recommendation
            if skill_info['availability'] == 'Low' or build_3yr_total < buy_3yr_total:
                recommendation = 'Build'
                rationale = f"{'Low market availability' if skill_info['availability'] == 'Low' else 'Cost effective'} - recommend internal training"
            else:
                recommendation = 'Buy'
                rationale = "External hiring more cost-effective"
            
            recommendations.append({
                'skill': skill,
                'people_needed': people_needed,
                'recommendation': recommendation,
                'buy_cost': buy_3yr_total,
                'build_cost': build_3yr_total,
                'savings': buy_3yr_total - build_3yr_total,
                'rationale': rationale
            })
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Buy Cost (3 years)", f"${total_buy_cost:,.0f}")
        with col2:
            st.metric("Total Build Cost (3 years)", f"${total_build_cost:,.0f}")
        with col3:
            total_savings = total_buy_cost - total_build_cost
            st.metric("Potential Savings", f"${total_savings:,.0f}")
        with col4:
            savings_pct = (total_savings / total_buy_cost * 100) if total_buy_cost > 0 else 0
            st.metric("Savings Percentage", f"{savings_pct:.1f}%")
        
        # Detailed recommendations
        st.markdown("#### 📋 Detailed Recommendations")
        
        for rec in recommendations:
            with st.expander(f"🎯 {rec['skill']} - {rec['recommendation']}"):
                st.markdown(f"**People Needed:** {rec['people_needed']}")
                st.markdown(f"**Buy Cost (3 years):** ${rec['buy_cost']:,.0f}")
                st.markdown(f"**Build Cost (3 years):** ${rec['build_cost']:,.0f}")
                st.markdown(f"**Potential Savings:** ${rec['savings']:,.0f}")
                st.markdown(f"**Rationale:** {rec['rationale']}")
        
        # Strategic insights
        st.markdown("#### 💡 Strategic Insights")
        
        build_count = sum(1 for r in recommendations if r['recommendation'] == 'Build')
        buy_count = len(recommendations) - build_count
        
        if build_count > buy_count:
            st.success("Build Strategy Recommended: Focus on internal training and capability development")
        elif buy_count > build_count:
            st.info("Buy Strategy Recommended: Prioritize external hiring for faster capability acquisition")
        else:
            st.warning("Hybrid Strategy Recommended: Balanced approach of building and buying capabilities")
        
        # Implementation timeline
        st.markdown("#### ⏱️ Implementation Timeline")
        
        max_training_time = max(skills_db[skill]['training_months'] for skill in selected_skills)
        
        st.markdown(f"""
        **Estimated Timeline:**
        - Immediate hiring: 3-4 months
        - Training completion: {max_training_time} months
        - Full capability: {max_training_time + 3} months
        
        **Risk Factors:**
        - Market competition for scarce skills
        - Training program effectiveness
        - Employee retention post-training
        """)

if __name__ == "__main__":
    main()