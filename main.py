import uvicorn

from src.app import app
from src.config.settings import get_api_settings


if __name__ == "__main__":
    """
        To debug in Development Environment, set var DEBUG=True.
    """
    settings = get_api_settings()

    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        debug=settings.DEBUG,
        reload=settings.DEBUG
    )
