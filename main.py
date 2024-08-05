import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer, util

# Setup of logging configurations.
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# Defining of the main FastAPI application.
app = FastAPI()


# Loading of the pre-trained SBERT model.
model = SentenceTransformer('all-MiniLM-L6-v2')


# Define schema(s) for the request and response.
class TextComparisonRequest(BaseModel):
    correct_answers: list[str] = Field(
        ...,
        description=(
            'The list of expected correct answers to a question.'
        ),
        examples=[
            [
                'It was just a dream.',
                'Chandu was only dreaming of flying.',
                'He was only dreaming.'
            ]
        ]
    )
    user_answer: str = Field(
        ...,
        description=(
            'The user\'s actual text answer or input to a question.'
        ),
        examples=[
            'Chandu only dreamt of flying.'
        ]
    )


class TextComparisonResponse(BaseModel):
    similarity_scores: list[float] = Field(
        ...,
        description=(
            'List of individual similarity scores upon comparing '
            'user text input to the expected answers.'
        ),
        examples=[
            [
                0.5203630636661963,
                0.8931472296869409,
                0.612681223305576
            ]
        ]
    )
    max_similarity: float = Field(
        ...,
        description=(
            'The highest similarity score from the list. '
            'This value is the one to check if the user\'s input '
            'is similar or not.'
        ),
        examples=[0.8931472296869409]
    )


# Exception Handlers
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
        content={"detail": exc.detail},
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
        content={"detail": exc.errors()},
    )


# Endpoints
@app.get('/heartbeat')
async def read_heartbeat():
    """
    Simple endpoint for checking if the API
    endpoint(s) are available or not.
    """
    return {
        'status': 'ONLINE',
        'message': 'Service endpoints are currently available.'
    }


@app.post('/compare', response_model=TextComparisonResponse)
async def compare_texts(request: TextComparisonRequest):
    """
    Performs the semantic context similarity comparison
    on a set of provided "expected" correct answers to
    a user's text input / answer.
    """
    try:

        # Encode all variations of correct answers.
        correct_embeddings = model.encode(request.correct_answers)

        # Encode the user's answer.
        user_embedding = model.encode(request.user_answer)

        # Compute the individual similarity scores.
        similarity_scores_tensor = util.cos_sim(
            user_embedding,
            correct_embeddings
        )
        similarity_scores = similarity_scores_tensor[0].tolist()

        # Determine the highest similarity score.
        max_similarity = max(similarity_scores)

        # We will return the individual similarity scores,
        # and the max similarity score on the list.
        return {
            'similarity_scores': similarity_scores,
            'max_similarity': max_similarity
        }

    except Exception:

        # We'll be careful here and catch any unexpected errors,
        # then it'll be re-raised as a `HTTP 500` response.
        raise HTTPException(
            status_code=500,
            detail=(
                'Something went wrong while processing '
                'your request.'
            )
        )
