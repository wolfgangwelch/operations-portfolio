import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_efficiency_data
from efficiency_engine import *
from visuals import *

st.title("Operational Efficiency Engine")

uploaded_file = st.file_uploader("Upload Operational Dataset")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_efficiency_data(df)

    rpt = revenue_per_transaction(df)

    rpu = revenue_per_unit(df)

    category_df = category_efficiency(df)

    signals = inefficiency_signals(df)

    st.metric("Revenue per Transaction", f"${rpt:.2f}")

    st.metric("Revenue per Unit", f"${rpu:.2f}")

    st.subheader("Category Efficiency")

    st.plotly_chart(category_efficiency_chart(category_df))

    st.dataframe(category_df)

    if signals:

        st.subheader("Efficiency Signals")

        for signal in signals:
            st.warning(signal)
