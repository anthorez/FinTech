import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import boto3
from io import StringIO

# Configuration
BUCKET_NAME = "datalake"
OBJECT_NAME = "synthetic/5m_customers.csv"
ROWS = 5_000_000

# MinIO/S3 connection
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

def generate_synthetic_data(n):
    np.random.seed(42)
    domains = ["example.com", "email.com", "site.org", "domain.net"]
    cities = ["Boerne", "San Antonio", "Austin", "Dallas", "Houston"]
    states = ["TX", "CA", "NY", "FL", "WA"]

    data = {
        "id": np.arange(1, n + 1),
        "first_name": np.random.choice(["John", "Jane", "Alice", "Bob", "Maria", "Luke", "Ella"], size=n),
        "last_name": np.random.choice(["Smith", "Johnson", "Lee", "Brown", "Garcia", "Martinez"], size=n),
        "email": [f"user{i}@{np.random.choice(domains)}" for i in range(1, n + 1)],
        "city": np.random.choice(cities, size=n),
        "state": np.random.choice(states, size=n),
        "signup_date": pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, size=n), unit="D")
    }

    return pd.DataFrame(data)

def upload_to_minio(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )

    bucket_name = "datalake"
    object_name = "synthetic/5m_customers.csv"

    # Check if bucket exists, and create if it doesn't
    existing_buckets = s3.list_buckets()
    if not any(b["Name"] == bucket_name for b in existing_buckets["Buckets"]):
        s3.create_bucket(Bucket=bucket_name)
        print(f"🪣 Created bucket '{bucket_name}'")

    # Upload the file
    s3.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=csv_buffer.getvalue()
    )
    print(f"✅ Uploaded {object_name} to MinIO bucket '{bucket_name}'")

# Run
if __name__ == "__main__":
    print("🔄 Generating 5 million rows...")
    df = generate_synthetic_data(ROWS)

    print("📤 Uploading to MinIO...")
    upload_to_minio(df)