"""
DataPulse - Loading Layer (SQLAlchemy 1.4 compatible)
"""
import pandas as pd
from sqlalchemy import create_engine, text
import logging, os, sys, socket

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from transformation.transform import (
    transform_sales, build_date_dim,
    transform_customers, transform_products
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("datapulse.load")

try:
    socket.gethostbyname("datapulse_postgres")
    HOST = "datapulse_postgres"
except:
    HOST = "localhost"

DB_URL = os.getenv(
    "DATAPULSE_DB_URL",
    f"postgresql://datapulse:datapulse123@{HOST}:5432/datapulse_db"
)
log.info(f"Connecting to: {HOST}:5432")


def get_engine():
    return create_engine(DB_URL)


def truncate_tables(engine):
    # engine.begin() auto-commits in SQLAlchemy 1.4
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE sales_fact, date_dim, customer_dim, product_dim RESTART IDENTITY CASCADE"
        ))
    log.info("Tables truncated")


def load_customer_dim(engine):
    df = transform_customers()
    df.to_sql("customer_dim", engine, if_exists="append", index=False, method="multi")
    log.info(f"customer_dim: {len(df)} rows loaded")


def load_product_dim(engine):
    df = transform_products()
    df.to_sql("product_dim", engine, if_exists="append", index=False, method="multi")
    log.info(f"product_dim: {len(df)} rows loaded")


def load_date_dim(engine, df_sales):
    date_df = build_date_dim(df_sales)
    date_df.to_sql("date_dim", engine, if_exists="append", index=False, method="multi")
    log.info(f"date_dim: {len(date_df)} rows loaded")


def load_sales_fact(engine, df_sales):
    with engine.connect() as conn:
        date_map = pd.read_sql("SELECT date_id, full_date FROM date_dim", conn)
    date_map["full_date"]    = pd.to_datetime(date_map["full_date"]).dt.date
    df_sales["order_date_d"] = df_sales["order_date"].dt.date
    df_merged = df_sales.merge(date_map, left_on="order_date_d", right_on="full_date", how="left")
    fact = df_merged[[
        "order_id", "date_id", "customer_id", "product_id",
        "quantity", "sales", "discount", "profit"
    ]].rename(columns={"sales": "total_amount"})
    fact.to_sql("sales_fact", engine, if_exists="append", index=False, method="multi")
    log.info(f"sales_fact: {len(fact)} rows loaded")


def log_etl_run(engine, status, records_in, records_out, message=""):
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO etl_logs (pipeline, status, records_in, records_out, message)
                VALUES (:pipeline, :status, :records_in, :records_out, :message)
            """), {"pipeline": "datapulse_superstore", "status": status,
                   "records_in": records_in, "records_out": records_out, "message": message})
    except Exception as e:
        log.warning(f"Could not write etl_log: {e}")


def run():
    engine = get_engine()
    try:
        truncate_tables(engine)
        load_customer_dim(engine)
        load_product_dim(engine)
        df_sales = transform_sales()
        load_date_dim(engine, df_sales)
        load_sales_fact(engine, df_sales)
        log_etl_run(engine, "SUCCESS", 9994, 9986)
        log.info("DataPulse ETL completed successfully!")
    except Exception as e:
        log_etl_run(engine, "FAILED", 0, 0, str(e))
        log.error(f"ETL failed: {e}")
        raise


if __name__ == "__main__":
    run()