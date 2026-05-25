"""
DataPulse - Transformation Layer
Cleans and validates Superstore data, builds all dimension tables.
Run: python transformation/transform.py
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("datapulse.transform")


def transform_sales(filepath="data/extracted/sales_raw.csv"):
    df = pd.read_csv(filepath)
    before = len(df)

    # Fix date
    df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=False)

    # Remove duplicates (same order + product combo)
    df.drop_duplicates(subset=["order_id", "product_id"], inplace=True)

    # Drop nulls in critical columns
    df.dropna(subset=["order_id", "customer_id", "product_id"], inplace=True)

    # Fix types
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["sales"]    = pd.to_numeric(df["sales"],    errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0)
    df["profit"]   = pd.to_numeric(df["profit"],   errors="coerce")

    # Remove invalid rows
    df = df[df["sales"] > 0]
    df = df[df["quantity"] > 0]

    # Add surrogate row key for fact table
    df = df.reset_index(drop=True)
    df["fact_id"] = df.index + 1

    log.info(f"Sales transform: {before} in -> {len(df)} clean records out")
    return df


def build_date_dim(df):
    """Generate date dimension from all unique order dates."""
    rows = []
    for d in df["order_date"].dt.date.unique():
        dt = pd.Timestamp(d)
        rows.append({
            "full_date":  d,
            "day":        dt.day,
            "month":      dt.month,
            "month_name": dt.strftime("%B"),
            "quarter":    dt.quarter,
            "year":       dt.year,
            "weekday":    dt.strftime("%A"),
            "is_weekend": dt.weekday() >= 5,
        })
    date_df = pd.DataFrame(rows).sort_values("full_date").reset_index(drop=True)
    log.info(f"date_dim: {len(date_df)} unique dates")
    return date_df


def transform_customers(filepath="data/extracted/customers.csv"):
    df = pd.read_csv(filepath)
    df.dropna(subset=["customer_id"], inplace=True)
    df.drop_duplicates(subset="customer_id", inplace=True)
    log.info(f"customer_dim: {len(df)} rows")
    return df


def transform_products(filepath="data/extracted/products.csv"):
    df = pd.read_csv(filepath)
    df.dropna(subset=["product_id"], inplace=True)
    df.drop_duplicates(subset="product_id", inplace=True)
    # Clean product names (remove extra whitespace)
    df["product_name"] = df["product_name"].str.strip()
    log.info(f"product_dim: {len(df)} rows")
    return df


if __name__ == "__main__":
    df = transform_sales()
    print("\nSales sample:")
    print(df[["order_id","customer_id","product_id","sales","profit"]].head())

    date_df = build_date_dim(df)
    print("\nDate dim sample:")
    print(date_df.head())
