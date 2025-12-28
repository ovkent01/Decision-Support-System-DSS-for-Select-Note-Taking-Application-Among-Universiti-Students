import streamlit as st
import home
import dashboard
from datacleanning import data_cleanning

data_cleanning()

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

with st.sidebar:
    st.header("Page Navigation")

    # Home 按钮
    if st.button("Home", key="nav_home"):
        st.session_state.page = 'Home'
    # Dashboard 按钮
    if st.button("Dash Board", key="nav_dashboard"):
        st.session_state.page = 'Dashboard'
    
    st.markdown("---")
    st.info(f"Current Page: **{st.session_state.page}**")

if st.session_state.page == 'Home':
    home.render_home_page()
elif st.session_state.page == 'Dashboard':
    dashboard.render_dashboard_page()