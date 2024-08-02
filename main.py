import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


# Defining of the main FastAPI application.
app = FastAPI()


# Loading of the pre-trained SBERT model.
# NOTE: Uses the `paraphrase-MiniLM-L6-v2`.
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


# Define the input schema for the request.
class TextComparisonRequest(BaseModel):
    correct_answers: list[str]
    user_answer: str


# Function to calculate Pearson correlation.
def pearson_correlation(x, y):
    """
    Calculates the pearson correlation value.
    """
    return np.corrcoef(x, y)[0, 1]


@app.post('/compare')
async def compare_texts(request: TextComparisonRequest):
    """
    Performs the semantic context similarity comparison
    on a set of provided "expected" correct answers to
    a user's text input / answer.

    Question:
        - Was Chandu really flying or was it just a dream?

    Expected Answers:
        - It was just a dream.
        - Chandu was only dreaming of flying.
        - He was only dreaming.
    """
    # Encode all variations of correct answers.
    correct_embeddings = model.encode(request.correct_answers)

    # Encode the user's answer
    user_embedding = model.encode(request.user_answer)

    # Compute similarity scores
    similarity_scores = [
        pearson_correlation(correct, user_embedding)
        for correct in correct_embeddings
    ]

    # Determine the highest similarity score
    max_similarity = max(similarity_scores)

    # We will return the individual similarity scores, and the max.
    return {
        'similarity_scores': similarity_scores,
        'max_similarity': max_similarity
    }
