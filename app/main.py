from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import endpoints
from app.core.logging import setup_logging

# Instantiate the app, and setup logging.
app = FastAPI(title='Readly API', version='1.0.0')
logger = setup_logging()


# Define exception handlers.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTPExceptions.
    Logs error details and returns a JSON response.
    """
    # Log the error along with request details
    headers = dict(request.headers)
    body = await request.body()
    logger.error(f"HTTPException occurred: {exc.detail}")
    logger.error(f"Request Headers: {headers}")
    logger.error(f"Request Body: {body.decode('utf-8')}")

    # Return JSON response with error details
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Custom exception handler for RequestValidationError.
    Logs validation error details and returns a JSON response.
    """
    # Log the error along with request details
    headers = dict(request.headers)
    body = await request.body()
    logger.error(f"RequestValidationError occurred: {exc.errors()}")
    logger.error(f"Request Headers: {headers}")
    logger.error(f"Request Body: {body.decode('utf-8')}")

    # Return JSON response with error details
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# Include the endpoint router.
app.include_router(endpoints.router)
