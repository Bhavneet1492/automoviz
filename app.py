import streamlit as st
from apps import phase1

#setting the page configuration
st.set_page_config(
    page_title="Data cleaning",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "Data Cleaning": phase1,
    "Data Visualization": phase1,
    "Make Predictions": phase1,
    "Business Insights": phase1,
    "Customer Segmentation": phase1,
}

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Select operation", list(PAGES.keys()))
page = PAGES[selection]
page.app()