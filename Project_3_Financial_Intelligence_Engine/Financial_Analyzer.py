import pandas as pd

def variance_analysis(df):

    df["variance"] = df["actual"] - df["budget"]

    df["variance_percent"] = (df["variance"] / df["budget"]) * 100

    return df


def category_expense_summary(df):

    category = df.groupby("category").agg(
        budget=("budget","sum"),
        actual=("actual","sum")
    ).reset_index()

    category["variance"] = category["actual"] - category["budget"]

    return category.sort_values("actual", ascending=False)


def overspending_alerts(df):

    alerts = []

    for _, row in df.iterrows():

        if row["variance_percent"] > 10:

            alerts.append(
                f"{row['category']} spending exceeds budget by {row['variance_percent']:.1f}%"
            )

    return alerts
