"""
DataPulse - Airflow DAG (Fixed for Docker paths)
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner":            "datapulse",
    "depends_on_past":  False,
    "start_date":       datetime(2024, 1, 1),
    "retries":          2,
    "retry_delay":      timedelta(minutes=2),
    "email_on_failure": False,
}

with DAG(
    dag_id="datapulse_superstore_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["datapulse", "superstore", "etl"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="cd /opt/airflow && python extraction/extract.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="cd /opt/airflow && python transformation/transform.py",
    )

    load = BashOperator(
        task_id="load_to_warehouse",
        bash_command="cd /opt/airflow && python loading/load.py",
    )

    validate = BashOperator(
        task_id="validate_data",
        bash_command="""cd /opt/airflow && python -c "
import pandas as pd
df = pd.read_csv('data/extracted/sales_raw.csv')
assert df['order_id'].notnull().all(), 'Null order IDs!'
assert (pd.to_numeric(df['sales']) > 0).all(), 'Negative sales!'
print(f'All checks passed! {len(df)} records validated.')
"
""",
    )

    extract >> transform >> load >> validate