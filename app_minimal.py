import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any

# Minimal app to demonstrate Build vs Buy Analysis functionality
st.set_page_config(
    page_title="AI Strategic Modeling Platform",
    page_icon="🎯",
    layout="wide"
)

def main():
    st.title("🔧 Build vs Buy Analysis - Demo")
    st.markdown("**Strategic workforce planning: Build internal capabilities or buy external talent**")
    
    # Sample data for demonstration
    sample_functions = {
        'Sales': {'headcount': 50, 'current_productivity': 7.5, 'annual_costs': 4500000},
        'IT': {'headcount': 30, 'current_productivity': 8.0, 'annual_costs': 6000000},
        'Marketing': {'headcount': 25, 'current_productivity': 6.8, 'annual_costs': 3000000}
    }
    
    sample_ai_initiatives = {
        'Sales': {
            'CRM Automation': {'ai_type': 'Automation', 'investment': 150000, 'complexity': 'Medium'},
            'Lead Scoring': {'ai_type': 'Machine Learning', 'investment': 200000, 'complexity': 'High'}
        },
        'IT': {
            'Infrastructure Monitoring': {'ai_type': 'Automation', 'investment': 100000, 'complexity': 'Low'},
            'Security Analytics': {'ai_type': 'Data Analytics', 'investment': 300000, 'complexity': 'High'}
        }
    }
    
    # Skills database
    skills_db = {
        'AI/ML Engineering': {
            'avg_salary': 140000,
            'training_cost': 25000,
            'training_time_months': 12,
            'market_availability': 'Low',
            'criticality': 'High'
        },
        'Data Science & Analytics': {
            'avg_salary': 120000,
            'training_cost': 15000,
            'training_time_months': 8,
            'market_availability': 'Medium',
            'criticality': 'High'
        },
        'Automation Engineering': {
            'avg_salary': 95000,
            'training_cost': 12000,
            'training_time_months': 6,
            'market_availability': 'Medium',
            'criticality': 'Medium'
        }
    }
    
    # Function selector
    selected_function = st.selectbox(
        "Select Function for Analysis:",
        list(sample_functions.keys())
    )
    
    if selected_function:
        # Display current state
        col1, col2, col3 = st.columns(3)
        
        func_data = sample_functions[selected_function]
        with col1:
            st.metric("Current Headcount", f"{func_data['headcount']:,}")
        with col2:
            st.metric("Productivity Score", f"{func_data['current_productivity']:.1f}/10")
        with col3:
            avg_cost = func_data['annual_costs'] / func_data['headcount']
            st.metric("Avg Cost per Employee", f"${avg_cost:,.0f}")
        
        # Analysis tabs
        tab1, tab2, tab3 = st.tabs(["Skills Gap Analysis", "Cost-Benefit Analysis", "Recommendations"])
        
        with tab1:
            st.subheader("Skills Gap Analysis")
            
            # Map AI initiatives to required skills
            required_skills = {}
            if selected_function in sample_ai_initiatives:
                for initiative, details in sample_ai_initiatives[selected_function].items():
                    ai_type = details['ai_type']
                    if ai_type == 'Machine Learning':
                        required_skills['AI/ML Engineering'] = 9
                    elif ai_type == 'Data Analytics':
                        required_skills['Data Science & Analytics'] = 8
                    elif ai_type == 'Automation':
                        required_skills['Automation Engineering'] = 7
            
            if required_skills:
                st.markdown("#### Required Skills Assessment")
                
                skills_data = []
                for skill_category, required_level in required_skills.items():
                    skill_info = skills_db.get(skill_category, {})
                    
                    # Estimate current capability (simplified)
                    current_capability = func_data['current_productivity'] * 0.7
                    gap = max(0, required_level - current_capability)
                    
                    skills_data.append({
                        'Skill Category': skill_category,
                        'Required Level': f"{required_level}/10",
                        'Current Level': f"{current_capability:.1f}/10",
                        'Gap': f"{gap:.1f}/10",
                        'Market Availability': skill_info.get('market_availability', 'Unknown'),
                        'Avg Salary': f"${skill_info.get('avg_salary', 0):,}",
                        'Training Cost': f"${skill_info.get('training_cost', 0):,}",
                        'Training Time': f"{skill_info.get('training_time_months', 0)} months"
                    })
                
                # Display skills table
                for skill in skills_data:
                    with st.expander(f"📊 {skill['Skill Category']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Required Level:** {skill['Required Level']}")
                            st.write(f"**Current Level:** {skill['Current Level']}")
                            st.write(f"**Gap:** {skill['Gap']}")
                        with col2:
                            st.write(f"**Market Availability:** {skill['Market Availability']}")
                            st.write(f"**Average Salary:** {skill['Avg Salary']}")
                            st.write(f"**Training Cost:** {skill['Training Cost']}")
                            st.write(f"**Training Time:** {skill['Training Time']}")
            else:
                st.info("No AI initiatives configured for this function.")
        
        with tab2:
            st.subheader("Cost-Benefit Analysis")
            
            if required_skills:
                st.markdown("#### Build vs Buy Comparison")
                
                for skill_category, required_level in required_skills.items():
                    skill_info = skills_db.get(skill_category, {})
                    
                    # Calculate people needed (simplified)
                    current_capability = func_data['current_productivity'] * 0.7
                    gap = max(0, required_level - current_capability)
                    people_needed = max(1, int(gap * 0.8))
                    
                    # Build scenario
                    training_cost = skill_info.get('training_cost', 10000)
                    market_salary = skill_info.get('avg_salary', 100000)
                    internal_salary = market_salary * 0.8
                    
                    build_onetime = training_cost * people_needed
                    build_annual = internal_salary * people_needed
                    build_3yr = build_onetime + (build_annual * 3)
                    
                    # Buy scenario
                    external_salary = market_salary * 1.2  # 20% premium
                    recruitment_cost = 15000 * people_needed
                    
                    buy_onetime = recruitment_cost
                    buy_annual = external_salary * people_needed
                    buy_3yr = buy_onetime + (buy_annual * 3)
                    
                    # Display comparison
                    with st.expander(f"💰 {skill_category} - Cost Analysis"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Build Strategy**")
                            st.write(f"People Needed: {people_needed}")
                            st.write(f"One-time Cost: ${build_onetime:,.0f}")
                            st.write(f"Annual Cost: ${build_annual:,.0f}")
                            st.write(f"3-Year Total: ${build_3yr:,.0f}")
                        
                        with col2:
                            st.markdown("**Buy Strategy**")
                            st.write(f"People Needed: {people_needed}")
                            st.write(f"One-time Cost: ${buy_onetime:,.0f}")
                            st.write(f"Annual Cost: ${buy_annual:,.0f}")
                            st.write(f"3-Year Total: ${buy_3yr:,.0f}")
                        
                        # Recommendation
                        if build_3yr < buy_3yr:
                            savings = buy_3yr - build_3yr
                            st.success(f"**Recommendation: BUILD** - Saves ${savings:,.0f} over 3 years")
                        else:
                            extra_cost = build_3yr - buy_3yr
                            st.info(f"**Recommendation: BUY** - ${extra_cost:,.0f} premium for faster implementation")
            else:
                st.info("No skills analysis available. Configure AI initiatives first.")
        
        with tab3:
            st.subheader("Strategic Recommendations")
            
            if required_skills:
                st.markdown("#### Implementation Strategy")
                
                build_count = 0
                buy_count = 0
                
                for skill_category, required_level in required_skills.items():
                    skill_info = skills_db.get(skill_category, {})
                    market_availability = skill_info.get('market_availability', 'Medium')
                    training_time = skill_info.get('training_time_months', 6)
                    
                    if market_availability == 'Low' and training_time <= 8:
                        recommendation = 'Build'
                        build_count += 1
                        rationale = f"Low market availability makes hiring difficult, while {training_time}-month training is manageable."
                    elif market_availability == 'High':
                        recommendation = 'Buy'
                        buy_count += 1
                        rationale = "High market availability makes external hiring cost-effective."
                    else:
                        recommendation = 'Build'
                        build_count += 1
                        rationale = "Balanced approach favoring internal development for sustainable capability building."
                    
                    with st.expander(f"🎯 {skill_category} - {recommendation}"):
                        st.write(f"**Recommendation:** {recommendation}")
                        st.write(f"**Rationale:** {rationale}")
                        
                        if recommendation == 'Build':
                            st.write("**Key Actions:**")
                            st.write(f"• Design comprehensive {skill_category.lower()} training program")
                            st.write("• Identify high-potential internal candidates")
                            st.write("• Establish partnerships with training providers")
                        else:
                            st.write("**Key Actions:**")
                            st.write(f"• Launch targeted recruitment for {skill_category}")
                            st.write("• Engage specialized recruitment agencies")
                            st.write("• Develop competitive compensation packages")
                
                # Summary
                st.markdown("#### Strategic Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Build Internally", build_count)
                with col2:
                    st.metric("Buy Externally", buy_count)
                with col3:
                    total_skills = len(required_skills)
                    build_ratio = (build_count / total_skills * 100) if total_skills > 0 else 0
                    st.metric("Build Preference", f"{build_ratio:.0f}%")
                
                # High-level recommendations
                st.markdown("#### Executive Recommendations")
                
                if build_count > buy_count:
                    st.success("💰 Strong case for build strategy - invest in comprehensive training programs")
                elif buy_count > build_count:
                    st.info("🎯 Buy strategy recommended - focus on strategic external hiring")
                else:
                    st.warning("📈 Balanced approach - consider hybrid build/buy strategy")
                
                if total_skills >= 3:
                    st.warning("⚡ Multiple critical skills needed - establish dedicated AI transformation team")
            else:
                st.info("Configure AI initiatives to see strategic recommendations.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This is a demonstration of the Build vs Buy Analysis module. The full platform includes integration with actual enterprise data, detailed Monte Carlo simulations, and comprehensive workforce analytics.")

if __name__ == "__main__":
    main()