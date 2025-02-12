#!/usr/bin/env python3

from dotenv import dotenv_values

from pyspark.sql import SparkSession
from influxdb_client import InfluxDBClient

from storage.influxdb import *
from processing.processing import *

env_vars = dotenv_values("spark.env")
globals().update(env_vars)


# Initialize the SparkSession
spark = SparkSession \
    .builder \
    .appName("LoraWan") \
    .config("spark.cassandra.connection.host", ','.join(CASSANDRA_CLUSTERS)) \
    .config("spark.cassandra.auth.username", CASSANDRA_USERNAME) \
    .config("spark.cassandra.auth.password", CASSANDRA_PASSWORD) \
    .getOrCreate()


# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxdb_client.write_api()


"""
========================================================================================
Input Reading
========================================================================================
"""


# DF that cyclically reads events from Kafka
df_kafka = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", KAFKA_STARTING_OFFSETS) \
    .option("failOnDataLoss", "false") \
    .load()


df_metadata = spark.read.option("header", True) \
    .csv(METADATA_HDFS_PATH) \
    .cache()


"""
========================================================================================
Analysis
========================================================================================
"""


df_stream = process_sensor_data(df_kafka=df_kafka, df_metadata=df_metadata)

df_stats = calculate_classroom_statistics(df_stream=df_stream, window_duration=WINDOW_DURATION)

df_correlations = compute_correlations(df_stream=df_stream, window_duration=WINDOW_DURATION)


"""
========================================================================================
Writing Streaming
========================================================================================
"""

df_stream \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.show(100)) \
    .start() \
    .awaitTermination()


# Write raw data on HDFS
df_stream.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("path", RAW_INDOOR_SENSOR_HDFS_PATH) \
    .option("checkpointLocation", CHECKPOINT_RAW_INDOOR_SENSOR_HDFS_PATH) \
    .start() \
    .awaitTermination()


# Write raw data to InfluxDB
df_stream.writeStream \
    .foreach(saveRawDataToInflux(write_api=write_api)) \
    .outputMode("append") \
    .start() \
    .awaitTermination()

# Write stats data to InfluxDB
df_stats.writeStream \
    .foreach(saveStatisticsDataToInflux(write_api=write_api)) \
    .trigger(processingTime=WINDOW_DURATION) \
    .outputMode("complete") \
    .start() \
    .awaitTermination()

# Write correlation data to InfluxDB
df_correlations.writeStream \
    .foreach(saveCorrelationDataToInflux(write_api=write_api)) \
    .trigger(processingTime=WINDOW_DURATION) \
    .outputMode("complete") \
    .start() \
    .awaitTermination()