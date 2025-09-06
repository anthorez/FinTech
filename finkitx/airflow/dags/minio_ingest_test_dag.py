from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from minio import Minio
import pandas as pd
import io

def fetch_csv_from_minio():
    client = Minio(
        endpoint="minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket = "sample-data"
    object_name = "sample.csv"

    if not client.bucket_exists(bucket):
        raise Exception(f"Bucket {bucket} does not exist")

    response = client.get_object(bucket, object_name)
    csv_data = response.read()
    df = pd.read_csv(io.BytesIO(csv_data))
    print("✅ Sample data from MinIO:")
    print(df.head())

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='minio_ingest_test_dag',
    schedule_interval='@daily',
    default_args=default_args,
    description='Test DAG to read a CSV from MinIO and log the data'
) as dag:

    read_and_log = PythonOperator(
        task_id='read_csv_from_minio',
        python_callable=fetch_csv_from_minio
    )