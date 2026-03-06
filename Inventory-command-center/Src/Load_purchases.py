import pandas as pd

from db_connection import get_cursor


def ensure_vendor(cur, vendor_name: str) -> int:
    cur.execute(
        """
        INSERT INTO vendors (vendor_name)
        VALUES (%s)
        ON CONFLICT (vendor_name) DO UPDATE SET vendor_name = EXCLUDED.vendor_name
        RETURNING vendor_id;
        """,
        (vendor_name,),
    )
    return cur.fetchone()[0]


def load_purchases(file_path: str = "data/raw/purchases.csv"):
    df = pd.read_csv(file_path)

    required = {
        "venue_id",
        "purchase_date",
        "vendor_name",
        "product_name",
        "purchase_unit",
        "quantity",
        "unit_cost",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in purchases file: {missing}")

    with get_cursor(commit=True) as (_, cur):
        for _, row in df.iterrows():
            vendor_id = ensure_vendor(cur, str(row["vendor_name"]).strip())

            cur.execute(
                "SELECT product_id, case_size FROM products WHERE product_name = %s;",
                (str(row["product_name"]).strip(),),
            )
            product = cur.fetchone()
            if not product:
                raise ValueError(f"Product not found: {row['product_name']}")

            product_id, case_size = product
            purchase_unit = str(row["purchase_unit"]).strip().lower()

            if purchase_unit not in {"case", "bottle"}:
                raise ValueError(f"Invalid purchase_unit: {purchase_unit}")

            quantity = float(row["quantity"])
            bottle_quantity = quantity * case_size if purchase_unit == "case" else quantity

            cur.execute(
                """
                INSERT INTO purchases (
                    venue_id,
                    purchase_date,
                    vendor_id,
                    product_id,
                    purchase_unit,
                    quantity,
                    unit_cost,
                    bottle_quantity
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    int(row["venue_id"]),
                    row["purchase_date"],
                    vendor_id,
                    product_id,
                    purchase_unit,
                    quantity,
                    float(row["unit_cost"]),
                    float(bottle_quantity),
                ),
            )

    print("Purchase data loaded successfully.")


if __name__ == "__main__":
    load_purchases()
