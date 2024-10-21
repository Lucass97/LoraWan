//Create keyspace
CREATE KEYSPACE IF NOT EXISTS StreamingKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
CREATE KEYSPACE IF NOT EXISTS BatchKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

//Create tables

CREATE TABLE IF NOT EXISTS BatchKeySpace.indoor_sensor_data_synthetic("TIMESTAMP" timestamp, "SENSOR_ID" int,
    "TEMPERATURE" float, "HUMIDITY" float, "PIR" float, "lighting" float,
    "CO2" float, "TVOC" float, "BAROMETRIC_PRESSURE" float, 
    PRIMARY KEY ("TIMESTAMP", "SENSOR_ID"));

CREATE TABLE IF NOT EXISTS BatchKeySpace.stats_by_year("YEAR" int,
    "AVG_TEMPERATURE" float, "MAX_TEMPERATURE" float, "MIN_TEMPERATURE" float,
    "AVG_HUMIDITY" float, "MAX_HUMIDITY" float, "MIN_HUMIDITY" float,
    "AVG_CO2" float, "MAX_CO2" float, "MIN_CO2" float,
    "AVG_LIGHTING" float, "MAX_LIGHTING" float, "MIN_LIGHTING" float, 
    "AVG_B_PRESSURE" float, "MAX_B_PRESSURE" float, "MIN_B_PRESSURE" float,
    "AVG_TVOC" float, "MAX_TVOC" float, "MIN_TVOC" float,
    "AVG_PIR" float, "MAX_PIR" float, "MIN_PIR" float,
    PRIMARY KEY ("YEAR"));

CREATE TABLE IF NOT EXISTS BatchKeySpace.stats_by_year_month("YEAR" int, "MONTH" int,
    "AVG_TEMPERATURE" float, "MAX_TEMPERATURE" float, "MIN_TEMPERATURE" float,
    "AVG_HUMIDITY" float, "MAX_HUMIDITY" float, "MIN_HUMIDITY" float,
    "AVG_CO2" float, "MAX_CO2" float, "MIN_CO2" float,
    "AVG_LIGHTING" float, "MAX_LIGHTING" float, "MIN_LIGHTING" float, 
    "AVG_B_PRESSURE" float, "MAX_B_PRESSURE" float, "MIN_B_PRESSURE" float,
    "AVG_TVOC" float, "MAX_TVOC" float, "MIN_TVOC" float,
    "AVG_PIR" float, "MAX_PIR" float, "MIN_PIR" float,
    PRIMARY KEY (("YEAR"), "MONTH"));

CREATE TABLE IF NOT EXISTS BatchKeySpace.stats_by_year_month_day("YEAR" int, "MONTH" int, "DAY" int,
    "AVG_TEMPERATURE" float, "MAX_TEMPERATURE" float, "MIN_TEMPERATURE" float,
    "AVG_HUMIDITY" float, "MAX_HUMIDITY" float, "MIN_HUMIDITY" float,
    "AVG_CO2" float, "MAX_CO2" float, "MIN_CO2" float,
    "AVG_LIGHTING" float, "MAX_LIGHTING" float, "MIN_LIGHTING" float, 
    "AVG_B_PRESSURE" float, "MAX_B_PRESSURE" float, "MIN_B_PRESSURE" float,
    "AVG_TVOC" float, "MAX_TVOC" float, "MIN_TVOC" float,
    "AVG_PIR" float, "MAX_PIR" float, "MIN_PIR" float,
    PRIMARY KEY (("YEAR"), "MONTH", "DAY"));

DESCRIBE TABLES;