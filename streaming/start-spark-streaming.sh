#!/bin/bash

SPARK_PACKAGES="com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,com.github.jnr:jnr-posix:3.1.20,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3"
BASE_PATH="/opt/bitnami/spark/spark-streaming"
SCRIPT_NAME="start-spark-streaming.py"
LOCAL_ENV_PATH="../env/spark.env"
DOCKER_ENV_PATH="${BASE_PATH}/spark.env" 
COMMON_FUNCTIONS_PATH="../scripts/spark_functions.sh"
SCRIPT_PATH="$BASE_PATH/$SCRIPT_NAME"

BACKGROUND_EXEC="false"

source "${COMMON_FUNCTIONS_PATH}"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --background) BACKGROUND_EXEC="true"; shift ;;  # Set background execution to true
        --foreground) BACKGROUND_EXEC="false"; shift ;;  # Set background execution to false
        *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;  # Handle unknown options
    esac
done

# Main script

echo -e "${YELLOW}Starting Spark streaming script...${NC}"
ensure_folder_exists "$BASE_PATH"
clear_folder "$BASE_PATH"
copy_env_file "$LOCAL_ENV_PATH" "$DOCKER_ENV_PATH"
copy_files "." "$BASE_PATH"
submit_spark_job "$SPARK_PACKAGES" "$SCRIPT_PATH" "$BACKGROUND_EXEC" "$DOCKER_ENV_PATH"