#!/usr/bin/env python3

from pyspark.sql import SparkSession

from processing.processing import *
from commons.misc.env import load_environment
from misc.parser import parse_batch_args

args = parse_batch_args()

load_environment(args.env_file)

from storage.postgresdb import save_to_postgres

POSTGRES_PROPERTIES = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": POSTGRES_DRIVER
}


spark = SparkSession \
    .builder \
    .appName("IoT-LoraWAN Batch Analysis") \
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


save_to_postgres(stats_by_class_year_week, "stats_by_class_year_week", POSTGRES_PROPERTIES)


spark.stop()
