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

# Creating the docker net
echo -e "${YELLOW}Creating shared Docker network...${NC}"
sudo docker network create shared-net || echo -e "${YELLOW}Network 'shared-net' already exists.${NC}"

# Starting services
start_services

# Building & starting the server-proxy
start_server_proxy

# Creating useful folder on HDFS
echo -e "${YELLOW}Creating useful folder on HDFS...${NC}"
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /iot-lorawan
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /iot-lorawan/raw
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /iot-lorawan/metadata
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /iot-lorawan/generated
sudo docker exec -it hadoop-namenode hadoop fs -chmod 777 /iot-lorawan/raw
sudo docker exec -it hadoop-namenode hadoop fs -chmod 777 /iot-lorawan/metadata
sudo docker exec -it hadoop-namenode hadoop fs -chmod 777 /iot-lorawan/generated

echo -e "${YELLOW}Creating checkpoints folder on HDFS...${NC}"
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /iot-lorawan/checkpoints
sudo docker exec -it hadoop-namenode hadoop fs -chmod 777 /iot-lorawan/checkpoints

echo -e "${YELLOW}Waiting for 120 seconds before proceeding...${NC}"
sleep 120

# Init cassandra
echo -e "${YELLOW}Initializing Cassandra database...${NC}"
bash storage/cassandra/create-db.sh
echo -e "${GREEN}Cassandra database initialized successfully!${NC}"
