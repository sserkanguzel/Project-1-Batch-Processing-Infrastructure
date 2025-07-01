from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='k8s_pod_operator_example',
    default_args=default_args,
    schedule_interval=None,
    description='Run a simple Kubernetes Pod from Airflow',
    tags=['k8s'],
) as dag:

    run_pod = KubernetesPodOperator(
        task_id="run-echo",
        name="run-echo",
        namespace="airflow",
        image="busybox",
        cmds=["echo", "Hello from KubernetesPodOperator!"],
        is_delete_operator_pod=True,  # Set False to keep pod after run (debugging)
    )
