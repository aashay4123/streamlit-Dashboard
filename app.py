

import Recruiters
import Companies
import Job_Board
import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient
from bson import ObjectId
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Connect & Load Data ---
@st.cache_data
def load_data():
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client.get_database("job_hunt")

    recruiters = list(db.recruiter_emails.find())
    companies = list(db.companies.find())
    jobs = list(db.job_listings.find())
    

    return pd.DataFrame(recruiters), pd.DataFrame(companies), pd.DataFrame(jobs)


# --- Streamlit Setup ---

# --- Load ---
recruiters_df, companies_df, jobs_df = load_data()
# --- Sanitize ObjectId fields for display compatibility ---
def clean_object_ids(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(lambda x: str(x) if isinstance(x, ObjectId) else x)

recruiters_df = clean_object_ids(recruiters_df)
companies_df = clean_object_ids(companies_df)
jobs_df = clean_object_ids(jobs_df)


# --- Company Mapping ---
company_map = {
    str(company["_id"]): company.get("company_name", "Unknown")
    for company in companies_df.to_dict("records")
}
recruiters_df["company_id"] = recruiters_df["company"].apply(lambda oid: str(oid) if oid else None)
recruiters_df["company_name"] = recruiters_df["company_id"].map(company_map).fillna("Unknown")

# --- Patch missing job fields ---
jobs_df["industry"] = jobs_df.get("industry", pd.Series(dtype="str")).replace(["", "N/A", None], "Unknown").fillna("Unknown")
jobs_df["work_model"] = jobs_df.get("work_model", pd.Series(dtype="str")).replace(["", "N/A", None], "Not Specified").fillna("Not Specified")
jobs_df["date_published"] = pd.to_datetime(jobs_df.get("date_published"), errors="coerce")




st.set_page_config(page_title="📊 Full Outreach Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📧 Recruiters", "🏢 Companies", "💼 Jobs"])

# Load data

# --- HOME PAGE ---
if page == "🏠 Home":
      # --- Optional: Debug Preview ---
    with st.expander("📦 Raw Data Preview"):
        st.subheader("Recruiters")
        st.dataframe(recruiters_df.head())
        st.subheader("Companies")
        st.dataframe(companies_df.head())
        st.subheader("Jobs")
        st.dataframe(jobs_df.head())
    
    # --- 1. Emails Sent Per Company ---
    st.markdown("### 1. 📬 Emails Sent Per Company")
    company_counts = recruiters_df["company_name"].value_counts().reset_index()
    company_counts.columns = ["Company", "Email Count"]
    chart1 = alt.Chart(company_counts).mark_bar().encode(
        x=alt.X("Company:N", sort='-y'),
        y="Email Count:Q",
        tooltip=["Company", "Email Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart1, use_container_width=True)
    
    # --- 2. Follow-up Status Breakdown ---
    st.markdown("### 2. 🔁 Follow-up Status Breakdown")
    followup_counts = recruiters_df["followup"].fillna(False).astype(bool).value_counts().reset_index()
    followup_counts.columns = ["Followed Up", "Count"]
    chart2 = alt.Chart(followup_counts).mark_arc().encode(
        theta="Count:Q",
        color="Followed Up:N",
        tooltip=["Followed Up", "Count"]
    ).properties(width=500, height=400)
    st.altair_chart(chart2)
    
    # --- 3. 🏭 Job Listings per Company Industry ---
    st.markdown("### 3. 🏭 Job Listings per Company Industry")
    
    # Map job.company → company.industry
    industry_map = {
        str(c["_id"]): c.get("industry", "Unknown") for c in companies_df.to_dict("records")
    }
    jobs_df["company_id"] = jobs_df["company"].apply(lambda oid: str(oid) if oid else None)
    jobs_df["industry"] = jobs_df["company_id"].map(industry_map).fillna("Unknown")
    
    industry_counts = jobs_df["industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Job Listings"]
    
    chart3 = alt.Chart(industry_counts).mark_bar().encode(
        x=alt.X("Industry:N", sort='-y'),
        y="Job Listings:Q",
        tooltip=["Industry", "Job Listings"]
    ).properties(width=700, height=400)
    
    st.altair_chart(chart3)
    
    
    # --- 4. 🏢 Job Company Name Distribution ---
    st.markdown("### 4. 🏢 Job Company Name Distribution")
    
    # Map job company ID to name using same mapping from companies_df
    jobs_df["company_id"] = jobs_df["company"].apply(lambda oid: str(oid) if oid else None)
    jobs_df["company_name"] = jobs_df["company_id"].map(company_map).fillna("Unknown")
    
    company_job_counts = jobs_df["company_name"].value_counts().reset_index()
    company_job_counts.columns = ["Company", "Job Count"]
    
    chart4 = alt.Chart(company_job_counts).mark_bar().encode(
        x=alt.X("Company:N", sort='-y'),
        y="Job Count:Q",
        tooltip=["Company", "Job Count"]
    ).properties(width=700, height=400)
    
    st.altair_chart(chart4)

# --- RECRUITERS PAGE ---
elif page == "📧 Recruiters":
    Recruiters.render()

# --- COMPANIES PAGE ---
elif page == "🏢 Companies":
    Companies.render()

# --- JOBS PAGE ---
elif page == "💼 Jobs":
    Job_Board.render()
