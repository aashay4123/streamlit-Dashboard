import streamlit as st
from utils import load_data, compute_metrics

st.set_page_config(page_title="Outreach Summary", layout="wide")
st.title("📬 Outreach Overview")

recruiters, companies, jobs = load_data()

st.subheader("📊 Outreach Summary")
metrics = compute_metrics(recruiters)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", metrics['total'])
col2.metric("Sent", metrics['sent'])
col3.metric("Failed", metrics['failed'])
col4.metric("Follow-ups", metrics['followup'])
col5.metric("Read", metrics['read'])

st.subheader("📍 Company Breakdown")
st.bar_chart(metrics["by_company"])

st.subheader("💼 Job Distribution")
st.bar_chart(metrics["by_job"])
