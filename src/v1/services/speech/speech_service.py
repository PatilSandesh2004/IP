from core.speech.speech_transcriber import SpeechTranscriber

class SpeechService:

    def __init__(
            self
    ):

        self.transcriber = SpeechTranscriber()

    async def transcribe_speech(
            self,
            file_path:str
    ):

        transcript = await self.transcriber.transcribe(file_path)

        return transcript