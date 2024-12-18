"""Response handler module"""

# Third-party library imports
from typing import Any, Dict, Optional, Tuple

class ResponseHandler:

    """
    A class to handle HTTP responses with standardized formats.
    """

    def __init__(self):
        """
        Initialize any shared state or resources here.
        """

    def success(self, data: Optional[Any] = None, message: str = "Success",
                status_code: int = 200) -> Dict[str, Any]:
        """
        Generate a success response.

        :param data: The data to include in the response.
        :param message: The message to include in the response.
        :param status_code: The HTTP status code for the response.
        :return: A tuple containing the response dictionary and the status code.
        """
        response = {
            "status": status_code,
            "message": message,
            "data": data
        }
        return response

    def error(self, data: Optional[Any] = None, message: str = "Internal Server Error",
              status_code: int = 500) -> Dict[str, Any]:
        """
        Generate an error response.

        :param data: The data to include in the response.
        :param message: The message to include in the response.
        :param status_code: The HTTP status code for the response.
        :return: A response dictionary.
        """
        response = {
            "status": status_code,
            "message": message,
            "data": data
        }
        return response

    def bad_request(self, data: Optional[Any] = None,
                    message: str = "Bad Request") -> Tuple[Dict[str, Any], int]:
        """
        Generate a bad request response.

        :param data: The data to include in the response.
        :param message: The message to include in the response.
        :return: A tuple containing the response dictionary and the status code.
        """
        return self.error(data=data, message=message, status_code=400)
