from services.speech.speech_service import SpeechService


class SpeechController:
    def __init__(self):
        self.service = SpeechService()

    async def transcribe_audio(
        self,
        file_path:str
    ):

       transcript=await self.service.transcribe_audio(file_path)
       return transcript