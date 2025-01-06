"""Utils module"""

# Standard library imports
# pylint: disable=unused-import,c-extension-no-member,wrong-import-order
import logging
from enum import Enum

class LogLevel(Enum):
    CRITICAL = 50
    FATAL = 50
    ERROR = 40
    WARNING = 30
    WARN = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


# Function to get a logger
def get_logger(name: str, log_level: LogLevel.value = LogLevel.INFO) -> logging.Logger:
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
    logger.setLevel(log_level)
    return logger
