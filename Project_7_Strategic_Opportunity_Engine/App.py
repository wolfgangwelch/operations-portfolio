import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_opportunity_data
from opportunity_engine import *
from visuals import *

st.title("Strategic Opportunity Engine")

uploaded_file = st.file_uploader("Upload Category Dataset")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_opportunity_data(df)

    share_df = category_revenue_share(df)

    growth_df = category_growth(df)

    signals = opportunity_signals(share_df, growth_df)

    st.subheader("Revenue Distribution")

    st.plotly_chart(revenue_distribution_chart(share_df))

    st.subheader("Category Growth")

    st.plotly_chart(growth_chart(growth_df))

    st.subheader("Category Data")

    st.dataframe(share_df.merge(growth_df, on="category"))

    if signals:

        st.subheader("Strategic Signals")

        for s in signals:
            st.warning(s)
