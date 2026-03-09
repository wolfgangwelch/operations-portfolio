from __future__ import annotations

from typing import Dict, Any

import numpy as np
import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    start_date=None,
    end_date=None,
    locations=None,
    categories=None,
) -> pd.DataFrame:
    filtered = df.copy()

    if start_date is not None:
        filtered = filtered[filtered["date"] >= pd.to_datetime(start_date)]

    if end_date is not None:
        filtered = filtered[filtered["date"] <= pd.to_datetime(end_date)]

    if locations:
        filtered = filtered[filtered["location"].isin(locations)]

    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    return filtered


def daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("date", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            transactions=("transaction_id", pd.Series.nunique),
            units=("units", "sum"),
        )
        .sort_values("date")
    )

    daily["avg_revenue_per_transaction"] = (
        daily["revenue"] / daily["transactions"].replace(0, np.nan)
    )
    daily["rolling_7_day_revenue"] = daily["revenue"].rolling(7, min_periods=1).mean()
    daily["rolling_30_day_revenue"] = daily["revenue"].rolling(30, min_periods=1).mean()

    return daily


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units=("units", "sum"),
            transactions=("transaction_id", pd.Series.nunique),
        )
        .sort_values("revenue", ascending=False)
    )

    total_revenue = summary["revenue"].sum()
    summary["revenue_share"] = (
        summary["revenue"] / total_revenue if total_revenue else 0
    )

    return summary


def location_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("location", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            units=("units", "sum"),
            transactions=("transaction_id", pd.Series.nunique),
        )
        .sort_values("revenue", ascending=False)
    )

    summary["revenue_per_transaction"] = (
        summary["revenue"] / summary["transactions"].replace(0, np.nan)
    )

    return summary


def distribution_summary(df: pd.DataFrame) -> pd.DataFrame:
    txn = (
        df.groupby("transaction_id", as_index=False)
        .agg(
            date=("date", "min"),
            location=("location", "first"),
            revenue=("revenue", "sum"),
            units=("units", "sum"),
        )
    )
    return txn


def detect_signals(daily_df: pd.DataFrame, category_df: pd.DataFrame) -> Dict[str, Any]:
    signals: Dict[str, Any] = {
        "trend_signal": None,
        "anomaly_signal": None,
        "concentration_signal": None,
    }

    if len(daily_df) >= 2:
        latest = daily_df["rolling_7_day_revenue"].iloc[-1]
        previous = daily_df["rolling_7_day_revenue"].iloc[-2]

        if pd.notna(latest) and pd.notna(previous):
            if latest > previous:
                signals["trend_signal"] = "Revenue trend is moving upward."
            elif latest < previous:
                signals["trend_signal"] = "Revenue trend is moving downward."
            else:
                signals["trend_signal"] = "Revenue trend is stable."

    if len(daily_df) >= 7:
        mean_revenue = daily_df["revenue"].mean()
        std_revenue = daily_df["revenue"].std(ddof=0)
        if std_revenue and std_revenue > 0:
            z_scores = (daily_df["revenue"] - mean_revenue) / std_revenue
            anomalies = daily_df[np.abs(z_scores) > 2]
            if not anomalies.empty:
                top_anomaly = anomalies.iloc[-1]
                signals["anomaly_signal"] = (
                    f"Anomalous revenue detected on {top_anomaly['date'].date()}."
                )

    if not category_df.empty:
        top_category = category_df.iloc[0]
        if top_category["revenue_share"] >= 0.50:
            signals["concentration_signal"] = (
                f"Revenue concentration detected: "
                f"{top_category['category']} contributes "
                f"{top_category['revenue_share']:.1%} of total revenue."
            )

    return signals


def build_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    daily = daily_summary(df)
    categories = category_summary(df)
    locations = location_summary(df)
    distribution = distribution_summary(df)
    signals = detect_signals(daily, categories)

    total_revenue = df["revenue"].sum()
    total_units = df["units"].sum()
    total_transactions = df["transaction_id"].nunique()
    avg_revenue_per_transaction = (
        total_revenue / total_transactions if total_transactions else 0
    )

    latest_7 = daily["rolling_7_day_revenue"].iloc[-1] if not daily.empty else 0
    previous_7 = daily["rolling_7_day_revenue"].iloc[-2] if len(daily) > 1 else latest_7
    trend_growth_pct = (
        ((latest_7 - previous_7) / previous_7) * 100 if previous_7 not in [0, np.nan] else 0
    )

    return {
        "metrics": {
            "total_revenue": total_revenue,
            "total_units": total_units,
            "total_transactions": total_transactions,
            "avg_revenue_per_transaction": avg_revenue_per_transaction,
            "trend_growth_pct": trend_growth_pct,
        },
        "daily": daily,
        "categories": categories,
        "locations": locations,
        "distribution": distribution,
        "signals": signals,
    }


def build_ai_summary_payload(analysis: Dict[str, Any]) -> Dict[str, Any]:
    categories = analysis["categories"]
    top_category = None
    if not categories.empty:
        top_category = {
            "name": categories.iloc[0]["category"],
            "revenue_share": float(categories.iloc[0]["revenue_share"]),
        }

    return {
        "metrics": analysis["metrics"],
        "top_category": top_category,
        "signals": analysis["signals"],
    }
