import ast
import builtins
import os
from dotenv import dotenv_values


def load_environment(env_file: str) -> None:
    if os.path.exists(env_file):
        print(f"Loading environment variables from: {env_file}")
        env_vars = dotenv_values(env_file)
        env_vars['INDOOR_SENSOR_ATTRIBUTE'] = ast.literal_eval(env_vars['INDOOR_SENSOR_ATTRIBUTE'])
        builtins.__dict__.update(env_vars)
        return env_vars
    else:
        print(f"Error: The specified env file '{env_file}' does not exist.")
        exit(1)