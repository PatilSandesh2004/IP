from fastapi import APIRouter

from fastapi import UploadFile

from fastapi import File

from fastapi import Form

from fastapi import Depends

from typing import Optional

from sqlalchemy.orm import Session

import shutil

import os

from utils.file_validator import FileValidator

from controllers.resume_analyzer.resume_controller import (
    ResumeController
)

from schemas.resume_ingestion.resume_ingestion_response_schema import (
    ResumeIngestionResponseSchema
)

from infrastructure.database.postgres.session import (
    get_db
)


router = APIRouter(

    prefix="/resume",

    tags=["Resume"]
)


validator = FileValidator()

controller = ResumeController()


@router.post(
    "/upload-resume"
)
async def upload_resume(

        file: Optional[UploadFile] = File(None),

        text_input: Optional[str] = Form(None)
):

    if file is None and text_input is None:

        return {
            "error": (
                "Please provide either file or text"
            )
        }

    if file is not None:

        if not validator.validate_Extension(

                file.filename
        ):

            return {
                "error": "Invalid file type"
            }

        os.makedirs(
            "temp",
            exist_ok=True
        )

        file_path = (
            f"temp/{file.filename}"
        )

        with open(
                file_path,
                "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        extracted_text = (
            await controller.extract_resume_file(
                file_path
            )
        )

    else:

        extracted_text = (
            await controller.extract_resume_text(
                text_input
            )
        )

    return {
        "extracted_text": extracted_text
    }


@router.post(

    "/ingest",

    response_model=(
        ResumeIngestionResponseSchema
    )
)
async def ingest_resume(

        user_id: int = Form(...),

        file: UploadFile = File(...),

        db: Session = Depends(
            get_db
        )
):

    if not validator.validate_Extension(

            file.filename
    ):

        return {
            "error": "Invalid file type"
        }

    os.makedirs(
        "temp",
        exist_ok=True
    )

    file_path = (
        f"temp/{file.filename}"
    )

    with open(
            file_path,
            "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    ingested_profile = (
        await controller.ingest_resume_profile(

            db=db,

            user_id=user_id,

            resume_file_path=file_path
        )
    )

    return (
        ResumeIngestionResponseSchema(

            message=(
                "Resume ingested successfully"
            ),

            candidate_profile_id=(
                ingested_profile.id
            )
        )
    )