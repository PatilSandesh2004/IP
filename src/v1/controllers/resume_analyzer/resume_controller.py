from services.resume_analyzer.resume_service import ResumeService


class ResumeController:

    def __init__(self):
        self.service = ResumeService()

    async def extract_resume_file(
            self,
            file_path
    ):

        return await self.service.extract_text_from_file(file_path)

    async def extract_resume_text(
            self,
            text_input
    ):

        return await self.service.extract_text_from_string(text_input)

    async def ingest_resume_profile(
            self,
            db,
            user_id,
            resume_file_path=None,
            resume_text_input=None
    ):

        return await self.service.ingest_resume_profile(
            db=db,
            user_id=user_id,
            resume_file_path=resume_file_path,
            resume_text_input=resume_text_input
        )
