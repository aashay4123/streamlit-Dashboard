import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data, compute_metrics

import Recruiters
import Companies
import Job_Board

# ✅ Must be first command
st.set_page_config(page_title="📊 Full Outreach Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📧 Recruiters", "🏢 Companies", "💼 Jobs"])

# Load data
recruiters, companies, jobs = load_data()
metrics = compute_metrics(recruiters)

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("📬 Full Outreach Summary")

    st.divider()
    st.markdown("### 📈 Metrics Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📊 Total Emails", metrics.get("total", 0))
    col2.metric("📤 Sent", metrics.get("sent", 0))
    col3.metric("❌ Failed", metrics.get("failed", 0))
    col4.metric("🔁 Follow-Ups", metrics.get("followup", 0))
    col5.metric("📖 Read", metrics.get("read", 0))

    st.markdown(f"""
    > You have contacted **{metrics.get('total', 0)}** recruiters so far.  
    > Of these, **{metrics.get('sent', 0)}** were successful, **{metrics.get('failed', 0)}** failed, and  
    > **{metrics.get('read', 0)}** have been read.
    """)

    st.divider()
    st.markdown("### 🏢 Company Email Volume")

    # 🏢 Company Chart
    if metrics.get("by_company"):
        company_df = pd.DataFrame.from_dict(metrics["by_company"], orient="index", columns=["Email Count"])
        company_df.index.name = "Company"
        company_df = company_df.reset_index()

        company_chart = alt.Chart(company_df).mark_bar().encode(
            x=alt.X('Company:N', sort='-y'),
            y='Email Count:Q',
            tooltip=['Company', 'Email Count']
        ).properties(width=700, height=400)

        st.altair_chart(company_chart, use_container_width=True)
    else:
        st.info("No email data available by company.")

    st.divider()
    st.markdown("### 💼 Job Posting Volume")

    # 💼 Job Chart
    if metrics.get("by_job"):
        job_df = pd.DataFrame.from_dict(metrics["by_job"], orient="index", columns=["Recruiter Count"])
        job_df.index.name = "Job"
        job_df = job_df.reset_index()

        job_chart = alt.Chart(job_df).mark_bar().encode(
            x=alt.X('Job:N', sort='-y'),
            y='Recruiter Count:Q',
            tooltip=['Job', 'Recruiter Count']
        ).properties(width=700, height=400)

        st.altair_chart(job_chart, use_container_width=True)
    else:
        st.info("No job posting data available.")

    st.divider()
    st.markdown("### 📬 Email Log")

    with st.expander("View Email Details"):
        recruiters_df = pd.DataFrame(recruiters)

        # Drop _id and convert all other complex fields to string
        if "_id" in recruiters_df.columns:
            recruiters_df = recruiters_df.drop(columns=["_id"])
        for col in recruiters_df.columns:
            recruiters_df[col] = recruiters_df[col].apply(str)

        st.dataframe(recruiters_df)

        def convert_df_to_csv_bytes(df: pd.DataFrame) -> bytes:
            return df.to_csv(index=False).encode("utf-8")

        if not recruiters_df.empty:
            csv = convert_df_to_csv_bytes(recruiters_df)
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
