import pandas as pd

def revenue_by_location(df):

    revenue = df.groupby("location").agg(
        revenue=("revenue","sum")
    ).reset_index()

    return revenue.sort_values("revenue", ascending=False)


def revenue_per_transaction(df):

    location = df.groupby("location").agg(
        revenue=("revenue","sum"),
        transactions=("transactions","sum")
    ).reset_index()

    location["revenue_per_transaction"] = location["revenue"] / location["transactions"]

    return location


def growth_by_location(df):

    df = df.sort_values("date")

    growth_list = []

    for location in df["location"].unique():

        loc = df[df["location"] == location]

        start = loc["revenue"].iloc[0]

        end = loc["revenue"].iloc[-1]

        growth = ((end - start) / start) * 100

        growth_list.append({
            "location": location,
            "growth_percent": growth
        })

    return pd.DataFrame(growth_list)


def portfolio_alerts(growth_df):

    alerts = []

    for _, row in growth_df.iterrows():

        if row["growth_percent"] < 0:

            alerts.append(
                f"⚠ {row['location']} revenue declining"
            )

    return alerts
