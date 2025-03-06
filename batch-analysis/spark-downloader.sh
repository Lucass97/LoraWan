#!/bin/bash

SPARK_PACKAGES="org.postgresql:postgresql:42.7.5,com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,com.github.jnr:jnr-posix:3.1.20,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3"
BASE_PATH="/opt/bitnami/spark/spark-downloader" 
SCRIPT_NAME="spark-downloader.py"
LOCAL_ENV_PATH="../env/spark.env"
DOCKER_ENV_PATH="${BASE_PATH}/spark.env" 
COMMON_FUNCTIONS_PATH="../scripts/spark_functions.sh"
SCRIPT_PATH="$BASE_PATH/$SCRIPT_NAME"

BACKGROUND_EXEC="false"

LOCAL_RAW_PATH="../data/raw"

source "${COMMON_FUNCTIONS_PATH}"

# Function to copy a specified file from the Spark container to the host
copy_from_container() {
    local container_path="$1"
    local host_destination="$2"

    echo -e "${YELLOW}Copying file from container to host...${NC}"
    sudo docker cp "spark-master:$container_path" "$host_destination" \
        && echo -e "${GREEN}File copied successfully to $host_destination!${NC}" \
        || echo -e "${RED}Failed to copy file from container to host${NC}"
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --background) BACKGROUND_EXEC="true"; shift ;;  # Set background execution to true
        --foreground) BACKGROUND_EXEC="false"; shift ;;  # Set background execution to false
        *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;  # Handle unknown options
    esac
done

# Main script

echo -e "${YELLOW}Starting Spark downloader script...${NC}"
ensure_folder_exists "$BASE_PATH"
clear_folder "$BASE_PATH"
copy_env_file "$LOCAL_ENV_PATH" "$DOCKER_ENV_PATH"
copy_files "." "$BASE_PATH"
submit_spark_job "$SPARK_PACKAGES" "$SCRIPT_PATH" "$BACKGROUND_EXEC" "$DOCKER_ENV_PATH"
copy_from_container "/opt/bitnami/spark/iot-lorawan/raw/indoor_sensor_data.csv" "../data/raw/"