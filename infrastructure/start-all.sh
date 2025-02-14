#!/bin/bash

# Output colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

compose_files=(
    'hadoop/docker-compose.yml'
    'spark/docker-compose.yml'
    'storage/cassandra/docker-compose.yml'
    'storage/influxdb/docker-compose.yml'
    'storage/postgres/docker-compose.yml'
    'ingestion/kafka/docker-compose.yml'
)


# Function to strating all services
start_services() {
    for compose_file in "${compose_files[@]}"; do
        echo -e "${YELLOW}Starting services from $compose_file...${NC}"
        sudo docker compose -f "$compose_file" up -d
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error starting services from $compose_file${NC}"
            exit 1
        fi
    done
    echo -e "${GREEN}All services have been started successfully!${NC}"
}

# Function to build and starting server-proxy
start_server_proxy() {
    echo -e "${YELLOW}Building & starting server-proxy...${NC}"
    sudo docker build -t server-proxy -f ingestion/server-proxy/Dockerfile ingestion/server-proxy
    sudo docker stop server-proxy 2>/dev/null
    sudo docker rm server-proxy 2>/dev/null
    sudo docker run --name server-proxy --network shared-net -d -p 80:80 server-proxy
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error starting server-proxy${NC}"
        exit 1
    fi
    echo -e "${GREEN}Server-proxy started successfully!${NC}"
}

# Function to create HDFS directories and set permissions
create_hdfs_directories() {
    echo -e "${YELLOW}Creating useful folders on HDFS...${NC}"
    
    directories=(
        "/iot-lorawan"
        "/iot-lorawan/raw"
        "/iot-lorawan/metadata"
        "/iot-lorawan/generated"
        "/iot-lorawan/checkpoints"
    )
    
    for dir in "${directories[@]}"; do
        echo -e -n "${GREEN}"
        sudo docker exec -it hadoop-namenode hadoop fs -mkdir "$dir"

        sudo docker exec -it hadoop-namenode hadoop fs -chmod 777 "$dir" \
            && echo -e "${GREEN}Set permissions for $dir${NC}" \
            || echo -e "${RED}Failed to set permissions for $dir${NC}"
    done
}

# Function to create a Docker network if it doesn't already exist
create_docker_network() {
    local network_name="shared-net"

    echo -e "${YELLOW}Creating Docker network: $network_name...${NC}"
    
    if sudo docker network ls | grep -q "$network_name"; then
        echo -e "${YELLOW}Network '$network_name' already exists.${NC}"
    else
        sudo docker network create "$network_name" \
            && echo -e "${GREEN}Docker network '$network_name' created successfully!${NC}" \
            || echo -e "${RED}Failed to create Docker network '$network_name'.${NC}"
    fi
}

# Function to initialize the Cassandra database
init_cassandra_db() {
    
    local script_path="$1"

    echo -e "${YELLOW}Initializing Cassandra database...${NC}"

    echo -e "${YELLOW}Waiting for 180 seconds before proceeding...${NC}"
    sleep 180
    
    if [ -f "$script_path" ]; then
        bash "$script_path" \
            && echo -e "${GREEN}Cassandra database initialized successfully!${NC}" \
            || echo -e "${RED}Failed to initialize Cassandra database.${NC}"
    else
        echo -e "${RED}Error: Cassandra initialization script not found at $script_path.${NC}"
    fi
}


# main script

create_docker_network
start_services
start_server_proxy
create_hdfs_directories
init_cassandra_db "storage/cassandra/create-db.sh"