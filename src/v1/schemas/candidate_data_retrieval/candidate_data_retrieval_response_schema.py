from pydantic import BaseModel

from typing import List

from typing import Dict

from typing import Any

from typing import Optional


class CandidateDataRetrievalResponseSchema(
    BaseModel
):

    name: Optional[str] = None
    raw_resume_text: Optional[str] = None

    id: int

    user_id: int

    mobile_number: Optional[str]

    title: Optional[str]

    summary: Optional[str]

    skills: List[str]

    certifications: List[str]

    known_languages: List[str]

    tools: List[str]

    frameworks: List[str]

    companies_worked_at: List[str]

    education: List[Dict[str, Any]]

    experience: List[Dict[str, Any]]

    projects: List[Dict[str, Any]]

    structured_resume_json: Dict[str, Any]

    class Config:

        from_attributes = True