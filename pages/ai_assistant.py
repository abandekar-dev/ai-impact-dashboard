import streamlit as st
from datetime import datetime
from utils.ai_assistant import AIAssistant, DashboardDataCollector

def show_ai_assistant():
    """AI Assistant conversational interface page"""
    
    st.header("🤖 AI Strategic Assistant")
    st.markdown("**Ask natural language questions about your AI implementation strategy**")
    
    # Initialize AI assistant
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    # Collect dashboard context
    context_data = DashboardDataCollector.collect_dashboard_context()
    data_completeness = DashboardDataCollector.get_data_completeness()
    
    # Show data availability status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Data Completeness", f"{data_completeness:.0f}%")
    
    with col2:
        configured_functions = len(context_data.get('baseline_data', {}))
        st.metric("Configured Functions", configured_functions)
    
    with col3:
        if context_data.get('predictions'):
            avg_roi = sum(p.get('roi', 0) for p in context_data['predictions'].values()) / len(context_data['predictions'])
            st.metric("Average ROI", f"{avg_roi:.1f}%")
        else:
            st.metric("Average ROI", "N/A")
    
    st.markdown("---")
    
    # Main chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display conversation history
        if hasattr(st.session_state.ai_assistant, 'conversation_history') and st.session_state.ai_assistant.conversation_history:
            st.subheader("💬 Conversation")
            
            for i, message in enumerate(st.session_state.ai_assistant.conversation_history):
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(f"**Executive:** {message['content']}")
                else:
                    with st.chat_message("assistant"):
                        st.markdown(f"**AI Assistant:** {message['content']}")
        
        # Input section
        st.subheader("Ask a Question")
        
        # Check if there's enough data for meaningful analysis
        if data_completeness < 40:
            st.warning("⚠️ Limited data available. For better insights, please configure more sections of the dashboard first.")
        
        # Suggested questions
        if context_data:
            suggestions = st.session_state.ai_assistant.get_suggested_questions(context_data)
            
            st.markdown("**💡 Suggested Questions:**")
            
            # Display suggestions in a grid
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                        # Process the suggested question
                        with st.spinner("Analyzing your data..."):
                            response = st.session_state.ai_assistant.analyze_dashboard_data(suggestion, context_data)
                            
                        # Display the response
                        with st.chat_message("user"):
                            st.markdown(f"**Executive:** {suggestion}")
                        
                        with st.chat_message("assistant"):
                            st.markdown(f"**AI Assistant:** {response}")
                        
                        st.rerun()
        
        st.markdown("---")
        
        # Custom question input
        question = st.text_area(
            "Ask your own question:",
            placeholder="e.g., 'What's our highest ROI opportunity?' or 'Which risks should we address first?'",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🚀 Ask AI", type="primary", disabled=not question.strip()):
                if not context_data:
                    st.error("No dashboard data available for analysis. Please configure some functions and AI initiatives first.")
                else:
                    with st.spinner("Analyzing your data..."):
                        response = st.session_state.ai_assistant.analyze_dashboard_data(question, context_data)
                    
                    # Display the response
                    with st.chat_message("user"):
                        st.markdown(f"**Executive:** {question}")
                    
                    with st.chat_message("assistant"):
                        st.markdown(f"**AI Assistant:** {response}")
                    
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat"):
                st.session_state.ai_assistant.clear_conversation()
                st.rerun()
    
    st.markdown("---")
    
    # Advanced features section
    with st.expander("🔧 Advanced Features"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export Conversation**")
            if st.button("📄 Export Chat History"):
                conversation_export = st.session_state.ai_assistant.export_conversation()
                st.download_button(
                    label="Download Conversation",
                    data=conversation_export,
                    file_name=f"ai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            st.markdown("**Context Information**")
            if st.button("📊 Show Data Context"):
                if context_data:
                    st.json(context_data)
                else:
                    st.info("No context data available")
    
    # Help and examples
    with st.expander("❓ How to Use the AI Assistant"):
        st.markdown("""
        **The AI Assistant can help you with:**
        
        **Strategic Questions:**
        - "What's our best ROI opportunity across all departments?"
        - "Which AI initiative should we implement first?"
        - "Are we ready for organization-wide AI transformation?"
        
        **Financial Analysis:**
        - "What's our total investment requirement and expected returns?"
        - "How does our budget allocation compare to industry standards?"
        - "What's the payback period for each department?"
        
        **Risk Assessment:**
        - "What are the main implementation risks we should watch out for?"
        - "Which departments have the highest change management risk?"
        - "How can we mitigate technical integration risks?"
        
        **Performance Insights:**
        - "Compare productivity gains between HR and Finance initiatives"
        - "Which functions show the strongest alignment with our objectives?"
        - "What timeline should we follow for maximum impact?"
        
        **Tips for Better Responses:**
        - Be specific about what you want to know
        - Reference particular departments or metrics when relevant
        - Ask follow-up questions to dive deeper into insights
        - Use the suggested questions as starting points
        """)
    
    # Data requirements notice
    if data_completeness < 60:
        st.info("""
        **💡 To get the most valuable insights from the AI Assistant:**
        - Configure baseline data for your enterprise functions
        - Set up AI initiatives with investment details
        - Define corporate objectives and KPIs
        - Specify budget constraints and change management readiness
        
        The more complete your data, the more accurate and useful the AI insights will be.
        """)
    
    # Status indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Assistant Status")
    
    if context_data:
        st.sidebar.success("✅ AI Assistant Ready")
        st.sidebar.markdown(f"Data completeness: {data_completeness:.0f}%")
        
        if st.session_state.ai_assistant.conversation_history:
            conversation_length = len(st.session_state.ai_assistant.conversation_history) // 2
            st.sidebar.markdown(f"Questions asked: {conversation_length}")
    else:
        st.sidebar.warning("⚠️ Limited Data Available")
        st.sidebar.markdown("Configure dashboard sections for better insights")