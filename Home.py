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
    cleaned = []
    for r in recruiters:
        cleaned.append({
            "first_name": r.get("first_name"),
            "last_name": r.get("last_name"),
            "email": r.get("email"),
            "position": r.get("position"),
            "confidence": r.get("confidence"),
            "mail_send_success": r.get("mail_send_success"),
            "followup": r.get("followup"),
            "read_status": r.get("read_status"),
            "sent_at": r.get("sent_at"),
        })

    rec_df = pd.DataFrame(cleaned)
    if "sent_at" in rec_df.columns:
        rec_df = rec_df.sort_values(by="sent_at", ascending=False)

    st.dataframe(rec_df, use_container_width=True)

else:
    st.warning("No recruiter records found.")
