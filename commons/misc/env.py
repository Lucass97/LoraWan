import ast
import builtins
import os

from dotenv import dotenv_values


def load_environment(env_file: str) -> dict:
    """
    Loads environment variables from a specified file.

    Args:
        env_file (str): The path to the environment file.

    Returns:
        dict: A dictionary containing the loaded environment variables.
        If the file does not exist, the program exits.
    """
    if not os.path.exists(env_file):
        exit(1)

    env_vars = dotenv_values(env_file)

    if env_vars.get('INDOOR_SENSOR_ATTRIBUTE'):
        try:
            env_vars['INDOOR_SENSOR_ATTRIBUTE'] = ast.literal_eval(env_vars['INDOOR_SENSOR_ATTRIBUTE'])
        except (ValueError, SyntaxError):
            env_vars['INDOOR_SENSOR_ATTRIBUTE'] = None

    builtins.__dict__.update(env_vars)
    return env_vars
