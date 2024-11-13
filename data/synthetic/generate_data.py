import argparse

from misc.settings import *
from synthetic_data_generator import SyntheticDataGenerator

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic data")

    parser.add_argument('--sensor', choices=['indoor', 'outdoor'], required=True,
                        help='Specify the sensor type: indoor or outdoor')

    parser.add_argument('--base_path', type=str, default=DEFAULT_SENSOR_PATH, 
                        help='Specify the path for data storage (default: {DEFAULT_SENSOR_PATH})')

    parser.add_argument('--max_data', type=int, default=DEFAULT_MAX_DATA,
                        help='Specify the number of iterations (default: {DEFAULT_MAX_DATA})')

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    data_generator = SyntheticDataGenerator(base_path=args.base_path, max_data=args.max_data, sensor_type=args.sensor)
    data_generator.generate()
