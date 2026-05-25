"""
DataPulse - Data Quality Tests (Superstore)
Run: python tests/test_transform.py
"""
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_raw_file_exists():
    assert os.path.exists("data/superstore.csv"), "FAIL: superstore.csv not found in data/"
    print("PASS: superstore.csv exists")

def test_extraction_outputs():
    for f in ["customers.csv", "products.csv", "sales_raw.csv"]:
        assert os.path.exists(f"data/extracted/{f}"), f"FAIL: {f} not found"
    print("PASS: All extracted files exist")

def test_no_null_keys():
    df = pd.read_csv("data/extracted/sales_raw.csv")
    assert df["order_id"].notnull().all(),    "FAIL: Null order_ids"
    assert df["customer_id"].notnull().all(), "FAIL: Null customer_ids"
    assert df["product_id"].notnull().all(),  "FAIL: Null product_ids"
    print("PASS: No null key columns")

def test_no_negative_sales():
    df = pd.read_csv("data/extracted/sales_raw.csv")
    assert (pd.to_numeric(df["sales"]) > 0).all(), "FAIL: Negative/zero sales"
    print("PASS: All sales values are positive")

def test_discount_range():
    df = pd.read_csv("data/extracted/sales_raw.csv")
    disc = pd.to_numeric(df["discount"])
    assert disc.between(0, 1).all(), "FAIL: Discount outside 0-1 range"
    print("PASS: Discounts in valid range")

def test_expected_row_count():
    df = pd.read_csv("data/superstore.csv", encoding="latin1")
    assert len(df) == 9994, f"FAIL: Expected 9994 rows, got {len(df)}"
    print(f"PASS: Row count correct ({len(df)} rows)")

if __name__ == "__main__":
    test_raw_file_exists()
    test_extraction_outputs()
    test_no_null_keys()
    test_no_negative_sales()
    test_discount_range()
    test_expected_row_count()
    print("\nAll tests passed!")
