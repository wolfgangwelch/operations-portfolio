import pandas as pd

from db_connection import connect_db


def forecast_liquor_demand() -> pd.DataFrame:
    conn = connect_db()

    sales = pd.read_sql("SELECT * FROM pos_sales;", conn)
    recipes = pd.read_sql("SELECT * FROM recipes;", conn)
    products = pd.read_sql(
        "SELECT product_id, product_name, category, ounces_per_bottle FROM products;",
        conn,
    )
    shot_categories = pd.read_sql("SELECT * FROM shot_categories;", conn)

    conn.close()

    if sales.empty:
        return pd.DataFrame()

    sales["sale_date"] = pd.to_datetime(sales["sale_date"])

    cocktail_sales = sales[sales["sale_type"] == "cocktail"].copy()
    shot_sales = sales[sales["sale_type"] == "shot"].copy()

    cocktail_usage = pd.DataFrame()
    if not cocktail_sales.empty:
        cocktail_usage = cocktail_sales.merge(
            recipes, left_on="item_name", right_on="drink_name", how="inner"
        )
        cocktail_usage["ounces_used"] = (
            cocktail_usage["quantity"] * cocktail_usage["ounces_per_drink"]
        )
        cocktail_usage = cocktail_usage.merge(
            products[["product_id", "product_name", "category", "ounces_per_bottle"]],
            on="product_id",
            how="left",
        )
        cocktail_usage["bottles_used"] = (
            cocktail_usage["ounces_used"] / cocktail_usage["ounces_per_bottle"]
        )
        cocktail_usage["week"] = cocktail_usage["sale_date"].dt.to_period("W").astype(str)

    shot_usage = pd.DataFrame()
    if not shot_sales.empty:
        shot_sales["category_name"] = shot_sales["item_name"].str.replace(
            " Shot", "", regex=False
        )
        shot_usage = shot_sales.merge(
            shot_categories, on="category_name", how="inner"
        ).merge(
            products[["product_id", "product_name", "category", "ounces_per_bottle"]],
            left_on="category_name",
            right_on="category",
            how="inner",
        )
        shot_usage["ounces_used"] = shot_usage["quantity"] * shot_usage["ounces_per_shot"]
        shot_usage["bottles_used"] = (
            shot_usage["ounces_used"] / shot_usage["ounces_per_bottle"]
        )
        shot_usage["week"] = shot_usage["sale_date"].dt.to_period("W").astype(str)

    usage_frames = []
    if not cocktail_usage.empty:
        usage_frames.append(
            cocktail_usage[["product_id", "product_name", "week", "bottles_used"]]
        )
    if not shot_usage.empty:
        usage_frames.append(
            shot_usage[["product_id", "product_name", "week", "bottles_used"]]
        )

    if not usage_frames:
        return pd.DataFrame()

    usage = pd.concat(usage_frames, ignore_index=True)
    weekly_usage = (
        usage.groupby(["product_id", "product_name", "week"], as_index=False)["bottles_used"]
        .sum()
    )

    forecast = (
        weekly_usage.groupby(["product_id", "product_name"], as_index=False)["bottles_used"]
        .mean()
        .rename(columns={"bottles_used": "forecast_bottles_next_week"})
        .sort_values("forecast_bottles_next_week", ascending=False)
    )

    return forecast


if __name__ == "__main__":
    print(forecast_liquor_demand().head(20))
