# Portfolio Performance Engine

## Overview

The Portfolio Performance Engine analyzes performance across multiple business locations or operational units.

The system evaluates revenue, efficiency, and growth patterns across locations to identify which units are performing strongest and which require operational attention.

This engine helps leaders answer key questions such as:

• Which locations generate the most revenue?  
• Which units operate most efficiently?  
• Which locations are growing or declining?  
• Where should operational focus be directed?

---

## Why This Tool Exists

Organizations operating multiple locations often struggle to quickly evaluate performance differences across their portfolio.

Individual reports may exist for each unit, but comparing performance across locations can require significant manual analysis.

The Portfolio Performance Engine was designed to:

• Aggregate performance across multiple locations  
• Compare revenue generation by location  
• Analyze efficiency differences between locations  
• Detect declining performance automatically  

This enables operators to quickly identify where intervention or strategic focus may be required.

---

## Core Diagnostics

### Revenue by Location

The engine ranks locations based on total revenue generation.

Example:

Location A = $420,000  
Location B = $365,000  
Location C = $290,000

This highlights the highest-performing business units.

---

### Revenue Efficiency by Location

Measures how much revenue each location generates per transaction.

Example:

Location A = $45 revenue per transaction  
Location B = $38 revenue per transaction  
Location C = $30 revenue per transaction

This helps evaluate operational productivity across locations.

---

### Location Growth Analysis

The engine evaluates revenue growth trends across locations.

Example:

Location A growth = +12%  
Location B growth = +4%  
Location C growth = -3%

This allows leaders to identify which units are expanding or declining.

---

### Portfolio Alerts

The system automatically flags declining locations.

Example warning:

⚠ Location C revenue declining

These alerts highlight areas where operational intervention may be required.

---

## Dashboard Features

The Streamlit dashboard provides interactive portfolio diagnostics including:

• Revenue comparison across locations  
• Location efficiency metrics  
• Growth trend comparisons  
• Portfolio performance alerts

These visualizations allow leaders to quickly evaluate performance differences across the organization.

---

## Sample Dataset

sample_reports/sample_portfolio_data.csv

Expected columns:

date  
location  
revenue  
transactions

---

## How the Engine Works

Upload Portfolio Dataset  
↓  
Data Parsing  
↓  
Column Normalization  
↓  
Revenue Aggregation by Location  
↓  
Efficiency Analysis  
↓  
Growth Trend Calculation  
↓  
Portfolio Alert Detection  
↓  
Dashboard Visualization

---

## Technology Stack

Python  
Pandas  
NumPy  
Plotly  
Streamlit

---

## Running the Application

pip install -r requirements.txt  
streamlit run app.py

---

## Use Case

This tool is designed for:

• Operations leaders  
• Portfolio managers  
• Business consultants  
• Strategy teams  

It provides a simple way to analyze performance across multiple locations or business units.

---

## Repository Context

This project is part of the Operational Intelligence Toolkit — a collection of analytical engines designed to help operators diagnose and improve business performance.
