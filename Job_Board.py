import streamlit as st
from utils import load_data
import pandas as pd

st.set_page_config(page_title="💼 Jobs", layout="wide")
st.title("💼 Job Listings")

_, _, jobs = load_data()

if jobs:
    df = pd.DataFrame(jobs)
    df = df[["job_title", "location", "role", "work_model", "skills", "date_published", "job_url"]]
    df["skills"] = df["skills"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
    df["job_url"] = df["job_url"].fillna("").apply(lambda x: f"[View Job]({x})" if x else "")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No job listings found.")
