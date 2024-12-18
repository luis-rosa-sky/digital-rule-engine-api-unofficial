"""Base app module"""

# Third-party library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app(title):
    """
    Creates and configures the Fast application.

    :param title: The title of the application.
    :return: The configured Fast application instance.
    """
    # Create the application instance
    app = FastAPI(title=title,
                  description="This is a very cool API.",
                  version="1.0",
                  openapi_url="/api/openapi.json",
                  root_path="/api/v1")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,  # Allows cookies to be sent with requests
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )

    return app
