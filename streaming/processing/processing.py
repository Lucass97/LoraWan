from pyspark.sql import functions as F
from pyspark.sql import DataFrame


def process_sensor_data(df_kafka: DataFrame, df_metadata: DataFrame) -> DataFrame:
    """
    Process and integrate Kafka sensor data with metadata for further analysis.

    This function extracts sensor data from Kafka messages, parses fields such as temperature, humidity, CO2, and more, and joins the processed data with metadata. It also converts UNIX timestamps to readable timestamp formats.

    Parameters:
        df_kafka (DataFrame): 
            - A Spark DataFrame containing Kafka data with 'key' and 'value' columns. 
            - The 'value' column is expected to be a JSON string containing sensor data fields.
        df_metadata (DataFrame): 
            - A Spark DataFrame containing metadata. 
            - Must include a 'DevEui' column to allow for a join with the sensor data.

    Returns:
        DataFrame: 
            - A Spark DataFrame with parsed sensor data fields joined with metadata.
            - Includes timestamp conversion for the `sendtime` field.
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
        F.get_json_object(df.value, '$.GWInfo[0].sendtime').alias('sendtime'),
        F.get_json_object(df.value, '$.parsedPayload.battery_voltage').cast('float').alias('battery_voltage'),
        F.get_json_object(df.value, '$.parsedPayload.door_status').cast('int').alias('door_status'),
        F.get_json_object(df.value, '$.parsedPayload.door_open_times').cast('int').alias('door_open_times'),
        F.get_json_object(df.value, '$.parsedPayload.last_open_minutes').cast('int').alias('last_open_minutes'),
        F.get_json_object(df.value, '$.parsedPayload.alarm').cast('int').alias('alarm')
    )

    # Convert sendtime to timestamp
    df = df.withColumn("sendtime", F.from_unixtime(F.col("sendtime") / 1000).cast("timestamp"))

    df_metadata = df_metadata.withColumnRenamed("DevEui", "DevEui_metadata")

    # Perform join with metadata
    df = df.join(df_metadata, df["DevEui"] == df_metadata["DevEui_metadata"], "left")

    df = df.drop("DevEui_metadata")

    return df


def calculate_classroom_statistics(df_stream: DataFrame, window_duration: str =  "10 minutes") -> DataFrame:
    """
    Calculate statistics for classroom metrics over a sliding time window.

    This function computes metrics such as mean, max, min, and standard deviation for classroom sensor data, grouped by institute, classroom, and a time window. It is designed to provide real-time insights into environmental conditions and sensor performance in educational settings.

    Parameters:
        df_stream (DataFrame): 
            - A Spark DataFrame containing streaming sensor data. 
            - Must include fields such as 'institute', 'classroom', and sensor metrics defined in `INDOOR_SENSOR_ATTRIBUTE`.
        window_duration (str): 
            - Duration of the sliding window for grouping data (e.g., "10 minutes").
            - Default is "10 minutes".

    Returns:
        DataFrame: 
            - A Spark DataFrame containing calculated statistics (mean, max, min, standard deviation) for each metric in `INDOOR_SENSOR_ATTRIBUTE` grouped by institute, classroom, and time window.
    """

    df_stats = df_stream.groupBy(
        F.window("sendtime", window_duration),
        "institute", 
        "classroom"
    ).agg(
        *[F.mean(col).alias(f"{col}_mean") for col in INDOOR_SENSOR_ATTRIBUTE] + 
         [F.max(col).alias(f"{col}_max") for col in INDOOR_SENSOR_ATTRIBUTE] + 
         [F.min(col).alias(f"{col}_min") for col in INDOOR_SENSOR_ATTRIBUTE] + 
         [F.stddev(col).alias(f"{col}_stddev") for col in INDOOR_SENSOR_ATTRIBUTE]
    )

    return df_stats



def compute_correlations(df_stream: DataFrame, window_duration: str = "10 minutes") -> DataFrame:
    """
    Compute correlations between key sensor metrics over a sliding time window.

    This function calculates correlation coefficients for pairs of sensor metrics such as temperature and humidity, CO2 and TVOC, and more. It provides insights into relationships between environmental factors and sensor readings.

    Parameters:
        df_stream (DataFrame): 
            - A Spark DataFrame containing streaming sensor data. 
            - Must include fields such as 'sendtime', 'institute', 'classroom', and relevant metrics for correlation calculations.
        window_duration (str): 
            - Duration of the sliding window for grouping data (e.g., "10 minutes").
            - Default is "10 minutes".

    Returns:
        DataFrame: 
            - A Spark DataFrame containing correlation coefficients for various metric pairs grouped by institute, classroom, and time window.
    """

    df_correlations = df_stream.groupBy(
        F.window("sendtime", window_duration),
        "institute", 
        "classroom"
    ).agg(
        F.corr("temperature", "humidity").alias("temp_humidity_corr"),
        F.corr("temperature", "pressure").alias("temp_pressure_corr"),
        F.corr("temperature", "co2").alias("temp_co2_corr"),
        F.corr("co2", "tvoc").alias("co2_tvoc_corr"),
        F.corr("light_level", "door_status").alias("light_door_corr"),
        F.corr("co2", "door_open_times").alias("co2_door_open_corr"),
        F.corr("battery", "battery_voltage").alias("battery_voltage_corr"),
        F.corr("pir", "co2").alias("pir_co2_corr")
    )

    return df_correlations