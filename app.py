import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("linkedin_jobs.csv")
    return df

st.markdown("### ") 
st.markdown("<span style='color: yellow; font-size: 30px;'>  Developed by: Ali Abid, ID: 380054</span>", unsafe_allow_html=True)



# Main app
st.title("LinkedIn Jobs Trends Analyzer")

# Load data
df = load_data()

if df.empty:
    st.warning("CSV is empty or missing required columns.")
else:
    st.success("Data loaded successfully!")

    # Display raw data
    if st.checkbox("Show raw data"):
        st.dataframe(df)

    # Top 5 most in-demand job titles
    st.subheader("Top 5 Most In-Demand Jobs")
    top_titles = df['Title'].value_counts().head(5)
    st.bar_chart(top_titles)


    # Cities with highest number of openings
    st.subheader("Cities with Highest Job Openings")
    if 'Location' in df.columns:
        city_counts = df['Location'].value_counts().head(10)
        st.bar_chart(city_counts)

    # Posting trends 
    st.subheader("Posting Trends Over Time")
    if 'Date Posted' in df.columns:
        df['Date Posted'] = pd.to_datetime(df['Date Posted'], errors='coerce')
        df = df.dropna(subset=['Date Posted'])  # 

        df['Post Date'] = df['Date Posted'].dt.date
        trend = df.groupby('Post Date').size().reset_index(name='Count')
        trend = trend.sort_values('Post Date')

        st.line_chart(trend.set_index('Post Date'))
    else:
        st.warning("No 'Date Posted' column found in the dataset.")

    # Button to manually refresh data
    if st.button("🔁 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
