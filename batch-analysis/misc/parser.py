import argparse


def parse_batch_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start Spark Batch Analysis script")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    return parser.parse_args()


def parse_downloader_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start Spark Downloader script")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    parser.add_argument("--profile", type=str, default="iaq", choices=["iaq", "finestra", "porta"], required=False, help="Profile to use: iaq, finestra, or porta")
    return parser.parse_args()