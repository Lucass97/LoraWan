#!/bin/bash

# Output colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

sudo docker exec -it spark-master rm -r /opt/bitnami/spark/misc

sudo docker cp ./stop-spark-streaming.py spark-master:/opt/bitnami/spark/stop-spark-streaming.py
sudo docker cp ./misc spark-master:/opt/bitnami/spark/misc

sudo docker exec -it spark-master spark-submit stop-spark-streaming.py