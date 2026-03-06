import pandas as pd

from db_connection import get_cursor


def load_transfers(file_path: str = "data/raw/transfers.csv"):
    df = pd.read_csv(file_path)

    required = {
        "transfer_date",
        "product_name",
        "from_venue",
        "from_location",
        "to_venue",
        "to_location",
        "quantity",
        "manager",
        "notes",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in transfers file: {missing}")

    with get_cursor(commit=True) as (_, cur):
        for _, row in df.iterrows():
            cur.execute(
                "SELECT product_id FROM products WHERE product_name = %s;",
                (str(row["product_name"]).strip(),),
            )
            product = cur.fetchone()
            if not product:
                raise ValueError(f"Product not found: {row['product_name']}")
            product_id = product[0]

            cur.execute(
                """
                INSERT INTO transfers (
                    transfer_date,
                    product_id,
                    from_venue,
                    from_location,
                    to_venue,
                    to_location,
                    quantity,
                    manager,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    row["transfer_date"],
                    product_id,
                    int(row["from_venue"]),
                    int(row["from_location"]),
                    int(row["to_venue"]),
                    int(row["to_location"]),
                    float(row["quantity"]),
                    str(row["manager"]).strip(),
                    str(row["notes"]).strip(),
                ),
            )

    print("Transfer data loaded successfully.")


if __name__ == "__main__":
    load_transfers()
