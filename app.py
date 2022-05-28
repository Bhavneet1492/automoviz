import streamlit as st
from apps import phase1,phase2,phase3,phase4,phase5



PAGES = {
    "Data Cleaning": phase1,
    "Data Visualization": phase2,
    "Make Predictions": phase3,
    "Business Insights": phase4,
    "Customer Segmentation": phase5,
}

#setting the page configuration
st.set_page_config(
    page_title="Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Select operation", list(PAGES.keys()))
page = PAGES[selection]
page.app()
