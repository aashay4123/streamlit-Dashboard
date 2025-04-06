import streamlit as st
import pandas as pd
from utils import load_data, compute_metrics

# Sidebar navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio(
    "Go to", ["🏠 Home", "📧 Recruiters", "🏢 Companies", "💼 Jobs"])

# Page router logic
if page == "🏠 Home":
    st.title("📬 Full Outreach Summary")
    recruiters, companies, jobs = load_data()
    metrics = compute_metrics(recruiters)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Emails", metrics["total"])
    col2.metric("Sent", metrics["sent"])
    col3.metric("Failed", metrics["failed"])
    col4.metric("Follow-Ups", metrics["followup"])
    col5.metric("Read", metrics["read"])

    st.markdown("## 🏢 Company Email Volume")
    company_df = pd.DataFrame.from_dict(
        metrics["by_company"], orient="index", columns=["Email Count"])
    st.bar_chart(company_df)

    st.markdown("## 💼 Job Posting Volume")
    job_df = pd.DataFrame.from_dict(
        metrics["by_job"], orient="index", columns=["Recruiter Count"])
    st.bar_chart(job_df)

elif page == "📧 Recruiters":
    import Recruiters
elif page == "🏢 Companies":
    import Companies
elif page == "💼 Jobs":
    import Job_Board
