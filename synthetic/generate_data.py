import argparse

from misc.settings import *
from generate_synthetic_data import generate_synthetic_data

def get_args():
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
    generate_synthetic_data(base_path=args.base_path, max_data=args.max_data, sensor=args.sensor)
