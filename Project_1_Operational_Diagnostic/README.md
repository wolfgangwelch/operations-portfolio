# Operational Diagnostic Engine

A Streamlit-based operational intelligence tool that ingests business reports, normalizes the data, analyzes performance trends, and generates executive insights.

## What it does

This engine is designed to help operators quickly diagnose business performance using structured operational reports.

It supports:

- CSV / Excel / PDF uploads
- smart report classification
- automatic data normalization
- processed dataset storage
- interactive filtering
- trend analysis
- category diagnostics
- AI-generated executive summaries

## Workflow

Upload reports → Parse → Normalize → Analyze → Visualize → Generate insights

## Core Analyses

- total revenue
- transaction count
- average revenue per transaction
- category contribution
- revenue concentration
- rolling trend analysis
- anomaly signals

## Dashboard Features

- date range filter
- location filter
- category filter
- revenue trend charts
- category contribution charts
- distribution analysis
- AI executive report

## Sample Data

Use `sample_reports/generate_sample_data.py` to generate a realistic large operational dataset.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
