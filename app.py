import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient
import os

# --- 🔄 Load Data ---
@st.cache_data
def load_data():
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client.get_database("job_hunt")

    recruiters = list(db.recruiter_emails.find())
    companies = list(db.companies.find())
    jobs = list(db.job_listings.find())

    recruiters_df = pd.DataFrame(recruiters)
    companies_df = pd.DataFrame(companies)
    jobs_df = pd.DataFrame(jobs)

    return recruiters_df, companies_df, jobs_df


# --- 🔢 Metrics Computation ---
def compute_basic_metrics(df):
    return {
        "total": len(df),
        "missing_emails": df["email"].isna().sum(),
        "read_rate": df["read_status"].mean() if "read_status" in df else 0
    }


# --- Streamlit App ---
st.set_page_config(page_title="📊 Recruiter Outreach Insights", layout="wide")
st.title("📈 Outreach Data Visualizations")

recruiters_df, companies_df, jobs_df = load_data()

st.markdown("### 1. 📬 Emails Sent Per Company")
if "company" in recruiters_df.columns:
    recruiters_df["company_name"] = recruiters_df["company"].apply(lambda c: c.get("company_name") if isinstance(c, dict) else "Unknown")
    email_per_company = recruiters_df.groupby("company_name").size().reset_index(name="Email Count")
    chart1 = alt.Chart(email_per_company).mark_bar().encode(
        x=alt.X("company_name:N", sort='-y', title="Company"),
        y=alt.Y("Email Count:Q"),
        tooltip=["company_name", "Email Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart1, use_container_width=True)

st.markdown("### 2. 🔁 Follow-up Status Breakdown")
followup_counts = recruiters_df["followup"].value_counts().reset_index()
followup_counts.columns = ["Followed Up", "Count"]
chart2 = alt.Chart(followup_counts).mark_arc().encode(
    theta="Count:Q",
    color="Followed Up:N",
    tooltip=["Followed Up", "Count"]
).properties(width=500, height=400)
st.altair_chart(chart2)

st.markdown("### 3. 📖 Read Status Over Time")
if "created_at" in recruiters_df.columns:
    recruiters_df["created_at"] = pd.to_datetime(recruiters_df["created_at"])
    time_read = recruiters_df.groupby(recruiters_df["created_at"].dt.date)["read_status"].sum().reset_index(name="Reads")
    chart3 = alt.Chart(time_read).mark_line(point=True).encode(
        x="created_at:T",
        y="Reads:Q",
        tooltip=["created_at", "Reads"]
    ).properties(width=700, height=400)
    st.altair_chart(chart3)

st.markdown("### 4. 🏭 Job Industry Distribution")
if "industry" in jobs_df.columns:
    industry_dist = jobs_df["industry"].value_counts().reset_index()
    industry_dist.columns = ["Industry", "Count"]
    chart4 = alt.Chart(industry_dist).mark_bar().encode(
        x=alt.X("Industry:N", sort='-y'),
        y="Count:Q",
        tooltip=["Industry", "Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart4)

st.markdown("### 5. 💼 Work Model Distribution")
if "work_model" in jobs_df.columns:
    work_model = jobs_df["work_model"].value_counts().reset_index()
    work_model.columns = ["Work Model", "Count"]
    chart5 = alt.Chart(work_model).mark_arc().encode(
        theta="Count:Q",
        color="Work Model:N",
        tooltip=["Work Model", "Count"]
    ).properties(width=500, height=400)
    st.altair_chart(chart5)

st.markdown("### 6. 🌍 Companies by Country")
if "country" in companies_df.columns:
    company_country = companies_df["country"].value_counts().reset_index()
    company_country.columns = ["Country", "Count"]
    chart6 = alt.Chart(company_country).mark_bar().encode(
        x=alt.X("Country:N", sort='-y'),
        y="Count:Q",
        tooltip=["Country", "Count"]
    ).properties(width=700, height=400)
    st.altair_chart(chart6)

st.markdown("### 7. 📅 Job Postings Over Time")
if "date_published" in jobs_df.columns:
    jobs_df["date_published"] = pd.to_datetime(jobs_df["date_published"])
    job_time = jobs_df.groupby(jobs_df["date_published"].dt.date).size().reset_index(name="Jobs Posted")
    chart7 = alt.Chart(job_time).mark_area().encode(
        x="date_published:T",
        y="Jobs Posted:Q",
        tooltip=["date_published", "Jobs Posted"]
    ).properties(width=700, height=400)
    st.altair_chart(chart7)
