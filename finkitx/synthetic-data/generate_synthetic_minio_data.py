import pandas as pd
import numpy as np
import boto3
from io import StringIO
from faker import Faker
from datetime import datetime, timedelta

# -------------------------------
# ⚙️ Config
# -------------------------------
ROWS = 1000000  # Adjust this to stress test
MINIO_BUCKET = "landing"
MINIO_FILENAME = "synthetic_large.csv"
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# -------------------------------
# 🧠 Data Generation
# -------------------------------
fake = Faker()
np.random.seed(42)

def generate_data(n=1000):
    data = {
        "id": np.arange(1, n + 1),
        "name": [fake.name() for _ in range(n)],
        "email": [fake.email() for _ in range(n)],
        "signup_date": [fake.date_between(start_date='-2y', end_date='today') for _ in range(n)],
        "balance": np.round(np.random.uniform(0, 10000, size=n), 2)
    }
    return pd.DataFrame(data)

df = generate_data(ROWS)

# -------------------------------
# ☁️ Upload to MinIO
# -------------------------------
# Ensure bucket exists
s3 = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

try:
    s3.head_bucket(Bucket=MINIO_BUCKET)
except:
    print(f"Bucket '{MINIO_BUCKET}' does not exist. Creating it...")
    s3.create_bucket(Bucket=MINIO_BUCKET)

# Upload CSV
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=MINIO_BUCKET, Key=MINIO_FILENAME, Body=csv_buffer.getvalue())

print(f"✅ Uploaded {ROWS} rows to MinIO bucket '{MINIO_BUCKET}' as '{MINIO_FILENAME}'")