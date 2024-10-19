import streamlit as st
from utils.logout_widget import logout_widget

def admin():
    st.title("Admin Page")
    logout_widget()
    