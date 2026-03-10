import pandas as pd


def revenue_trend(df):

    df = df.sort_values("date")

    start = df["revenue"].iloc[0]

    end = df["revenue"].iloc[-1]

    growth = ((end - start) / start) * 100

    return growth


def revenue_per_transaction(df):

    revenue = df["revenue"].sum()

    transactions = df["transactions"].sum()

    return revenue / transactions


def revenue_per_unit(df):

    revenue = df["revenue"].sum()

    units = df["units"].sum()

    return revenue / units


def category_distribution(df):

    category = df.groupby("category").agg(
        revenue=("revenue","sum")
    ).reset_index()

    total = category["revenue"].sum()

    category["share"] = category["revenue"] / total

    return category


def executive_signals(df):

    signals = []

    category = category_distribution(df)

    for _, row in category.iterrows():

        if row["share"] > 0.6:

            signals.append(
                f"⚠ {row['category']} dominates revenue mix"
            )

    growth = revenue_trend(df)

    if growth < 0:

        signals.append(
            "⚠ Overall revenue declining"
        )

    return signals
