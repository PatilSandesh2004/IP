from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.database.postgres.base import (
    Base
)

from infrastructure.database.postgres.database import (
    engine
)

from routers.jd_analyzer.jd_router import (
    router as jd_router
)

from routers.resume_jd_analysis.resume_jd_analysis_router import (
    router as resume_jd_analysis_router
)

from routers.interview_engine.interview_router import (
    router as interview_router
)

from routers.resume_ingestion.resume_ingestion_router import (
    router as resume_ingestion_router
)

from routers.auth.auth_router import (
    router as auth_router
)

from routers.candidate_data_retrieval.candidate_data_retrieval_router import (
    router as candidate_data_retrieval_router
)

from routers.speech.speech_router import (
    router as speech_router
)   

from models.candidate_profile_model import (
    CandidateProfile
)

from models.user_model import (
    User
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_database_tables():

    Base.metadata.create_all(bind=engine)


@app.get("/")
async def home():

    return {
        "message": "resume analyser running"
    }


app.include_router(
    jd_router
)

app.include_router(
    resume_jd_analysis_router
)

app.include_router(
    interview_router
)

app.include_router(
    resume_ingestion_router
)

app.include_router(
    auth_router
)

app.include_router(
    candidate_data_retrieval_router
)
app.include_router(
    speech_router
)