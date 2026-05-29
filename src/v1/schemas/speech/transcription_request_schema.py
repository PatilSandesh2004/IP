from pydantic import BaseModel

from typing import Optional


class TranscriptionRequestSchema(
    BaseModel
):

    language: Optional[str] = "en"