#!/usr/bin/env python3

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import get_json_object, when, lit
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from misc.utilities import *

cluster_seeds = ['localhost:9042', 'localhost:9043']

# initialize the SparkSession
spark = SparkSession \
    .builder \
    .appName("Flight Streaming Analysis") \
    .config("spark.cassandra.connection.host", ','.join(cluster_seeds)) \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .getOrCreate()


# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url="http://influxdb2:8086", token="admin_admin_123456789", org="RomaTre")
write_api = influxdb_client.write_api()


# DF that cyclically reads events from Kafka
df_kafka = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092") \
    .option("subscribe", "live-data") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()


df_metadata = spark.read.option("header", True) \
    .csv("hdfs://hadoop-namenode:8020/iot-lorawan/metadata/sensor_registry_armellini.csv") \
    .cache()

df = df_kafka.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df = process_sensor_data(df_kafka=df_kafka, df_metadata=df_metadata)

"""query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start() \
    .awaitTermination()"""

"""# Apply watermark before aggregation
df_with_watermark = df.withWatermark("sendtime", "5 minutes")

# Esegui l'aggregazione sul DataFrame con watermark
correlation_df = df_with_watermark \
    .groupBy("DevEui") \
    .agg(
        F.corr("temperature", "humidity").alias("temp_humidity_corr"),
        F.corr("battery", "temperature").alias("battery_temp_corr"),
        F.corr("co2", "humidity").alias("co2_humidity_corr"),
        F.corr("battery_voltage", "door_status").alias("battery_door_corr"),
        F.corr("door_open_times", "co2").alias("door_co2_corr")
    )"""


"""
========================================================================================
Writing Streaming
========================================================================================
"""

# Write raw data on HDFS
"""df.writeStream \
    .format("csv") \
    .outputMode("append") \
    .option("path", "hdfs://hadoop-namenode:8020/iot-lorawn/raw/indoor_sensor_data.csv") \
    .option("checkpointLocation", "hdfs://hadoop-namenode:8020/iot-loraw/raw/checkpoints/indoor_sensor_data") \
    .start() \
    .awaitTermination()"""


def saveRawDataToInflux(row) -> None:
    point = Point("sensor_data") \
        .tag("DevEui", row.DevEui) \
        .tag("institute", row.institute) \
        .tag("profile", row.profile) \
        .tag("classroom", row.classroom) \
        .field("temperature", row.temperature) \
        .field("humidity", row.humidity) \
        .field("battery", row.battery) \
        .field("co2", row.co2) \
        .field("tvoc", row.tvoc) \
        .field("pressure", row.pressure) \
        .field("light_level", row.light_level) \
        .field("pir", row.pir) \
        .field("battery_voltage", row.battery_voltage) \
        .field("door_status", row.door_status) \
        .field("door_open_times", row.door_open_times) \
        .field("last_open_minutes", row.last_open_minutes) \
        .field("alarm", row.alarm) \
        .time(row.sendtime)
    try:
        write_api.write(bucket="home", org="RomaTre", record=point)
        print("Write successful")
    except Exception as e:
        print(f"Write failed: {e}")


# Write raw data to influxdb
df.writeStream \
    .foreach(saveRawDataToInflux) \
    .outputMode("append") \
    .start() \
    .awaitTermination()

"""def saveCorrelationDataToInflux(row) -> None:

    point = Point("correlation_data") \
        .tag("DevEui", row.DevEui) \
        .field("battery_temp_corr", row.battery_temp_corr) \
        .field("co2_humidity_corr", row.co2_humidity_corr) \
        .field("battery_door_corr", row.battery_door_corr) \
        .field("door_co2_corr", row.door_co2_corr) \
    
    try:
        write_api.write(bucket="home", org="RomaTre", record=point)
        print("Correlation write successful")
    except Exception as e:
        print(f"Write failed: {e}")"""

# write correlation data to InfluxDB
"""correlation_df.writeStream \
    .foreach(saveCorrelationDataToInflux) \
    .outputMode("update") \
    .start() \
    .awaitTermination()"""