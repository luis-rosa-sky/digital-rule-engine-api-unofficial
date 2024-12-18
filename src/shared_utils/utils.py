"""Utils module"""

# Standard library imports
# pylint: disable=unused-import,c-extension-no-member,wrong-import-order
import logging

# Function to get a logger
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name and configure it.

    :param name: Name of the logger.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
