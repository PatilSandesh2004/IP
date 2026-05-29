from pydantic import BaseModel

from datetime import datetime


class ResumeVersionSchema(
    BaseModel
):

    resume_version: int

    uploaded_at: datetime

    is_active: bool