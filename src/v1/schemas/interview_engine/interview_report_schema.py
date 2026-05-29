from pydantic import BaseModel

from typing import List


class InterviewReportSchema(
    BaseModel
):

    overall_interview_score: int

    technical_score: int

    communication_score: int

    problem_solving_score: int

    project_understanding_score: int

    confidence_score: int

    system_design_score: int

    interview_readiness: str

    hiring_recommendation: str

    technical_strengths: List[str]

    technical_weaknesses: List[str]

    strong_topics: List[str]

    weak_topics: List[str]

    missing_concepts: List[str]

    positive_observations: List[str]

    improvement_recommendations: List[str]

    learning_roadmap: List[str]

    interview_summary: str