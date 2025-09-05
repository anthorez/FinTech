#!/bin/bash

echo "🔍 Modern Data Stack Health Check"
echo "================================"

# Define services and their health check URLs
declare -A services=(
    ["PostgreSQL"]="localhost:5432"
    ["MinIO"]="http://localhost:9000/minio/health/live"
    ["Kafka UI"]="http://localhost:8080"
    ["Schema Registry"]="http://localhost:8081"
    ["Flink"]="http://localhost:8082"
    ["Trino"]="http://localhost:8083/v1/info"
    ["Airflow"]="http://localhost:8084/health"
    ["Metabase"]="http://localhost:3000/api/health"
    ["Jupyter"]="http://localhost:8888"
    ["Pinot Controller"]="http://localhost:9002/health"
)

echo "📊 Service Health Status:"
for service in "${!services[@]}"; do
    url=${services[$service]}
    
    if [[ $url == http* ]]; then
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo "✅ $service - Healthy"
        else
            echo "❌ $service - Unhealthy ($url)"
        fi
    else
        # For non-HTTP services, try netcat
        IFS=':' read -r host port <<< "$url"
        if nc -z "$host" "$port" 2>/dev/null; then
            echo "✅ $service - Running"
        else
            echo "❌ $service - Not responding"
        fi
    fi
done

echo ""
echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "📋 Quick Access URLs:"
echo "   Metabase:         http://localhost:3000"
echo "   Kafka UI:         http://localhost:8080"
echo "   Trino:            http://localhost:8083"
echo "   Airflow:          http://localhost:8084"
echo "   Jupyter:          http://localhost:8888"
echo "   MinIO Console:    http://localhost:9001"
echo "   Pinot Controller: http://localhost:9002"
