from pydantic import BaseModel


class AnswerSubmissionSchema(
    BaseModel
):

    session_id: str

    answer: str

    question_id: int = None

    answer_type: str = "text"