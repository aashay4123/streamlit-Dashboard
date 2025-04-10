import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient
from bson import ObjectId
import os

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
st.set_page_config(page_title="📊 Outreach Dashboard", layout="wide")
st.title("📈 Recruiter Outreach Dashboard")

# --- Load ---
recruiters_df, companies_df, jobs_df = load_data()

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

# --- 3. Read Status Over Time ---
st.markdown("### 3. 📖 Read Status Over Time")
recruiters_df["created_at"] = pd.to_datetime(recruiters_df["created_at"], errors="coerce")
read_data = recruiters_df.dropna(subset=["created_at"])
read_data = read_data.groupby(read_data["created_at"].dt.date)["read_status"].sum().reset_index(name="Reads")
if not read_data.empty:
    chart3 = alt.Chart(read_data).mark_line(point=True).encode(
        x="created_at:T",
        y="Reads:Q",
        tooltip=["created_at", "Reads"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)
else:
    st.warning("⚠️ No valid timestamps or read data.")

# --- 4. Job Industry Distribution ---
st.markdown("### 4. 🏭 Job Industry Distribution")
industry_counts = jobs_df["industry"].value_counts().reset_index()
industry_counts.columns = ["Industry", "Count"]
chart4 = alt.Chart(industry_counts).mark_bar().encode(
    x=alt.X("Industry:N", sort='-y'),
    y="Count:Q",
    tooltip=["Industry", "Count"]
).properties(width=700, height=400)
st.altair_chart(chart4)

# --- 5. Work Model Distribution ---
st.markdown("### 5. 🧑‍💻 Work Model Distribution")
wm_counts = jobs_df["work_model"].value_counts().reset_index()
wm_counts.columns = ["Work Model", "Count"]
chart5 = alt.Chart(wm_counts).mark_arc().encode(
    theta="Count:Q",
    color="Work Model:N",
    tooltip=["Work Model", "Count"]
).properties(width=500, height=400)
st.altair_chart(chart5)

# --- 6. Companies by Country ---
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
    st.warning("⚠️ No country data in company table.")

# --- 7. Job Postings Over Time ---
st.markdown("### 7. 🗓️ Job Postings Over Time")
valid_jobs = jobs_df.dropna(subset=["date_published"])
if not valid_jobs.empty:
    job_time = valid_jobs.groupby(valid_jobs["date_published"].dt.date).size().reset_index(name="Jobs Posted")
    chart7 = alt.Chart(job_time).mark_area().encode(
        x="date_published:T",
        y="Jobs Posted:Q",
        tooltip=["date_published", "Jobs Posted"]
    ).properties(width=700, height=400)
    st.altair_chart(chart7)
else:
    st.warning("⚠️ No job posting dates found.")
