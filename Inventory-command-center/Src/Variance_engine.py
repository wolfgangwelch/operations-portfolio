import pandas as pd

from db_connection import connect_db


def calculate_inventory_variance() -> pd.DataFrame:
    conn = connect_db()

    counts = pd.read_sql(
        """
        SELECT venue_id, location_id, product_id, count_date, quantity
        FROM inventory_counts
        ORDER BY count_date;
        """,
        conn,
    )
    purchases = pd.read_sql(
        """
        SELECT venue_id, product_id, purchase_date, bottle_quantity
        FROM purchases;
        """,
        conn,
    )
    transfers = pd.read_sql(
        """
        SELECT
            product_id,
            transfer_date,
            from_venue,
            from_location,
            to_venue,
            to_location,
            quantity
        FROM transfers;
        """,
        conn,
    )
    venues = pd.read_sql("SELECT venue_id, venue_name FROM venues;", conn)
    products = pd.read_sql("SELECT product_id, product_name FROM products;", conn)

    conn.close()

    counts["count_date"] = pd.to_datetime(counts["count_date"])
    purchases["purchase_date"] = pd.to_datetime(purchases["purchase_date"])
    transfers["transfer_date"] = pd.to_datetime(transfers["transfer_date"])

    results = []

    grouped = counts.groupby(["venue_id", "location_id", "product_id"])
    for (venue_id, location_id, product_id), group in grouped:
        group = group.sort_values("count_date")
        if len(group) < 2:
            continue

        for i in range(1, len(group)):
            start_row = group.iloc[i - 1]
            end_row = group.iloc[i]

            start_date = start_row["count_date"]
            end_date = end_row["count_date"]

            purchases_in_window = purchases[
                (purchases["venue_id"] == venue_id)
                & (purchases["product_id"] == product_id)
                & (purchases["purchase_date"] > start_date)
                & (purchases["purchase_date"] <= end_date)
            ]["bottle_quantity"].sum()

            transfer_in = transfers[
                (transfers["to_venue"] == venue_id)
                & (transfers["to_location"] == location_id)
                & (transfers["product_id"] == product_id)
                & (transfers["transfer_date"] > start_date)
                & (transfers["transfer_date"] <= end_date)
            ]["quantity"].sum()

            transfer_out = transfers[
                (transfers["from_venue"] == venue_id)
                & (transfers["from_location"] == location_id)
                & (transfers["product_id"] == product_id)
                & (transfers["transfer_date"] > start_date)
                & (transfers["transfer_date"] <= end_date)
            ]["quantity"].sum()

            expected_inventory = (
                start_row["quantity"] + purchases_in_window + transfer_in - transfer_out
            )
            actual_inventory = end_row["quantity"]
            variance = actual_inventory - expected_inventory

            results.append(
                {
                    "venue_id": venue_id,
                    "location_id": location_id,
                    "product_id": product_id,
                    "period_start": start_date.date(),
                    "period_end": end_date.date(),
                    "start_inventory": start_row["quantity"],
                    "purchases": float(purchases_in_window),
                    "transfer_in": float(transfer_in),
                    "transfer_out": float(transfer_out),
                    "expected_inventory": float(expected_inventory),
                    "actual_inventory": float(actual_inventory),
                    "variance": float(variance),
                }
            )

    result_df = pd.DataFrame(results)
    if result_df.empty:
        return result_df

    result_df = result_df.merge(venues, on="venue_id", how="left")
    result_df = result_df.merge(products, on="product_id", how="left")

    cols = [
        "venue_name",
        "product_name",
        "period_start",
        "period_end",
        "start_inventory",
        "purchases",
        "transfer_in",
        "transfer_out",
        "expected_inventory",
        "actual_inventory",
        "variance",
    ]
    return result_df[cols].sort_values(["venue_name", "product_name", "period_end"])


if __name__ == "__main__":
    print(calculate_inventory_variance().head(20))
