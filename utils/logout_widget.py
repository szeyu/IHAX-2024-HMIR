import streamlit as st

def logout_widget():
    with st.sidebar:
        if(st.button("Logout")):
            st.session_state["authenticated"] = False
            st.session_state["pages"] = "login"
            st.rerun()