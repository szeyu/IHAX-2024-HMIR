import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.logout_widget import logout_widget

# File paths
CSV_FILE = 'database/tutor.csv'
UPLOAD_DIR = 'uploads'

def admin():
    # Custom CSS for clean design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f7f7f7;
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
    .file-card {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
    }
    .file-card:hover {
        transform: scale(1.02);
    }
    .file-info strong {
        color: #2c3e50;
        display: block;
        margin-bottom: 10px;
    }
    .status-approved {
        background-color: #2ecc71;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
    }
    .status-rejected {
        background-color: #e74c3c;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
    }
    .status-pending {
        background-color: #f39c12;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
    }
    .decision-buttons {
        margin-top: 10px;
    }
    .decision-buttons button {
        margin-right: 10px;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
    }
    .approve-button {
        background-color: #2ecc71;
        color: white;
        border: none;
    }
    .reject-button {
        background-color: #e74c3c;
        color: white;
        border: none;
    }
    .approve-button:hover, .reject-button:hover {
        cursor: pointer;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header'><h1>Admin Page - Review Tutor Uploads</h1></div>", unsafe_allow_html=True)

    logout_widget()

    # Ensure the database directory exists
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    # Function to load existing data or create a new dataframe if the file doesn't exist
    def load_data():
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            return df
        else:
            return pd.DataFrame(columns=['id', 'filename', 'subject', 'description', 'grade', 'upload_date', 'avg_rating', 'num_ratings', 'system_prompt', 'file_path', 'userID', 'status'])

    # Function to save data back to the CSV file
    def save_data(df):
        df.to_csv(CSV_FILE, index=False)

    # Load the data
    df = load_data()

    # Filter for files with 'pending' status
    pending_files = df[df['status'] == 'pending']

    if pending_files.empty:
        st.write("No pending files for approval.")
    else:
        st.markdown("<div class='section'><h2>Pending Files for Review</h2></div>", unsafe_allow_html=True)

        for _, row in pending_files.iterrows():
            with st.expander(f"{row['subject']} - {row['grade']} (Uploaded by User {row['userID']})"):
                st.markdown(f"""
                <div class='file-card'>
                    <div class='file-info'><strong>Filename:</strong> {row['filename']}</div>
                    <div class='file-info'><strong>Description:</strong> {row['description']}</div>
                    <div class='file-info'><strong>Upload Date:</strong> {row['upload_date']}</div>
                    <div class='file-info'><strong>Average Rating:</strong> {row['avg_rating']:.1f} ({row['num_ratings']} ratings)</div>
                    <div class='file-info'><strong>System Prompt:</strong> {row['system_prompt']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Add a download button for the file
                with open(row['file_path'], "rb") as file:
                    st.download_button(
                        label="Download File",
                        data=file,
                        file_name=row['filename'],
                        mime="application/octet-stream",
                        key=f"download_{row['id']}"
                    )

                # Provide options for approval or rejection
                decision = st.radio(
                    f"Approve or Reject this file (ID: {row['id']})",
                    ('Pending', 'Approved', 'Rejected'),
                    index=['pending', 'approved', 'rejected'].index(row['status']),
                    key=f"decision_{row['id']}"
                )

                # Update the status in the dataframe
                if st.button(f"Submit decision for {row['filename']}", key=f"submit_{row['id']}"):
                    df.loc[df['id'] == row['id'], 'status'] = decision.lower()
                    df.loc[df['id'] == row['id'], 'admin_decision_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(df)
                    st.success(f"File {row['filename']} has been {decision.lower()}.")

if __name__ == "__main__":
    admin()
