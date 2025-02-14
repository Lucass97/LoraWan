//Create keyspace
CREATE KEYSPACE IF NOT EXISTS StreamingKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
CREATE KEYSPACE IF NOT EXISTS BatchKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

//Create tables

CREATE TABLE IF NOT EXISTS BatchKeySpace.stats_by_year_week(
    YEAR int, 
    WEEK int, 
    DevEui text,
    AVG_TEMPERATURE float, 
    MAX_TEMPERATURE float, 
    MIN_TEMPERATURE float, 
    STDDEV_TEMPERATURE float,
    AVG_HUMIDITY float, 
    MAX_HUMIDITY float, 
    MIN_HUMIDITY float, 
    STDDEV_HUMIDITY float,
    AVG_CO2 float, 
    MAX_CO2 float, 
    MIN_CO2 float, 
    STDDEV_CO2 float,
    AVG_LIGHT_LEVEL float, 
    MAX_LIGHT_LEVEL float, 
    MIN_LIGHT_LEVEL float, 
    STDDEV_LIGHT_LEVEL float,
    AVG_PRESSURE float, 
    MAX_PRESSURE float, 
    MIN_PRESSURE float, 
    STDDEV_PRESSURE float,
    AVG_TVOC float, 
    MAX_TVOC float, 
    MIN_TVOC float, 
    STDDEV_TVOC float,
    PRIMARY KEY (YEAR, WEEK)
);


CREATE TABLE IF NOT EXISTS BatchKeySpace.stats_by_class_year_week(
    CLASSROOM text, 
    INSTITUTE text, 
    DevEui text, 
    YEAR int, 
    WEEK int,
    AVG_TEMPERATURE float, 
    MAX_TEMPERATURE float, 
    MIN_TEMPERATURE float, 
    STDDEV_TEMPERATURE float,
    AVG_HUMIDITY float, 
    MAX_HUMIDITY float, 
    MIN_HUMIDITY float, 
    STDDEV_HUMIDITY float,
    AVG_CO2 float, 
    MAX_CO2 float, 
    MIN_CO2 float, 
    STDDEV_CO2 float,
    AVG_LIGHT_LEVEL float, 
    MAX_LIGHT_LEVEL float, 
    MIN_LIGHT_LEVEL float, 
    STDDEV_LIGHT_LEVEL float,
    AVG_PRESSURE float, 
    MAX_PRESSURE float, 
    MIN_PRESSURE float, 
    STDDEV_PRESSURE float,
    AVG_TVOC float, 
    MAX_TVOC float, 
    MIN_TVOC float, 
    STDDEV_TVOC float,
    PRIMARY KEY (CLASSROOM, INSTITUTE, YEAR, WEEK)
);


ALTER TABLE BatchKeySpace.stats_by_class_year_week
    WITH custom_properties = {
    'comment': 'Statistics computed on sensor data, aggregated by classroom, institute, year, and week.'
};

ALTER TABLE BatchKeySpace.stats_by_year_week
    WITH custom_properties = {
    'comment': 'Statistics computed on sensor data, aggregated by year, and week.'
};


DESCRIBE TABLES;