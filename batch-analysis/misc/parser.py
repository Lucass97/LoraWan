import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start Spark Streaming with environment file")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    return parser.parse_args()