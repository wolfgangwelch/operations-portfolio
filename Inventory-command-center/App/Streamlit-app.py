import streamlit as st
from src.reporting_engine import build_reports

st.set_page_config(
    page_title="Asset Inventory Control Engine",
    layout="wide"
)

st.title("Asset Inventory Control Engine")

variance, reorder = build_reports()

page = st.sidebar.selectbox(
    "View",
    [
        "Inventory Variance",
        "Reorder Recommendations"
    ]
)

if page == "Inventory Variance":

    st.header("Inventory Variance Report")
    st.dataframe(variance)

if page == "Reorder Recommendations":

    st.header("Reorder Recommendations")
    st.dataframe(reorder)
