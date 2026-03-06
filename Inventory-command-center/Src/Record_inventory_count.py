import pandas as pd
from datetime import datetime

from db_connection import get_cursor


def fetch_df(cur, query: str) -> pd.DataFrame:
    cur.execute(query)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=cols)


def record_count():
    with get_cursor(commit=True) as (_, cur):
        venues = fetch_df(cur, "SELECT venue_id, venue_name FROM venues ORDER BY venue_id;")
        print("\nAvailable Venues:")
        print(venues.to_string(index=False))

        venue_id = int(input("\nEnter venue_id: "))

        cur.execute(
            """
            SELECT location_id, location_name
            FROM locations
            WHERE venue_id = %s
            ORDER BY location_id;
            """,
            (venue_id,),
        )
        loc_rows = cur.fetchall()
        locations = pd.DataFrame(loc_rows, columns=["location_id", "location_name"])
        print("\nLocations:")
        print(locations.to_string(index=False))

        location_id = int(input("\nEnter location_id: "))

        print("\nEnter inventory counts. Type 'done' when finished.\n")

        while True:
            product_name = input("Product name: ").strip()
            if product_name.lower() == "done":
                break

            cur.execute(
                """
                SELECT product_id, product_name
                FROM products
                WHERE LOWER(product_name) = LOWER(%s);
                """,
                (product_name,),
            )
            product = cur.fetchone()
            if not product:
                print("Product not found.\n")
                continue

            product_id = product[0]
            quantity = float(input("Quantity (partial bottles allowed): ").strip())
            count_type = input("Count type (weekly/audit): ").strip().lower()

            if count_type not in {"weekly", "audit"}:
                print("Invalid count type.\n")
                continue

            count_date = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not count_date:
                count_date = datetime.today().strftime("%Y-%m-%d")

            cur.execute(
                """
                INSERT INTO inventory_counts (
                    venue_id,
                    location_id,
                    product_id,
                    count_date,
                    quantity,
                    count_type
                )
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (venue_id, location_id, product_id, count_date, quantity, count_type),
            )
            print("Count recorded.\n")


if __name__ == "__main__":
    record_count()
