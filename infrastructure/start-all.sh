#!/bin/bash
sudo docker compose -f hadoop/docker-compose.yml -f spark/docker-compose.yml up -d