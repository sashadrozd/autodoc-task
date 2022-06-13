import os

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import timedelta, datetime
import pandas as pd

from scripts.dag_1.transformations import transform_orders_df, generate_report

EMAIL_TO = os.getenv("EMAIL_TO")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "catchup": False,
    "schedule_interval": timedelta(days=1),
    "start_date": datetime(2022, 6, 12),
}


def compare_files(ti):
    orders_original = pd.read_csv("/data/orders1.csv")
    orders_generated = pd.read_csv("/data/orders2.csv")

    orders_original = transform_orders_df(orders_original)

    generate_report(df1=orders_generated, df2=orders_original)

    if orders_original.equals(orders_generated):
        html_content = "<h4>Transformation generate correct file. Comparison details attached.</h4>"
    else:
        html_content = "<h4>File was generated with mistakes. Comparison details attached.</h4>"

    ti.xcom_push(key="html_content", value=html_content)


with DAG(dag_id="dag_1", default_args=default_args) as dag:
    compare_files = PythonOperator(
        task_id="compare_files", python_callable=compare_files
    )
    send_email_task = EmailOperator(
        task_id="send_email_task",
        to=EMAIL_TO,
        subject="File Comparison | Report",
        html_content="{{task_instance.xcom_pull(task_ids='compare_files', key='html_content')}}",
        files=["/data/report.txt"],
    )

compare_files >> send_email_task
