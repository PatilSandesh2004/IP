from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import UploadFile

from sqlalchemy.orm import Session

import json
import os
import shutil

from infrastructure.database.postgres.session import get_db

from controllers.candidate_data_retrieval.candidate_data_retrieval_controller import (
    CandidateDataRetrievalController
)

from schemas.candidate_data_retrieval.candidate_profile_upsert_schema import (
    CandidateProfileUpsertSchema
)

from schemas.candidate_data_retrieval.candidate_data_retrieval_response_schema import (
    CandidateDataRetrievalResponseSchema
)


router = APIRouter(prefix="/candidate", tags=["Candidate Data Retrieval"])

controller = CandidateDataRetrievalController()


def _parse_json_field(value, default):

    if value is None or value == "":
        return default

    if isinstance(value, (list, dict)):
        return value

    return json.loads(value)


@router.get("/{user_id}", response_model=CandidateDataRetrievalResponseSchema)
async def get_candidate_data(user_id: int, db: Session = Depends(get_db)):

    candidate_data = await controller.get_candidate_data(db=db, user_id=user_id)

    if not candidate_data:
        raise HTTPException(status_code=404, detail="Candidate data not found")

    return candidate_data


@router.post("/create-profile", response_model=CandidateDataRetrievalResponseSchema)
async def create_candidate_profile(request: Request, db: Session = Depends(get_db)):

    content_type = request.headers.get("content-type", "")
    resume_file_path = None
    resume_text_input = None

    if content_type.startswith("multipart/form-data"):

        form = await request.form()
        resume_file = form.get("resume_file")

        if resume_file and getattr(resume_file, "filename", None):

            os.makedirs("temp", exist_ok=True)
            resume_file_path = f"temp/{resume_file.filename}"

            with open(resume_file_path, "wb") as buffer:
                shutil.copyfileobj(resume_file.file, buffer)

        resume_text_input = form.get("resume_text_input")

        profile_data = CandidateProfileUpsertSchema(
            user_id=int(form.get("user_id")),
            name=form.get("name"),
            mobile_number=form.get("mobile_number"),
            title=form.get("title"),
            summary=form.get("summary"),
            skills=_parse_json_field(form.get("skills"), []),
            certifications=_parse_json_field(form.get("certifications"), []),
            known_languages=_parse_json_field(form.get("known_languages"), []),
            tools=_parse_json_field(form.get("tools"), []),
            frameworks=_parse_json_field(form.get("frameworks"), []),
            companies_worked_at=_parse_json_field(form.get("companies_worked_at"), []),
            education=_parse_json_field(form.get("education"), []),
            experience=_parse_json_field(form.get("experience"), []),
            projects=_parse_json_field(form.get("projects"), []),
            raw_resume_text=form.get("raw_resume_text"),
            structured_resume_json=_parse_json_field(form.get("structured_resume_json"), {}),
            resume_text_input=resume_text_input,
        )

    else:

        payload = await request.json()
        profile_data = CandidateProfileUpsertSchema(**payload)
        resume_text_input = profile_data.resume_text_input

    candidate_profile = await controller.create_candidate_profile(
        db=db,
        profile_data=profile_data,
        resume_file_path=resume_file_path,
        resume_text_input=resume_text_input,
    )

    return candidate_profile