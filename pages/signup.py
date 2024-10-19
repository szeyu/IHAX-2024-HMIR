import streamlit as st
import pandas as pd

def signup():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "tutor", "admin"])

    if st.button("Sign Up"):
        users_df = pd.read_csv("database/users.csv")

        if username in users_df['username'].values:
            st.error("Username already exists")
        else:
            new_user = pd.DataFrame({
                'userID': [users_df['userID'].max() + 1],
                'username': [username],
                'password': [password],
                'role': [role]
            })
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv('database/users.csv', index=False)
            st.success("Account created successfully")
            st.session_state['pages'] = 'login'
            st.rerun()

    if st.button("Go to Login"):
        st.session_state['pages'] = 'login'
        st.rerun()