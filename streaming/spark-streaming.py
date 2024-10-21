#!/usr/bin/env python3

from pyspark.sql import SparkSession
from pyspark.sql.functions import get_json_object, month, avg, col, lit, sum
from datetime import datetime
from influxdb import InfluxDBClient, DataFrameClient

client = InfluxDBClient(host='localhost', port=8086, database='flight', username="user", password="pass")
client.switch_database('flight')

cluster_seeds = ['localhost:9042', 'localhost:9043']
# initialize the SparkSession

spark = SparkSession \
    .builder \
    .appName("Flight Streaming Analysis") \
    .config("spark.cassandra.connection.host", ','.join(cluster_seeds)) \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .getOrCreate()

# DF that cyclically reads events from Kafka
df_kafka = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "live-data") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

df = df_kafka.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df = df.select(
    get_json_object(df.value, '$.TEMPERATURE').alias('TEMPERATURE'),
    get_json_object(df.value, '$.HUMIDITY').alias('HUMIDITY'),
    get_json_object(df.value, '$.PIR').alias('PIR'),
    get_json_object(df.value, '$.LIGHTING').alias('LIGHTING'),
    get_json_object(df.value, '$.TVOC').alias('TVOC'),
    get_json_object(df.value, '$.CO2').alias('CO2'),
    get_json_object(df.value, '$.BAROMETRIC_PRESSURE').alias('BAROMETRIC_PRESSURE')
)


"""
========================================================================================
Analysis for Grafana
========================================================================================
"""

def saveRawDataToInflux(row):

    timestamp = row.get("TIMESTAMP", datetime.now())
    
    json_body = [
        {
            "measurement": "sensor_data",
            "tags": {
                "SENSOR_ID": row["SENSOR_ID"],
            },
            "time": timestamp,
            "fields": {
                "TEMPERATURE": row["TEMPERATURE"],
                "HUMIDITY": row["HUMIDITY"],
                "PIR": row["PIR"],
                "LIGHTING": row["LIGHTING"],
                "CO2": row["CO2"],
                "TVOC": row["TVOC"],
                "BAROMETRIC_PRESSURE": row["BAROMETRIC_PRESSURE"]
            }
        }
    ]
    
    client.write_points(json_body)


"""
========================================================================================
Writing Streaming
========================================================================================
"""

influx_query = df.writeStream \
    .foreach(saveRawDataToInflux) \
    .start()

influx_query.awaitTermination()