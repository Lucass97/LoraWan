# TODO


from pyspark.sql import SparkSession

from misc.constants import *

# Creazione di una sessione Spark
spark = SparkSession.builder \
    .appName("Raw Downloader") \
    .getOrCreate()

local_path = "iot-lorawan/raw/indoor_sensor_data.csv"

try:
    # Leggi il file da HDFS
    df = spark.read.text(RAW_INDOOR_SENSOR_HDFS_PATH)

    # Salva il DataFrame nel filesystem locale
    df.write.mode("overwrite").text(local_path)

    print(f"File scaricato con successo da HDFS: {RAW_INDOOR_SENSOR_HDFS_PATH} a {local_path}")
except Exception as e:
    print(f"Si è verificato un errore durante il download: {e}")
finally:
    # Ferma la sessione Spark
    spark.stop()
