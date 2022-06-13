from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from clickhouse_driver import Client

from scripts.dag_2.transformations import (
    transform_orders_df,
    transform_products_df,
    transform_returns_df,
    merge_transformed_dfs,
    transform_merged_df,
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "catchup": False,
    "schedule_interval": timedelta(days=1),
    "start_date": datetime(2022, 6, 12),
}


def generate_orders_summary():
    client = Client(host="clickhouse", settings={"use_numpy": True})

    orders_df = client.query_dataframe("SELECT * from orders")
    products_df = client.query_dataframe("SELECT * from products")
    returns_df = client.query_dataframe("SELECT * from returns")

    transformed_orders_df = transform_orders_df(orders_df)
    transformed_products_df = transform_products_df(products_df)
    transformed_returns_df = transform_returns_df(returns_df)

    merged_df = merge_transformed_dfs(
        transformed_orders_df, transformed_products_df, transformed_returns_df
    )

    result_df = transform_merged_df(merged_df)

    client.insert_dataframe("INSERT INTO orders_summary VALUES", result_df)


with DAG(dag_id="dag_2", default_args=default_args) as dag:
    generate_orders_summary_task = PythonOperator(
        task_id="generate_orders_summary", python_callable=generate_orders_summary,
    )

    generate_orders_summary_task
