import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.logout_widget import logout_widget

# File paths
CSV_FILE = 'database/tutor.csv'
UPLOAD_DIR = 'uploads'

def admin():
    st.title("Admin Page - Review Tutor Uploads")
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
        st.header("Pending Files for Review")
        
        for _, row in pending_files.iterrows():
            with st.expander(f"{row['subject']} - {row['grade']} (Uploaded by User {row['userID']})"):
                st.write(f"Filename: {row['filename']}")
                st.write(f"Description: {row['description']}")
                st.write(f"Upload Date: {row['upload_date']}")
                st.write(f"Average Rating: {row['avg_rating']:.1f}")
                st.write(f"Number of Ratings: {row['num_ratings']}")
                st.write(f"System Prompt: {row['system_prompt']}")
                
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
