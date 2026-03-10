import pandas as pd

def normalize_financial_data(df):

    column_map = {
        "date":"date",
        "category":"category",
        "budget":"budget",
        "actual":"actual"
    }

    df = df.rename(columns=column_map)

    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
    df["actual"] = pd.to_numeric(df["actual"], errors="coerce")

    return df
