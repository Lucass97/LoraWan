#!/bin/bash

compose_files=(
    'hadoop/docker-compose.yml'
    'spark/docker-compose.yml'
    'storage/cassandra/docker-compose.yml'
    'ingestion/kafka/docker-compose.yml'
)

delete_cassandra_volumes() {
    read -p "Do you want to delete the Cassandra volumes (cassandra1-data, cassandra2-data, cassandra3-data)? [y/N] " confirm
    confirm=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    if [[ "$confirm" == "y" || "$confirm" == "yes" ]]; then
        echo "Deleting Cassandra volumes..."
        sudo docker volume rm cassandra_cassandra1-data cassandra_cassandra2-data cassandra_cassandra3-data
        if [ $? -ne 0 ]; then
            echo "Error deleting Cassandra volumes"
            exit 1
        fi
    else
        echo "Cassandra volumes not deleted."
    fi
}

stop_services() {
    for compose_file in "${compose_files[@]}"; do
        echo "Stopping services from $compose_file..."
        sudo docker compose -f "$compose_file" down
        if [ $? -ne 0 ]; then
            echo "Error from $compose_file"
            exit 1
        fi
    done
    echo "All services have been started successfully!"
}


stop_services
delete_cassandra_volumes