import os

from misc.settings import DEFAULT_INDOOR_SENSOR_FILENAME, DEFAULT_OUTDOOR_SENSOR_FILENAME, DEFAULT_SENSOR_PATH
from models.outdoor_sensor import OutdoorSensor
from models.indoor_sensor import IndoorSensor
from models.prompts import INDOOR_SENSOR_PROMPT, OUTDOOR_SENSOR_PROMPT


def get_sensor_info(sensor_type: str = "indoor", base_path=DEFAULT_SENSOR_PATH):
    
    if sensor_type == "indoor": 
        return IndoorSensor, INDOOR_SENSOR_PROMPT, os.path.join(base_path, DEFAULT_INDOOR_SENSOR_FILENAME)
    if sensor_type == "outdoor":
        return OutdoorSensor, OUTDOOR_SENSOR_PROMPT, os.path.join(base_path, DEFAULT_OUTDOOR_SENSOR_FILENAME)