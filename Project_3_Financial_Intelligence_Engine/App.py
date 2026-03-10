import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_financial_data
from financial_analyzer import *
from visuals import *

st.title("Financial Intelligence Engine")

uploaded_file = st.file_uploader("Upload Financial Report")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_financial_data(df)

    variance_df = variance_analysis(df)

    category_df = category_expense_summary(df)

    alerts = overspending_alerts(variance_df)

    st.subheader("Budget vs Actual")

    st.plotly_chart(budget_vs_actual_chart(category_df))

    st.subheader("Expense Distribution")

    st.plotly_chart(expense_mix_chart(category_df))

    st.subheader("Expense Summary")

    st.dataframe(category_df)

    if alerts:

        st.subheader("Overspending Alerts")

        for alert in alerts:
            st.warning(alert)
