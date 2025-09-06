# Modern Data Stack

This project provisions a full-featured local data stack using Docker Compose, tailored for analytics, streaming, orchestration, and modeling workloads. All port conflicts are resolved, credentials are pre-set, and each service is configured with persistence and health checks.

## Stack Overview

| Service         | Purpose                                      | Port(s)     |
|----------------|----------------------------------------------|-------------|
| PostgreSQL      | OLTP transactional database                  | 5432        |
| MinIO           | S3-compatible object storage                 | 9000, 9001  |
| Kafka           | Message broker for streaming pipelines       | 9092        |
| Schema Registry | Avro schema management for Kafka             | 8081        |
| Kafka UI        | Kafka topic browser                          | 8080        |
| Flink           | Real-time stream processing engine           | 8082        |
| Pinot           | Real-time OLAP analytics engine              | 9002, 8099  |
| Trino           | Federated SQL query engine                   | 8083        |
| Airflow         | Workflow orchestration                       | 8084        |
| Metabase        | BI dashboard and self-service analytics      | 3000        |
| Jupyter         | Notebook-based data exploration              | 8888        |
| SQLMesh         | Data modeling and CI/CD with DBT compatibility | 7600        |

## Default Credentials

| Service     | Username     | Password     |
|-------------|--------------|--------------|
| PostgreSQL  | admin        | admin123     |
| Metabase    | admin        | admin123     |
| MinIO       | minioadmin   | minioadmin   |
| Airflow     | admin        | admin123     |
| JupyterLab  | Token        | admin123     |

## File Structure

```

## Quick Start

1. Run the deployment script:

    ```bash
    ./deploy-bulletproof.sh
    ```

2. Launch the stack:

    ```bash
    docker-compose up -d
    ```

3. Check all service UIs:

| Service     | URL                         |
|-------------|-----------------------------|
| PostgreSQL  | localhost:5432              |
| MinIO       | http://localhost:9001       |
| Kafka UI    | http://localhost:8080       |
| Schema Reg. | http://localhost:8081       |
| Flink       | http://localhost:8082       |
| Pinot Ctrl  | http://localhost:9002       |
| Trino       | http://localhost:8083       |
| Airflow     | http://localhost:8084       |
| Metabase    | http://localhost:3000       |
| Jupyter     | http://localhost:8888       |
| SQLMesh     | http://localhost:7600       |


## Data Initialization

- PostgreSQL is seeded using `init-sql/01-init.sql` at container startup.
- Airflow DAGs are loaded from `airflow/dags/`
- Trino catalogs (PostgreSQL and in-memory) are pre-mounted via `trino-config/`

## Notes

- All ports are explicitly mapped to avoid conflicts.
- Volumes ensure container data persistence between restarts.
- SQLMesh UI is currently deprecated upstream and may eventually be removed.

## Requirements

- Docker + Docker Compose
- ARM64 (Apple Silicon) or Linux
- No other services running on the stack’s ports

---

This stack is designed for local development, experimentation, and prototype production workloads.

## ⚠️ Technical Debt

While this setup provides a powerful and modular foundation for modern analytics, there are known areas for improvement:

- **Airflow Secrets Handling**: Secrets are stored in environment variables. Replace with a secrets backend (e.g., HashiCorp Vault or Docker secrets).
- **Database Initialization Timing**: Metabase requires the `metabase` database to exist before starting. Currently, this requires a manual step or a script.
- **Security Hardening**: Default credentials are used across many services. These should be updated before production deployment.
- **Lack of Orchestration for Initial DAGs**: Airflow doesn’t pre-load DAGs or verify plugins. Consider adding a bootstrapping script.
- **Monitoring & Observability**: No Prometheus/Grafana setup for infrastructure metrics or alerting.
- **Local-only Development**: There is no deployment strategy defined for cloud-native environments (e.g., Kubernetes).
