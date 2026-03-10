# Financial Intelligence Engine

## Overview

The Financial Intelligence Engine is an operational analytics tool designed to analyze financial performance by comparing budgeted spending against actual expenses.

The system ingests structured financial reports and automatically evaluates cost performance, highlights overspending risks, and surfaces expense distribution patterns across operational categories.

This engine helps operators, consultants, and analysts quickly answer critical financial questions such as:

• Are operational expenses exceeding budget expectations?  
• Which cost centers represent the largest portion of spending?  
• Where are budget variances occurring?  
• Are cost increases outpacing operational growth?

The goal of this engine is to accelerate financial diagnostics and provide clear visibility into cost structure and spending performance.

---

## Why This Tool Exists

Most organizations track budgets and expenses but lack an efficient way to rapidly diagnose where spending is drifting away from expectations.

Financial reports often exist in separate systems and require manual review to understand performance.

The Financial Intelligence Engine was built to:

• Normalize financial report data  
• Compare budgeted spending against actual expenses  
• Detect overspending trends automatically  
• Identify expense distribution patterns across operational categories  

By automating these diagnostics, operators can quickly detect financial risks and make informed operational adjustments.

---

## Core Diagnostics

The engine produces several financial diagnostic outputs.

### Budget vs Actual Analysis

Compares planned spending against actual expenditures.

Example output:

Labor  
Budget: $120,000  
Actual: $145,000  
Variance: +$25,000  

Inventory  
Budget: $80,000  
Actual: $76,000  
Variance: -$4,000  

This allows operators to immediately identify where financial deviations occur.

---

### Expense Category Distribution

Determines the share of total expenses attributed to each operational category.

Example:

Labor = 42%  
Inventory = 31%  
Marketing = 12%  
Utilities = 8%  
Other = 7%

Understanding expense composition is critical for evaluating cost structure and operational efficiency.

---

### Variance Detection

The engine calculates both absolute and percentage variance between budgeted and actual spending.

Example:

Labor variance: +21%  
Marketing variance: +60%

This highlights which areas of the business are exceeding planned financial limits.

---

### Overspending Alerts

The system automatically flags categories that exceed budget thresholds.

Example warning:

⚠ Labor spending exceeds budget by 21%  
⚠ Marketing spending exceeds budget by 60%

These alerts allow operators to quickly identify financial risks requiring intervention.

---

## Dashboard Features

The Streamlit dashboard provides interactive financial diagnostics including:

• Budget vs Actual comparison charts  
• Expense distribution visualizations  
• Category-level spending summaries  
• Automatic overspending alerts  

These visualizations allow users to quickly identify financial patterns and spending risks.

---

## Sample Dataset

A sample dataset is included to demonstrate the expected input format.

sample_reports/sample_financial_data.csv

Expected columns:

date  
category  
budget  
actual  

These fields represent the operational category, planned spending, and actual expense performance.

---

## How the Engine Works

The analysis workflow follows a structured pipeline:

Upload Financial Report  
↓  
Data Parsing  
↓  
Column Normalization  
↓  
Budget vs Actual Comparison  
↓  
Expense Distribution Analysis  
↓  
Variance Calculation  
↓  
Overspending Risk Detection  
↓  
Dashboard Visualization

This pipeline allows the system to transform raw financial reports into actionable financial diagnostics.

---

## Technology Stack

This project was built using the following tools:

Python  
Pandas  
Plotly  
Streamlit  

These technologies enable fast data processing and interactive operational dashboards.

---

## Running the Application

To run the dashboard locally:

pip install -r requirements.txt  
streamlit run app.py  

Once running, upload a financial report and the dashboard will automatically generate financial diagnostics.

---

## Use Case

This tool is designed for:

• Operations leaders  
• Business consultants  
• Financial analysts  
• Strategy and BizOps teams  

It provides a fast way to evaluate cost performance, diagnose financial risks, and improve operational budgeting.

---

## Repository Context

This project is part of a larger Operational Intelligence Toolkit — a collection of analytical engines designed to help operators quickly diagnose business performance using structured data analysis systems.
