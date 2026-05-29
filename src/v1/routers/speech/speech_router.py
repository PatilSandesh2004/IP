from fastapi import APIRouter

from fastapi import UploadFile

from fastapi import File

import shutil

import os

from controllers.speech.speech_controller import (
    SpeechController
)

from schemas.speech.transcription_response_schema import (
    TranscriptionResponseSchema
)


router = APIRouter(

    prefix="/speech",

    tags=["Speech"]
)


controller = (
    SpeechController()
)


@router.post(

    "/transcribe",

    response_model=(
        TranscriptionResponseSchema
    )
)
async def transcribe_audio(

        audio: UploadFile = File(...)
):

    os.makedirs(
        "temp_audio",
        exist_ok=True
    )

    file_path = (
        f"temp_audio/{audio.filename}"
    )

    with open(
            file_path,
            "wb"
    ) as buffer:

        shutil.copyfileobj(
            audio.file,
            buffer
        )

    transcript = (
        await controller.transcribe_audio(
            file_path
        )
    )

    return (
        TranscriptionResponseSchema(

            transcript=transcript
        )
    )