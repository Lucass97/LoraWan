# CASSANDRA SETTINGS

CASSANDRA_CLUSTERS = ['localhost:9042', 'localhost:9043']
CASSANDRA_USERNAME = "cassandra"
CASSANDRA_PASSWORD = "cassandra"

#INFLUXDB SETTINGS

INFLUXDB_URL = "http://influxdb2:8086"
INFLUXDB_TOKEN = "admin_admin_123456789"
INFLUXDB_ORG = "RomaTre"
INFLUXDB_BUCKET = "home"

# KAFKA SETTINGS

KAFKA_SERVER = "kafka1:9092"
KAFKA_TOPIC = "live-data"
KAFKA_STARTING_OFFSETS = "earliest"

# HDFS SETTINGS

METADATA_HDFS_PATH = "hdfs://hadoop-namenode:8020/iot-lorawan/metadata/sensor_registry_armellini.csv"
RAW_INDOOR_SENSOR_HDFS_PATH = "hdfs://hadoop-namenode:8020/iot-lorawn/raw/indoor_sensor_data.csv"
CHECKPOINT_RAW_INDOOR_SENSOR_HDFS_PATH = "hdfs://hadoop-namenode:8020/iot-loraw/raw/checkpoints/indoor_sensor_data"

# STREAMING SETTINGS
WINDOW_DURATION = "30 minutes"
INDOOR_SENSOR_ATTRIBUTE = ['temperature', 'humidity', 'battery', 'co2', 'tvoc', 'pressure', 'light_level']