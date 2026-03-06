import pandas as pd

from db_connection import get_cursor


def load_pos_sales(file_path: str = "data/raw/pos_sales.csv"):
    df = pd.read_csv(file_path)

    required = {"venue_id", "sale_date", "item_name", "sale_type", "quantity"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in POS sales file: {missing}")

    with get_cursor(commit=True) as (_, cur):
        for _, row in df.iterrows():
            sale_type = str(row["sale_type"]).strip().lower()
            if sale_type not in {"cocktail", "shot"}:
                raise ValueError(f"Invalid sale_type: {sale_type}")

            cur.execute(
                """
                INSERT INTO pos_sales (
                    venue_id,
                    sale_date,
                    item_name,
                    sale_type,
                    quantity
                )
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    int(row["venue_id"]),
                    row["sale_date"],
                    str(row["item_name"]).strip(),
                    sale_type,
                    int(row["quantity"]),
                ),
            )

    print("POS sales loaded successfully.")


if __name__ == "__main__":
    load_pos_sales()
