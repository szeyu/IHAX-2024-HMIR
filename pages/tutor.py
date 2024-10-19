import streamlit as st
from utils.logout_widget import logout_widget
import pandas as pd
import os
from datetime import datetime
import json

# Files to store the tutor uploads metadata and ratings
CSV_FILE = 'database/tutor.csv'
UPLOAD_DIR = 'uploads'

def tutor():
    st.title("Tutor Page")

    logout_widget()
    
    # Check if the user is authenticated and is a tutor
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Please log in to view this page.")
        st.stop()

    userID = st.session_state['userID']

    # Ensure the database and upload directories exist
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Function to load existing data or create a new dataframe if the file doesn't exist
    def load_data():
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            return df
        else:
            return pd.DataFrame(columns=['id', 'filename', 'subject', 'description', 'grade', 'upload_date', 'avg_rating', 'num_ratings', 'system_prompt', 'file_path', 'userID'])

    # Function to save uploaded file
    def save_uploaded_file(uploaded_file):
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    # Function to save data
    def save_data(df):
        df.to_csv(CSV_FILE, index=False)

    # Load existing data
    df = load_data()

    # Input fields for file upload
    subject = st.text_input("Subject")
    uploaded_file = st.file_uploader("Choose a file")
    description = st.text_area("Description")
    grade = st.selectbox("Suitable for Grade", [f"Primary {i}" for i in range(1, 7)] + [f"Secondary {i}" for i in range(1, 6)])

    if st.button("Upload"):
        if uploaded_file is not None and subject and description and grade:
            file_path = save_uploaded_file(uploaded_file)
            new_id = df['id'].max() + 1 if len(df) > 0 else 1
            new_row = pd.DataFrame({
                'id': [new_id],
                'filename': [uploaded_file.name],
                'subject': [subject],
                'description': [description],
                'grade': [grade],
                'upload_date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                'avg_rating': [0.0],
                'num_ratings': [0],
                'system_prompt': [f"You are the {subject} teacher"],
                'file_path': [file_path],
                'userID': [userID]  # Store the current logged-in user's userID
            })
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("File successfully uploaded")
        else:
            st.error("Please fill all fields and upload a file")

    # Display uploaded materials
    st.header("Your Uploaded Materials")
    user_materials = df[df['userID'] == userID]
    if user_materials.empty:
        st.write("You haven't uploaded any files yet.")
    else:
        for _, row in user_materials.iterrows():
            with st.expander(f"{row['subject']} - {row['grade']}"):
                st.write(f"Filename: {row['filename']}")
                st.write(f"Description: {row['description']}")
                st.write(f"Upload Date: {row['upload_date']}")
                st.write(f"Average Rating: {row['avg_rating']:.1f}")
                st.write(f"Number of Ratings: {row['num_ratings']}")
                st.write(f"System Prompt: {row['system_prompt']}")
                
                # Add a download button for the file with a unique key
                with open(row['file_path'], "rb") as file:
                    st.download_button(
                        label="Download File",
                        data=file,
                        file_name=row['filename'],
                        mime="application/octet-stream",
                        key=f"download_{row['id']}"  # Unique key for each download button
                    )

if __name__ == "__main__":
    tutor()