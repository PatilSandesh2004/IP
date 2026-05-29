from sqlalchemy.orm import Session

from models.candidate_profile_model import (
    CandidateProfile
)


class CandidateDataRetriever:

    async def retrieve_candidate_data(

            self,

            db: Session,

            user_id: int
    ):

        candidate_profile = (

            db.query(
                CandidateProfile
            )

            .filter(
                CandidateProfile.user_id == user_id
            )

            .first()
        )

        return candidate_profile