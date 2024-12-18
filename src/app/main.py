"""Fast api module"""

# Third-party library imports
# pylint: disable=unused-import,import-error,wildcard-import,broad-exception-caught
from ..shared_utils.utils import get_logger
from ..shared_utils.base_app import create_app
from .router.rules_engine_api import router as rule_engine_router

# Service name
SERVICE_NAME = "app"

# Configure logging
logger = get_logger(SERVICE_NAME)

# Create the Fast app
app = create_app(SERVICE_NAME)

# Mount the GraphQL app
app.include_router(rule_engine_router, prefix="/run", tags=["Rule Engine"])
logger.debug("Running the digital rule engine api...")

# If you want to run the app directly from the script
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.critical("An error occurred: %s", str(e))
