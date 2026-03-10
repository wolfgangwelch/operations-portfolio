import pandas as pd

def parse_uploaded_file(uploaded_file):

    filename = uploaded_file.name

    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if filename.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Unsupported file type")
