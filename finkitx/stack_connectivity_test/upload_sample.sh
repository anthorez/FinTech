#!/bin/bash
# Upload sample_users.csv to MinIO using mc client
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb -p local/test-bucket
mc cp sample_users.csv local/test-bucket/
