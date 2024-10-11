#!/usr/bin/env python3
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, month, avg, year, dayofweek, count, when, sum, last_day, next_day, dayofyear, \
    dayofmonth, datediff, row_number, lit, max


cluster_seeds = ['localhost:9042', 'localhost:9043']

spark = SparkSession \
    .builder \
    .appName("Flight Batch Analysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
    #config("spark.cassandra.connection.host", ','.join(cluster_seeds)) \
    #.config("spark.cassandra.auth.username", "cassandra") \
    #.config("spark.cassandra.auth.password", "cassandra") \
    

df = spark.read.option("header", True).csv("hdfs://hadoop-namenode:8020/generated/indoor_sensor_data.csv").cache()


df.show()


spark.stop()
