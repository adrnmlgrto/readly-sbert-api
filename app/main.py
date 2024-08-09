import re
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.api import endpoints
from app.core.logging import setup_logging

app = FastAPI(title='Readly API', version='1.0.0')
logger, in_memory_handler = setup_logging()
templates = Jinja2Templates(directory='app/templates')

log_pattern = re.compile(
    r'(?P<timestamp>[\d\-:, ]+) - (?P<level>\w+) - (?P<file>\w+\.py):(?P<line>\d+) - (?P<message>.*)'
)


def parse_log_helper(log):
    """
    Parsing of the log records helper.
    """
    # Match to the regex pattern for parsing.
    match = log_pattern.match(log)
    if match:
        return match.groupdict()

    # Else we return a dict with empty strings.
    return {
        'timestamp': '',
        'level': '',
        'file': '',
        'line': '',
        'message': log
    }


def humanize_timestamp(timestamp: str) -> str:
    """
    Function for `Jinja2` template filter
    for humanizing timestamps.
    """
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
    return dt.strftime('%b %d, %Y (%I:%M %p)')


# Register the filter with Jinja2
templates.env.filters['humanize_timestamp'] = humanize_timestamp


@app.get('/errors', response_class=HTMLResponse, include_in_schema=False)
async def dashboard(request: Request):
    """
    Render the logging dashboard HTML page.
    """
    # Parse then put into the list the log records.
    log_records = [
        parse_log_helper(log)
        for log in in_memory_handler.get_log_records()
    ]

    return templates.TemplateResponse(
        'dashboard.html',
        {
            'request': request,
            'log_records': log_records
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    # Prepare the log message for the HTTPException.
    log_message = f'[HTTP {exc.status_code}] {exc.detail}'

    # Log the error to the memory stream.
    logger.error(log_message)

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({'detail': exc.detail}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    # Prepare the log message for the validation error.
    log_message = f'[HTTP 422] {exc.errors()}'

    # Log the error to the memory stream.
    logger.error(log_message)

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({'detail': exc.errors()}),
    )

app.include_router(endpoints.router)
