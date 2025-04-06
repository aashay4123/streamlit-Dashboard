import streamlit as st
import pandas as pd
from utils import load_data


def render():
    st.title("🏢 Company Profiles")

    _, companies, _ = load_data()

    if companies:
        df = pd.DataFrame(companies)
        df["technologies"] = df["technologies"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else "")
        df["linkedin_url"] = df["linkedin_url"].fillna(
            "").apply(lambda x: f"[LinkedIn]({x})" if x else "")
        df["website"] = df["website"].fillna("").apply(
            lambda x: f"[Website]({x})" if x else "")
        df = df[["company_name", "industry", "location", "employees",
                 "founded", "technologies", "linkedin_url", "website"]]
        df = df.sort_values(by="founded", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No company data available.")
