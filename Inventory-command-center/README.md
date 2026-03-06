# Venue Inventory Command Center

A multi-venue inventory and bar control system built for nightlife operations.

The platform automates:

- inventory counts
- vendor purchases
- internal bar transfers
- inter-club transfers
- cocktail recipe mapping
- shot-based theoretical usage
- variance detection
- demand forecasting

## Core Business Problem

Nightlife venues often manage inventory through spreadsheets and ad hoc counting processes.  
That approach breaks down when you need:

- consistent weekly counts
- monthly audits
- bottle-level depletion tracking
- club-to-club borrowing
- purchase normalization
- reliable variance detection

This project converts that process into a structured operational data platform.

## Venue Network Modeled

- Gold Club
- Condor
- Hustler Club
- Penthouse
- Garden of Eden
- Little Darlings
- Hungry Eye
- Centerfolds
- New Century

## System Architecture

```mermaid
flowchart TD

A[POS System] --> B[POS Sales Loader]
C[Vendor Purchases] --> D[Purchase Loader]
E[Inventory Counts] --> F[Inventory Count Loader]
G[Product Transfers] --> H[Transfer Loader]

B --> I[(PostgreSQL Database)]
D --> I
F --> I
H --> I

I --> J[Recipe Engine]
J --> K[Theoretical Liquor Usage]
K --> L[Inventory Engine]
L --> M[Variance Engine]
M --> N[Analytics Views]
N --> O[Streamlit Dashboard]
