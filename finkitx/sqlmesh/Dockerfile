FROM --platform=linux/arm64 python:3.11-slim

# Set work directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install SQLMesh with optional features (web UI + Airflow + dbt compatibility)
RUN pip install "sqlmesh[web,airflow]"

# Set entrypoint
CMD ["sqlmesh"]