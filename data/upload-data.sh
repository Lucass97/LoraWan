#!bin/bash

sudo docker exec -it hadoop-namenode mkdir /opt/hadoop/data
sudo docker exec -it hadoop-namenode mkdir /opt/hadoop/data/iot-lorawan

sudo docker cp ./generated hadoop-namenode:/opt/hadoop/data/iot-lorawan/generated
sudo docker cp ./metadata hadoop-namenode:/opt/hadoop/data/iot-lorawan/metadata

sudo docker exec -it hadoop-namenode hadoop fs -put /opt/hadoop/data/iot-lorawan/generated/indoor_sensor_data.csv /iot-lorawan/generated/indoor_sensor_data.csv
sudo docker exec -it hadoop-namenode hadoop fs -put /opt/hadoop/data/iot-lorawan/metadata/sensor_registry_armellini.csv /iot-lorawan/metadata/sensor_registry_armellini.csv