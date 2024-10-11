from langchain_groq import ChatGroq
import csv
import os

from models.indoor_sensor import IndoorSensor
from misc.settings import *
from models.prompts import *

def generate_synthetic_data(base_path:str, max_data: int, sensor:str):

    llm = ChatGroq(
        model=MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        timeout=TIMEOUT,
        max_retries=MAX_RETRIES
    )

    structured_model = llm.with_structured_output(IndoorSensor)

    file_path = os.path.join(base_path, DEFAULT_INDOOR_SENSOR_FILENAME)

    with open(file_path, mode='w', newline='') as file:
        fieldnames = list(IndoorSensor.__fields__.keys())

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for _ in range(max_data):
            response = structured_model.invoke(INDOOR_SENSOR_PROMPT)
            writer.writerow(response.dict())
            print(f"Generated: {response}")