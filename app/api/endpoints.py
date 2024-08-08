from fastapi import APIRouter, HTTPException, status

from app.models.schemas import TextComparisonRequest, TextComparisonResponse
from app.services.compare import compare_texts

# Defining of the API Router.
router = APIRouter()


@router.get('/heartbeat')
async def read_heartbeat():
    """
    Simple endpoint for checking if the API
    endpoint(s) are available or not.
    """
    return {
        'status': 'ONLINE',
        'message': 'Service endpoints are currently available.'
    }


@router.post('/compare', response_model=TextComparisonResponse)
async def compare_texts_endpoint(request: TextComparisonRequest):
    """
    Performs the semantic context similarity comparison
    on a set of provided "expected" correct answers to
    a user's text input / answer.
    """
    try:

        # Extract the data from the request.
        correct_answers = request.correct_answers
        user_answer = request.user_answer

        # Call the service function with individual parameters.
        similarity_scores, max_similarity = await compare_texts(
            correct_answers,
            user_answer
        )

        # Construct the response using the Pydantic model.
        return TextComparisonResponse(
            similarity_scores=similarity_scores,
            max_similarity=max_similarity
        )

    except Exception as e:

        # We'll be careful here and catch any unexpected errors,
        # then it'll be re-raised as a `HTTP 500` response.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                'An unknown error has occurred while '
                f'processing your request. Details: "{str(e)}"'
            )
        )
