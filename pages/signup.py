import streamlit as st
import pandas as pd

def signup():
    # Custom CSS for styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
    }
    .signup-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .signup-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #3498db;
        margin-bottom: 20px;
    }
    .signup-input {
        margin-bottom: 15px;
    }
    .signup-button {
        width: 100%;
        padding: 10px;
        background-color: #2ecc71;
        color: white;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .signup-button:hover {
        background-color: #27ae60;
    }
    .login-link {
        text-align: center;
        margin-top: 15px;
    }
    .login-link button {
        background-color: #3498db;
        color: white;
        padding: 10px;
        width: 100%;
        border-radius: 5px;
        border: none;
        font-size: 1rem;
        font-weight: bold;
    }
    .login-link button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sign Up container
    st.markdown("<div class='signup-container'>", unsafe_allow_html=True)

    # Title for the sign up page
    st.markdown("<h1 class='signup-title'>Sign Up</h1>", unsafe_allow_html=True)

    # Input fields for username, password, and role
    username = st.text_input("Username", placeholder="Choose a username", key="signup_username", help="Enter your desired username")
    password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password", help="Enter a strong password")
    role = st.selectbox("Role", ["student", "tutor", "admin"], help="Select your role")

    # Sign Up button
    if st.button("Sign Up", key="signup_button"):
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

    # Go to Login button
    st.markdown("<div class='login-link'>", unsafe_allow_html=True)
    if st.button("Go to Login", help="Click to return to the login page"):
        st.session_state['pages'] = 'login'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Closing the sign up container
    st.markdown("</div>", unsafe_allow_html=True)

# Run the signup function when this file is executed
if __name__ == "__main__":
    signup()
