#!/bin/bash

SPARK_PACKAGES="org.postgresql:postgresql:42.7.5,com.github.jnr:jnr-posix:3.1.20"
BASE_PATH="/opt/bitnami/spark/spark"
SCRIPT_NAME="start-spark.py"
LOCAL_ENV_PATH="../env/spark.env"
DOCKER_ENV_PATH="${BASE_PATH}/spark.env"
COMMON_FUNCTIONS_PATH="../scripts/spark_functions.sh"
COMMONS_PACKAGE="../commons"
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
copy_files "$COMMONS_PACKAGE" "$BASE_PATH" # Copy commons python library
submit_spark_job "$SPARK_PACKAGES" "$SCRIPT_PATH" "$BACKGROUND_EXEC" "$DOCKER_ENV_PATH"