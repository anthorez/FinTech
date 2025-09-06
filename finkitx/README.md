# Modern Data Stack

A modern data stack with all the essential components for data engineering, analytics, and machine learning.

## Management

### Scale a service
```bash
docker-compose up -d --scale flink-taskmanager=3
```

## Sample Data

The stack comes with sample data in PostgreSQL:
- `customers` table with sample customer data
- `orders` table with sample order data
- Pre-configured connections in Metabase and Trino

## Configuration

All configuration files are automatically created:
- Trino: `./trino-config/`
- Airflow: `./airflow/dags/`
- Jupyter: `./notebooks/`

## Next Steps

1. Connect to PostgreSQL and explore sample data
2. Create your first Metabase dashboard
3. Set up Kafka topics and Flink jobs
4. Query across databases with Trino
