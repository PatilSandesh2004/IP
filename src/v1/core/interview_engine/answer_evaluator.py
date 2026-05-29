import json

from infrastructure.clients.llm.groq_llm_client import GroqLLMClient
# from prompts.resume_jd_analysis.resume_jd_analysis_prompt import RESUME_JD_ANALYSIS_PROMPT

from prompts.interview_engine.answer_evaluation_prompt import ANSWER_EVALUATION_PROMPT

class AnswerEvaluator:
    def __init__(self):

        self.llm_client = GroqLLMClient()

    async def evaluate_answer(
            self,
            question,
            candidate_answer,
            session_data
    ):
        
        prompt=ANSWER_EVALUATION_PROMPT.format(
            question=question,

            candidate_answer=candidate_answer,

            weak_topics=session_data[
                "weak_topics"
            ],
            strong_topics=session_data[
                "strong_topics"
            ]

        )

        response = await self.llm_client.generate_response(
            prompt=prompt,
            temperature=0.2,
        )

        cleaned_response = response.strip()
        return json.loads(cleaned_response)