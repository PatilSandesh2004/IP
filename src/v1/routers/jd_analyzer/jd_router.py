from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from typing import Optional

import shutil

from utils.file_validator import FileValidator

from controllers.jd_analyzer.jd_controller import JDController


router = APIRouter()

validator = FileValidator()

controller = JDController()


@router.post("/process-jd")
async def process_jd(
    file: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None)
):

    if file is None and text_input is None:

        return {
            "error": "Please provide either a file or text input"
        }

    if file is not None:

        if not validator.validate_Extension(
            file.filename
        ):

            return {
                "error": "Invalid file type"
            }

        file_path = f"temp/{file.filename}"

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        extracted_text = await controller.process_jd_file(
            file_path
        )

    else:

        extracted_text = await controller.process_jd_text(
            text_input
        )

    return {
        "extracted_text": extracted_text
    }