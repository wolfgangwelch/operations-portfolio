from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def revenue_trend_chart(daily_df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily_df["date"],
            y=daily_df["revenue"],
            mode="lines+markers",
            name="Daily Revenue",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily_df["date"],
            y=daily_df["rolling_7_day_revenue"],
            mode="lines",
            name="7-Day Rolling Average",
        )
    )
    return fig


def category_contribution_chart(category_df: pd.DataFrame):
    return px.pie(
        category_df,
        names="category",
        values="revenue",
        title="Revenue Contribution by Category",
    )


def category_bar_chart(category_df: pd.DataFrame):
    return px.bar(
        category_df,
        x="category",
        y="revenue",
        title="Revenue by Category",
    )


def revenue_distribution_chart(distribution_df: pd.DataFrame):
    return px.histogram(
        distribution_df,
        x="revenue",
        nbins=30,
        title="Revenue Distribution by Transaction",
    )
