from pyspark.sql.functions import avg, max, min, stddev, year, weekofyear


def define_aggregation_statistics() -> list:
    """
    Defines aggregation statistics for the specified columns.

    Returns:
        list: A list of aggregation expressions.
    """
    agg_stats = [
        avg("temperature").alias("avg_temperature"),
        max("temperature").alias("max_temperature"),
        min("temperature").alias("min_temperature"),
        stddev("temperature").alias("stddev_temperature"),
        avg("humidity").alias("avg_humidity"),
        max("humidity").alias("max_humidity"),
        min("humidity").alias("min_humidity"),
        stddev("humidity").alias("stddev_humidity"),
        avg("co2").alias("avg_co2"),
        max("co2").alias("max_co2"),
        min("co2").alias("min_co2"),
        stddev("co2").alias("stddev_co2"),
        avg("light_level").alias("avg_light_level"),
        max("light_level").alias("max_light_level"),
        min("light_level").alias("min_light_level"),
        stddev("light_level").alias("stddev_light_level"),
        avg("pressure").alias("avg_pressure"),
        max("pressure").alias("max_pressure"),
        min("pressure").alias("min_pressure"),
        stddev("pressure").alias("stddev_pressure"),
        avg("tvoc").alias("avg_tvoc"),
        max("tvoc").alias("max_tvoc"),
        min("tvoc").alias("min_tvoc"),
        stddev("tvoc").alias("stddev_tvoc"),
    ]

    return agg_stats


def aggregate_by_year_week(df, agg_stats):
    """
    Aggregates data by year and week.

    Args:
        df (DataFrame): The input DataFrame.
        agg_stats (list): A list of aggregation expressions.

    Returns:
        DataFrame: A DataFrame aggregated by year and week.
    """
    stats_by_year_week = df.groupBy(
        year("sendtime").alias("year"), weekofyear("sendtime").alias("week")
    ).agg(*agg_stats)

    return stats_by_year_week


def aggregate_by_class_year_week(df, agg_stats):
    """
    Aggregates data by classroom, institute, year, and week.

    Args:
        df (DataFrame): The input DataFrame.
        agg_stats (list): A list of aggregation expressions.

    Returns:
        DataFrame: A DataFrame aggregated by classroom, institute, year, and week.
    """
    stats_by_class_year_week = df.groupBy(
        "classroom",
        "institute",
        year("sendtime").alias("year"),
        weekofyear("sendtime").alias("week"),
    ).agg(*agg_stats)

    return stats_by_class_year_week
