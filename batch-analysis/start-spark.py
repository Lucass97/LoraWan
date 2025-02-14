#!/usr/bin/env python3

from pyspark.sql import SparkSession

from processing.processing import *
from misc.env import load_environment
from misc.parser import parse_args

args = parse_args()

load_environment(args.env_file)

from storage.cassandradb import save_to_cassandra
from storage.postgresdb import save_to_postgres

POSTGRES_PROPERTIES = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": POSTGRES_DRIVER
}


spark = SparkSession \
    .builder \
    .appName("LoraWan") \
    .config("spark.cassandra.connection.host", ','.join(CASSANDRA_CLUSTERS)) \
    .config("spark.cassandra.auth.username", CASSANDRA_USERNAME) \
    .config("spark.cassandra.auth.password", CASSANDRA_PASSWORD) \
    .getOrCreate()


"""
========================================================================================
Input Reading
========================================================================================
"""


df = spark.read.option("header", True) \
    .option("inferSchema", "true") \
    .parquet(RAW_INDOOR_SENSOR_HDFS_PATH) \
    .cache() 


"""
========================================================================================
Analysis
========================================================================================
"""


agg_stats = define_aggregation_statistics()
stats_by_year_week = aggregate_by_year_week(df, agg_stats)
stats_by_class_year_week = aggregate_by_class_year_week(df, agg_stats)


"""
========================================================================================
Writing Streaming
========================================================================================
"""


save_to_cassandra(stats_by_class_year_week, "stats_by_class_year_week")
save_to_cassandra(stats_by_year_week, "stats_by_year_week")

save_to_postgres(df, "stats_by_class_year_week", POSTGRES_PROPERTIES)


spark.stop()