from services.jd_analyzer.jd_service import JDService


class JDController:

    def __init__(self):
        self.service = JDService()

    async def process_jd_text(
            self,
            jd_text
    ):

        return await self.service.process_jd_from_text(jd_text)

    async def process_jd_file(
            self,
            file_path
    ):

        return await self.service.process_jd_from_file(file_path)