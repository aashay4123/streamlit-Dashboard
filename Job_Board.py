import streamlit as st
from utils import load_data

st.set_page_config(page_title="Job Listings", layout="wide")
st.title("💼 Job Board")

_, _, jobs = load_data()

search_term = st.text_input("Search by title or skill...")
filtered_jobs = []

for job in jobs:
    if (
        search_term.lower() in (job.get("job_title") or "").lower()
        or search_term.lower() in " ".join(job.get("skills") or []).lower()
    ):
        filtered_jobs.append(job)

st.markdown(f"### {len(filtered_jobs)} result(s) found")

for job in filtered_jobs:
    with st.expander(f"{job.get('job_title', 'N/A')} at {job.get('location', 'Unknown')}"):
        st.write(f"**Role:** {job.get('role', 'N/A')}")
        st.write(f"**Location:** {job.get('location', 'N/A')}")
        st.write(f"**Skills:** {' | '.join(job.get('skills', []) or [])}")
        st.write(f"**Description:**
{job.get('job_description', '')[:500]}...")
        st.markdown(f"[View Job Posting]({job.get('job_url', '#')})", unsafe_allow_html=True)
