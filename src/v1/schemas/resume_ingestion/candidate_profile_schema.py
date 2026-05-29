from pydantic import BaseModel

from pydantic import Field

from typing import List

from typing import Dict

from typing import Any

from typing import Optional


class CandidateProfileSchema(
    BaseModel
):

    user_id: int
    mobile_number: Optional[str] = None
    title: Optional[str] = None

    summary: Optional[str] = None

    skills: List[str] = Field(
        default_factory=list
    )

    certifications: List[str] = Field(
        default_factory=list
    )

    known_languages: List[str] = Field(
        default_factory=list
    )

    tools: List[str] = Field(
        default_factory=list
    )

    frameworks: List[str] = Field(
        default_factory=list
    )

    companies_worked_at: List[str] = Field(
        default_factory=list
    )

    education: List[
        Dict[str, Any]
    ] = Field(
        default_factory=list
    )

    experience: List[
        Dict[str, Any]
    ] = Field(
        default_factory=list
    )

    projects: List[
        Dict[str, Any]
    ] = Field(
        default_factory=list
    )

    resume_text: str

    structured_resume: Dict[
        str,
        Any
    ]