from fastapi import APIRouter

from controllers.interview_engine.interview_controller import (
    InterviewController
)

from schemas.interview_engine.start_interview_schema import (
    StartInterviewSchema
)

from schemas.interview_engine.answer_submission_schema import (
    AnswerSubmissionSchema
)


router = APIRouter()

controller = (
    InterviewController()
)


@router.post("/start")
async def start_interview(

        request: StartInterviewSchema
):

    response = (
        await controller.start_interview(

            resume_analysis=request.resume_analysis
        )
    )

    return response


@router.post("/answer")
async def submit_answer(

        request: AnswerSubmissionSchema
):

    response = (
        await controller.submit_answer(

            session_id=request.session_id,

            answer=request.answer
        )
    )

    return response