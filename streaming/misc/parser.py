import argparse

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for starting Spark Streaming.

    Returns:
        argparse.Namespace: Parsed arguments.

    Arguments:
        --env-file (str, required): Path to the .env file.
    """
    parser = argparse.ArgumentParser(description="Start Spark Streaming with environment file")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    return parser.parse_args()
