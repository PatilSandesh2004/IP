from core.resume_jd_analysis.resume_jd_analyzer import (
    ResumeJDAnalyzer
)

from services.resume_analyzer.resume_service import (
    ResumeService
)

from services.jd_analyzer.jd_service import (
    JDService
)


class ResumeJDAnalysisService:
    """
    Service for analyzing
    resume against job description.
    """

    def __init__(self):

        self.resume_service = (
            ResumeService()
        )

        self.jd_service = (
            JDService()
        )

        self.analyzer = (
            ResumeJDAnalyzer()
        )

    async def analyze(

        self,

        resume_file_path=None,

        resume_text_input=None,

        jd_file_path=None,

        jd_text_input=None
    ):

        if resume_file_path:

            resume_text = (
                await self.resume_service.extract_text_from_file(
                    resume_file_path
                )
            )

        else:

            resume_text = (
                await self.resume_service.extract_text_from_string(
                    resume_text_input
                )
            )

        if jd_file_path:

            jd_text = (
                await self.jd_service.process_jd_from_file(
                    jd_file_path
                )
            )

        else:

            jd_text = (
                await self.jd_service.process_jd_from_text(
                    jd_text_input
                )
            )

        analyzed_response = (
            await self.analyzer.analyze(

                resume_text=resume_text,

                jd_text=jd_text
            )
        )

        return analyzed_response