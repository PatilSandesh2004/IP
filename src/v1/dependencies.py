import os

from dotenv import load_dotenv

load_dotenv()



class SYSTEM:
    """
    System class to hold system-wide constants and configurations.
    """

    # Load the GROQ API key from environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL=os.getenv("GROQ_MODEL")
    GROQ_SPEECH_TO_TEXT_MODEL=os.getenv("GROQ_SPEECH_TO_TEXT_MODEL")
    POSTGRES_HOST=os.getenv("POSTGRES_HOST")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT")
    POSTGRES_DB=os.getenv("POSTGRES_DB")
    POSTGRES_USER=os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")    






