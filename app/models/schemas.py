from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
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


class TextComparisonRequest(BaseModel):
    questions: list[QuestionSchema] = Field(
        ...,
        description=(
            'The list of each question\'s `correct_answers`, '
            'and `user_answer`. Should contain at least one (1) item.'
        ),
        min_length=1
    )


class TextComparisonResponse(BaseModel):
    max_similarity_scores: list[float] = Field(
        ...,
        description=(
            'The list of max similarity scores from the '
            'first question to the last question in order.'
        ),
        examples=[[
            0.8931472296869409,
            0.7481487743874386,
            0.9412736237618937,
            0.3693782387326723,
            0.8237823782623171
        ]]
    )
