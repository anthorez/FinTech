from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from io import StringIO
import os
import boto3

# DAG Config
MINIO_BUCKET = "landing"
MINIO_FILENAME = "synthetic_large_100k.csv"  # Change as needed
POSTGRES_TABLE = "synthetic_customers"
POSTGRES_SCHEMA = "public"

# MinIO Config
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# Postgres Config
PG_HOST = "postgres"
PG_PORT = 5432
PG_DB = "finkit"
PG_USER = "admin"
PG_PASSWORD = "admin123"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

dag = DAG(
    dag_id='load_large_csv_to_postgres',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['minio', 'postgres', 'bulkload'],
)


def fetch_csv_from_minio(**kwargs):
    s3 = boto3.client(
        's3',
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    obj = s3.get_object(Bucket=MINIO_BUCKET, Key=MINIO_FILENAME)
    df = pd.read_csv(obj['Body'])
    kwargs['ti'].xcom_push(key='csv_data', value=df.to_json(orient='records'))
    return f"Retrieved {len(df)} records"


def load_to_postgres(**kwargs):
    import json

    # Load data
    df = pd.DataFrame(json.loads(kwargs['ti'].xcom_pull(key='csv_data')))
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    # Connect
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    cur = conn.cursor()

    # Create table if not exists (flexible schema based on columns)
    create_stmt = f"""
    CREATE TABLE IF NOT EXISTS {POSTGRES_SCHEMA}.{POSTGRES_TABLE} (
        id INT,
        name TEXT,
        email TEXT,
        signup_date DATE,
        balance NUMERIC
    );
    """
    cur.execute(create_stmt)
    conn.commit()

    # Copy insert
    buffer.seek(0)
    cur.copy_expert(
        sql=f"COPY {POSTGRES_SCHEMA}.{POSTGRES_TABLE} (id, name, email, signup_date, balance) FROM STDIN WITH CSV",
        file=buffer
    )
    conn.commit()
    cur.close()
    conn.close()

    return f"Loaded {len(df)} rows into {POSTGRES_SCHEMA}.{POSTGRES_TABLE}"


fetch_task = PythonOperator(
    task_id='fetch_csv_from_minio',
    python_callable=fetch_csv_from_minio,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    provide_context=True,
    dag=dag,
)

fetch_task >> load_task