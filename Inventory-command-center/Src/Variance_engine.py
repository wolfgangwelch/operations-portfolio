import pandas as pd
from src.data_loader import load_inventory, load_usage

def calculate_variance():

    inventory = load_inventory()
    usage = load_usage()

    merged = pd.merge(
        inventory,
        usage,
        on=["entity_id","asset_id","date"],
        how="left"
    )

    merged["usage_units"] = merged["usage_units"].fillna(0)

    merged["expected_remaining"] = (
        merged["quantity_on_hand"] - merged["usage_units"]
    )

    merged["variance"] = (
        merged["expected_remaining"] - merged["quantity_on_hand"]
    )

    return merged
