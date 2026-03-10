import pandas as pd

def category_revenue_share(df):

    category = df.groupby("category").agg(
        revenue=("revenue","sum")
    ).reset_index()

    total = category["revenue"].sum()

    category["revenue_share"] = category["revenue"] / total

    return category


def category_growth(df):

    df = df.sort_values("date")

    growth_data = []

    for category in df["category"].unique():

        cat = df[df["category"] == category]

        start = cat["revenue"].iloc[0]

        end = cat["revenue"].iloc[-1]

        growth = ((end - start) / start) * 100

        growth_data.append({
            "category":category,
            "growth_percent":growth
        })

    return pd.DataFrame(growth_data)


def opportunity_signals(share_df, growth_df):

    signals = []

    merged = share_df.merge(growth_df, on="category")

    for _, row in merged.iterrows():

        if row["growth_percent"] > 10 and row["revenue_share"] < 0.2:

            signals.append(
                f"Opportunity: {row['category']} growing quickly but underrepresented in revenue mix"
            )

        if row["growth_percent"] < 0:

            signals.append(
                f"⚠ {row['category']} revenue declining"
            )

    return signals
