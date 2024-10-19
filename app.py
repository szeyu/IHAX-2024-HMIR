import streamlit as st
from utils.init_session import init_session
from pages.login import login
from pages.signup import signup
from pages.admin import admin
from pages.tutor import tutor
from pages.student import student

# Clear the sidebar
st.sidebar.empty()

init_session()

# A container for the main content
main_container = st.container()
with main_container:
    if st.session_state['authenticated']:
        if st.session_state['pages'] == 'admin':
            admin()
        elif st.session_state['pages'] == 'tutor':
            tutor()
        elif st.session_state['pages'] == 'student':
            student()
    else:
        if st.session_state['pages'] == 'login':
            login()
        elif st.session_state['pages'] == 'signup':
            signup()