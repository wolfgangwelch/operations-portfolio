from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from parser import parse_uploaded_file
from classifier import classify_report, auto_detect_column_mapping
from normalizer import normalize_report
from analyzer import apply_filters, build_analysis, build_ai_summary_payload
from visuals import (
    revenue_trend_chart,
    category_contribution_chart,
    category_bar_chart,
    revenue_distribution_chart,
)
from insights import generate_consultant_report


st.set_page_config(page_title="Operational Diagnostic Engine", layout="wide")
st.title("Operational Diagnostic Engine")


PROCESSED_DIR = Path("processed_data")
PROCESSED_DIR.mkdir(exist_ok=True)
PROCESSED_PATH = PROCESSED_DIR / "normalized_data.csv"


st.sidebar.header("Upload Reports")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more operational reports",
    type=["csv", "xlsx", "xls", "pdf"],
    accept_multiple_files=True,
)

assigned_location = st.sidebar.text_input(
    "Optional location name for uploaded files",
    value="Primary Location"
)

all_normalized = []
classification_rows = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            raw_df, suffix = parse_uploaded_file(uploaded_file)

            if raw_df.empty:
                st.warning(f"{uploaded_file.name}: no parseable table found.")
                continue

            report_type = classify_report(list(raw_df.columns))
            mapping = auto_detect_column_mapping(list(raw_df.columns))

            normalized_df = normalize_report(
                raw_df,
                mapping=mapping,
                assigned_location=assigned_location,
            )

            normalized_df["source_file"] = uploaded_file.name
            normalized_df["report_type"] = report_type

            all_normalized.append(normalized_df)

            classification_rows.append(
                {
                    "file_name": uploaded_file.name,
                    "file_type": suffix,
                    "report_type": report_type,
                    "rows_parsed": len(normalized_df),
                }
            )

        except Exception as exc:
            st.error(f"Failed to process {uploaded_file.name}: {exc}")

    if all_normalized:
        full_df = pd.concat(all_normalized, ignore_index=True)
        full_df.to_csv(PROCESSED_PATH, index=False)

        st.success("Reports parsed and normalized successfully.")

        with st.expander("Detected Report Classification"):
            st.dataframe(pd.DataFrame(classification_rows), use_container_width=True)

        st.subheader("Interactive Filters")

        min_date = full_df["date"].min().date()
        max_date = full_df["date"].max().date()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
        )

        locations = sorted(full_df["location"].dropna().unique().tolist())
        selected_locations = st.multiselect(
            "Select Location(s)",
            options=locations,
            default=locations,
        )

        categories = sorted(full_df["category"].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Select Category(s)",
            options=categories,
            default=categories,
        )

        filtered_df = apply_filters(
            full_df,
            start_date=date_range[0] if len(date_range) > 0 else None,
            end_date=date_range[1] if len(date_range) > 1 else None,
            locations=selected_locations,
            categories=selected_categories,
        )

        analysis = build_analysis(filtered_df)
        metrics = analysis["metrics"]

        st.subheader("Key Metrics")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Revenue", f"${metrics['total_revenue']:,.0f}")
        c2.metric("Transactions", f"{metrics['total_transactions']:,}")
        c3.metric("Units", f"{metrics['total_units']:,}")
        c4.metric("Avg Revenue / Transaction", f"${metrics['avg_revenue_per_transaction']:,.2f}")
        c5.metric("Trend Signal", f"{metrics['trend_growth_pct']:.2f}%")

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Overview",
            "Deep Analysis",
            "Signals",
            "Executive Report",
            "Processed Data",
            "Exports",
        ])

        with tab1:
            st.plotly_chart(revenue_trend_chart(analysis["daily"]), use_container_width=True)
            st.plotly_chart(category_contribution_chart(analysis["categories"]), use_container_width=True)

        with tab2:
            st.plotly_chart(category_bar_chart(analysis["categories"]), use_container_width=True)
            st.plotly_chart(revenue_distribution_chart(analysis["distribution"]), use_container_width=True)

            st.markdown("### Category Summary")
            st.dataframe(analysis["categories"], use_container_width=True)

            st.markdown("### Location Summary")
            st.dataframe(analysis["locations"], use_container_width=True)

        with tab3:
            signals = analysis["signals"]
            for key, value in signals.items():
                if value:
                    st.warning(value)
            if not any(signals.values()):
                st.info("No major signals detected in the selected range.")

        with tab4:
            summary_payload = build_ai_summary_payload(analysis)
            consultant_report = generate_consultant_report(summary_payload)
            st.text_area("AI Consultant Report", consultant_report, height=400)

        with tab5:
            st.dataframe(filtered_df, use_container_width=True)

        with tab6:
            st.download_button(
                label="Download Processed Dataset",
                data=filtered_df.to_csv(index=False).encode("utf-8"),
                file_name="normalized_data.csv",
                mime="text/csv",
            )

            st.download_button(
                label="Download Daily Summary",
                data=analysis["daily"].to_csv(index=False).encode("utf-8"),
                file_name="daily_summary.csv",
                mime="text/csv",
            )

            st.download_button(
                label="Download Category Summary",
                data=analysis["categories"].to_csv(index=False).encode("utf-8"),
                file_name="category_summary.csv",
                mime="text/csv",
            )
    else:
        st.info("No usable data was parsed from uploaded files.")
else:
    st.info("Upload one or more reports to begin analysis.")
