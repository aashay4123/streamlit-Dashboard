import streamlit as st
import pandas as pd
from utils import load_data


def render():
    st.title("📧 Recruiter Email Records")

    recruiters, _, _ = load_data()

    if recruiters:
        cleaned = []
        for r in recruiters:
            cleaned.append({
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

        rec_df = pd.DataFrame(cleaned)
        rec_df = rec_df.sort_values(by="sent_at", ascending=False)
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.warning("No recruiter data found.")
