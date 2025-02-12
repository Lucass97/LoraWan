#!/bin/bash

# Define output colors for better readability
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Function to copy a specified .env file into the Spark container
copy_env_file() {
    local env_file="$1"
    local destination_path="$2"

    echo -e "${YELLOW}Copying .env file to spark-master:$destination_path...${NC}"
    if [ -f "$env_file" ]; then
        sudo docker cp "$env_file" spark-master:"$destination_path" \
            && echo -e "${GREEN}.env file copied successfully to $destination_path!${NC}" \
            || echo -e "${RED}Failed to copy .env file to $destination_path${NC}"
    else
        echo -e "${RED}Error: $env_file not found. Continuing without copying .env file.${NC}"
    fi
}

# Function to ensure a specified folder exists inside the Spark container
ensure_folder_exists() {
    local folder_path="$1"

    echo -e "${YELLOW}Ensuring $folder_path exists in spark-master...${NC}"
    sudo docker exec -it spark-master mkdir -p "$folder_path" \
        && echo -e "${GREEN}$folder_path ensured.${NC}" \
        || echo -e "${RED}Failed to ensure $folder_path.${NC}"
}


# Function to clear a specified folder inside the Spark container
clear_folder() {
    local folder_path="$1"

    echo -e "${YELLOW}Clearing $folder_path in spark-master...${NC}"
    sudo docker exec -it spark-master rm -rf "$folder_path/*" \
        && echo -e "${GREEN}Cleared $folder_path${NC}" \
        || echo -e "${RED}Failed to clear $folder_path${NC}"
}


# Function to copy files into a specified path inside the Spark container
copy_files() {
    local source_path="$1"
    local destination_path="$2"

    echo -e "${YELLOW}Copying files from $source_path to spark-master:$destination_path...${NC}"
    sudo docker cp "$source_path" spark-master:"$destination_path" \
        && echo -e "${GREEN}All files copied successfully!${NC}" \
        || echo -e "${RED}Failed to copy files to $destination_path${NC}"
}

submit_spark_job() {
    local spark_packages="$1"
    local script_path="$2"
    local background_flag="$3"

    echo -e "${YELLOW}Submitting Spark job: $script_path with packages: $spark_packages...${NC}"

    if [ "$background_flag" == "true" ]; then
        # Submit Spark job in the background using nohup
        sudo docker exec -d spark-master nohup spark-submit --packages "$spark_packages" "$script_path" > /dev/null 2>&1 & \
        echo -e "${GREEN}Spark job submitted in the background successfully!${NC}"
    else
        # Submit Spark job in the foreground
        sudo docker exec -it spark-master spark-submit \
            --packages "$spark_packages" "$script_path" \
            && echo -e "${GREEN}Spark job submitted successfully!${NC}" \
            || echo -e "${RED}Failed to submit Spark job.${NC}"
    fi
}