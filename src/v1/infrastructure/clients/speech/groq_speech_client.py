import os 
from groq import Groq

from dependencies import SYSTEM

class GroqSpeechClient:

    def __init__(self):
        self.client = Groq(
            api_key=SYSTEM.GROQ_API_KEY
        )


    async def transcribe_audio(
        self,
        file_path:str,
    ):
        
        with open(
            file_path,
            "rb"
        ) as audio_file:

            transcription=self.client.audio.transcriptions.create(
                file=audio_file,
                model=SYSTEM.GROQ_SPEECH_TO_TEXT_MODEL,
                response_format="json"
            )

            return transcription.text