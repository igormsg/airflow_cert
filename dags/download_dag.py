from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain, cross_downstream


from datetime import datetime, timedelta

default_args = {
	'retries': 5,
	'retry_delay': timedelta(minutes=1),
	'email_on_failure': True,
	'email_on_retry': True
}

#def _download_data(ds,my_param):
def _download_data(ti,**kwargs):
	#print(ds)
	#print(my_param)
	with open('/tmp/my_fyle.txt','w') as f:
		f.write('my_data')
	ti.xcom_push(key='my_key',value=33)

#def _check_data(ti):
def _check_data(**kwargs):
	#my_xcom = ti.xcom_pull(key='return_value', task_ids=['download_data'])
	#my_xcom = kwargs['ti'].xcom_pull(key='return_value', task_ids=['download_data'])
	my_xcom = kwargs['ti'].xcom_pull(key='my_key', task_ids=['download_data'])
	print(my_xcom)

def _fail_callback(context):
	print('callback123')
	print(context)

with DAG(
    dag_id='download_dag',
    schedule_interval='@daily',
    start_date=days_ago(3),
    catchup=True,
    default_args=default_args
    ) as dag:
    
    download_data = PythonOperator(
    	task_id='download_data',
    	python_callable=_download_data
    	#op_kwargs={'my_param':42}
    )

    check_data = PythonOperator(
    	task_id='check_data',
    	python_callable=_check_data
    )

    wait_data = FileSensor(
    	task_id='wait_data',
    	fs_conn_id='fs_default',
    	filepath='my_file.txt',
    	poke_interval=30
    )

    process_data = BashOperator(
    	task_id='process_data',
    	bash_command='exit 1',
    	on_failure_callback=_fail_callback
    )

    #download_data.set_downstream(wait_data)

    #wait_data.set_downstream(process_data)

    #download_data >> [wait_data,process_data]

    #download_data >> wait_data >> process_data

    #chain(download_data,wait_data,process_data)

    #cross_downstream([download_data,check_data],[wait_data,process_data])

    download_data << check_data << wait_data << process_data
    #check_data >> [wait_data,process_data]


    