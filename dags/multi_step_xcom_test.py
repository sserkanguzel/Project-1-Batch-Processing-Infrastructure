from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

from datetime import timedelta

default_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="multi_step_xcom_example",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    def generate_message(**kwargs):
        message = "Hello from PythonOperator"
        kwargs['ti'].xcom_push(key='msg', value=message)

    generate_task = PythonOperator(
        task_id='generate_message',
        python_callable=generate_message,
        provide_context=True,
    )
    
    process_in_pod = KubernetesPodOperator(
        task_id='process_message_in_pod',
        name='process-message',
        namespace='airflow',
        image='python:3.9-slim',
        cmds=["python", "-c"],
        arguments=[
            "import os, json; "
            "msg = os.getenv('MESSAGE', ''); "
            "processed = f'Processed: {msg}'; "
            "print(processed); "
            "json.dump({'return': processed}, open('/airflow/xcom/return.json', 'w'))"
        ],
        env_vars={
            'MESSAGE': '{{ ti.xcom_pull(task_ids="generate_message", key="msg") }}'
        },
        get_logs=True,
        in_cluster=True,
        is_delete_operator_pod=True,
        do_xcom_push=True,
    )

    def consume_message(**kwargs):
        logs = kwargs['ti'].xcom_pull(task_ids='process_message_in_pod')
        print(f"Message from pod logs:\n{logs}")

    consume_task = PythonOperator(
        task_id='consume_result',
        python_callable=consume_message,
        provide_context=True,
    )

    generate_task >> process_in_pod >> consume_task
