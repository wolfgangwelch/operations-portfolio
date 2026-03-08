import pandas as pd

def load_entities():
    return pd.read_csv("data/raw/entities.csv")

def load_assets():
    return pd.read_csv("data/raw/assets.csv")

def load_inventory():
    df = pd.read_csv("data/raw/inventory_counts.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_usage():
    df = pd.read_csv("data/raw/asset_usage.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_reorder_rules():
    return pd.read_csv("data/raw/reorder_rules.csv")
