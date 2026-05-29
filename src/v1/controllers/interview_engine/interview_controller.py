from services.interview_engine.interview_service import (
    InterviewService
)


class InterviewController:
    """
    Interview controller layer.
    """

    def __init__(self):

        self.service = (
            InterviewService()
        )

    async def start_interview(

            self,

            resume_analysis
    ):

        return await self.service.start_interview(

            resume_analysis=resume_analysis
        )

    async def submit_answer(

            self,

            session_id,

            answer
    ):

        return await self.service.submit_answer(

            session_id=session_id,

            answer=answer
        )