from sqlalchemy.orm import Session

from services.resume_ingestion.resume_ingestion_service import (
    ResumeIngestionService
)


class ResumeIngestionController:
    """
    Controller layer for resume ingestion.
    """

    def __init__(
            self
    ):

        self.service = (
            ResumeIngestionService()
        )

    async def ingest_resume(

            self,

            db: Session,

            user_id: int,

            resume_text: str
    ):

        ingested_profile = (
            await self.service.ingest_resume(

                db=db,

                user_id=user_id,

                resume_text=resume_text
            )
        )

        return ingested_profile