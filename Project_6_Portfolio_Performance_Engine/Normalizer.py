import pandas as pd

def normalize_portfolio_data(df):

    column_map = {
        "date":"date",
        "location":"location",
        "revenue":"revenue",
        "transactions":"transactions"
    }

    df = df.rename(columns=column_map)

    df["date"] = pd.to_datetime(df["date"])

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    df["transactions"] = pd.to_numeric(df["transactions"], errors="coerce")

    return df
