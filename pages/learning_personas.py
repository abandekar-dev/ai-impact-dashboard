import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from utils.learning_personas import LearningPersonaAnalyzer, DynamicCurriculumBuilder

def show_learning_personas():
    """AI Learning and Upskilling Personas Analysis"""
    
    st.header("🎓 AI Learning & Upskilling Personas")
    st.markdown("**Dynamic curriculum generation and personalized learning paths across the enterprise**")
    
    # Check if baseline data exists
    if not st.session_state.baseline_data:
        st.warning("Please configure baseline data for enterprise functions first in 'Input by Department/Business'.")
        return
    
    # Initialize analyzers
    persona_analyzer = LearningPersonaAnalyzer()
    curriculum_builder = DynamicCurriculumBuilder()
    
    # Analyze personas across all departments
    with st.spinner("Analyzing learning personas across the enterprise..."):
        persona_analysis = persona_analyzer.analyze_enterprise_personas(st.session_state.baseline_data)
    
    st.markdown("---")
    
    # Main analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Enterprise Overview",
        "🏢 Department Personas", 
        "📚 Dynamic Curricula",
        "📊 Skill Gap Analysis",
        "🎯 Learning Pathways"
    ])
    
    with tab1:
        show_enterprise_overview(persona_analysis, curriculum_builder)
    
    with tab2:
        show_department_personas(persona_analysis, curriculum_builder)
    
    with tab3:
        show_dynamic_curricula(persona_analysis, curriculum_builder)
    
    with tab4:
        show_skill_gap_analysis(persona_analysis)
    
    with tab5:
        show_learning_pathways(persona_analysis)

def show_enterprise_overview(persona_analysis: dict, curriculum_builder: DynamicCurriculumBuilder):
    """Show enterprise-level persona overview"""
    
    st.subheader("🌐 Enterprise Learning Persona Overview")
    
    analysis = persona_analysis.get('persona_analysis', {})
    enterprise_personas = persona_analysis.get('enterprise_personas', [])
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_personas = analysis.get('total_personas', 0)
        st.metric("Total Personas", total_personas)
    
    with col2:
        avg_proficiency = analysis.get('average_proficiency', 0)
        st.metric("Avg AI Proficiency", f"{avg_proficiency:.1f}/100")
    
    with col3:
        skill_gaps = len(analysis.get('top_skill_gaps', []))
        st.metric("Critical Skill Gaps", skill_gaps)
    
    with col4:
        enterprise_count = len(enterprise_personas)
        st.metric("Enterprise Personas", enterprise_count)
    
    # Proficiency distribution
    st.markdown("#### 📊 AI Proficiency Distribution")
    
    proficiency_dist = analysis.get('proficiency_distribution', {})
    if proficiency_dist:
        prof_df = pd.DataFrame([
            {"Level": level, "Count": count} 
            for level, count in proficiency_dist.items()
        ])
        
        fig = px.pie(prof_df, values='Count', names='Level', 
                    title="AI Proficiency Levels Across Enterprise")
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning preferences
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Learning Style Distribution")
        learning_styles = analysis.get('learning_style_distribution', {})
        if learning_styles:
            style_df = pd.DataFrame([
                {"Style": style, "Count": count}
                for style, count in learning_styles.items()
            ])
            
            fig = px.bar(style_df, x='Style', y='Count',
                        title="Preferred Learning Styles")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏰ Time Availability Patterns")
        time_patterns = analysis.get('time_availability_patterns', {})
        if time_patterns:
            time_df = pd.DataFrame([
                {"Availability": pattern, "Count": count}
                for pattern, count in time_patterns.items()
            ])
            
            fig = px.bar(time_df, x='Availability', y='Count',
                        title="Time Availability for Learning")
            st.plotly_chart(fig, use_container_width=True)
    
    # Enterprise-level personas
    st.markdown("#### 🎯 Enterprise-Level Personas")
    
    if enterprise_personas:
        persona_data = []
        for persona in enterprise_personas:
            persona_data.append({
                "Persona": persona.name,
                "AI Proficiency": f"{persona.current_ai_proficiency:.1f}/100",
                "Learning Style": persona.learning_style,
                "Time Availability": persona.time_availability,
                "Key Motivations": ", ".join(persona.motivation_factors[:2]),
                "Top Skill Gaps": len([gap for gap in persona.skill_gaps.values() if gap > 50])
            })
        
        persona_df = pd.DataFrame(persona_data)
        st.dataframe(persona_df, use_container_width=True)
        
        # Generate curricula for enterprise personas
        st.markdown("#### 📚 Enterprise Curriculum Overview")
        
        selected_persona = st.selectbox(
            "Select Enterprise Persona for Curriculum",
            options=[p.name for p in enterprise_personas],
            index=0
        )
        
        if selected_persona:
            persona = next(p for p in enterprise_personas if p.name == selected_persona)
            
            with st.spinner("Generating dynamic curriculum..."):
                curriculum = curriculum_builder.build_curriculum_for_persona(persona)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Modules", len(curriculum.learning_path))
            
            with col2:
                st.metric("Duration (Hours)", f"{curriculum.total_duration:.0f}")
            
            with col3:
                estimated_weeks = curriculum.total_duration / (4 if persona.time_availability == "Moderate" else 2 if persona.time_availability == "Limited" else 8)
                st.metric("Estimated Weeks", f"{estimated_weeks:.0f}")
    else:
        st.info("No enterprise personas generated. This typically occurs when there's insufficient department data.")

