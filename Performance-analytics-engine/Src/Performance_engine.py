from src.kpi_engine import calculate_kpis

def summarize_performance():

    df = calculate_kpis()

    summary = df.groupby("entity_id").agg(
        total_revenue=("revenue","sum"),
        avg_ticket=("avg_ticket","mean"),
        revenue_per_labor_hour=("revenue_per_labor_hour","mean"),
        labor_efficiency=("labor_efficiency","mean")
    ).reset_index()

    return summary
