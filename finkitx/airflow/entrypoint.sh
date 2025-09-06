#!/bin/bash
echo "🔧 Initializing Airflow DB..."
airflow db init

echo "🔐 Creating admin user (if needed)..."
airflow users create \
    --username admin \
    --password admin123 \
    --firstname first \
    --lastname last \
    --role Admin

echo "🚀 Starting services..."
airflow scheduler &

exec airflow webserver