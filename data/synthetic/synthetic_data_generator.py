import csv
from langchain_groq import ChatGroq

from misc.utilities import get_sensor_info
from misc.settings import *
from models.prompts import *


class SyntheticDataGenerator:
    
    def __init__(self, base_path: str, sensor_type: str, max_data: int) -> None:
        
        self.base_path = base_path
        self.sensor_type = sensor_type
        self.max_data = max_data

        self.llm = ChatGroq(
            model=MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            timeout=TIMEOUT,
            max_retries=MAX_RETRIES
        )

        self.SENSOR_CLASS, self.SENSOR_PROMPT, self.SENSOR_PATH = get_sensor_info(
            sensor_type=self.sensor_type,
            base_path=self.base_path
        )

        self.structured_model = self.llm.with_structured_output(self.SENSOR_CLASS)

    def generate(self) -> None:
        """Generates synthetic data and saves it to a CSV file."""
        try:
            # Open the file to write data
            with open(self.SENSOR_PATH, mode='w', newline='') as file:
                fieldnames = list(self.SENSOR_CLASS.__fields__.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Write the header (column names)
                writer.writeheader()

                # Generate and write data rows
                for _ in range(self.max_data):
                    try:
                        # Invoke the model to generate synthetic data
                        response = self.structured_model.invoke(self.SENSOR_PROMPT)
                        writer.writerow(response.dict())
                        print(f"Generated: {response}")
                    except Exception as e:
                        print(f"Error occurred while generating data: {e}. Continuing to the next.")
        except Exception as e:
            print(f"Error occurred while writing to file: {e}")