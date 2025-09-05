from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sample_data_pipeline',
    default_args=default_args,
    description='Sample Data Pipeline',
    schedule_interval=timedelta(hours=1),
    catchup=False
)

task1 = BashOperator(
    task_id='extract_data',
    bash_command='echo "Extracting data..."',
    dag=dag
)

task2 = BashOperator(
    task_id='transform_data', 
    bash_command='echo "Transforming data..."',
    dag=dag
)

task1 >> task2
