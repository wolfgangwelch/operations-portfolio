import pandas as pd


def category_performance(df):

    category = df.groupby("category").agg(
        revenue=("revenue","sum"),
        units=("units","sum")
    ).reset_index()

    total_revenue = category["revenue"].sum()

    category["revenue_share"] = category["revenue"] / total_revenue

    return category.sort_values("revenue", ascending=False)


def sku_dominance(df):

    sku = df.groupby(["category","sku"]).agg(
        revenue=("revenue","sum"),
        units=("units","sum")
    ).reset_index()

    sku["category_total"] = sku.groupby("category")["revenue"].transform("sum")

    sku["category_share"] = sku["revenue"] / sku["category_total"]

    return sku.sort_values(["category","revenue"], ascending=False)


def concentration_risk(category_df):

    warnings = []

    for _, row in category_df.iterrows():

        if row["revenue_share"] > 0.5:

            warnings.append(
                f"{row['category']} contributes {row['revenue_share']:.1%} of total revenue."
            )

    return warnings
