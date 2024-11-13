import json
import argparse
from kafka import KafkaConsumer

from misc.logger import *


LOGGER = CustomLogger('Kafka Client')

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Kafka CSV Consumer')
    parser.add_argument('--topic', type=str, required=True, help='Kafka topic to consume data from')
    parser.add_argument('--group', type=str, required=False, default='default-group', help='Kafka consumer group')

    return parser.parse_args()

def consume_data(topic: str, group_id: str) -> None:
   
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:29092',
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest'
    )

    LOGGER.info(f"Starting to consume from topic: {topic}")

    for message in consumer:
        LOGGER.info(f"Received message: {message.value}")

    consumer.close()

if __name__ == "__main__":
    args = get_args()
    consume_data(args.topic, args.group)