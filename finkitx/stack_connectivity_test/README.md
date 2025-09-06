# Local Connectivity Test - Modern Data Stack

## 🧪 Use Case

Test connectivity across:
- MinIO (S3)
- Airflow (ETL)
- PostgreSQL (structured data)
- Trino & Metabase (query/BI layers)

## 🛠️ Files

- `sample_users.csv` – Demo dataset
- `upload_sample.sh` – Upload script to MinIO
- `airflow/dags/load_users_from_minio.py` – DAG to load CSV from MinIO → PostgreSQL
- `init-sql/01-init.sql` – Creates the target table

## ✅ Steps

1. Upload sample file to MinIO:
   ```bash
   chmod +x upload_sample.sh
   ./upload_sample.sh
   ```

2. Ensure `init-sql/01-init.sql` is run on Postgres startup (already mounted).

3. Trigger DAG `load_users_from_minio` in the Airflow UI (http://localhost:8084).

4. Validate data landed in Postgres:
   ```sql
   SELECT * FROM users;
   ```

5. Query it via Trino or visualize in Metabase.

---
This flow confirms E2E data flow between key services.
