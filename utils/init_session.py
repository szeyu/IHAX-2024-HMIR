import streamlit as st

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False
    if "pages" not in st.session_state:
        st.session_state['pages'] = 'login'
    if "userID" not in st.session_state:
        st.session_state['userID'] = ''
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_admin" not in st.session_state:
        st.session_state['is_admin'] = False

