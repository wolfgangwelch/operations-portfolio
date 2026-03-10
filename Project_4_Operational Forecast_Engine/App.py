import streamlit as st

from parser import parse_uploaded_file
from normalizer import normalize_forecast_data
from forecast_engine import *
from visuals import *

st.title("Operational Forecast Engine")

uploaded_file = st.file_uploader("Upload Revenue History")

if uploaded_file:

    df = parse_uploaded_file(uploaded_file)

    df = normalize_forecast_data(df)

    forecast_df = build_forecast(df)

    growth = growth_rate(df)

    signal = volatility_signal(df)

    st.subheader("Revenue Forecast")

    st.plotly_chart(forecast_chart(df, forecast_df))

    st.metric("Revenue Growth Rate", f"{growth:.2f}%")

    if signal:

        st.warning(signal)
