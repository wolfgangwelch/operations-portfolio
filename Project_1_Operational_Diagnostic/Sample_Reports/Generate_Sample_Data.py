from __future__ import annotations

import numpy as np
import pandas as pd


def generate_sample_data(rows: int = 12000) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    dates = pd.date_range("2025-01-01", periods=180, freq="D")
    locations = ["Primary Location"]
    categories = ["Category A", "Category B", "Category C", "Category D"]
    skus = {
        "Category A": ["A_1", "A_2", "A_3", "A_4"],
        "Category B": ["B_1", "B_2", "B_3"],
        "Category C": ["C_1", "C_2", "C_3", "C_4", "C_5"],
        "Category D": ["D_1", "D_2"],
    }

    records = []

    for i in range(rows):
        date = rng.choice(dates)
        location = rng.choice(locations)
        category = rng.choice(categories, p=[0.42, 0.28, 0.20, 0.10])
        sku = rng.choice(skus[category])
        units = int(rng.integers(1, 5))

        base_price = {
            "Category A": 42,
            "Category B": 28,
            "Category C": 18,
            "Category D": 55,
        }[category]

        revenue = round(base_price * units * float(rng.uniform(0.9, 1.15)), 2)

        records.append(
            {
                "date": date,
                "location": location,
                "category": category,
                "sku": sku,
                "units": units,
                "revenue": revenue,
                "transaction_id": f"TXN_{100000 + i}",
            }
        )

    return pd.DataFrame(records).sort_values("date").reset_index(drop=True)


if __name__ == "__main__":
    df = generate_sample_data()
    df.to_csv("sample_reports/sample_operational_data.csv", index=False)
    print("Sample dataset generated: sample_reports/sample_operational_data.csv")
