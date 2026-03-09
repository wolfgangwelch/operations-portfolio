from __future__ import annotations

import io
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import pdfplumber


def parse_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))


def parse_excel(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_excel(io.BytesIO(file_bytes))


def parse_pdf(file_bytes: bytes) -> pd.DataFrame:
    """
    Extracts tables from a PDF and concatenates them.
    Assumes clean tabular PDFs.
    """
    tables: List[pd.DataFrame] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_table()
            if extracted and len(extracted) > 1:
                header = extracted[0]
                rows = extracted[1:]
                df = pd.DataFrame(rows, columns=header)
                tables.append(df)

    if not tables:
        return pd.DataFrame()

    return pd.concat(tables, ignore_index=True)


def parse_uploaded_file(uploaded_file) -> Tuple[pd.DataFrame, str]:
    """
    Returns dataframe + detected file extension.
    """
    filename = uploaded_file.name
    suffix = Path(filename).suffix.lower()
    file_bytes = uploaded_file.getvalue()

    if suffix == ".csv":
        return parse_csv(file_bytes), suffix
    if suffix in [".xlsx", ".xls"]:
        return parse_excel(file_bytes), suffix
    if suffix == ".pdf":
        return parse_pdf(file_bytes), suffix

    raise ValueError(f"Unsupported file type: {suffix}")
