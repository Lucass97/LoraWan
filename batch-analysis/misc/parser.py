import argparse


def parse_batch_args() -> argparse.Namespace:
    """
    Parses arguments for the Spark Batch Analysis script.

    Returns:
        argparse.Namespace: Parsed arguments.

    Arguments:
        --env-file (str, required): Path to the .env file.
    """
    parser = argparse.ArgumentParser(description="Start Spark Batch Analysis script")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    return parser.parse_args()


def parse_downloader_args() -> argparse.Namespace:
    """
    Parses arguments for the Spark Downloader script.

    Returns:
        argparse.Namespace: Parsed arguments.

    Arguments:
        --env-file (str, required): Path to the .env file.
        --profile (str, optional): Profile to use ('iaq', 'finestra', 'porta'). Default: 'iaq'.
        --local-path (str, required): Local path to save the downloaded file.
    """
    parser = argparse.ArgumentParser(description="Start Spark Downloader script")
    parser.add_argument("--env-file", type=str, required=True, help="Path to the .env file")
    parser.add_argument("--profile", type=str, default="iaq", choices=["iaq", "finestra", "porta"], help="Profile to use: iaq, finestra, or porta")
    parser.add_argument("--local-path", type=str, required=True, help="Local path to save the file")
    return parser.parse_args()
