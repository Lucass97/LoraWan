import os

os.environ["GROQ_API_KEY"] = "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"

MODEL = "llama3-70b-8192" #"mixtral-8x7b-32768"
TEMPERATURE = 1.0
MAX_TOKENS = None
TIMEOUT = None
MAX_RETRIES = 2

DEFAULT_MAX_DATA = 1000
DEFAULT_SENSOR_PATH = "../data/generated"
DEFAULT_INDOOR_SENSOR_FILENAME = "indoor_sensor_data.csv"