#!/bin/bash

#TODO

# Define output colors for better readability
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Function to clean up directories in the container
remove_directories() {
    echo -e "${YELLOW}Removing directories in spark-master...${NC}"
    local directories=("misc")
    for dir in "${directories[@]}"; do
        sudo docker exec -it spark-master rm -r /opt/bitnami/spark/$dir \
            && echo -e "${GREEN}Removed /$dir${NC}" \
            || echo -e "${RED}Failed to remove /$dir${NC}"
    done
}

# Function to copy files into the container
copy_files() {
    echo -e "${YELLOW}Copying files to spark-master...${NC}"
    declare -A items=(
        ["./spark-downloader.py"]="/opt/bitnami/spark/spark-downloader.py"
        ["./misc"]="/opt/bitnami/spark/misc"
    )

    echo -e "${GREEN}"

    for src in "${!items[@]}"; do
        dst=${items[$src]}
        sudo docker cp $src spark-master:$dst \
            || echo -e "${RED}Failed to copy $src to $dst${NC}"
    done
}

# Main script
echo -e "${YELLOW}Starting Spark downloader script...${NC}"

remove_directories
copy_files

# Run the Spark stop script
echo -e "${YELLOW}Stopping Spark downloader job...${NC}"
sudo docker exec -it spark-master spark-submit spark-downloader.py \
    && echo -e "${GREEN}Spark downloader job stopped successfully!${NC}" \
    || echo -e "${RED}Failed to stop Spark downloader job.${NC}"

echo -e "${YELLOW}Script completed.${NC}"