import pandas as pd

from db_connection import get_cursor


def load_recipes(file_path: str = "data/raw/recipes.csv"):
    df = pd.read_csv(file_path)

    required = {"drink_name", "product_name", "ounces_per_drink"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in recipes file: {missing}")

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
                INSERT INTO recipes (drink_name, product_id, ounces_per_drink)
                VALUES (%s, %s, %s)
                ON CONFLICT (drink_name, product_id) DO UPDATE
                SET ounces_per_drink = EXCLUDED.ounces_per_drink;
                """,
                (
                    str(row["drink_name"]).strip(),
                    product_id,
                    float(row["ounces_per_drink"]),
                ),
            )

    print("Recipes loaded successfully.")


if __name__ == "__main__":
    load_recipes()
