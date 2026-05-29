from infrastructure.clients.llm.groq_llm_client import GroqLLMClient
from prompts.interview_engine.question_generation_prompt import QUESTION_GENERATION_PROMPT


class QuestionGenerator:

    def __init__(self):
        self.llm_client = GroqLLMClient()

    async def generate_question(
            self,
            session_data
    ):

        return await self.generate_questions(
            session_data
        )

    async def generate_questions(
            self,
            session_data
    ):
        
        prompt = QUESTION_GENERATION_PROMPT.format(

            current_question_number=session_data.get(
                "current_question_number",
                0
            ),

            asked_questions=session_data.get(
                "asked_questions",
                []
            ),

            weak_topics=session_data.get(
                "weak_topics",
                []
            ),

            strong_topics=session_data.get(
                "strong_topics",
                []
            ),

            previous_answers=session_data.get(
                "candidate_answers",
                []
            ),

            resume_analysis=session_data[
                "resume_analysis"
            ]
        )

        response = await self.llm_client.generate_response(
            prompt=prompt,
            temperature=0.6,
            
        )

        return response.strip()
