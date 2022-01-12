from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from src.config.settings import get_api_settings
from src.endpoints import employees

settings = get_api_settings()

app = FastAPI()
app.include_router(employees.router)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Make a General purpose, and simple, ExceptionHandler.
    :param request: HTTP Request info
    :param exc: Exception object to catch.
    :return: JSON Response.
    """
    content = {
        "message": f"Oops! did something in the system. Contact a System Master.",
    }

    if settings.DEBUG:
        content.update({
            "detail": f"{exc}"
        })

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)