def show_department_personas(persona_analysis: dict, curriculum_builder: DynamicCurriculumBuilder):
    """Show department-specific personas"""
    
    st.subheader("🏢 Department-Specific Personas")
    
    department_personas = persona_analysis.get('department_personas', {})
    
    if not department_personas:
        st.warning("No department personas available. Please ensure departments are configured.")
        return
    
    # Department selection
    selected_dept = st.selectbox("Select Department", list(department_personas.keys()))
    
    if selected_dept and selected_dept in department_personas:
        dept_personas = department_personas[selected_dept]
        
        st.markdown(f"#### 👥 {selected_dept} Learning Personas")
        
        # Persona overview
        persona_overview = []
        for persona in dept_personas:
            persona_overview.append({
                "Role Level": persona.role_level,
                "AI Proficiency": f"{persona.current_ai_proficiency:.1f}/100",
                "Learning Style": persona.learning_style,
                "Time Availability": persona.time_availability,
                "Technical Background": persona.technical_background,
                "Top Skill Gap": max(persona.skill_gaps.items(), key=lambda x: x[1])[0] if persona.skill_gaps else "None",
                "Gap Severity": f"{max(persona.skill_gaps.values()):.1f}" if persona.skill_gaps else "0"
            })
        
        overview_df = pd.DataFrame(persona_overview)
        st.dataframe(overview_df, use_container_width=True)
        
        # Detailed persona analysis
        st.markdown("#### 🔍 Detailed Persona Analysis")
        
        selected_role = st.selectbox(
            "Select Role Level for Details",
            options=[p.role_level for p in dept_personas]
        )
        
        persona = next((p for p in dept_personas if p.role_level == selected_role), None)
        
        if persona:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Learning Profile**")
                st.write(f"**Current AI Proficiency:** {persona.current_ai_proficiency:.1f}/100")
                st.write(f"**Learning Style:** {persona.learning_style}")
                st.write(f"**Time Availability:** {persona.time_availability}")
                st.write(f"**Technical Background:** {persona.technical_background}")
                
                st.markdown("**💪 Motivation Factors**")
                for motivation in persona.motivation_factors:
                    st.write(f"• {motivation}")
                
                st.markdown("**📋 Preferred Learning Formats**")
                for format_type in persona.preferred_learning_format:
                    st.write(f"• {format_type}")
            
            with col2:
                st.markdown("**🎯 Career Goals**")
                for goal in persona.career_goals:
                    st.write(f"• {goal}")
                
                st.markdown("**📊 Skill Gaps Analysis**")
                if persona.skill_gaps:
                    gap_df = pd.DataFrame([
                        {"Skill": skill, "Gap Level": gap}
                        for skill, gap in persona.skill_gaps.items()
                    ]).sort_values("Gap Level", ascending=False)
                    
                    fig = px.bar(gap_df.head(5), x='Gap Level', y='Skill',
                                orientation='h',
                                title="Top 5 Skill Gaps",
                                color='Gap Level',
                                color_continuous_scale='Reds')
                    st.plotly_chart(fig, use_container_width=True)
            
            # Generate personalized curriculum
            st.markdown("#### 📚 Personalized Curriculum")
            
            if st.button(f"Generate Curriculum for {persona.role_level}", key=f"gen_curr_{selected_dept}_{selected_role}"):
                with st.spinner("Building personalized curriculum..."):
                    curriculum = curriculum_builder.build_curriculum_for_persona(persona)
                
                show_curriculum_details(curriculum, curriculum_builder)

