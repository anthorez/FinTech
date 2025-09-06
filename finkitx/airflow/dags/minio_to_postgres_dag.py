from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import boto3
import psycopg2
import io

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 1),
}

dag = DAG(
    'minio_to_postgres_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def fetch_csv_from_minio():
    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='minioadmin',
        aws_secret_access_key='minioadmin',
        region_name='us-east-1'
    )

    obj = s3.get_object(Bucket='datasets', Key='users.csv')
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    df.to_csv('/tmp/users.csv', index=False)
    print(df.head())  # Log preview

def insert_csv_to_postgres():
    df = pd.read_csv('/tmp/users.csv')

    conn = psycopg2.connect(
        host='postgres',
        port='5432',
        database='finkit',
        user='admin',
        password='admin123'
    )
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            age INT
        )
    """)

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (row['name'], row['email'], int(row['age']))
        )

    conn.commit()
    cur.close()
    conn.close()

with dag:
    t1 = PythonOperator(
        task_id='fetch_csv_from_minio',
        python_callable=fetch_csv_from_minio
    )

    t2 = PythonOperator(
        task_id='insert_csv_to_postgres',
        python_callable=insert_csv_to_postgres
    )

    t1 >> t2