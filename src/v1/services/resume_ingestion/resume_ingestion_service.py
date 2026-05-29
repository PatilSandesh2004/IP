from sqlalchemy.orm import Session

from core.resume_ingestion.candidate_profile_extractor import (
    CandidateProfileExtractor
)

from models.candidate_profile_model import (
    CandidateProfile
)

from models.user_model import (
    User
)


class ResumeIngestionService:
    """
    Main resume ingestion service.
    """

    def __init__(
            self
    ):

        self.extractor = CandidateProfileExtractor()

    async def ingest_resume(

            self,

            db: Session,

            user_id,

            resume_text
    ):

        extracted_profile = await self.extractor.extract_candidate_profile(
            user_id=user_id,
            resume_text=resume_text
        )

        candidate_profile = db.query(CandidateProfile).filter(
            CandidateProfile.user_id == extracted_profile.user_id
        ).first()

        if not candidate_profile:
            candidate_profile = CandidateProfile(
                user_id=extracted_profile.user_id,
                raw_resume_text=extracted_profile.resume_text,
                structured_resume_json=extracted_profile.structured_resume
            )
            db.add(candidate_profile)

        candidate_profile.mobile_number = extracted_profile.mobile_number
        candidate_profile.title = extracted_profile.title
        candidate_profile.summary = extracted_profile.summary
        candidate_profile.skills = extracted_profile.skills
        candidate_profile.certifications = extracted_profile.certifications
        candidate_profile.known_languages = extracted_profile.known_languages
        candidate_profile.tools = extracted_profile.tools
        candidate_profile.frameworks = extracted_profile.frameworks
        candidate_profile.companies_worked_at = extracted_profile.companies_worked_at
        candidate_profile.education = extracted_profile.education
        candidate_profile.experience = extracted_profile.experience
        candidate_profile.projects = extracted_profile.projects
        candidate_profile.raw_resume_text = extracted_profile.resume_text
        candidate_profile.structured_resume_json = extracted_profile.structured_resume

        db.commit()
        db.refresh(candidate_profile)

        user = db.query(User).filter(User.id == extracted_profile.user_id).first()
        if user:
            user.profile_completed = True
            db.commit()

        return candidate_profile
