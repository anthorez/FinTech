from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import boto3
import psycopg2
from io import StringIO

def fetch_from_minio(**kwargs):
    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin"
    )
    obj = s3.get_object(Bucket="test-bucket", Key="sample_users.csv")
    data = obj['Body'].read().decode('utf-8')
    kwargs['ti'].xcom_push(key='csv_data', value=data)

def load_to_postgres(**kwargs):
    csv_data = kwargs['ti'].xcom_pull(task_ids='fetch_from_minio', key='csv_data')
    df = pd.read_csv(StringIO(csv_data))

    conn = psycopg2.connect(
        host="airflow-postgres",
        database="airflow",
        user="airflow",
        password="airflow123"
    )
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO users (id, first_name, last_name, email, signup_date) VALUES (%s, %s, %s, %s, %s)",
            (row['id'], row['first_name'], row['last_name'], row['email'], row['signup_date'])
        )
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="load_users_from_minio",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="fetch_from_minio",
        python_callable=fetch_from_minio
    )

    t2 = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    t1 >> t2
