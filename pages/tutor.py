import streamlit as st
from utils.logout_widget import logout_widget
import pandas as pd
import os
from datetime import datetime

# Files to store the tutor uploads metadata and ratings
CSV_FILE = 'database/tutor.csv'
UPLOAD_DIR = 'uploads'

def tutor():
    # Custom CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f6;
        color: #1e1e1e;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .header {
        background-color: #3498db;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .header h1 {
        margin: 0;
        font-size: 2.5em;
    }
    .section {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .section h2 {
        color: #3498db;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .upload-form label {
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
    }
    .upload-form input, .upload-form select, .upload-form textarea {
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .upload-form button {
        background-color: #2ecc71;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
    }
    .upload-form button:hover {
        background-color: #27ae60;
    }
    .file-card {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .file-card h3 {
        margin-top: 0;
        color: #3498db;
    }
    .status {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
    }
    .status-pending { background-color: #f39c12; color: white; }
    .status-approved { background-color: #2ecc71; color: white; }
    .status-rejected { background-color: #e74c3c; color: white; }
    .download-btn {
        background-color: #3498db;
        color: white;
        padding: 5px 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        font-size: 0.9em;
    }
    .download-btn:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown("""
    <div class="container">
        <div class="header">
            <h1>Tutor Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)

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
            if 'status' not in df.columns:
                df['status'] = 'pending'
            return df
        else:
            return pd.DataFrame(columns=['id', 'username', 'filename', 'subject', 'description', 'grade', 'upload_date', 'avg_rating', 'num_ratings', 'system_prompt', 'file_path', 'userID', 'status'])

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

    # Upload Material Section
    st.markdown("""
    <div class="section">
        <h2>Upload New Material</h2>
        <form class="upload-form">
    """, unsafe_allow_html=True)

    subject = st.text_input("Subject")
    grade = st.selectbox("Suitable for Grade", [f"Primary {i}" for i in range(1, 7)] + [f"Secondary {i}" for i in range(1, 6)])
    uploaded_file = st.file_uploader("Choose a file")
    description = st.text_area("Description")

    if st.button("Upload Material"):
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
                'userID': [userID],
                'status': ['pending']
            })
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("File successfully uploaded and pending approval")
        else:
            st.error("Please fill all fields and upload a file")

    st.markdown("""
        </form>
    </div>
    """, unsafe_allow_html=True)

    # My Uploads Section
    st.markdown("""
    <div class="section">
        <h2>Your Uploaded Materials</h2>
    """, unsafe_allow_html=True)

    user_materials = df[df['userID'] == userID]
    if user_materials.empty:
        st.info("You haven't uploaded any files yet.")
    else:
        for _, row in user_materials.iterrows():
            status_class = f"status-{row['status']}"
            st.markdown(f"""
            <div class="file-card">
                <h3>{row['subject']} - {row['grade']}</h3>
                <p><strong>Filename:</strong> {row['filename']}</p>
                <p><strong>Description:</strong> {row['description']}</p>
                <p><strong>Upload Date:</strong> {row['upload_date']}</p>
                <p><strong>Average Rating:</strong> {row['avg_rating']:.1f} ({row['num_ratings']} ratings)</p>
                <p><span class="status {status_class}">{row['status'].capitalize()}</span></p>
            </div>
            """, unsafe_allow_html=True)

            with open(row['file_path'], "rb") as file:
                st.download_button(
                    label="Download File",
                    data=file,
                    file_name=row['filename'],
                    mime="application/octet-stream",
                    key=f"download_{row['id']}"
                )

    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    tutor()