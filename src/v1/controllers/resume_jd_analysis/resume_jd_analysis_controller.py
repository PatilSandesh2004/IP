from services.resume_jd_analysis.resume_jd_analysis_service import ResumeJDAnalysisService

class ResumeJDAnalysisController:

    def __init__(self):
        self.service = ResumeJDAnalysisService()

    async def analyze(
        self,
        resume_file_path=None,
        resume_text_input=None,
        jd_file_path=None,
        jd_text_input=None
    ):

        return await self.service.analyze(
            resume_file_path=resume_file_path,
            resume_text_input=resume_text_input,
            jd_file_path=jd_file_path,
            jd_text_input=jd_text_input
        )