
# Modern Data Stack - Ports and Credentials

## ✅ Login Credentials

| Service      | Username      | Password      | Notes                         |
|--------------|---------------|---------------|-------------------------------|
| **PostgreSQL** | `admin`        | `admin123`     | DB: `finkit` (Port: 5432)     |
| **Metabase**   | `admin`        | `admin123`     | Web UI login                  |
| **MinIO**      | `minioadmin`   | `minioadmin`   | Access + Secret keys          |
| **Airflow**    | `admin`        | `admin123`     | Web UI login                  |
| **JupyterLab** | Token login    | `admin123`     | Use token at first launch     |

## 🔌 Port Mappings

| Service           | Local URL                          | Port(s)      |
|-------------------|------------------------------------|--------------|
| **PostgreSQL**     | —                                  | `5432`       |
| **MinIO (API)**    | http://localhost:9000              | `9000`       |
| **MinIO Console**  | http://localhost:9001              | `9001`       |
| **Kafka UI**       | http://localhost:8080              | `8080`       |
| **Schema Registry**| http://localhost:8081              | `8081`       |
| **Flink UI**       | http://localhost:8082              | `8082`       |
| **Trino UI**       | http://localhost:8083              | `8083`       |
| **Airflow UI**     | http://localhost:8084              | `8084`       |
| **Pinot Console**  | http://localhost:9002              | `9002`       |
| **Pinot Broker**   | http://localhost:8099              | `8099`       |
| **Metabase**       | http://localhost:3000              | `3000`       |
| **JupyterLab**     | http://localhost:8888              | `8888`       |
| **SQLMesh UI**     | http://localhost:7600              | `7600`       |
