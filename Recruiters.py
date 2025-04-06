import streamlit as st
from utils import load_data
import pandas as pd

st.set_page_config(page_title="📧 Recruiters", layout="wide")
st.title("📧 Recruiter Email Logs")

recruiters, _, _ = load_data()

if recruiters:
    df = pd.DataFrame(recruiters)
    df = df[["first_name", "last_name", "email", "position", "confidence", "mail_sent", "mail_send_success", "followup", "read_status", "sent_at"]]
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No recruiter data found.")
