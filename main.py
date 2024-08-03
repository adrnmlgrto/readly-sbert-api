from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer, util


# Defining of the main FastAPI application.
app = FastAPI()


# Loading of the pre-trained SBERT model.
# NOTE: Uses the `paraphrase-MiniLM-L6-v2`.
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


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

    # We will return the individual similarity scores, and the max.
    return TextComparisonResponse(
        similarity_scores=similarity_scores,
        max_similarity=max_similarity
    )
