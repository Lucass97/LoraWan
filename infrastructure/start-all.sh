#!/bin/bash

compose_files=(
    'hadoop/docker-compose.yml'
    'spark/docker-compose.yml'
    'storage/cassandra/docker-compose.yml'
    'storage/influxdb/docker-compose.yml'
    'ingestion/kafka/docker-compose.yml'
)

start_services() {
    for compose_file in "${compose_files[@]}"; do
        echo "Starting services from $compose_file..."
        sudo docker compose -f "$compose_file" up -d
        if [ $? -ne 0 ]; then
            echo "Error from $compose_file"
            exit 1
        fi
    done
    echo "All services have been started successfully!"
}


sudo docker network create shared-net
start_services
echo "Waiting for 80 seconds before proceeding..."
sleep 80
bash storage/cassandra/create-db.sh