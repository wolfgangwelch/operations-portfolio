import pandas as pd

def normalize_sales_data(df):

    column_map = {
        "date":"date",
        "category":"category",
        "sku":"sku",
        "units":"units",
        "revenue":"revenue"
    }

    df = df.rename(columns=column_map)

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")

    return df
