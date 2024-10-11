#!bin/bash
sudo docker cp  ./generated hadoop-namenode:/opt/hadoop/data/generated
sudo docker exec -it hadoop-namenode hadoop fs -mkdir /generated
sudo docker exec -it hadoop-namenode hadoop fs -put /opt/hadoop/data/generated/indoor_sensor_data.csv /generated/indoor_sensor_data.csv