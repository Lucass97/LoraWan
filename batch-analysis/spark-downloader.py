from pyspark.sql import SparkSession
from misc.env import load_environment
from misc.parser import parse_args

args = parse_args()

load_environment(args.env_file)

spark = SparkSession.builder \
    .appName("Raw Downloader") \
    .getOrCreate()

local_path = "iot-lorawan/raw/indoor_sensor_data.csv"


try:
    df = spark.read.parquet(RAW_INDOOR_SENSOR_HDFS_PATH)

    df_ordered = df.orderBy("sendtime")

    df_ordered.coalesce(1).write.mode("overwrite").option("header", "true").csv(local_path)

    print(f"File successfully downloaded from HDFS: {RAW_INDOOR_SENSOR_HDFS_PATH} to {local_path}")

except Exception as e:
    print(f"An error occurred during the download: {e}")

finally:
    spark.stop()