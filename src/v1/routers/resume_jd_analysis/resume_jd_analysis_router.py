import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from utils.file_validator import FileValidator

from controllers.resume_jd_analysis.resume_jd_analysis_controller import (
    ResumeJDAnalysisController
)


router = APIRouter()

validator = FileValidator()

controller = (
    ResumeJDAnalysisController()
)


@router.post("/analyze")
async def analyze_resume_and_jd(

    resume_file: UploadFile = File(None),

    resume_text_input: str = Form(None),

    jd_file: UploadFile = File(None),

    jd_text_input: str = Form(None)
):

    resume_file_path = None

    jd_file_path = None

    if not resume_file and not resume_text_input:

        return {
            "error": "Resume input required"
        }

    if not jd_file and not jd_text_input:

        return {
            "error": "JD input required"
        }

    if resume_file:

        if not validator.validate_extension(
            resume_file.filename
        ):

            return {
                "error": "Invalid resume file type"
            }

        resume_file_path = (
            f"temp/{resume_file.filename}"
        )

        with open(
                resume_file_path,
                "wb"
        ) as buffer:

            shutil.copyfileobj(
                resume_file.file,
                buffer
            )

    if jd_file:

        if not validator.validate_extension(
            jd_file.filename
        ):

            return {
                "error": "Invalid JD file type"
            }

        jd_file_path = (
            f"temp/{jd_file.filename}"
        )

        with open(
                jd_file_path,
                "wb"
        ) as buffer:

            shutil.copyfileobj(
                jd_file.file,
                buffer
            )

    response = await controller.analyze(

        resume_file_path=resume_file_path,

        resume_text_input=resume_text_input,

        jd_file_path=jd_file_path,

        jd_text_input=jd_text_input
    )

    return response