import json
import csv
import time
import argparse
from kafka import KafkaProducer
from misc.logger import *


LOGGER = CustomLogger('Kafka Client')

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Kafka CSV Producer')
    parser.add_argument('--topic', type=str, required=True, help='Kafka topic to send data to')
    parser.add_argument('--file', type=str, required=True, help='Path to the CSV file')

    return parser.parse_args()


def produce_data(topic: str, file_path: str) -> None:

    producer = KafkaProducer(
        bootstrap_servers='localhost:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    with open(file_path) as file:
        reader = csv.DictReader(file, delimiter=",")
        index = 0
        for row in reader:
            LOGGER.info("Sending data...")
            LOGGER.debug(f"Row data: {row}")
            producer.send(topic=topic, value=row)
            producer.flush()
            index += 1

            if (index % 20) == 0:
                LOGGER.info(f"Sent {index} messages, sleeping for 100 seconds...")
                time.sleep(100)

    LOGGER.info("Finished sending data.")

    producer.close()


if __name__ == '__main__':
    args = get_args()
    produce_data(args.topic, args.file)