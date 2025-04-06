import streamlit as st
from utils import load_data
from datetime import datetime

st.set_page_config(page_title="Recruiter Activity", layout="wide")
st.title("📬 Recruiter Email Logs")

recruiters, companies, jobs = load_data()

st.write(f"Total recruiters found: {len(recruiters)}")

for r in recruiters:
    name = f"{r.get('first_name', '')} {r.get('last_name', '')}".strip()
    with st.expander(f"{name or 'Unnamed'} - {r['email']}"):
        st.write(r)
