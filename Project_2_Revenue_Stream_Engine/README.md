# Revenue Stream Intelligence Engine

## Overview

The Revenue Stream Intelligence Engine is an operational analytics tool designed to analyze revenue composition across categories and individual SKUs.

The system ingests structured sales reports and automatically identifies which revenue streams drive business performance and where potential concentration risks exist.

This engine helps operators and consultants quickly answer critical questions such as:

• Where does the majority of revenue originate?  
• Which products dominate their category?  
• Are revenue streams overly concentrated in a single category or SKU?  
• Which areas of the business present the strongest growth opportunity?

---

## Why This Tool Exists

Most businesses generate multiple sales reports but lack a clear understanding of how revenue is distributed across their product or service offerings.

This engine was designed to:

• Normalize raw sales data  
• Evaluate revenue contribution by category  
• Identify dominant SKUs within each category  
• Detect revenue concentration risks  

The goal is to accelerate revenue structure diagnostics, allowing operators to quickly identify where strategic focus should be placed.

---

## Core Diagnostics

The engine produces several analytical outputs.

### Revenue Mix Analysis

Determines the percentage contribution of each revenue category.

Example output:

Bar = 42%  
Food = 28%  
VIP = 20%  
Covers = 10%

---

### Category Performance Ranking

Ranks revenue categories based on total revenue and units sold.

This helps identify which operational areas drive the majority of revenue.

---

### SKU Dominance Analysis

Evaluates revenue contribution of individual SKUs within their category.

Example:

Bar Revenue = $400,000

Don Julio = 58%  
Casamigos = 22%  
Patron = 9%  
Other = 11%

This reveals which individual items dominate category performance.

---

### Revenue Concentration Detection

The system automatically flags revenue concentration risks.

Example warning:

⚠ Revenue concentration detected  
Bar contributes 62% of total revenue

High concentration can represent operational risk or lack of revenue diversification.

---

## Dashboard Features

The Streamlit dashboard provides interactive visualizations including:

• Revenue Mix Pie Chart  
• Category Revenue Bar Chart  
• SKU Dominance Tables  
• Revenue Concentration Warnings  
• Category Performance Tables  

These visualizations allow users to quickly identify revenue patterns and opportunities.

---

## Sample Dataset

A sample dataset is included in the repository to demonstrate the expected input format.

sample_reports/sample_sales_data.csv

Expected columns:

date  
category  
sku  
units  
revenue  

---

## How the Engine Works

The analysis workflow follows a structured pipeline.

Upload Sales Report  
↓  
Data Parsing  
↓  
Column Normalization  
↓  
Revenue Composition Analysis  
↓  
Category Performance Ranking  
↓  
SKU Dominance Detection  
↓  
Revenue Concentration Risk Detection  
↓  
Dashboard Visualization  

---

## Technology Stack

This project was built using the following tools:

Python  
Pandas  
Plotly  
Streamlit  

These tools enable fast operational analysis and interactive data visualization.

---

## Running the Application

To run the dashboard locally:

pip install -r requirements.txt  
streamlit run app.py  

Once running, upload a sales report and the dashboard will automatically generate revenue diagnostics.

---

## Use Case

This tool is designed for:

• Operational leaders  
• Consultants  
• Business analysts  
• Revenue strategy teams  

It provides a fast way to diagnose revenue structure and category performance across any industry that generates structured sales data.

---

## Repository Context

This project is part of a larger Operational Intelligence Toolkit — a collection of analytical engines designed to help operators quickly diagnose business performance using structured data analysis systems.
