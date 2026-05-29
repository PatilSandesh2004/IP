from infrastructure.clients.llm.groq_llm_client import (
    GroqLLMClient
)

from prompts.interview_engine.interview_report_prompt import (
    INTERVIEW_REPORT_PROMPT
)


class InterviewReportGenerator:
    """
    Generates final interview evaluation report.
    """

    def __init__(self):

        self.llm = GroqLLMClient()

    async def generate_report(

            self,

            session_data
    ):

        prompt = INTERVIEW_REPORT_PROMPT.format(

            asked_questions=session_data[
                "asked_questions"
            ],

            candidate_answers=session_data[
                "candidate_answers"
            ],

            answer_evaluations=session_data[
                "answer_evaluations"
            ],

            weak_topics=session_data[
                "weak_topics"
            ],

            strong_topics=session_data[
                "strong_topics"
            ]
        )

        response = await self.llm.generate_response(

            prompt=prompt,

            temperature=0.3
        )

        return response.strip()