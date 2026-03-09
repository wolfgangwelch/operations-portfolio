import streamlit as st
import pandas as pd

from parser import parse_uploaded_file
from normalizer import normalize_sales_data
from revenue_analyzer import *
from visuals import *

st.title("Revenue Stream Intelligence Engine")

uploaded_file = st.file_uploader("Upload Sales Report")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_sales_data(df)

    category_df = category_performance(df)

    sku_df = sku_dominance(df)

    warnings = concentration_risk(category_df)

    st.subheader("Revenue Mix")

    st.plotly_chart(revenue_mix_chart(category_df))

    st.subheader("Category Performance")

    st.plotly_chart(category_bar_chart(category_df))

    st.subheader("Category Table")

    st.dataframe(category_df)

    st.subheader("SKU Dominance")

    st.dataframe(sku_df)

    if warnings:

        st.subheader("Revenue Concentration Risks")

        for w in warnings:
            st.warning(w)
