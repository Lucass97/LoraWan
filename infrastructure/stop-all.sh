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


# Function to delete Cassandra volumes
delete_cassandra_volumes() {
    read -p "$(echo -e "${YELLOW}Do you want to delete the Cassandra volumes? [y/N] ${NC}")" confirm
    confirm=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    if [[ "$confirm" == "y" || "$confirm" == "yes" ]]; then
        echo -e "${YELLOW}Deleting Cassandra volumes...${NC}"
        sudo docker volume rm cassandra_cassandra1-data cassandra_cassandra2-data cassandra_cassandra3-data
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error deleting Cassandra volumes${NC}"
            exit 1
        fi
        echo -e "${GREEN}Cassandra volumes deleted successfully!${NC}"
    else
        echo -e "${GREEN}Cassandra volumes not deleted.${NC}"
    fi
}

# Function to delete Hadoop volumes
delete_hadoop_volumes() {
    read -p "$(echo -e "${YELLOW}Do you want to delete the Hadoop volumes? [y/N] ${NC}")" confirm
    confirm=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    if [[ "$confirm" == "y" || "$confirm" == "yes" ]]; then
        echo -e "${YELLOW}Deleting Hadoop volumes...${NC}"
        sudo docker volume rm hadoop_datanode1-data hadoop_datanode2-data hadoop_namenode-data
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error deleting Hadoop volumes${NC}"
            exit 1
        fi
        echo -e "${GREEN}Hadoop volumes deleted successfully!${NC}"
    else
        echo -e "${GREEN}Hadoop volumes not deleted.${NC}"
    fi
}

# Function to delete InfluxDB volumes
delete_influxdb_volumes() {
    read -p "$(echo -e "${YELLOW}Do you want to delete the InfluxDB volumes? [y/N] ${NC}")" confirm
    confirm=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    if [[ "$confirm" == "y" || "$confirm" == "yes" ]]; then
        echo -e "${YELLOW}Deleting InfluxDB volumes...${NC}"
        sudo docker volume rm influxdb_influxdb2-config influxdb_influxdb2-data
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error deleting Hadoop volumes${NC}"
            exit 1
        fi
        echo -e "${GREEN}InfluxDB volumes deleted successfully!${NC}"
    else
        echo -e "${GREEN}InfluxDB volumes not deleted.${NC}"
    fi
}

# Function to stop all services
stop_services() {
    for compose_file in "${compose_files[@]}"; do
        echo -e "${YELLOW}Stopping services from $compose_file...${NC}"
        sudo docker compose -f "$compose_file" down
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error stopping services from $compose_file${NC}"
            exit 1
        fi
    done
    echo -e "${GREEN}All services have been stopped successfully!${NC}"
}

# Function to stop and remove the server-proxy container
stop_and_remove_server_proxy() {
    echo -e "${YELLOW}Stopping and removing server-proxy container...${NC}"

    # Stop the container
    sudo docker stop server-proxy \
        && echo -e "${GREEN}Server-proxy container stopped successfully!${NC}" \
        || echo -e "${RED}Failed to stop server-proxy container.${NC}"

    # Remove the container
    sudo docker rm server-proxy \
        && echo -e "${GREEN}Server-proxy container removed successfully!${NC}" \
        || echo -e "${RED}Failed to remove server-proxy container.${NC}"
}


# Main script

stop_services
stop_and_remove_server_proxy
delete_cassandra_volumes
delete_hadoop_volumes
delete_influxdb_volumes