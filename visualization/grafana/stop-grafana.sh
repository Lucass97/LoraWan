#!/bin/bash

# Output colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

echo -e "${YELLOW}Stopping Grafana with Docker Compose...${NC}"
sudo docker compose down

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Grafana stopped successfully.${NC}"
else
    echo -e "${RED}Failed to stop Grafana.${NC}"
fi
