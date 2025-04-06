import streamlit as st
from utils import load_data
import pandas as pd

st.set_page_config(page_title="📧 Recruiter Logs", layout="wide")
st.title("📧 Recruiter Email Records")

recruiters, _, _ = load_data()

if recruiters:
    df = pd.DataFrame(recruiters)

    # Fill missing fields with None
    for col in ["first_name", "last_name", "email", "position", "confidence", "mail_sent", "followup", "read_status", "sent_at"]:
        if col not in df.columns:
            df[col] = None

    df = df[["first_name", "last_name", "email", "position", "confidence",
             "mail_sent",  "followup", "read_status", "sent_at"]]
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No recruiter data found.")
