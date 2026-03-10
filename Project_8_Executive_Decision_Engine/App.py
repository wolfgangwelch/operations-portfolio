import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_executive_data
from decision_engine import *
from visuals import *

st.title("Executive Decision Engine")

uploaded_file = st.file_uploader("Upload Business Dataset")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_executive_data(df)

    growth = revenue_trend(df)

    rpt = revenue_per_transaction(df)

    rpu = revenue_per_unit(df)

    category_df = category_distribution(df)

    signals = executive_signals(df)

    st.metric("Revenue Growth", f"{growth:.2f}%")

    st.metric("Revenue per Transaction", f"${rpt:.2f}")

    st.metric("Revenue per Unit", f"${rpu:.2f}")

    st.subheader("Revenue Trend")

    st.plotly_chart(revenue_trend_chart(df))

    st.subheader("Revenue Distribution")

    st.plotly_chart(category_distribution_chart(category_df))

    if signals:

        st.subheader("Executive Signals")

        for signal in signals:
            st.warning(signal)
