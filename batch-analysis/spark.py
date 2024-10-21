#!/usr/bin/env python3
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, month, avg, year, dayofweek, count, when, sum, last_day, next_day, dayofyear, \
    dayofmonth, datediff, row_number, lit, max, min

from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType, TimestampType
from misc.utilities import *



cluster_seeds = ['cassandra1.shared-net:9042', 'cassandra2.shared-net:9042']

spark = SparkSession \
    .builder \
    .appName("Flight Batch Analysis") \
    .master("spark://spark-master:7077") \
    .config("spark.cassandra.connection.host", ','.join(cluster_seeds)) \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .getOrCreate()


schema = StructType([
    StructField("TIMESTAMP", TimestampType(), True), 
    StructField("SENSOR_ID", IntegerType(), True),    
    StructField("TEMPERATURE", FloatType(), True),   
    StructField("HUMIDITY", FloatType(), True),       
    StructField("PIR", FloatType(), True),          
    StructField("LIGHTING", FloatType(), True),    
    StructField("CO2", FloatType(), True),           
    StructField("TVOC", FloatType(), True),         
    StructField("BAROMETRIC_PRESSURE", IntegerType(), True) 
])
      
      
# Input
df = spark.read.option("header", True) \
    .schema(schema) \
    .csv("hdfs://hadoop-namenode:8020/generated/indoor_sensor_data.csv") \
    .cache()
    

agg_stats = (
        avg("TEMPERATURE").alias("AVG_TEMPERATURE"),
        max("TEMPERATURE").alias("MAX_TEMPERATURE"),
        min("TEMPERATURE").alias("MIN_TEMPERATURE"),
        avg("HUMIDITY").alias("AVG_HUMIDITY"),
        max("HUMIDITY").alias("MAX_HUMIDITY"),
        min("HUMIDITY").alias("MIN_HUMIDITY"),
        avg("CO2").alias("AVG_CO2"),
        max("CO2").alias("MAX_CO2"),
        min("CO2").alias("MIN_CO2"),
        avg("PIR").alias("AVG_PIR"),
        max("PIR").alias("MAX_PIR"),
        min("PIR").alias("MIN_PIR"),
        avg("LIGHTING").alias("AVG_LIGHTING"),
        max("LIGHTING").alias("MAX_LIGHTING"),
        min("LIGHTING").alias("MIN_LIGHTING"),
        avg("BAROMETRIC_PRESSURE").alias("AVG_B_PRESSURE"),
        max("BAROMETRIC_PRESSURE").alias("MAX_B_PRESSURE"),
        min("BAROMETRIC_PRESSURE").alias("MIN_B_PRESSURE"),
        avg("TVOC").alias("AVG_TVOC"),
        max("TVOC").alias("MAX_TVOC"),
        min("TVOC").alias("MIN_TVOC"),
    )

stats_by_year = df.groupBy(year("TIMESTAMP").alias("YEAR")) \
                .agg(*agg_stats)


stats_by_year_month = df.groupBy(year("TIMESTAMP").alias("YEAR"), month("TIMESTAMP").alias("MONTH")) \
                .agg(*agg_stats)


stats_by_year_month_day = df.groupBy(year("TIMESTAMP").alias("YEAR"), 
                month("TIMESTAMP").alias("MONTH"), 
                dayofmonth("TIMESTAMP").alias("DAY")) \
                .agg(*agg_stats)

# save raw data
"""df.write \
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="indoor_sensor_data_synthetic", keyspace="batchkeyspace") \
    .save()"""


# save data to cassandra
save_to_cassandra(stats_by_year, "stats_by_year")
save_to_cassandra(stats_by_year_month, "stats_by_year_month")
save_to_cassandra(stats_by_year_month_day, "stats_by_year_month_day")

spark.stop()