def show_dynamic_curricula(persona_analysis: dict, curriculum_builder: DynamicCurriculumBuilder):
    """Show dynamic curriculum generation capabilities"""
    
    st.subheader("📚 Dynamic Curriculum Generation")
    
    enterprise_personas = persona_analysis.get('enterprise_personas', [])
    department_personas = persona_analysis.get('department_personas', {})
    
    if not enterprise_personas and not department_personas:
        st.warning("No personas available for curriculum generation.")
        return
    
    # Curriculum generation options
    st.markdown("#### 🎛️ Curriculum Generation Options")
    
    generation_type = st.radio(
        "Select Curriculum Type",
        ["Enterprise-Level Curriculum", "Department-Specific Curriculum", "Custom Persona Curriculum"]
    )
    
    if generation_type == "Enterprise-Level Curriculum":
        if enterprise_personas:
            selected_persona = st.selectbox(
                "Select Enterprise Persona",
                options=[p.name for p in enterprise_personas]
            )
            
            persona = next(p for p in enterprise_personas if p.name == selected_persona)
            
        else:
            st.warning("No enterprise personas available.")
            return
    
    elif generation_type == "Department-Specific Curriculum":
        if department_personas:
            dept_options = list(department_personas.keys())
            selected_dept = st.selectbox("Select Department", dept_options)
            
            if selected_dept in department_personas:
                role_options = [p.role_level for p in department_personas[selected_dept]]
                selected_role = st.selectbox("Select Role Level", role_options)
                
                persona = next(p for p in department_personas[selected_dept] if p.role_level == selected_role)
        else:
            st.warning("No department personas available.")
            return
    
    else:  # Custom Persona Curriculum
        st.markdown("#### 🛠️ Custom Persona Builder")
        
        col1, col2 = st.columns(2)
        
        with col1:
            custom_name = st.text_input("Persona Name", "Custom Learner")
            custom_dept = st.selectbox("Department", list(department_personas.keys()) if department_personas else ["Custom"])
            custom_role = st.selectbox("Role Level", ["Entry", "Mid", "Senior", "Executive"])
            custom_proficiency = st.slider("Current AI Proficiency", 0, 100, 50)
        
        with col2:
            custom_style = st.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic", "Reading"])
            custom_time = st.selectbox("Time Availability", ["Limited", "Moderate", "Flexible"])
            custom_background = st.selectbox("Technical Background", ["None", "Basic", "Intermediate", "Advanced"])
        
        # Create custom persona (simplified)
        from utils.learning_personas import LearningPersona
        
        persona = LearningPersona(
            persona_id="custom_persona",
            name=custom_name,
            description=f"Custom {custom_role} learner in {custom_dept}",
            department=custom_dept,
            role_level=custom_role,
            current_ai_proficiency=custom_proficiency,
            learning_style=custom_style,
            time_availability=custom_time,
            technical_background=custom_background,
            motivation_factors=["Skill Development", "Career Growth"],
            preferred_learning_format=["Self-paced Online", "Hands-on Labs"],
            career_goals=["Develop AI expertise"],
            skill_gaps={"AI Fundamentals": 60, "Data Literacy": 50, "Process Automation": 40}
        )
    
    # Generate curriculum
    if st.button("🚀 Generate Dynamic Curriculum", key="generate_dynamic"):
        with st.spinner("Creating personalized learning path..."):
            curriculum = curriculum_builder.build_curriculum_for_persona(persona)
        
        show_curriculum_details(curriculum, curriculum_builder)

