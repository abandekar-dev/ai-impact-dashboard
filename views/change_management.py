import streamlit as st
import pandas as pd
from typing import Dict, List
from datetime import datetime

def show_change_management():
    """Change Management Readiness input page"""
    
    st.header("🔄 Change Management Readiness")
    st.markdown("**Assess organizational culture and readiness for AI transformation**")
    
    # Initialize session state
    if 'change_management' not in st.session_state:
        st.session_state.change_management = {}
    
    st.markdown("---")
    
    # Organizational Culture Assessment
    st.subheader("🏛️ Organizational Culture Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Innovation Culture")
        
        innovation_appetite = st.selectbox(
            "Innovation Appetite",
            ["Risk Averse", "Conservative", "Moderate", "Innovative", "Pioneering"],
            index=2,
            help="Organization's willingness to adopt new technologies"
        )
        
        failure_tolerance = st.selectbox(
            "Failure Tolerance",
            ["Very Low", "Low", "Moderate", "High", "Very High"],
            index=2,
            help="How the organization handles failed initiatives"
        )
        
        learning_orientation = st.selectbox(
            "Learning Orientation",
            ["Reactive", "Adaptive", "Proactive", "Continuous", "Leading Edge"],
            index=2,
            help="Organization's commitment to learning and development"
        )
        
        decision_making_speed = st.selectbox(
            "Decision Making Speed",
            ["Very Slow", "Slow", "Moderate", "Fast", "Very Fast"],
            index=2,
            help="Speed of organizational decision making"
        )
    
    with col2:
        st.markdown("#### Collaboration & Communication")
        
        cross_functional_collaboration = st.selectbox(
            "Cross-functional Collaboration",
            ["Siloed", "Limited", "Moderate", "Strong", "Seamless"],
            index=2,
            help="Level of collaboration across departments"
        )
        
        communication_transparency = st.selectbox(
            "Communication Transparency",
            ["Closed", "Limited", "Moderate", "Open", "Fully Transparent"],
            index=2,
            help="Openness of internal communication"
        )
        
        knowledge_sharing = st.selectbox(
            "Knowledge Sharing Culture",
            ["Hoarding", "Limited", "Moderate", "Collaborative", "Open Source"],
            index=2,
            help="Willingness to share knowledge across teams"
        )
        
        feedback_receptiveness = st.selectbox(
            "Feedback Receptiveness",
            ["Resistant", "Defensive", "Neutral", "Receptive", "Seeking"],
            index=3,
            help="How well feedback is received and acted upon"
        )
    
    st.markdown("---")
    
    # Previous Change Experience
    st.subheader("📚 Previous Change Experience")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Past Transformations")
        
        previous_tech_implementations = st.number_input(
            "Major Tech Implementations (Last 5 Years)",
            min_value=0, max_value=20, value=3,
            help="Number of major technology implementations"
        )
        
        success_rate_previous = st.slider(
            "Success Rate of Previous Changes (%)",
            min_value=0, max_value=100, value=70,
            help="Percentage of successful change initiatives"
        )
        
        digital_transformation_experience = st.selectbox(
            "Digital Transformation Experience",
            ["None", "Minimal", "Some", "Extensive", "Multiple Successful"],
            index=2,
            help="Level of digital transformation experience"
        )
    
    with col2:
        st.markdown("#### Lessons Learned")
        
        change_management_maturity = st.selectbox(
            "Change Management Maturity",
            ["Ad-hoc", "Developing", "Defined", "Managed", "Optimized"],
            index=2,
            help="Maturity of change management processes"
        )
        
        stakeholder_engagement_quality = st.selectbox(
            "Stakeholder Engagement Quality",
            ["Poor", "Fair", "Good", "Very Good", "Excellent"],
            index=2,
            help="Quality of stakeholder engagement in past changes"
        )
        
        lessons_learned_documented = st.checkbox(
            "Lessons Learned Documented",
            value=True,
            help="Whether lessons from previous changes are documented"
        )
    
    st.markdown("---")
    
    # Leadership & Sponsorship
    st.subheader("👔 Leadership & Sponsorship")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Executive Support")
        
        ceo_sponsorship = st.selectbox(
            "CEO Sponsorship Level",
            ["None", "Minimal", "Moderate", "Strong", "Champion"],
            index=3,
            help="Level of CEO support for AI initiatives"
        )
        
        board_support = st.selectbox(
            "Board of Directors Support",
            ["Resistant", "Neutral", "Supportive", "Enthusiastic", "Driving"],
            index=2,
            help="Board support for AI transformation"
        )
        
        senior_leadership_alignment = st.slider(
            "Senior Leadership Alignment (%)",
            min_value=0, max_value=100, value=80,
            help="Percentage of senior leaders aligned on AI strategy"
        )
    
    with col2:
        st.markdown("#### Middle Management")
        
        middle_mgmt_buy_in = st.slider(
            "Middle Management Buy-in (%)",
            min_value=0, max_value=100, value=60,
            help="Percentage of middle managers supporting AI initiatives"
        )
        
        change_champion_network = st.selectbox(
            "Change Champion Network",
            ["None", "Informal", "Developing", "Established", "Mature"],
            index=2,
            help="Strength of change champion network"
        )
        
        manager_change_skills = st.selectbox(
            "Manager Change Skills",
            ["Weak", "Basic", "Moderate", "Strong", "Expert"],
            index=2,
            help="Change management skills of managers"
        )
    
    with col3:
        st.markdown("#### Resource Commitment")
        
        dedicated_change_resources = st.checkbox(
            "Dedicated Change Resources",
            value=False,
            help="Whether dedicated change management resources are allocated"
        )
        
        change_budget_allocated = st.checkbox(
            "Change Budget Allocated",
            value=False,
            help="Whether specific budget is allocated for change management"
        )
        
        external_change_support = st.selectbox(
            "External Change Support",
            ["None", "Consultants", "Coaches", "Full Service", "Partnership"],
            index=1,
            help="Level of external change management support"
        )
    
    st.markdown("---")
    
    # Employee Readiness
    st.subheader("👥 Employee Readiness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Workforce Characteristics")
        
        tech_literacy_level = st.selectbox(
            "Technology Literacy Level",
            ["Low", "Basic", "Intermediate", "Advanced", "Expert"],
            index=2,
            help="Overall technology literacy of workforce"
        )
        
        ai_awareness_level = st.selectbox(
            "AI Awareness Level",
            ["Unaware", "Basic", "Informed", "Knowledgeable", "Expert"],
            index=2,
            help="Current awareness of AI capabilities"
        )
        
        workforce_age_distribution = st.selectbox(
            "Workforce Age Distribution",
            ["Mostly Senior", "Senior Heavy", "Balanced", "Young Heavy", "Mostly Young"],
            index=2,
            help="Age distribution of workforce"
        )
        
        tenure_distribution = st.selectbox(
            "Employee Tenure Distribution",
            ["Mostly Long", "Long Heavy", "Mixed", "Short Heavy", "Mostly New"],
            index=2,
            help="Distribution of employee tenure"
        )
    
    with col2:
        st.markdown("#### Attitudes & Concerns")
        
        change_resistance_level = st.slider(
            "Expected Change Resistance (%)",
            min_value=0, max_value=100, value=40,
            help="Expected percentage of employees resistant to change"
        )
        
        job_security_concerns = st.slider(
            "Job Security Concerns (%)",
            min_value=0, max_value=100, value=60,
            help="Percentage of employees with job security concerns"
        )
        
        skill_obsolescence_fear = st.slider(
            "Skill Obsolescence Fear (%)",
            min_value=0, max_value=100, value=50,
            help="Percentage concerned about skills becoming obsolete"
        )
        
        enthusiasm_for_ai = st.slider(
            "Enthusiasm for AI (%)",
            min_value=0, max_value=100, value=30,
            help="Percentage of employees enthusiastic about AI"
        )
    
    st.markdown("---")
    
    # Communication & Training Strategy
    st.subheader("📢 Communication & Training Strategy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Communication Plan")
        
        communication_channels = st.multiselect(
            "Primary Communication Channels",
            ["Email", "Intranet", "Town Halls", "Team Meetings", "Newsletters", "Video Messages", "Social Platform"],
            default=["Email", "Team Meetings", "Town Halls"],
            help="Select primary communication channels"
        )
        
        communication_frequency = st.selectbox(
            "Communication Frequency",
            ["Monthly", "Bi-weekly", "Weekly", "Multiple per week", "Daily"],
            index=2,
            help="Planned frequency of AI initiative communications"
        )
        
        two_way_communication = st.checkbox(
            "Two-way Communication Channels",
            value=True,
            help="Whether feedback channels are established"
        )
    
    with col2:
        st.markdown("#### Training Approach")
        
        training_modality = st.multiselect(
            "Training Modalities",
            ["In-person", "Virtual", "Self-paced", "Peer-to-peer", "Mentoring", "Job shadowing"],
            default=["Virtual", "Self-paced"],
            help="Select training delivery methods"
        )
        
        training_timeline_weeks = st.number_input(
            "Training Timeline (weeks)",
            min_value=1, max_value=52, value=12,
            help="Expected duration of training program"
        )
        
        training_budget_per_person = st.number_input(
            "Training Budget per Person ($)",
            min_value=0, value=2000, step=100,
            help="Budget allocated per employee for training"
        )
    
    # Save change management data
    if st.button("💾 Save Change Management Assessment", type="primary"):
        change_data = {
            'organizational_culture': {
                'innovation_appetite': innovation_appetite,
                'failure_tolerance': failure_tolerance,
                'learning_orientation': learning_orientation,
                'decision_making_speed': decision_making_speed,
                'cross_functional_collaboration': cross_functional_collaboration,
                'communication_transparency': communication_transparency,
                'knowledge_sharing': knowledge_sharing,
                'feedback_receptiveness': feedback_receptiveness
            },
            'previous_experience': {
                'previous_tech_implementations': previous_tech_implementations,
                'success_rate_previous': success_rate_previous,
                'digital_transformation_experience': digital_transformation_experience,
                'change_management_maturity': change_management_maturity,
                'stakeholder_engagement_quality': stakeholder_engagement_quality,
                'lessons_learned_documented': lessons_learned_documented
            },
            'leadership_sponsorship': {
                'ceo_sponsorship': ceo_sponsorship,
                'board_support': board_support,
                'senior_leadership_alignment': senior_leadership_alignment,
                'middle_mgmt_buy_in': middle_mgmt_buy_in,
                'change_champion_network': change_champion_network,
                'manager_change_skills': manager_change_skills,
                'dedicated_change_resources': dedicated_change_resources,
                'change_budget_allocated': change_budget_allocated,
                'external_change_support': external_change_support
            },
            'employee_readiness': {
                'tech_literacy_level': tech_literacy_level,
                'ai_awareness_level': ai_awareness_level,
                'workforce_age_distribution': workforce_age_distribution,
                'tenure_distribution': tenure_distribution,
                'change_resistance_level': change_resistance_level,
                'job_security_concerns': job_security_concerns,
                'skill_obsolescence_fear': skill_obsolescence_fear,
                'enthusiasm_for_ai': enthusiasm_for_ai
            },
            'communication_training': {
                'communication_channels': communication_channels,
                'communication_frequency': communication_frequency,
                'two_way_communication': two_way_communication,
                'training_modality': training_modality,
                'training_timeline_weeks': training_timeline_weeks,
                'training_budget_per_person': training_budget_per_person
            },
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state.change_management = change_data
        st.success("Change management assessment saved successfully!")
    
    # Display readiness score and summary
    if 'change_management' in st.session_state and st.session_state.change_management:
        st.markdown("---")
        st.subheader("📊 Change Readiness Assessment")
        
        change_data = st.session_state.change_management
        
        # Calculate readiness scores
        culture_score = calculate_culture_readiness(change_data.get('organizational_culture', {}))
        leadership_score = calculate_leadership_readiness(change_data.get('leadership_sponsorship', {}))
        employee_score = calculate_employee_readiness(change_data.get('employee_readiness', {}))
        
        overall_readiness = (culture_score + leadership_score + employee_score) / 3
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            readiness_color = "green" if overall_readiness > 70 else "orange" if overall_readiness > 50 else "red"
            st.metric("Overall Readiness", f"{overall_readiness:.0f}%")
            st.markdown(f":{readiness_color}[{get_readiness_level(overall_readiness)}]")
        
        with col2:
            st.metric("Culture Readiness", f"{culture_score:.0f}%")
        
        with col3:
            st.metric("Leadership Readiness", f"{leadership_score:.0f}%")
        
        with col4:
            st.metric("Employee Readiness", f"{employee_score:.0f}%")
        
        # Readiness chart
        import plotly.graph_objects as go
        
        categories = ['Culture', 'Leadership', 'Employees', 'Overall']
        scores = [culture_score, leadership_score, employee_score, overall_readiness]
        
        fig = go.Figure(data=go.Bar(
            x=categories,
            y=scores,
            marker_color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
        ))
        fig.update_layout(title="Change Readiness Scores", yaxis_title="Readiness %")
        st.plotly_chart(fig, use_container_width=True)
        
        # Export change management data
        if st.button("📄 Export Change Management Data"):
            import json
            change_json = json.dumps(change_data, indent=2, default=str)
            
            st.download_button(
                label="Download Change Management Assessment",
                data=change_json,
                file_name=f"change_management_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def calculate_culture_readiness(culture_data):
    """Calculate culture readiness score"""
    if not culture_data:
        return 0
    
    score_map = {
        'innovation_appetite': {'Risk Averse': 20, 'Conservative': 40, 'Moderate': 60, 'Innovative': 80, 'Pioneering': 100},
        'failure_tolerance': {'Very Low': 20, 'Low': 40, 'Moderate': 60, 'High': 80, 'Very High': 100},
        'learning_orientation': {'Reactive': 20, 'Adaptive': 40, 'Proactive': 60, 'Continuous': 80, 'Leading Edge': 100},
        'cross_functional_collaboration': {'Siloed': 20, 'Limited': 40, 'Moderate': 60, 'Strong': 80, 'Seamless': 100}
    }
    
    scores = []
    for key, mapping in score_map.items():
        if key in culture_data:
            scores.append(mapping.get(culture_data[key], 50))
    
    return sum(scores) / len(scores) if scores else 50

def calculate_leadership_readiness(leadership_data):
    """Calculate leadership readiness score"""
    if not leadership_data:
        return 0
    
    scores = []
    
    # CEO sponsorship
    ceo_map = {'None': 0, 'Minimal': 25, 'Moderate': 50, 'Strong': 75, 'Champion': 100}
    if 'ceo_sponsorship' in leadership_data:
        scores.append(ceo_map.get(leadership_data['ceo_sponsorship'], 50))
    
    # Board support
    board_map = {'Resistant': 20, 'Neutral': 40, 'Supportive': 60, 'Enthusiastic': 80, 'Driving': 100}
    if 'board_support' in leadership_data:
        scores.append(board_map.get(leadership_data['board_support'], 50))
    
    # Alignment and buy-in percentages
    if 'senior_leadership_alignment' in leadership_data:
        scores.append(leadership_data['senior_leadership_alignment'])
    if 'middle_mgmt_buy_in' in leadership_data:
        scores.append(leadership_data['middle_mgmt_buy_in'])
    
    return sum(scores) / len(scores) if scores else 50

def calculate_employee_readiness(employee_data):
    """Calculate employee readiness score"""
    if not employee_data:
        return 0
    
    scores = []
    
    # Tech literacy
    tech_map = {'Low': 20, 'Basic': 40, 'Intermediate': 60, 'Advanced': 80, 'Expert': 100}
    if 'tech_literacy_level' in employee_data:
        scores.append(tech_map.get(employee_data['tech_literacy_level'], 50))
    
    # AI awareness
    ai_map = {'Unaware': 20, 'Basic': 40, 'Informed': 60, 'Knowledgeable': 80, 'Expert': 100}
    if 'ai_awareness_level' in employee_data:
        scores.append(ai_map.get(employee_data['ai_awareness_level'], 50))
    
    # Resistance (inverted)
    if 'change_resistance_level' in employee_data:
        scores.append(100 - employee_data['change_resistance_level'])
    
    # Enthusiasm
    if 'enthusiasm_for_ai' in employee_data:
        scores.append(employee_data['enthusiasm_for_ai'])
    
    return sum(scores) / len(scores) if scores else 50

def get_readiness_level(score):
    """Get readiness level description"""
    if score >= 80:
        return "High Readiness"
    elif score >= 60:
        return "Moderate Readiness"
    elif score >= 40:
        return "Low Readiness"
    else:
        return "Very Low Readiness"