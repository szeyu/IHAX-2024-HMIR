import streamlit as st

def init_session():
    """
    Initialize the session state to handle user authentication and other session data.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "pages" not in st.session_state:
        st.session_state["pages"] = "login"

    if "userID" not in st.session_state:
        st.session_state["userID"] = ""

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "message_count" not in st.session_state:
        st.session_state["message_count"] = 0

    if "rating_given" not in st.session_state:
        st.session_state["rating_given"] = False

    if "show_rating_prompt" not in st.session_state:
        st.session_state["show_rating_prompt"] = False

