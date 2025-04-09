import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data, compute_metrics

import Recruiters
import Companies
import Job_Board

# ✅ Must be first command
st.set_page_config(page_title="📊 Full Outreach Dashboard", layout="wide")

# Load data once and reuse
recruiters, companies, jobs = load_data()
metrics = compute_metrics(recruiters)

# Sidebar navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📧 Recruiters", "🏢 Companies", "💼 Jobs"])

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("📬 Full Outreach Summary")

    st.divider()
    st.markdown("### 📈 Metrics Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📊 Total Emails", metrics["total"])
    col2.metric("📤 Sent", metrics["sent"])
    col3.metric("❌ Failed", metrics["failed"])
    col4.metric("🔁 Follow-Ups", metrics["followup"])
    col5.metric("📖 Read", metrics["read"])

    st.markdown(f"""
    > You have contacted **{metrics['total']}** recruiters so far.  
    > Of these, **{metrics['sent']}** were successful, **{metrics['failed']}** failed, and  
    > **{metrics['read']}** have been read.
    """)

    st.divider()
    st.markdown("### 🏢 Company Email Volume")

    company_df = pd.DataFrame.from_dict(metrics["by_company"], orient="index", columns=["Email Count"])
    company_df.index.name = "Company"
    company_df = company_df.reset_index()

    company_chart = alt.Chart(company_df).mark_bar().encode(
        x=alt.X('Company:N', sort='-y'),
        y='Email Count:Q',
        tooltip=['Company', 'Email Count']
    ).properties(width=700, height=400)

    st.altair_chart(company_chart, use_container_width=True)

    st.divider()
    st.markdown("### 💼 Job Posting Volume")

    job_df = pd.DataFrame.from_dict(metrics["by_job"], orient="index", columns=["Recruiter Count"])
    job_df.index.name = "Job"
    job_df = job_df.reset_index()

    job_chart = alt.Chart(job_df).mark_bar().encode(
        x=alt.X('Job:N', sort='-y'),
        y='Recruiter Count:Q',
        tooltip=['Job', 'Recruiter Count']
    ).properties(width=700, height=400)

    st.altair_chart(job_chart, use_container_width=True)

    st.divider()
    st.markdown("### 📬 Email Log")

    with st.expander("View Email Details"):
        st.dataframe(recruiters)
    
    def convert_df_to_csv_bytes(df: pd.DataFrame) -> bytes:
        return df.to_csv(index=False).encode("utf-8")
    
    if not recruiters.empty:
        csv = convert_df_to_csv_bytes(recruiters)
        st.download_button(
            label="⬇️ Download Email Log as CSV",
            data=csv,
            file_name="outreach_log.csv",
            mime="text/csv",
        )

# --- RECRUITERS PAGE ---
elif page == "📧 Recruiters":
    Recruiters.render()

# --- COMPANIES PAGE ---
elif page == "🏢 Companies":
    Companies.render()

# --- JOBS PAGE ---
elif page == "💼 Jobs":
    Job_Board.render()