def show_curriculum_details(curriculum, curriculum_builder):
    """Show detailed curriculum information"""
    
    st.markdown("#### 📋 Generated Curriculum Details")
    
    # Curriculum overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Modules", len(curriculum.learning_path))
    
    with col2:
        st.metric("Duration (Hours)", f"{curriculum.total_duration:.0f}")
    
    with col3:
        milestones_count = len(curriculum.milestones)
        st.metric("Learning Milestones", milestones_count)
    
    with col4:
        timeline_weeks = len(set(curriculum.completion_timeline.values()))
        st.metric("Timeline (Weeks)", timeline_weeks)
    
    # Learning path visualization
    st.markdown("#### 🛤️ Learning Path")
    
    path_data = []
    for i, module_id in enumerate(curriculum.learning_path):
        module = curriculum_builder.module_library[module_id]
        path_data.append({
            "Order": i + 1,
            "Module": module.title,
            "Category": module.skill_category,
            "Difficulty": module.difficulty_level,
            "Duration (Hours)": module.duration_hours,
            "Format": module.format_type,
            "Timeline": curriculum.completion_timeline.get(module_id, "TBD")
        })
    
    path_df = pd.DataFrame(path_data)
    st.dataframe(path_df, use_container_width=True)
    
    # Learning path flow visualization
    if len(curriculum.learning_path) > 0:
        categories = [curriculum_builder.module_library[mod_id].skill_category for mod_id in curriculum.learning_path]
        difficulties = [curriculum_builder.module_library[mod_id].difficulty_level for mod_id in curriculum.learning_path]
        
        fig = go.Figure()
        
        # Create flow chart
        for i, (module_id, category, difficulty) in enumerate(zip(curriculum.learning_path, categories, difficulties)):
            module = curriculum_builder.module_library[module_id]
            
            color_map = {"Foundation": "lightblue", "Technical": "lightgreen", 
                        "Application": "lightyellow", "Leadership": "lightcoral"}
            
            fig.add_trace(go.Scatter(
                x=[i], y=[0],
                mode='markers+text',
                marker=dict(size=20, color=color_map.get(category, "lightgray")),
                text=module.title,
                textposition="top center",
                name=category,
                showlegend=True if i == 0 or categories[i] != categories[i-1] else False
            ))
        
        fig.update_layout(
            title="Learning Path Flow",
            xaxis_title="Module Sequence",
            yaxis=dict(visible=False),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Milestones
    st.markdown("#### 🏆 Learning Milestones")
    
    if curriculum.milestones:
        milestone_data = []
        for name, details in curriculum.milestones.items():
            milestone_data.append({
                "Milestone": name,
                "Completion %": f"{details['completion_percentage']:.0f}%",
                "Module": curriculum_builder.module_library[details['module_id']].title,
                "Reward": details['reward'],
                "Assessment": "Required" if details['assessment_required'] else "Optional"
            })
        
        milestone_df = pd.DataFrame(milestone_data)
        st.dataframe(milestone_df, use_container_width=True)
    
    # Adaptive rules
    with st.expander("🔧 Adaptive Learning Rules"):
        st.json(curriculum.adaptive_rules)

def show_skill_gap_analysis(persona_analysis: dict):
    """Show comprehensive skill gap analysis"""
    
    st.subheader("📊 Enterprise Skill Gap Analysis")
    
    skill_gap_analysis = persona_analysis.get('skill_gap_analysis', {})
    
    if not skill_gap_analysis:
        st.warning("No skill gap analysis available.")
        return
    
    # Top skill gaps
    top_gaps = skill_gap_analysis.get('prioritized_skill_gaps', [])
    
    if top_gaps:
        st.markdown("#### 🎯 Top Priority Skill Gaps")
        
        gap_data = []
        for skill, analysis in top_gaps[:10]:
            gap_data.append({
                "Skill": skill,
                "Average Gap": f"{analysis['average_gap']:.1f}",
                "Max Gap": f"{analysis['max_gap']:.1f}",
                "Personas Affected": analysis['personas_affected'],
                "Priority Level": f"{analysis['priority_level']:.1f}"
            })
        
        gap_df = pd.DataFrame(gap_data)
        st.dataframe(gap_df, use_container_width=True)
        
        # Skill gap visualization
        fig = px.scatter(gap_df, 
                        x='Average Gap', 
                        y='Personas Affected',
                        size='Priority Level',
                        hover_data=['Skill'],
                        title="Skill Gap Priority Matrix",
                        labels={'Average Gap': 'Average Gap Level', 'Personas Affected': 'Number of Personas Affected'})
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Enterprise priorities
    enterprise_priorities = skill_gap_analysis.get('enterprise_skill_priorities', [])
    
    if enterprise_priorities:
        st.markdown("#### 🏢 Enterprise Skill Priorities")
        
        priority_list = "\n".join([f"• {skill}" for skill in enterprise_priorities])
        st.markdown(priority_list)
        
        # Investment recommendations
        st.markdown("#### 💰 Training Investment Recommendations")
        
        investment_data = []
        for i, skill in enumerate(enterprise_priorities[:5]):
            # Find skill in analysis
            skill_analysis = next((analysis for s, analysis in top_gaps if s == skill), None)
            if skill_analysis:
                personas_affected = skill_analysis[1]['personas_affected']
                avg_gap = skill_analysis[1]['average_gap']
                
                # Estimate investment (simplified calculation)
                estimated_cost = personas_affected * avg_gap * 50  # $50 per gap point per person
                
                investment_data.append({
                    "Priority": i + 1,
                    "Skill": skill,
                    "Estimated Cost": f"${estimated_cost:,.0f}",
                    "Expected Impact": "High" if avg_gap > 60 else "Medium",
                    "Timeline": "3-6 months" if avg_gap > 70 else "6-12 months"
                })
        
        if investment_data:
            invest_df = pd.DataFrame(investment_data)
            st.dataframe(invest_df, use_container_width=True)

def show_learning_pathways(persona_analysis: dict):
    """Show learning pathway recommendations"""
    
    st.subheader("🎯 Enterprise Learning Pathways")
    
    learning_pathways = persona_analysis.get('learning_pathways', {})
    
    if not learning_pathways:
        st.warning("No learning pathways available.")
        return
    
    # Pathway overview
    st.markdown("#### 📚 Available Learning Tracks")
    
    pathway_data = []
    for track_name, track_info in learning_pathways.items():
        pathway_data.append({
            "Track": track_name,
            "Description": track_info['description'],
            "Duration": f"{track_info['duration_weeks']} weeks",
            "Modules": len(track_info['modules']),
            "Target Personas": track_info['target_personas'],
            "Assessment": track_info['assessment']
        })
    
    pathway_df = pd.DataFrame(pathway_data)
    st.dataframe(pathway_df, use_container_width=True)
    
    # Detailed pathway view
    st.markdown("#### 🔍 Pathway Details")
    
    selected_pathway = st.selectbox(
        "Select Learning Track for Details",
        list(learning_pathways.keys())
    )
    
    if selected_pathway in learning_pathways:
        pathway = learning_pathways[selected_pathway]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Curriculum Modules**")
            for i, module in enumerate(pathway['modules'], 1):
                st.write(f"{i}. {module}")
            
            st.markdown("**🎯 Learning Formats**")
            for format_type in pathway['learning_formats']:
                st.write(f"• {format_type}")
        
        with col2:
            st.markdown("**📊 Track Metrics**")
            st.write(f"**Duration:** {pathway['duration_weeks']} weeks")
            st.write(f"**Target Learners:** {pathway['target_personas']} personas")
            st.write(f"**Assessment Method:** {pathway['assessment']}")
            
            # Pathway progression visualization
            modules = pathway['modules']
            weeks = list(range(1, len(modules) + 1))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=weeks,
                y=[1] * len(weeks),
                mode='markers+text',
                text=modules,
                textposition="top center",
                marker=dict(size=15, color='lightblue'),
                name="Modules"
            ))
            
            fig.update_layout(
                title=f"{selected_pathway} Progression",
                xaxis_title="Week",
                yaxis=dict(visible=False),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Pathway recommendations
    st.markdown("#### 💡 Pathway Recommendations")
    
    recommendations = [
        "Implement Foundation Track for employees with < 30% AI proficiency",
        "Create department-specific versions of Application Track", 
        "Establish mentorship programs for Innovation Track participants",
        "Consider blended learning approaches for maximum effectiveness",
        "Develop assessment criteria aligned with business objectives"
    ]
    
    for rec in recommendations:
        st.write(f"• {rec}")
    
    # Implementation roadmap
    st.markdown("#### 🗺️ Implementation Roadmap")
    
    roadmap_data = [
        {"Phase": "Phase 1 (Months 1-2)", "Activities": "Launch Foundation Track, Set up learning infrastructure"},
        {"Phase": "Phase 2 (Months 3-4)", "Activities": "Deploy Application Track, Begin mentor training"},
        {"Phase": "Phase 3 (Months 5-6)", "Activities": "Launch Innovation Track, Evaluate progress"},
        {"Phase": "Phase 4 (Months 7-8)", "Activities": "Optimize pathways, Scale successful programs"}
    ]
    
    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True)