from pathlib import Path
from typing import List

import pandas as pd
import pdfplumber


RAW_PDF_PATH = Path("data/raw/Gold Club Liquor Inventory.pdf")
OUTPUT_PATH = Path("data/processed/products_master.csv")

NON_ALCOHOLIC_CATEGORIES = {
    "Soda",
    "Juice",
    "Energy Drink",
    "Water",
    "Mixer",
    "Non-Alcoholic",
}

CATEGORY_KEYWORDS = {
    "Vodka": ["vodka", "grey goose", "titos", "belvedere", "ketel"],
    "Tequila": ["tequila", "patron", "don julio", "casamigos", "herradura"],
    "Whiskey": ["whiskey", "bourbon", "jameson", "jack", "maker", "crown"],
    "Cognac": ["cognac", "hennessy", "remy"],
    "Rum": ["rum", "bacardi", "captain morgan"],
    "Gin": ["gin", "bombay", "tanqueray", "hendrick"],
    "Champagne/Wine": ["champagne", "wine", "moet", "veuve", "prosecco"],
    "Beer": ["beer", "corona", "heineken", "modelo", "bud", "coors"],
    "Energy Drink": ["red bull"],
    "Soda": ["coke", "sprite", "ginger ale", "tonic", "club soda"],
    "Juice": ["cranberry", "orange juice", "pineapple", "grapefruit"],
    "Water": ["water", "fiji", "sparkling"],
    "Mixer": ["sour mix", "simple syrup", "grenadine"],
}


def infer_category(product_name: str) -> str:
    name = product_name.lower().strip()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            return category
    return "Other"


def default_pour(category: str, alcoholic: bool) -> float | None:
    if not alcoholic:
        return None
    if category in {"Tequila", "Cognac", "Whiskey"}:
        return 2.0
    return 1.5


def extract_rows(pdf_path: Path) -> List[List[str]]:
    rows: List[List[str]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                rows.extend(table)
    return rows


def parse_inventory_sheet(pdf_path: Path = RAW_PDF_PATH) -> pd.DataFrame:
    rows = extract_rows(pdf_path)
    cleaned_products = []

    for row in rows:
        if not row:
            continue
        candidate = str(row[0]).strip() if row[0] else ""
        if not candidate:
            continue

        lowered = candidate.lower()
        skip_tokens = {
            "item",
            "cost",
            "main bar",
            "vip bar",
            "storage",
            "display",
            "total",
            "category",
            "inventory",
            "purchase",
            "sales",
            "pc",
            "pour cost",
        }
        if lowered in skip_tokens:
            continue
        if any(token in lowered for token in ["beginning inventory", "ending inventory"]):
            continue
        if len(candidate) < 2:
            continue

        cleaned_products.append(candidate)

    df = pd.DataFrame({"product_name": sorted(set(cleaned_products))})
    df["category"] = df["product_name"].apply(infer_category)
    df["alcoholic"] = ~df["category"].isin(NON_ALCOHOLIC_CATEGORIES)
    df["bottle_ml"] = df["alcoholic"].apply(lambda x: 750 if x else None)
    df["ounces_per_bottle"] = df["alcoholic"].apply(lambda x: 25.36 if x else None)
    df["default_pour_oz"] = df.apply(
        lambda row: default_pour(row["category"], row["alcoholic"]), axis=1
    )
    df["case_size"] = df["category"].apply(lambda c: 24 if c == "Beer" else 6)
    df["par_level"] = df["category"].apply(lambda c: 24 if c == "Beer" else 6)

    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    products = parse_inventory_sheet()
    products.to_csv(OUTPUT_PATH, index=False)
    print(f"Product catalog created at {OUTPUT_PATH}")
