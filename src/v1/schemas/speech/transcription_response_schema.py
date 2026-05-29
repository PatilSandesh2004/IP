from pydantic import BaseModel


class TranscriptionResponseSchema(
    BaseModel
):

    transcript: str