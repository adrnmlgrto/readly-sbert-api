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
async def compute_similarities(request: TextComparisonRequest):
    """
    Performs a semantic context similarity comparison
    with a list of expected "correct answers" and the
    "user answer" for each question.

    **Note**: Provide at least one (1) item in the `questions` parameter.
    """
    try:

        # Define the `max_similarity_scores` list to return.
        max_similarity_scores = []

        # Iterate over each question to compute / compare.
        for question in request.questions:

            # Compute the similarity score for each question.
            # NOTE: Similarity scores are for DEBUG purposes.
            similarity_scores, max_similarity = await compare_texts(
                question.correct_answers,
                question.user_answer
            )

            # Append the computed max similarity score to the list.
            # NOTE: List is ordered so it is from Q1 - Q(n).
            max_similarity_scores.append(max_similarity)

        # Construct the response using the Pydantic model.
        return TextComparisonResponse(
            max_similarity_scores=max_similarity_scores
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
