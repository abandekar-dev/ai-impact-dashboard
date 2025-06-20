import streamlit as st
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Impact Predictive Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'ai_initiatives' not in st.session_state:
    st.session_state.ai_initiatives = {}
if 'baseline_data' not in st.session_state:
    st.session_state.baseline_data = {}

def main():
    st.title("🎯 AI Impact Predictive Dashboard")
    st.markdown("### Enterprise AI Implementation Analysis Platform")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis",
        ["Overview", "Function Analysis", "Executive Summary"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Function Analysis":
        show_function_analysis()
    elif page == "Executive Summary":
        show_executive_summary()

def show_overview():
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Functions", len(st.session_state.ai_initiatives))
    
    with col2:
        total_investment = sum(
            init.get('investment', 0) 
            for func_data in st.session_state.ai_initiatives.values() 
            for init in func_data.values()
        )
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col3:
        st.metric("Active Projects", "Coming Soon")
    
    with col4:
        st.metric("Predicted ROI", "Coming Soon")
    
    st.markdown("---")
    
    # Getting Started Guide
    st.subheader("Getting Started")
    st.markdown("""
    1. **Navigate to Function Analysis** to configure your enterprise functions
    2. **Add AI initiatives** for each business function
    3. **Review predictions** in the Executive Summary
    4. **Export reports** for stakeholder presentation
    """)

def show_function_analysis():
    st.header("Function Analysis")
    
    # Function selection
    function_types = [
        "Finance & Accounting", "Human Resources", "Operations & Supply Chain",
        "Sales & Marketing", "Customer Service", "IT & Technology",
        "Legal & Compliance", "R&D & Innovation", "Executive Leadership"
    ]
    
    selected_function = st.selectbox("Select Enterprise Function", function_types)
    
    if selected_function:
        st.subheader(f"{selected_function} Configuration")
        
        # Initialize function data if not exists
        if selected_function not in st.session_state.ai_initiatives:
            st.session_state.ai_initiatives[selected_function] = {}
        
        # AI Initiative Configuration
        with st.expander("Add New AI Initiative", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                initiative_name = st.text_input("Initiative Name")
                ai_type = st.selectbox("AI Type", [
                    "Machine Learning", "Natural Language Processing", 
                    "Computer Vision", "Robotic Process Automation",
                    "Predictive Analytics", "Chatbots & Virtual Assistants"
                ])
                complexity = st.selectbox("Complexity", ["Low", "Medium", "High"])
            
            with col2:
                investment = st.number_input("Investment ($)", min_value=0, value=50000)
                timeline = st.number_input("Timeline (months)", min_value=1, max_value=36, value=6)
                expected_roi = st.number_input("Expected ROI (%)", min_value=0, value=15)
            
            if st.button("Add Initiative"):
                if initiative_name:
                    st.session_state.ai_initiatives[selected_function][initiative_name] = {
                        'type': ai_type,
                        'complexity': complexity,
                        'investment': investment,
                        'timeline': timeline,
                        'expected_roi': expected_roi,
                        'created': datetime.now().isoformat()
                    }
                    st.success(f"Added {initiative_name} to {selected_function}")
                    st.rerun()
        
        # Display existing initiatives
        if st.session_state.ai_initiatives[selected_function]:
            st.subheader("Current Initiatives")
            
            for name, data in st.session_state.ai_initiatives[selected_function].items():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{name}**")
                        st.write(f"Type: {data['type']}")
                    
                    with col2:
                        st.write(f"Investment: ${data['investment']:,.0f}")
                        st.write(f"Timeline: {data['timeline']} months")
                    
                    with col3:
                        st.write(f"Complexity: {data['complexity']}")
                        st.write(f"Expected ROI: {data['expected_roi']}%")
                    
                    with col4:
                        if st.button("Remove", key=f"remove_{name}"):
                            del st.session_state.ai_initiatives[selected_function][name]
                            st.rerun()
                    
                    st.markdown("---")

def show_executive_summary():
    st.header("Executive Summary")
    
    if not any(st.session_state.ai_initiatives.values()):
        st.info("No AI initiatives configured yet. Please add initiatives in Function Analysis.")
        return
    
    # Summary metrics
    total_functions = len([f for f in st.session_state.ai_initiatives.values() if f])
    total_initiatives = sum(len(initiatives) for initiatives in st.session_state.ai_initiatives.values())
    total_investment = sum(
        init.get('investment', 0) 
        for func_data in st.session_state.ai_initiatives.values() 
        for init in func_data.values()
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Functions Configured", total_functions)
    
    with col2:
        st.metric("Total Initiatives", total_initiatives)
    
    with col3:
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    st.markdown("---")
    
    # Function breakdown
    st.subheader("Initiative Breakdown by Function")
    
    for function, initiatives in st.session_state.ai_initiatives.items():
        if initiatives:
            st.write(f"**{function}** ({len(initiatives)} initiatives)")
            
            for name, data in initiatives.items():
                st.write(f"  • {name}: ${data['investment']:,.0f} ({data['timeline']} months)")
    
    # Export functionality
    st.markdown("---")
    st.subheader("Export Data")
    
    if st.button("Download Configuration"):
        config_data = {
            'export_date': datetime.now().isoformat(),
            'initiatives': st.session_state.ai_initiatives,
            'summary': {
                'total_functions': total_functions,
                'total_initiatives': total_initiatives,
                'total_investment': total_investment
            }
        }
        
        st.download_button(
            label="Download JSON",
            data=json.dumps(config_data, indent=2),
            file_name=f"ai_initiatives_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()