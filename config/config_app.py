# version 4.0.2 - 02/13/2026 - INT to BIGINT, PyMSQL to MySQLdb, mysql procedures for each server & format - see changelog
# function: app_config module for configuration file that runs application
# synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
# author: Will Raymond <farmfreshsoftware@gmail.com>

import json
import os

# Function to load configuration
def load_file(filepath='config.json'):
    """
    Loads configuration settings from a JSON file.
    """
    # Ensure the file exists before trying to open it
    if not os.path.exists(filepath):
        print(f"Error: Configuration file '{filepath}' not found.")
        # You might raise an exception or handle this as appropriate for your app
        raise FileNotFoundError(f"Configuration file not found at {filepath}")
        return None

    try:
        with open(filepath, 'r') as config_file:
            config_data = json.load(config_file)
        return config_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{filepath}': {e}")
        return None
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}")
        return None
