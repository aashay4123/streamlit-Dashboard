import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient
from bson import ObjectId
import os

# --- 🔌 Connect and Load Data ---
@st.cache_data
def load_data():
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client.get_database("job_hunt")

    recruiters = list(db.recruiter_emails.find())
    companies = list(db.companies.find())
    jobs = list(db.job_listings.find())

    return pd.DataFrame(recruiters), pd.DataFrame(companies), pd.DataFrame(jobs)

# --- ✅ Setup Streamlit ---
st.set_page_config(page_title="📊 Outreach Dashboard", layout="wide")
st.title("📈 Recruiter Outreach Dashboard")

# --- 📦 Load Data ---
recruiters_df, companies_df, jobs_df = load_data()

# --- 🧠 Map Company Names ---
company_map = {str(c["_id"]): c.get("company_name", "Unknown") for c in companies_df.to_dict("records")}
recruiters_df["company_id"] = recruiters_df["company"].apply(lambda oid: str(oid) if oid else None)
recruiters_df["company_name"] = recruiters_df["company_id"].map(company_map).fillna("Unknown")

# --- 1. 📬 Emails Sent Per Company ---
st.markdown("### 1. 📬 Emails Sent Per Company")
if not recruiters_df.empty:
    company_counts = recruiters_df["company_name"].value_counts().reset_index()
    company_counts.columns = ["Company", "Email Count"]
    chart1 = alt.Chart(company_counts).mark_bar().encode(
        x=alt.X("Company:N", sort='-y'),
        y="Email Count:Q",
        tooltip=["Company", "Email Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart1, use_container_width=True)
else:
    st.warning("No recruiter data available.")

# --- 2. 🔁 Follow-up Status ---
st.markdown("### 2. 🔁 Follow-up Status Breakdown")
if "followup" in recruiters_df.columns:
    followup_counts = recruiters_df["followup"].fillna(False).value_counts().reset_index()
    followup_counts.columns = ["Followed Up", "Count"]
    chart2 = alt.Chart(followup_counts).mark_arc().encode(
        theta="Count:Q",
        color="Followed Up:N",
        tooltip=["Followed Up", "Count"]
    ).properties(width=500, height=400)
    st.altair_chart(chart2)
else:
    st.warning("No follow-up data available.")

# --- 3. 📖 Read Status Over Time ---
st.markdown("### 3. 📖 Read Status Over Time")
if "created_at" in recruiters_df.columns and "read_status" in recruiters_df.columns:
    recruiters_df["created_at"] = pd.to_datetime(recruiters_df["created_at"], errors="coerce")
    time_read = recruiters_df.groupby(recruiters_df["created_at"].dt.date)["read_status"].sum().reset_index(name="Reads")
    chart3 = alt.Chart(time_read).mark_line(point=True).encode(
        x="created_at:T",
        y="Reads:Q",
        tooltip=["created_at", "Reads"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)
else:
    st.warning("No read status or date data available.")

# --- 4. 🏭 Job Industry Distribution ---
st.markdown("### 4. 🏭 Job Industry Distribution")
if "industry" in jobs_df.columns and jobs_df["industry"].notnull().any():
    industry_counts = jobs_df["industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]
    chart4 = alt.Chart(industry_counts).mark_bar().encode(
        x=alt.X("Industry:N", sort='-y'),
        y="Count:Q",
        tooltip=["Industry", "Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart4)
else:
    st.warning("No job industry data available.")

# --- 5. 🏢 Work Model Distribution ---
st.markdown("### 5. 🏢 Work Model Distribution")
if "work_model" in jobs_df.columns and jobs_df["work_model"].notnull().any():
    wm_counts = jobs_df["work_model"].value_counts().reset_index()
    wm_counts.columns = ["Work Model", "Count"]
    chart5 = alt.Chart(wm_counts).mark_arc().encode(
        theta="Count:Q",
        color="Work Model:N",
        tooltip=["Work Model", "Count"]
    ).properties(width=500, height=400)
    st.altair_chart(chart5)
else:
    st.warning("No work model data available.")

# --- 6. 🌍 Companies by Country ---
st.markdown("### 6. 🌍 Companies by Country")
if "country" in companies_df.columns and companies_df["country"].notnull().any():
    country_counts = companies_df["country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]
    chart6 = alt.Chart(country_counts).mark_bar().encode(
        x=alt.X("Country:N", sort='-y'),
        y="Count:Q",
        tooltip=["Country", "Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart6)
else:
    st.warning("No country data in companies.")

# --- 7. 📅 Job Postings Over Time ---
st.markdown("### 7. 📅 Job Postings Over Time")
if "date_published" in jobs_df.columns and jobs_df["date_published"].notnull().any():
    jobs_df["date_published"] = pd.to_datetime(jobs_df["date_published"], errors="coerce")
    job_time = jobs_df.groupby(jobs_df["date_published"].dt.date).size().reset_index(name="Jobs Posted")
    chart7 = alt.Chart(job_time).mark_area().encode(
        x="date_published:T",
        y="Jobs Posted:Q",
        tooltip=["date_published", "Jobs Posted"]
    ).properties(width=700, height=400)
    st.altair_chart(chart7)
else:
    st.warning("No job date data found.")
