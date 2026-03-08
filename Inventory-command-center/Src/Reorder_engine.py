import pandas as pd
from src.data_loader import load_inventory, load_reorder_rules

def generate_reorder_recommendations():

    inventory = load_inventory()
    reorder = load_reorder_rules()

    merged = pd.merge(
        inventory,
        reorder,
        on="asset_id",
        how="left"
    )

    reorder_items = merged[
        merged["quantity_on_hand"] <= merged["reorder_threshold"]
    ]

    reorder_items["recommended_order"] = reorder_items["reorder_quantity"]

    return reorder_items
