import pandas as pd

def revenue_per_transaction(df):

    total_revenue = df["revenue"].sum()

    total_transactions = df["transactions"].sum()

    rpt = total_revenue / total_transactions

    return rpt


def revenue_per_unit(df):

    total_revenue = df["revenue"].sum()

    total_units = df["units"].sum()

    rpu = total_revenue / total_units

    return rpu


def category_efficiency(df):

    category = df.groupby("category").agg(
        revenue=("revenue","sum"),
        units=("units","sum"),
        transactions=("transactions","sum")
    ).reset_index()

    category["revenue_per_unit"] = category["revenue"] / category["units"]

    category["revenue_per_transaction"] = category["revenue"] / category["transactions"]

    return category.sort_values("revenue_per_unit", ascending=False)


def inefficiency_signals(df):

    signals = []

    rpt = revenue_per_transaction(df)

    if rpt < 20:

        signals.append(
            "⚠ Low revenue per transaction detected"
        )

    rpu = revenue_per_unit(df)

    if rpu < 10:

        signals.append(
            "⚠ Low revenue per unit detected"
        )

    return signals
