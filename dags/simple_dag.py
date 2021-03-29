from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

with DAG(
    dag_id='simple_dag',
    schedule_interval='@daily',
    start_date=days_ago(3),
    catchup=True
    ) as dag:
    
    task_1 = DummyOperator(
        task_id = 'task1'
    )


    