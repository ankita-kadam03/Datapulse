"""
DataPulse - Extraction Layer
Reads raw Superstore CSV and splits into dimension source files.
Run: python extraction/extract.py
"""
import pandas as pd
import os, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("datapulse.extract")

RAW_FILE = "data/superstore.csv"
os.makedirs("data/extracted", exist_ok=True)

def extract():
    log.info(f"Reading {RAW_FILE} ...")
    df = pd.read_csv(RAW_FILE, encoding="latin1")
    log.info(f"Loaded {len(df)} raw rows, {df.shape[1]} columns")

    # ── Customer dimension ──────────────────────────────────────────
    customer_dim = df[["Customer ID","Customer Name","Segment","City","State","Region"]]\
        .drop_duplicates(subset="Customer ID")\
        .rename(columns={
            "Customer ID":   "customer_id",
            "Customer Name": "customer_name",
            "Segment":       "segment",
            "City":          "city",
            "State":         "state",
            "Region":        "region",
        })
    customer_dim.to_csv("data/extracted/customers.csv", index=False)
    log.info(f"customer_dim: {len(customer_dim)} unique customers")

    # ── Product dimension ───────────────────────────────────────────
    product_dim = df[["Product ID","Product Name","Category","Sub-Category"]]\
        .drop_duplicates(subset="Product ID")\
        .rename(columns={
            "Product ID":   "product_id",
            "Product Name": "product_name",
            "Category":     "category",
            "Sub-Category": "sub_category",
        })
    product_dim.to_csv("data/extracted/products.csv", index=False)
    log.info(f"product_dim: {len(product_dim)} unique products")

    # ── Sales fact (raw) ────────────────────────────────────────────
    sales = df[[
        "Order ID","Order Date","Customer ID","Product ID",
        "City","State","Region","Ship Mode",
        "Sales","Quantity","Discount","Profit"
    ]].rename(columns={
        "Order ID":    "order_id",
        "Order Date":  "order_date",
        "Customer ID": "customer_id",
        "Product ID":  "product_id",
        "Ship Mode":   "ship_mode",
        "Sales":       "sales",
        "Quantity":    "quantity",
        "Discount":    "discount",
        "Profit":      "profit",
    })
    sales.to_csv("data/extracted/sales_raw.csv", index=False)
    log.info(f"sales_raw: {len(sales)} rows extracted")

    log.info("Extraction complete!")
    return df

if __name__ == "__main__":
    extract()
