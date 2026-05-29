from infrastructure.clients.llm.groq_llm_client import (
    GroqLLMClient
)

from prompts.interview_engine.followup_question_prompt import (
    FOLLOWUP_QUESTION_PROMPT
)


class FollowupQuestionGenerator:
    """
    Generates intelligent follow-up questions
    based on candidate weak answers.
    """

    def __init__(self):

        self.llm = GroqLLMClient()

    async def generate_followup_question(

            self,

            previous_question,

            candidate_answer,

            evaluation
    ):

        prompt = FOLLOWUP_QUESTION_PROMPT.format(

            previous_question=previous_question,

            candidate_answer=candidate_answer,

            weak_topics=evaluation.get(
                "weak_topics",
                []
            ),

            missing_concepts=evaluation.get(
                "missing_concepts",
                []
            ),

            followup_reason=evaluation.get(
                "followup_reason",
                ""
            )
        )

        response = await self.llm.generate_response(

            prompt=prompt,

            temperature=0.5
        )

        return response.strip()