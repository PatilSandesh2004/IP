from sqlalchemy.orm import Session

from services.candidate_data_retrieval.candidate_data_retrieval_service import (
    CandidateDataRetrievalService
)

from schemas.candidate_data_retrieval.candidate_profile_upsert_schema import (
    CandidateProfileUpsertSchema
)


class CandidateDataRetrievalController:
    """
    Controller layer for candidate data retrieval.
    """

    def __init__(self):

        self.service = CandidateDataRetrievalService()

    async def get_candidate_data(self, db: Session, user_id: int):

        return await self.service.get_candidate_data(db=db, user_id=user_id)

    async def create_candidate_profile(
            self,
            db: Session,
            profile_data: CandidateProfileUpsertSchema,
            resume_file_path=None,
            resume_text_input=None
    ):

        return await self.service.create_candidate_profile(
            db=db,
            profile_data=profile_data,
            resume_file_path=resume_file_path,
            resume_text_input=resume_text_input
        )