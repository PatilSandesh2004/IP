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

from schemas.candidate_data_retrieval.candidate_profile_upsert_schema import (
    CandidateProfileUpsertSchema
)

from services.resume_analyzer.resume_service import (
    ResumeService
)


class CandidateDataRetrievalService:

    def __init__(self):

        self.resume_service = ResumeService()
        self.profile_extractor = CandidateProfileExtractor()

    def _prefer(self, primary, fallback):

        if primary is None:
            return fallback

        if isinstance(primary, str):
            return primary.strip() or fallback

        if isinstance(primary, list):
            return primary or fallback

        if isinstance(primary, dict):
            return primary or fallback

        return primary

    async def get_candidate_data(self, db: Session, user_id: int):

        candidate_profile = db.query(CandidateProfile).filter(
            CandidateProfile.user_id == user_id
        ).first()

        if not candidate_profile:
            return None

        user = db.query(User).filter(User.id == user_id).first()

        if user:
            candidate_profile.name = user.name
            candidate_profile.email = user.email

        return candidate_profile

    async def create_candidate_profile(
            self,
            db: Session,
            profile_data: CandidateProfileUpsertSchema,
            resume_file_path=None,
            resume_text_input=None
    ):

        extracted_profile = None

        if resume_file_path or resume_text_input:

            if resume_file_path:
                resume_text = await self.resume_service.extract_text_from_file(
                    resume_file_path
                )
            else:
                resume_text = await self.resume_service.extract_text_from_string(
                    resume_text_input or ""
                )

            extracted_profile = await self.profile_extractor.extract_candidate_profile(
                user_id=profile_data.user_id,
                resume_text=resume_text
            )

        profile_payload = profile_data.dict()

        if extracted_profile:

            extracted_payload = extracted_profile.dict()

            for field_name in (
                "mobile_number",
                "title",
                "summary",
                "skills",
                "certifications",
                "known_languages",
                "tools",
                "frameworks",
                "companies_worked_at",
                "education",
                "experience",
                "projects"
            ):
                profile_payload[field_name] = self._prefer(
                    profile_payload.get(field_name),
                    extracted_payload.get(field_name)
                )

            profile_payload["raw_resume_text"] = self._prefer(
                profile_payload.get("raw_resume_text"),
                extracted_payload.get("resume_text")
            ) or ""

            profile_payload["structured_resume_json"] = self._prefer(
                profile_payload.get("structured_resume_json"),
                extracted_payload.get("structured_resume")
            ) or {}

        candidate_profile = db.query(CandidateProfile).filter(
            CandidateProfile.user_id == profile_payload["user_id"]
        ).first()

        if not candidate_profile:
            candidate_profile = CandidateProfile(
                user_id=profile_payload["user_id"],
                raw_resume_text=profile_payload.get("raw_resume_text") or "",
                structured_resume_json=profile_payload.get("structured_resume_json") or {}
            )
            db.add(candidate_profile)

        candidate_profile.mobile_number = profile_payload.get("mobile_number")
        candidate_profile.title = profile_payload.get("title")
        candidate_profile.summary = profile_payload.get("summary")
        candidate_profile.skills = profile_payload.get("skills")
        candidate_profile.certifications = profile_payload.get("certifications")
        candidate_profile.known_languages = profile_payload.get("known_languages")
        candidate_profile.tools = profile_payload.get("tools")
        candidate_profile.frameworks = profile_payload.get("frameworks")
        candidate_profile.companies_worked_at = profile_payload.get("companies_worked_at")
        candidate_profile.education = profile_payload.get("education")
        candidate_profile.experience = profile_payload.get("experience")
        candidate_profile.projects = profile_payload.get("projects")
        candidate_profile.raw_resume_text = profile_payload.get("raw_resume_text") or candidate_profile.raw_resume_text
        candidate_profile.structured_resume_json = profile_payload.get("structured_resume_json") or candidate_profile.structured_resume_json

        user = db.query(User).filter(User.id == profile_payload["user_id"]).first()

        if user and profile_payload.get("name"):
            user.name = profile_payload["name"]

        db.commit()
        db.refresh(candidate_profile)

        if user:
            user.profile_completed = True
            db.commit()

        return candidate_profile