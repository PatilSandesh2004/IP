from sqlalchemy import Column

from sqlalchemy import Integer

from sqlalchemy import String

from sqlalchemy import Text

from sqlalchemy import DateTime

from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime

from infrastructure.database.postgres.base import (
    Base
)


class CandidateProfile(
    Base
):

    __tablename__ = (
        "candidate_profiles"
    )

    id = Column(

        Integer,

        primary_key=True,

        index=True
    )

    user_id = Column(

        Integer,

        nullable=False
    )

    mobile_number = Column(

        String,

        nullable=True
    )

    title = Column(

        String,

        nullable=True
    )

    summary = Column(

        Text,

        nullable=True
    )

    skills = Column(

        JSONB,

        nullable=True
    )

    certifications = Column(

        JSONB,

        nullable=True
    )

    known_languages = Column(

        JSONB,

        nullable=True
    )

    tools = Column(

        JSONB,

        nullable=True
    )

    frameworks = Column(

        JSONB,

        nullable=True
    )

    companies_worked_at = Column(

        JSONB,

        nullable=True
    )

    education = Column(

        JSONB,

        nullable=True
    )

    experience = Column(

        JSONB,

        nullable=True
    )

    projects = Column(

        JSONB,

        nullable=True
    )

    raw_resume_text = Column(

        Text,

        nullable=False
    )

    structured_resume_json = Column(

        JSONB,

        nullable=False
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )