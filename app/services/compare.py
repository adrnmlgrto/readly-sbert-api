from typing import List, Tuple

from sentence_transformers import SentenceTransformer

# Loading and initialization of the pre-trained SBERT model.
# NOTE: By default, it uses the cosine similarity function.
model = SentenceTransformer('all-MiniLM-L6-v2')


async def compare_texts(
    correct_answers: List[str],
    user_answer: str
) -> Tuple[List[float], float]:
    """
    Compare a user's answer to a list of expected
    correct answers utilizing the SBERT model.
    """
    # Encoding of the sentence embeddings into vectors.
    correct_embeddings = model.encode(correct_answers)
    user_embedding = model.encode(user_answer)

    # Computation of similarity scores. (Uses COSINE SIMILARITY)
    similarity_scores = model.similarity(
        user_embedding, correct_embeddings
    )[0].tolist()

    # Get the highest similarity score from comparing
    # the user's answer to a list of expected answers.
    max_similarity = max(similarity_scores)

    return similarity_scores, max_similarity
