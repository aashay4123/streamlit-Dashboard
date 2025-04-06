import streamlit as st
from utils import load_data
import pandas as pd

st.set_page_config(page_title="📧 Recruiter Logs", layout="wide")
st.title("📧 Recruiter Email Records")

recruiters, _, _ = load_data()

if recruiters:
    # Normalize missing keys and build consistent rows
    cleaned_recruiters = []
    for r in recruiters:
        cleaned_recruiters.append({
            "first_name": r.get("first_name"),
            "last_name": r.get("last_name"),
            "email": r.get("email"),
            "position": r.get("position"),
            "confidence": r.get("confidence"),
            "mail_sent": r.get("mail_sent"),
            "mail_send_success": r.get("mail_send_success"),
            "followup": r.get("followup"),
            "read_status": r.get("read_status"),
            "sent_at": r.get("sent_at"),
        })

    # Create DataFrame and sort by sent_at (latest first)
    rec_df = pd.DataFrame(cleaned_recruiters)
    if "sent_at" in rec_df.columns:
        rec_df = rec_df.sort_values(by="sent_at", ascending=False)

    st.dataframe(rec_df, use_container_width=True)

else:
    st.warning("No recruiter data found.")
