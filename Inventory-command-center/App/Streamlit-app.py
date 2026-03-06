import pandas as pd
import streamlit as st

from src.db_connection import connect_db
from src.inventory_engine import inventory_snapshot, inventory_value, low_stock_alerts
from src.variance_engine import calculate_inventory_variance
from src.demand_forecast import forecast_liquor_demand


st.set_page_config(page_title="Inventory Command Center", layout="wide")
st.title("Venue Inventory Command Center")

page = st.sidebar.selectbox(
    "Select View",
    [
        "Inventory Snapshot",
        "Inventory Value",
        "Low Stock Alerts",
        "Transfers",
        "Vendor Spend",
        "Variance Report",
        "Demand Forecast",
    ],
)


def load_query(query: str) -> pd.DataFrame:
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


if page == "Inventory Snapshot":
    st.header("Current Inventory Snapshot")
    df = inventory_snapshot()
    st.dataframe(df, use_container_width=True)

elif page == "Inventory Value":
    st.header("Inventory Value")
    df = inventory_value()
    st.dataframe(df, use_container_width=True)

elif page == "Low Stock Alerts":
    st.header("Low Stock Alerts")
    df = low_stock_alerts()
    st.dataframe(df, use_container_width=True)

elif page == "Transfers":
    st.header("Transfers")
    query = """
    SELECT
        t.transfer_date,
        p.product_name,
        fv.venue_name AS from_venue,
        fl.location_name AS from_location,
        tv.venue_name AS to_venue,
        tl.location_name AS to_location,
        t.quantity,
        t.manager,
        t.notes
    FROM transfers t
    JOIN products p ON t.product_id = p.product_id
    JOIN venues fv ON t.from_venue = fv.venue_id
    JOIN locations fl ON t.from_location = fl.location_id
    JOIN venues tv ON t.to_venue = tv.venue_id
    JOIN locations tl ON t.to_location = tl.location_id
    ORDER BY t.transfer_date DESC;
    """
    st.dataframe(load_query(query), use_container_width=True)

elif page == "Vendor Spend":
    st.header("Vendor Spend")
    query = """
    SELECT
        p.purchase_date,
        v.vendor_name,
        ve.venue_name,
        pr.product_name,
        p.purchase_unit,
        p.quantity,
        p.bottle_quantity,
        p.unit_cost,
        p.bottle_quantity * p.unit_cost AS estimated_cost
    FROM purchases p
    LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
    JOIN venues ve ON p.venue_id = ve.venue_id
    JOIN products pr ON p.product_id = pr.product_id
    ORDER BY p.purchase_date DESC;
    """
    st.dataframe(load_query(query), use_container_width=True)

elif page == "Variance Report":
    st.header("Inventory Variance Report")
    df = calculate_inventory_variance()
    st.dataframe(df, use_container_width=True)

elif page == "Demand Forecast":
    st.header("Next Week Demand Forecast")
    df = forecast_liquor_demand()
    st.dataframe(df, use_container_width=True)
