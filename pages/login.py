import streamlit as st
import pandas as pd

def login():
    # Custom CSS for styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .login-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #3498db;
        margin-bottom: 20px;
    }
    .login-input {
        margin-bottom: 15px;
    }
    .login-button {
        width: 100%;
        padding: 10px;
        background-color: #3498db;
        color: white;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .login-button:hover {
        background-color: #2980b9;
    }
    .signup-link {
        text-align: center;
        margin-top: 15px;
    }
    .signup-link button {
        background-color: #2ecc71;
        color: white;
        padding: 10px;
        width: 100%;
        border-radius: 5px;
        border: none;
        font-size: 1rem;
        font-weight: bold;
    }
    .signup-link button:hover {
        background-color: #27ae60;
    }
    </style>
    """, unsafe_allow_html=True)

    # Login container
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    # EduKita title
    st.markdown("<h1 class='login-title'>Login</h1>", unsafe_allow_html=True)

    # Username and password input fields
    username = st.text_input("Username", placeholder="Enter your username", key="username", help="Please enter your registered username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="password", help="Please enter your password")

    # Login button
    if st.button("Login", key="login", help="Click to login to your account"):
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

    # Signup link
    st.markdown("<div class='signup-link'>", unsafe_allow_html=True)
    if st.button("Go to Signup", help="Click to create a new account"):
        st.session_state['pages'] = 'signup'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Closing the login container
    st.markdown("</div>", unsafe_allow_html=True)

# Run the login function when this file is executed
if __name__ == "__main__":
    login()
