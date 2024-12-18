"""Decorator handler module"""

# Standard library imports
# Third-party library imports
from fastapi import Header, HTTPException
from typing import Annotated
from .utils import get_logger

# Configure logging
logger = get_logger("decorator-handler")

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        logger.error("X-Token header invalid")
        raise HTTPException(status_code=400, detail="X-Token header invalid")
