import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils.logout_widget import logout_widget

users_df = pd.read_csv('database/users.csv')
tutors_df = pd.read_csv('database/tutor.csv')

merged_df = pd.merge(tutors_df, users_df, left_on='id', right_on='userID', how='left')

def student():
    st.title("Welcome, Student!")
    logout_widget()

    learning_data = {
        "Week": [f"Week {i}" for i in range(1, 13)],
        "Learning Hours": np.random.randint(5, 20, size=12),  
    }
    learning_df = pd.DataFrame(learning_data)

    tabs = ["Analytics", "Find Tutor"]
    selected_tab = st.tabs(tabs)

    st.markdown(
        """
        <style>
        .title-style {
            font-size:40px;
            color:#ff4b4b;  
            font-weight: bold;
        }
        .custom-border {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #f7f7f7;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .border-container {
            border: 1px solid #FF4B4B; /* Smaller border width */
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: #fff;
            transition: transform 0.2s; /* Smooth scaling effect */
        }
        .border-container:hover {
            transform: scale(1.02); /* Slightly enlarge on hover */
        }
        .tutor-info {
            color: #333; /* Darker text color for better readability */
        }
        .analytics-info {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .analytic-card {
            background-color: #f9f9f9;
            border: 1px solid #FF4B4B;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            flex: 1 1 200px; /* Adjusts the size */
            max-width: 300px; /* Maximum width of each card */
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Home Page
    with selected_tab[0]:
        st.subheader("Learning Time Analytics")

        chart = alt.Chart(learning_df).mark_area(
            line={'color': 'darkblue'}, 
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#FFB3BA', offset=0),  
                       alt.GradientStop(color='#FFDFBA', offset=0.2),  
                       alt.GradientStop(color='#FFFFBA', offset=0.4), 
                       alt.GradientStop(color='#BAFFC9', offset=0.6), 
                       alt.GradientStop(color='#BAE1FF', offset=0.8),  
                       alt.GradientStop(color='#B3BAFF', offset=1)]
            )
        ).encode(
            x='Week',
            y='Learning Hours'
        ).properties(
            width=700,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        # Analyzation section
        total_hours = learning_df["Learning Hours"].sum()
        average_hours = learning_df["Learning Hours"].mean()
        max_hours = learning_df["Learning Hours"].max()
        min_hours = learning_df["Learning Hours"].min()

        st.markdown("<h4 style='text-align: center;'>Learning Statistics</h4>", unsafe_allow_html=True)

        # Create a container for the analytics cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"<div class='analytic-card'><strong>Total Learning Hours:</strong><br>{total_hours}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div class='analytic-card'><strong>Average Learning Hours:</strong><br>{average_hours:.2f}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='analytic-card'><strong>Max Learning Hours:</strong><br>{max_hours}</div>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<div class='analytic-card'><strong>Min Learning Hours:</strong><br>{min_hours}</div>", unsafe_allow_html=True)

        # Provide feedback based on average hours
        if average_hours < 10:
            st.write("You may want to increase your learning time to meet your goals!")
        else:
            st.write("Great job! You're spending a good amount of time learning each week.")

    # Find Tutor Page
    with selected_tab[1]:
        st.subheader("Find a Tutor by Grade, Subject, or Name")

        selected_grades = st.multiselect("Select Grades", merged_df["grade"].unique())
        selected_subjects = st.multiselect("Select Subjects", merged_df["subject"].unique())

        search_query = st.text_input("Search Tutor by Name", placeholder="e.g., Ali bin Abu")

        if selected_grades:
            filtered_tutors = merged_df[merged_df["grade"].isin(selected_grades)]
        else:
            filtered_tutors = merged_df

        if selected_subjects:
            filtered_tutors = filtered_tutors[filtered_tutors["subject"].isin(selected_subjects)]

        if search_query:
            filtered_tutors = filtered_tutors[filtered_tutors["username"].str.contains(search_query, case=False)]

        filtered_tutors = filtered_tutors.sort_values(by="avg_rating", ascending=False)

        if not filtered_tutors.empty:
            st.write("Available Tutors:")

            for index, tutor in filtered_tutors.iterrows():
                tutor_info_html = f"""
                    <div class='border-container tutor-info'>
                        <strong>Tutor Name:</strong> {tutor['username']}<br>
                        <strong>Subject:</strong> {tutor['subject']}<br>
                        <strong>Grade:</strong> {tutor['grade']}<br>
                        <strong>Average Rating:</strong> {tutor['avg_rating']}<br>
                    </div>
                """
                st.markdown(tutor_info_html, unsafe_allow_html=True)

                if st.button(f"Start Chat with {tutor['username']}", key=f"chat_{index}"):
                    st.success(f"Connecting to {tutor['username']}'s chatbot...")
                    st.session_state["file_path"] = tutor["file_path"]
                    st.session_state["pages"] = "chatbot"
                    st.rerun()

        else:
            st.write("No tutors available for the selected grade, subject, or name.")
