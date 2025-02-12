#!/bin/bash

BASE_PATH="/opt/bitnami/spark/spark-streaming"
SCRIPT_NAME_TO_STOP="start-spark-streaming.py"
COMMON_FUNCTIONS_PATH="../scripts/spark_functions.sh"

source "${COMMON_FUNCTIONS_PATH}"

# Function to stop a Spark job running inside a Docker container
stop_spark_job() {
    
  local SCRIPT_NAME="$1"
  local CONTAINER_NAME="spark-master"

  # Find the PID of the process inside the container
  PID=$(sudo docker exec $CONTAINER_NAME ps aux | grep "$SCRIPT_NAME" | grep -v "grep" | awk '{print $2}')

  # Check if the PID was found
  if [ -z "$PID" ]; then
    echo -e "${RED}Process $SCRIPT_NAME not found running in container $CONTAINER_NAME.${NC}"
    return 1
  else
    echo -e "${GREEN}Found PID $PID for process $SCRIPT_NAME.${NC}"
    # Kill the process
    sudo docker exec $CONTAINER_NAME kill $PID
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}Process $SCRIPT_NAME (PID $PID) successfully terminated.${NC}"
    else
      echo -e "${RED}Error killing process $SCRIPT_NAME (PID $PID).${NC}"
      return 1
    fi
  fi
}

# Main script

echo -e "${YELLOW}Stopping Spark streaming script...${NC}"
stop_spark_job "$SCRIPT_NAME_TO_STOP"
clear_folder "$BASE_PATH"