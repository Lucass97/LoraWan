#!/bin/bash

# Output colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

echo -e "${YELLOW}Starting Grafana with Docker Compose...${NC}"
sudo docker compose up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Grafana started successfully.${NC}"
else
   
