from pydantic import BaseModel


class StartInterviewSchema(
    BaseModel
):

    resume_analysis: dict = None

    resume_text: str = None

    jd_text: str = None