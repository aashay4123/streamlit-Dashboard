import streamlit as st
from utils import load_data
import pandas as pd

# st.set_page_config(page_title="🏢 Companies", layout="wide")

st.title("🏢 Company Profiles")

_, companies, _ = load_data()

if companies:
    df = pd.DataFrame(companies)
    df = df[["company_name", "industry", "location", "employees",
             "founded", "technologies", "linkedin_url", "website"]]
    df["technologies"] = df["technologies"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else "")
    df["linkedin_url"] = df["linkedin_url"].fillna(
        "").apply(lambda x: f"[LinkedIn]({x})" if x else "")
    df["website"] = df["website"].fillna("").apply(
        lambda x: f"[Website]({x})" if x else "")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No companies found.")
