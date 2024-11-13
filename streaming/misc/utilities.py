from datetime import datetime

from pyspark.sql import functions as F
from pyspark.sql import DataFrame

def convert_timestamp_in_datetime(timestamp) -> datetime:
    
    if timestamp is None:
        return
    
    return datetime.fromtimestamp(int(timestamp)/1000)


def process_sensor_data(df_kafka: DataFrame, df_metadata: DataFrame) -> DataFrame:
    """
    Process and join Kafka sensor data with metadata.
    
    Parameters:
        df_kafka (DataFrame): DataFrame containing the Kafka data with 'key' and 'value' columns.
        df_metadata (DataFrame): DataFrame containing metadata.
        
    Returns:
        DataFrame: The final joined DataFrame with parsed and processed fields.
    """

    # Select and cast fields from Kafka data
    df = df_kafka.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    df = df.select(
        F.get_json_object(df.value, '$.parsedPayload.temperature').cast('float').alias('temperature'),
        F.get_json_object(df.value, '$.parsedPayload.humidity').cast('float').alias('humidity'),
        F.get_json_object(df.value, '$.parsedPayload.battery').cast('float').alias('battery'),
        F.get_json_object(df.value, '$.parsedPayload.co2').cast('float').alias('co2'),
        F.get_json_object(df.value, '$.parsedPayload.tvoc').cast('float').alias('tvoc'),
        F.get_json_object(df.value, '$.parsedPayload.pressure').cast('float').alias('pressure'),
        F.get_json_object(df.value, '$.parsedPayload.light_level').cast('int').alias('light_level'),
        F.get_json_object(df.value, '$.parsedPayload.pir').alias('pir'),
        F.get_json_object(df.value, '$.DevEui').alias('DevEui'),
        F.get_json_object(df.value, '$.deviceName').alias('deviceName'),
        F.get_json_object(df.value, '$.GWInfo[0].gwname').alias('gwname'),
        F.get_json_object(df.value, '$.GWInfo[0].sendtime').cast('int').alias('sendtime'),
        F.get_json_object(df.value, '$.parsedPayload.battery_voltage').cast('float').alias('battery_voltage'),
        F.get_json_object(df.value, '$.parsedPayload.door_status').cast('int').alias('door_status'),
        F.get_json_object(df.value, '$.parsedPayload.door_open_times').cast('int').alias('door_open_times'),
        F.get_json_object(df.value, '$.parsedPayload.last_open_minutes').cast('int').alias('last_open_minutes'),
        F.get_json_object(df.value, '$.parsedPayload.alarm').cast('int').alias('alarm')
    )

    # Convert sendtime to timestamp
    df = df.withColumn("sendtime", F.from_unixtime(F.col("sendtime") / 1000).cast("timestamp"))

    # Perform join with metadata
    df = df.join(df_metadata, df["DevEui"] == df_metadata["DevEui"], "left")

    return df