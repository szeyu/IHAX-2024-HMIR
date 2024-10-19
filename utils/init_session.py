import streamlit as st
import os
from jamaibase import JamAI
import dotenv
dotenv.load_dotenv()

JAMAIBASE_API_KEY = os.getenv("JAMAIBASE_API_KEY")
PROJ_ID = os.getenv("PROJ_ID")

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False
    if "pages" not in st.session_state:
        st.session_state['pages'] = 'login'
    if "userID" not in st.session_state:
        st.session_state['userID'] = ''
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = "You are helpful assistant"
    if "knowledge_base_id" not in st.session_state:
        st.session_state["knowledge_base_id"] = "tutor-1-algebra"
        
    # Initialize JamAI client
    if "jamai_client" not in st.session_state:
        st.session_state.jamai_client = JamAI(api_key=JAMAIBASE_API_KEY, project_id=PROJ_ID)
