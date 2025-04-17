import streamlit as st
import sqlite3
import pandas as pd

# Function to connect to SQLite and fetch data
def fetch_data():
    conn = sqlite3.connect('gym_classes.db')
    df = pd.read_sql_query("SELECT * FROM classes", conn)
    conn.close()
    return df

# Streamlit app title
st.title("Gym Web Scraper")

# Display a short description
st.write("This app shows gym class schedules scraped from the website.")

# Fetch gym data
df = fetch_data()

# Display the data in a table
st.write("### Gym Classes Schedule", df)

# Add a filter option for schedule
schedule_filter = st.selectbox("Filter by Day", ["All Days"] + list(df['schedule'].unique()))

# Filter the data based on the selected schedule
if schedule_filter != "All Days":
    filtered_df = df[df['schedule'] == schedule_filter]
else:
    filtered_df = df

# Display filtered data
st.write(f"### Classes on {schedule_filter}" if schedule_filter != "All Days" else "### All Classes", filtered_df)

# CSV export button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="gym_classes_schedule.csv",
    mime="text/csv"
)

# Optional: Chatbot-like feature (for querying)
query = st.text_input("Ask me about the gym schedule (e.g., 'Show me classes on Monday')")
if query:
    if "monday" in query.lower():
        monday_classes = df[df['schedule'].str.contains("Monday", case=False)]
        st.write(monday_classes)
    else:
        st.write("Sorry, I can only filter by days of the week. Try 'Monday', 'Tuesday', etc.")
