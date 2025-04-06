import streamlit as st
from utils import fetch_model_logs
import pandas as pd

st.set_page_config(page_title="Model Usage", layout="wide")
st.title("🧠 Model Usage Insights")

logs = fetch_model_logs()

if logs:
    df = pd.DataFrame(logs)
    st.metric("Average Prompt Length", round(df["prompt_tokens"].mean(), 2))
    st.metric("Average Completion Tokens", round(df["completion_tokens"].mean(), 2))

    st.subheader("📈 Prompt Token Distribution")
    st.line_chart(df.set_index("timestamp")["prompt_tokens"])

    st.subheader("🧪 Generation Success Rate")
    st.bar_chart(df["status"].value_counts())

    with st.expander("🔍 Sample Prompts"):
        for i, row in df.head(3).iterrows():
            st.code(row["prompt"][:500] + "...", language="markdown")
else:
    st.info("No model logs yet. Enable logging to track generation details.")
