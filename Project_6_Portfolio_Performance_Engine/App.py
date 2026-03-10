import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_portfolio_data
from portfolio_engine import *
from visuals import *

st.title("Portfolio Performance Engine")

uploaded_file = st.file_uploader("Upload Portfolio Dataset")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_portfolio_data(df)

    revenue_df = revenue_by_location(df)

    efficiency_df = revenue_per_transaction(df)

    growth_df = growth_by_location(df)

    alerts = portfolio_alerts(growth_df)

    st.subheader("Revenue by Location")

    st.plotly_chart(revenue_by_location_chart(revenue_df))

    st.subheader("Location Efficiency")

    st.dataframe(efficiency_df)

    st.subheader("Growth Comparison")

    st.plotly_chart(growth_chart(growth_df))

    if alerts:

        st.subheader("Portfolio Alerts")

        for alert in alerts:
            st.warning(alert)
