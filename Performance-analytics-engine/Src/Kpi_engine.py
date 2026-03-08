import pandas as pd
from src.data_loader import load_sales, load_labor, load_guests

def calculate_kpis():

    sales = load_sales()
    labor = load_labor()
    guests = load_guests()

    merged = sales.merge(labor, on=["entity_id","date"])
    merged = merged.merge(guests, on=["entity_id","date"])

    merged["revenue_per_labor_hour"] = merged["revenue"] / merged["labor_hours"]

    merged["avg_ticket"] = merged["revenue"] / merged["guests"]

    merged["labor_efficiency"] = merged["guests"] / merged["labor_hours"]

    return merged
