import streamlit as st
from utils import load_data
import pandas as pd


def render():
    # st.set_page_config(page_title="💼 Job Listings", layout="wide")
    st.title("💼 Job Listings")

    _, _, jobs = load_data()

    if jobs:
        df = pd.DataFrame(jobs)

        # Safely add any missing columns
        required_cols = ["job_title", "location", "role",
                         "work_model", "skills", "date_published", "job_url"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = None

        # Convert lists to strings
        df["skills"] = df["skills"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else "")
        df["job_url"] = df["job_url"].fillna("").apply(
            lambda x: f"[View]({x})" if x else "")

        df = df[required_cols]
        df = df.sort_values(by="date_published",
                            ascending=False, na_position="last")

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No job listings found.")
