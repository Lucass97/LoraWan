from influxdb_client import Point

from misc.constants import *

def saveRawDataToInflux(write_api):
    
    def inner_function(row) -> None:
        point = Point("sensor_data") \
            .tag("DevEui", row.DevEui) \
            .tag("institute", row.institute) \
            .tag("profile", row.profile) \
            .tag("classroom", row.classroom) \
            .field("temperature", row.temperature) \
            .field("humidity", row.humidity) \
            .field("battery", row.battery) \
            .field("co2", row.co2) \
            .field("tvoc", row.tvoc) \
            .field("pressure", row.pressure) \
            .field("light_level", row.light_level) \
            .field("pir", row.pir) \
            .field("battery_voltage", row.battery_voltage) \
            .field("door_status", row.door_status) \
            .field("door_open_times", row.door_open_times) \
            .field("last_open_minutes", row.last_open_minutes) \
            .field("alarm", row.alarm) \
            .time(row.sendtime)
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print("Write successful")
        except Exception as e:
            print(f"Write failed: {e}")
    
    return inner_function


def saveCorrelationDataToInflux(write_api):

    def inner_function(row) -> None:
        
        point = Point("correlation_data") \
            .tag("institute", row.institute) \
            .tag("classroom", row.classroom) \
            .field("temp_humidity_corr", row.temp_humidity_corr) \
            .field("temp_co2_corr", row.temp_co2_corr) \
            .field("co2_tvoc_corr", row.co2_tvoc_corr) \
            .field("light_door_corr", row.light_door_corr) \
            .field("door_status_open_corr", row.door_status_open_corr) \
            .field("battery_voltage_corr", row.battery_voltage_corr) \
            .field("pir_co2_corr", row.pir_co2_corr)
        
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print("Correlation write successful")
        except Exception as e:
            print(f"Write failed: {e}")

    return inner_function


def saveStatisticsDataToInflux(write_api):

    def inner_function(row) -> None:

        point = Point("classroom_statistics") \
            .tag("institute", row.institute) \
            .tag("classroom", row.classroom) \
            .field("temperature_mean", row.temperature_mean) \
            .field("temperature_max", row.temperature_max) \
            .field("temperature_min", row.temperature_min) \
            .field("temperature_stddev", row.temperature_stddev) \
            .field("humidity_mean", row.humidity_mean) \
            .field("humidity_max", row.humidity_max) \
            .field("humidity_min", row.humidity_min) \
            .field("humidity_stddev", row.humidity_stddev) \
            .field("battery_mean", row.battery_mean) \
            .field("battery_max", row.battery_max) \
            .field("battery_min", row.battery_min) \
            .field("battery_stddev", row.battery_stddev) \
            .field("co2_mean", row.co2_mean) \
            .field("co2_max", row.co2_max) \
            .field("co2_min", row.co2_min) \
            .field("co2_stddev", row.co2_stddev) \
            .field("tvoc_mean", row.tvoc_mean) \
            .field("tvoc_max", row.tvoc_max) \
            .field("tvoc_min", row.tvoc_min) \
            .field("tvoc_stddev", row.tvoc_stddev) \
            .field("pressure_mean", row.pressure_mean) \
            .field("pressure_max", row.pressure_max) \
            .field("pressure_min", row.pressure_min) \
            .field("pressure_stddev", row.pressure_stddev) \
            .field("light_level_mean", row.light_level_mean) \
            .field("light_level_max", row.light_level_max) \
            .field("light_level_min", row.light_level_min) \
            .field("light_level_stddev", row.light_level_stddev)
        
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print("Statistics write successful")
        except Exception as e:
            print(f"Write failed: {e}")

    return inner_function
