import streamlit as st
from utils.logout_widget import logout_widget

def student():
    st.title("Student Page")
    logout_widget()