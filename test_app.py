import streamlit as st

st.title("AI Impact Predictive Dashboard - Test Version")
st.write("Testing basic Streamlit functionality...")

# Test basic components
st.sidebar.title("Navigation")
st.sidebar.write("This is a test to verify Streamlit is working")

col1, col2 = st.columns(2)
with col1:
    st.metric("Test Metric 1", "100")
with col2:
    st.metric("Test Metric 2", "200")

st.success("Basic Streamlit functionality is working!")