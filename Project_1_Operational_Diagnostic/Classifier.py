from typing import List


COLUMN_ALIASES = {
    "date": [
        "date", "transaction_date", "order_date", "sale_date", "business_date"
    ],
    "location": [
        "location", "site", "store", "venue", "branch", "unit"
    ],
    "category": [
        "category", "department", "segment", "product_category", "revenue_stream"
    ],
    "sku": [
        "sku", "item", "product", "product_name", "item_name"
    ],
    "units": [
        "units", "quantity", "qty", "units_sold", "count"
    ],
    "revenue": [
        "revenue", "sales", "net_sales", "gross_sales", "sales_total", "total_sales"
    ],
    "transaction_id": [
        "transaction_id", "txn_id", "ticket_id", "receipt_id", "order_id"
    ],
}


def _normalize_columns(columns: List[str]) -> List[str]:
    return [str(col).strip().lower() for col in columns]


def classify_report(columns: List[str]) -> str:
    normalized = _normalize_columns(columns)

    has_revenue = any(alias in normalized for alias in COLUMN_ALIASES["revenue"])
    has_sku = any(alias in normalized for alias in COLUMN_ALIASES["sku"])
    has_units = any(alias in normalized for alias in COLUMN_ALIASES["units"])
    has_txn = any(alias in normalized for alias in COLUMN_ALIASES["transaction_id"])

    if has_revenue and has_sku and has_units:
        return "item_sales_report"

    if has_revenue and has_txn:
        return "transaction_summary_report"

    if has_revenue:
        return "generic_revenue_report"

    return "unknown_report"


def auto_detect_column_mapping(columns: List[str]) -> dict:
    normalized = _normalize_columns(columns)
    mapping = {}

    for target_field, aliases in COLUMN_ALIASES.items():
        detected = None
        for original, norm in zip(columns, normalized):
            if norm in aliases:
                detected = original
                break
        mapping[target_field] = detected

    return mapping
