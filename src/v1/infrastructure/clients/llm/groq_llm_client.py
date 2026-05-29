from groq import Groq

from dependencies import SYSTEM


class GroqLLMClient:
    """
    Client for interacting with Groq LLM models.
    """

    def __init__(self):

        self.client = Groq(
            api_key=SYSTEM.GROQ_API_KEY
        )

    async def generate_response(

        self,

        prompt,

        model=SYSTEM.GROQ_MODEL,

        temperature=0.2,

        max_tokens=4000
    ):

        response = self.client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=temperature,

            max_tokens=max_tokens
        )

        return response.choices[0].message.content