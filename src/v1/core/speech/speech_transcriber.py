from infrastructure.clients.speech.groq_speech_client import GroqSpeechClient

class SpeechTranscriber:
    def __init__(self):
        self.groq_clinet = GroqSpeechClient()

    async def transcribe(self,file_path:str):

        transcript=await self.groq_clinet.transcribe_audio(file_path)
        return transcript
    