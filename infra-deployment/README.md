# Modern Data Stack

A production-ready modern data stack with all the essential components for data engineering, analytics, and machine learning.

## 🏗️ Architecture

- **PostgreSQL** - OLTP database for transactional data
- **MinIO** - S3-compatible object storage  
- **Apache Kafka** - Message streaming platform
- **Apache Flink** - Stream processing engine
- **Apache Pinot** - Real-time OLAP database
- **Trino** - Federated query engine
- **Apache Airflow** - Workflow orchestration
- **Metabase** - Business intelligence platform
- **Jupyter** - Data science notebooks

## 🚀 Quick Start

```bash
# One command deployment
./deploy-bulletproof.sh

# Check health
./health-check.sh
```

## 🌐 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Metabase | http://localhost:3000 | Setup required |
| Kafka UI | http://localhost:8080 | None |
| Trino | http://localhost:8083 | None |
| Airflow | http://localhost:8084 | admin/admin123 |
| Jupyter | http://localhost:8888 | token: admin123 |
| MinIO Console | http://localhost:9001 | minioadmin/minioadmin |
| Pinot Controller | http://localhost:9002 | None |

## 🛠️ Management

```bash
# Start all services
docker-compose up -d

# Stop all services  
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Scale a service
docker-compose up -d --scale flink-taskmanager=3
```

## 📊 Sample Data

The stack comes with sample data in PostgreSQL:
- `customers` table with sample customer data
- `orders` table with sample order data
- Pre-configured connections in Metabase and Trino

## 🔧 Configuration

All configuration files are automatically created:
- Trino: `./trino-config/`
- Airflow: `./airflow/dags/`
- Jupyter: `./notebooks/`

## 🚨 Troubleshooting

1. **Port conflicts**: Check `docker-compose ps` and modify ports in docker-compose.yml
2. **Permission issues**: Run `chmod -R 777 airflow/`
3. **Service not starting**: Check logs with `docker-compose logs [service-name]`
4. **Health check**: Run `./health-check.sh`

## 📈 Next Steps

1. Connect to PostgreSQL and explore sample data
2. Create your first Metabase dashboard
4. Set up Kafka topics and Flink jobs
5. Query across databases with Trino
