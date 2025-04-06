import streamlit as st
from utils import load_data, compute_metrics
import pandas as pd

st.set_page_config(page_title="📊 Full Outreach Dashboard", layout="wide")
st.title("📬 Full Outreach Summary")

recruiters, companies, jobs = load_data()
metrics = compute_metrics(recruiters)

# Summary Section
st.markdown("## 🚀 Summary Statistics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Emails", metrics["total"])
col2.metric("Sent", metrics["sent"])
col3.metric("Failed", metrics["failed"])
col4.metric("Follow-Ups", metrics["followup"])
col5.metric("Read", metrics["read"])

# Company Distribution
st.markdown("## 🏢 Company Email Volume")
company_df = pd.DataFrame.from_dict(metrics["by_company"], orient="index", columns=["Email Count"]).sort_values("Email Count", ascending=False)
st.bar_chart(company_df)

# Job Distribution
st.markdown("## 💼 Job Posting Volume")
job_df = pd.DataFrame.from_dict(metrics["by_job"], orient="index", columns=["Recruiter Count"]).sort_values("Recruiter Count", ascending=False)
st.bar_chart(job_df)

# Recruiters Breakdown
st.markdown("## 📧 Recruiters Snapshot")
if recruiters:
    rec_df = pd.DataFrame(recruiters)[["first_name", "last_name", "email", "position", "confidence", "mail_send_success", "followup", "read_status", "sent_at"]]
    st.dataframe(rec_df)
else:
    st.warning("No recruiter records found.")
