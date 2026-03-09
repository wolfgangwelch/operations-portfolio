from __future__ import annotations

from typing import Dict, Optional

import pandas as pd


STANDARD_COLUMNS = [
    "date",
    "location",
    "category",
    "sku",
    "units",
    "revenue",
    "transaction_id",
]


def normalize_report(
    df: pd.DataFrame,
    mapping: Dict[str, Optional[str]],
    assigned_location: Optional[str] = None,
) -> pd.DataFrame:
    """
    Convert arbitrary uploaded columns into a standard internal schema.
    """
    normalized = pd.DataFrame()

    for target_col in STANDARD_COLUMNS:
        source_col = mapping.get(target_col)
        if source_col and source_col in df.columns:
            normalized[target_col] = df[source_col]
        else:
            normalized[target_col] = None

    if assigned_location:
        normalized["location"] = normalized["location"].fillna(assigned_location)

    # Type cleanup
    if normalized["date"].notna().any():
        normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")

    if normalized["units"].notna().any():
        normalized["units"] = pd.to_numeric(normalized["units"], errors="coerce")

    if normalized["revenue"].notna().any():
        normalized["revenue"] = pd.to_numeric(normalized["revenue"], errors="coerce")

    # Fill missing units with 1 if transaction-style data lacks units
    normalized["units"] = normalized["units"].fillna(1)

    # Drop rows with no date or no revenue
    normalized = normalized.dropna(subset=["date", "revenue"]).copy()

    # Default labels
    normalized["location"] = normalized["location"].fillna("Unassigned Location")
    normalized["category"] = normalized["category"].fillna("Uncategorized")
    normalized["sku"] = normalized["sku"].fillna("Unknown SKU")

    # Transaction ID fallback
    if normalized["transaction_id"].isna().all():
        normalized["transaction_id"] = [
            f"TXN_{i+1}" for i in range(len(normalized))
        ]

    return normalized.reset_index(drop=True)
