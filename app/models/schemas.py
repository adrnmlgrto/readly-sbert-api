from pydantic import BaseModel, Field


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
