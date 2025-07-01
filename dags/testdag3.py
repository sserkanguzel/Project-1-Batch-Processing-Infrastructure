from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello World")

with DAG(
    dag_id="simple_hello_world",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="print_hello",
        python_callable=hello_world,
    )