from pydantic import BaseModel


class ResumeIngestionResponseSchema(
    BaseModel
):

    message: str

    candidate_profile_id: int