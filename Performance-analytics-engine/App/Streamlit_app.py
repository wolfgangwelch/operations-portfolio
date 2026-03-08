import streamlit as st
from src.performance_engine import summarize_performance

st.set_page_config(
    page_title="Performance Analytics Engine",
    layout="wide"
)

st.title("Performance Analytics Engine")

df = summarize_performance()

st.subheader("Performance Summary")

st.dataframe(df)

st.bar_chart(df.set_index("entity_id")["total_revenue"])
