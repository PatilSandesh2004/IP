from core.resume_analyzer.pdf_parser import PDFParser
from controllers.resume_ingestion.resume_ingestion_controller import (
    ResumeIngestionController
)
from docx import Document


class ResumeService:

    def __init__(
            self
    ):

        self.parser = PDFParser()
        self.ingestion_controller = ResumeIngestionController()

    async def extract_text_from_file(
            self,
            file_path
    ):

        if file_path.endswith(".pdf"):

            extracted_text = (
                self.parser.extract_text(
                    file_path
                )
            )

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            extracted_text = "\n".join(

                para.text

                for para in doc.paragraphs
            )

        elif file_path.endswith(".txt"):

            with open(
                    file_path,
                    "r",
                    encoding="utf-8"
            ) as f:

                extracted_text = f.read()

        else:

            extracted_text = ""

        return extracted_text

    async def extract_text_from_string(
            self,
            text_input
    ):

        return text_input.strip()
    
    async def ingest_resume_profile(

        self,

        db,

        user_id,

        resume_file_path=None,

        resume_text_input=None
    ):

        if resume_file_path:

            processed_resume = (
                await self.extract_text_from_file(
                    resume_file_path
                )
            )

        else:

            processed_resume = (
                await self.extract_text_from_string(
                    resume_text_input
                )
            )

        ingested_profile = (
            await self.ingestion_controller.ingest_resume(

                db=db,

                user_id=user_id,

                resume_text=processed_resume
            )
        )

        return ingested_profile