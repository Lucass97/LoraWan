//Create keyspace
CREATE KEYSPACE IF NOT EXISTS StreamingKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
CREATE KEYSPACE IF NOT EXISTS BatchKeySpace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

//Create tables

CREATE TABLE IF NOT EXISTS BatchKeySpace.indoor_sensor_data_synthetic ("TEMPERATURE" int, "HUMIDITY" float, "PIR" int, "CO2" int, "TVOC" int, BAROMETRIC_PRESSURE int, primary key ("TEMPERATURE"));