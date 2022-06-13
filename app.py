# importing streamlit and apps for each page from the "apps" folder

import streamlit as st
from apps import phase1,phase2,phase3,phase4,phase5


# linking page names on sidebar to app files in the "app" folder

PAGES = {
    "Data Cleaning": phase1,
    "Data Visualization": phase2,
    "Make Predictions": phase3,
    "Business Insights": phase4,
    "Customer Segmentation": phase5,
} 


# setting the page configuration

st.set_page_config(
    page_title="Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# hiding the menu and the footer

hide_menu_style="""
                <style>
                   #MainMenu {visibility:hidden;} 
                   footer {visibility:hidden;} 
                </style>
                """
st.markdown(hide_menu_style,True)


# setting the sidebar for navigating through multiple apps (or pages or dashboards)

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Select operation", list(PAGES.keys()))  # option that the user chooses from the sidebar
page = PAGES[selection] # PAGES value (app name from the "apps" folder) with user's choice as the key
page.app() # running the app for the selected page choice 
