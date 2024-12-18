"""Config module"""

# Standard library imports
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "rules_config.db")

def get_config(section):
    """
    Reads the configuration file and returns the configuration section as a dictionary.

    Args:
        section (str): The section to fetch from the configuration.

    Returns:
        dict: The configuration section, or an empty dictionary if the section is not found.
    """
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file '{CONFIG_PATH}' not found.")

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            return config.get(section, {})
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from the configuration file '{CONFIG_PATH}'.") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
