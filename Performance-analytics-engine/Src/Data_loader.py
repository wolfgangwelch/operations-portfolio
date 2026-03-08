import pandas as pd

def load_entities():
    return pd.read_csv("data/raw/entities.csv")

def load_sales():
    df = pd.read_csv("data/raw/sales.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_labor():
    df = pd.read_csv("data/raw/labor_hours.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_guests():
    df = pd.read_csv("data/raw/guest_counts.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df
