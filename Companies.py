import streamlit as st
from utils import load_data

st.set_page_config(page_title="Companies", layout="wide")
st.title("🏢 Company Directory")

_, companies, _ = load_data()

industry_filter = st.selectbox("Filter by industry", ["All"] + list(set([c.get("industry", "") for c in companies if c.get("industry")])))
tech_filter = st.text_input("Filter by tech stack (comma-separated)", "")

filtered = []

for c in companies:
    if industry_filter != "All" and c.get("industry") != industry_filter:
        continue
    if tech_filter:
        filters = [t.strip().lower() for t in tech_filter.split(",")]
        techs = [t.lower() for t in (c.get("technologies") or [])]
        if not any(f in techs for f in filters):
            continue
    filtered.append(c)

st.markdown(f"### {len(filtered)} companies found")

for c in filtered:
    with st.expander(c["company_name"]):
        st.write(f"**Industry:** {c.get('industry', 'N/A')}")
        st.write(f"**Employees:** {c.get('employees', 'N/A')}")
        st.write(f"**Founded:** {c.get('founded', 'N/A')}")
        st.write(f"**Location:** {c.get('location') or f'{c.get('city', '')}, {c.get('country', '')}'}")
        st.write(f"**Website:** {c.get('website', 'N/A')}")
        st.write(f"**Tech Stack:** {', '.join(c.get('technologies', []) or [])}")
