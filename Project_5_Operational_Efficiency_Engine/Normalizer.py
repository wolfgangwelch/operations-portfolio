import pandas as pd

def normalize_efficiency_data(df):

    column_map = {
        "date":"date",
        "category":"category",
        "units":"units",
        "revenue":"revenue",
        "transactions":"transactions"
    }

    df = df.rename(columns=column_map)

    df["date"] = pd.to_datetime(df["date"])

    df["units"] = pd.to_numeric(df["units"], errors="coerce")

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    df["transactions"] = pd.to_numeric(df["transactions"], errors="coerce")

    return df
