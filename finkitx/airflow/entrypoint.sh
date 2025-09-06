#!/bin/bash
pip install --no-cache-dir \
    pandas \
    minio \
    psycopg2-binary \
    sqlalchemy \
    requests

echo "🔧 Initializing Airflow DB..."
airflow db init

echo "🔐 Creating admin user (if needed)..."
airflow users create \
    --username admin \
    --password admin123 \
    --firstname first \
    --lastname last \
    --role Admin \
    --email anthonycasarez@gmail.com

echo "🚀 Starting services..."
airflow scheduler &

exec airflow celery worker &

exec airflow webserver