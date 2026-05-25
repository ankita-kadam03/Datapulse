"""
DataPulse - Data Generator
Generates realistic fake retail data for all dimension + fact tables.
Run: python extraction/generate_data.py
"""
import pandas as pd
from faker import Faker
import random, os

fake = Faker()
random.seed(42)

CATEGORIES = {
    "Electronics":    ["Phones", "Laptops", "Tablets", "Accessories"],
    "Furniture":      ["Chairs", "Tables", "Bookcases", "Shelving"],
    "Office Supplies":["Paper", "Pens", "Binders", "Labels"],
    "Clothing":       ["Shirts", "Shoes", "Bags", "Watches"],
}
REGIONS  = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]

os.makedirs("data", exist_ok=True)

def gen_customers(n=200):
    rows = [
        {
            "customer_id":   f"CUST{i:04d}",
            "customer_name": fake.name(),
            "segment":       random.choice(SEGMENTS),
            "city":          fake.city(),
            "state":         fake.state(),
            "region":        random.choice(REGIONS),
        }
        for i in range(1, n + 1)
    ]
    pd.DataFrame(rows).to_csv("data/customers.csv", index=False)
    print(f"Generated {n} customers -> data/customers.csv")

def gen_products(n=50):
    rows = []
    for i in range(1, n + 1):
        cat = random.choice(list(CATEGORIES.keys()))
        rows.append({
            "product_id":   f"PROD{i:03d}",
            "product_name": fake.catch_phrase(),
            "category":     cat,
            "sub_category": random.choice(CATEGORIES[cat]),
        })
    pd.DataFrame(rows).to_csv("data/products.csv", index=False)
    print(f"Generated {n} products -> data/products.csv")

def gen_stores(n=10):
    rows = [
        {
            "store_id":   f"STORE{i:02d}",
            "store_name": f"{fake.city()} Store",
            "city":       fake.city(),
            "state":      fake.state(),
            "region":     random.choice(REGIONS),
        }
        for i in range(1, n + 1)
    ]
    pd.DataFrame(rows).to_csv("data/stores.csv", index=False)
    print(f"Generated {n} stores -> data/stores.csv")

def gen_sales(n=2000):
    customers = pd.read_csv("data/customers.csv")["customer_id"].tolist()
    products  = pd.read_csv("data/products.csv")["product_id"].tolist()
    stores    = pd.read_csv("data/stores.csv")["store_id"].tolist()
    rows = []
    for _ in range(n):
        qty   = random.randint(1, 15)
        price = round(random.uniform(10, 800), 2)
        disc  = round(random.choice([0, 0.1, 0.2, 0.3]), 2)
        total = round(qty * price * (1 - disc), 2)
        rows.append({
            "order_id":     f"ORD-{fake.unique.random_int(10000, 99999)}",
            "customer_id":  random.choice(customers),
            "product_id":   random.choice(products),
            "store_id":     random.choice(stores),
            "order_date":   fake.date_between(start_date="-2y", end_date="today"),
            "quantity":     qty,
            "unit_price":   price,
            "discount":     disc,
            "total_amount": total,
            "profit":       round(total * random.uniform(0.05, 0.35), 2),
        })
    pd.DataFrame(rows).to_csv("data/sales_raw.csv", index=False)
    print(f"Generated {n} sales records -> data/sales_raw.csv")

if __name__ == "__main__":
    gen_customers()
    gen_products()
    gen_stores()
    gen_sales()
    print("\nAll data generated successfully!")
