import streamlit as st
import random

# Simple function to provide yes/no responses
def simple_yes_no_response():
    return random.choice(["Yes", "No"])

# Main app function
def chatbot():
    st.title("Simple Yes/No Chatbot")
    
    # a button to go back
    with st.sidebar:
        if(st.button("Back")):
            st.session_state["pages"] = "student"
            st.rerun()

    # If the chat has been cleared, reset the chat history
    if "clear_chat" in st.session_state and st.session_state.clear_chat:
        st.session_state.chat_history = []
        st.session_state.clear_chat = False  # Reset the flag after clearing

    # Container for chat history
    chat_container = st.container()

    # Display chat history
    with chat_container:
        st.header("Chat with the Bot")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Keep input box at the bottom
    question = st.chat_input("Ask a question (you will get 'Yes' or 'No' answers)")

    if question:
        # Save user's question to the chat history
        st.session_state.chat_history.append({"role": "user", "content": question})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(question)

        # Get a yes/no response and display it
        response = simple_yes_no_response()
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response)

    # Clear chat button
    if st.button("Double Click to Clear Chat"):
        st.session_state.clear_chat = True  # Set the flag to clear the chat
        st.session_state.chat_history = []  # Clear the chat history