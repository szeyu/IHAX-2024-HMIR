import streamlit as st
import pandas as pd

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users_df = pd.read_csv('database/users.csv')
        user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]

        if not user.empty:
            st.session_state['authenticated'] = True
            st.session_state['pages'] = user.iloc[0]['role']
            st.session_state['userID'] = user.iloc[0]['userID']
            st.success(f"Logged in as {username}")
            print(f"Logged in as {username} with userID={st.session_state['userID']}")
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Go to Signup"):
        st.session_state['pages'] = 'signup'
        st.rerun()