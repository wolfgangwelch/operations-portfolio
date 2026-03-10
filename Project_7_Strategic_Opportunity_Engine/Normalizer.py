import pandas as pd

def normalize_opportunity_data(df):

    column_map = {
        "date":"date",
        "category":"category",
        "revenue":"revenue",
        "units":"units"
    }

    df = df.rename(columns=column_map)

    df["date"] = pd.to_datetime(df["date"])

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    df["units"] = pd.to_numeric(df["units"], errors="coerce")

    return df
