# from core.interview_engine.interview_session_manager import (
#     InterviewSessionManager
# )

# from core.interview_engine.question_generator import (
#     QuestionGenerator
# )

# from core.interview_engine.answer_evaluator import (
#     AnswerEvaluator
# )

# from core.interview_engine.interview_flow_manager import (
#     InterviewFlowManager
# )

# from core.interview_engine.followup_question_generator import (
#     FollowupQuestionGenerator
# )

# from core.interview_engine.interview_report_generator import (
#     InterviewReportGenerator
# )


# class InterviewService:
#     """
#     Main interview orchestration service.
#     """

#     def __init__(self):

#         self.session_manager = (
#             InterviewSessionManager()
#         )

#         self.question_generator = (
#             QuestionGenerator()
#         )

#         self.answer_evaluator = (
#             AnswerEvaluator()
#         )

#         self.flow_manager = (
#             InterviewFlowManager()
#         )

#         self.followup_generator = (
#             FollowupQuestionGenerator()
#         )

#         self.report_generator = (
#             InterviewReportGenerator()
#         )

#     async def start_interview(

#             self,

#             resume_analysis
#     ):

#         session_id = (
#             self.session_manager.create_session(

#                 resume_analysis=resume_analysis
#             )
#         )

#         session_data = (
#             self.session_manager.get_session(
#                 session_id
#             )
#         )

#         first_question = (
#             await self.question_generator.generate_question(
#                 session_data
#             )
#         )

#         self.session_manager.add_question(

#             session_id,

#             first_question
#         )

#         self.session_manager.update_question_number(
#             session_id
#         )

#         return {

#             "session_id": session_id,

#             "question": first_question
#         }

#     async def submit_answer(

#             self,

#             session_id,

#             answer
#     ):

#         session_data = (
#             self.session_manager.get_session(
#                 session_id
#             )
#         )

#         previous_question = session_data[
#             "asked_questions"
#         ][-1]

#         self.session_manager.add_answer(

#             session_id,

#             answer
#         )

#         evaluation = (
#             await self.answer_evaluator.evaluate_answer(

#                 question=previous_question,

#                 candidate_answer=answer,

#                 session_data=session_data
#             )
#         )

#         self.session_manager.add_evaluation(

#             session_id,

#             evaluation
#         )

#         for topic in evaluation.get(
#                 "weak_topics",
#                 []
#         ):

#             self.session_manager.add_weak_topic(

#                 session_id,

#                 topic
#             )

#         for topic in evaluation.get(
#                 "strong_topics",
#                 []
#         ):

#             self.session_manager.add_strong_topic(

#                 session_id,

#                 topic
#             )

#         flow_decision = (
#             self.flow_manager.decide_next_step(

#                 evaluation=evaluation,

#                 session_data=session_data
#             )
#         )

#         if flow_decision["action"] == "END_INTERVIEW":

#             report = (
#                 await self.report_generator.generate_report(
#                     session_data
#                 )
#             )

#             return {

#                 "interview_completed": True,

#                 "report": report
#             }

#         elif flow_decision["action"] == "FOLLOWUP_QUESTION":

#             next_question = (
#                 await self.followup_generator.generate_followup_question(

#                     previous_question=previous_question,

#                     candidate_answer=answer,

#                     evaluation=evaluation
#                 )
#             )

#         else:

#             next_question = (
#                 await self.question_generator.generate_question(
#                     session_data
#                 )
#             )

#         self.session_manager.add_question(

#             session_id,

#             next_question
#         )

#         self.session_manager.update_question_number(
#             session_id
#         )

#         return {

#             "interview_completed": False,

#             "evaluation": evaluation,

#             "next_question": next_question
#         }


from core.interview_engine.interview_session_manager import (
    InterviewSessionManager
)

from core.interview_engine.question_generator import (
    QuestionGenerator
)

from core.interview_engine.answer_evaluator import (
    AnswerEvaluator
)

from core.interview_engine.interview_flow_manager import (
    InterviewFlowManager
)

from core.interview_engine.followup_question_generator import (
    FollowupQuestionGenerator
)

from core.interview_engine.interview_report_generator import (
    InterviewReportGenerator
)

from services.resume_jd_analysis.resume_jd_analysis_service import (
    ResumeJDAnalysisService
)


class InterviewService:
    """
    Main interview orchestration service.
    """

    def __init__(self):

        self.session_manager = (
            InterviewSessionManager()
        )

        self.question_generator = (
            QuestionGenerator()
        )

        self.answer_evaluator = (
            AnswerEvaluator()
        )

        self.flow_manager = (
            InterviewFlowManager()
        )

        self.followup_generator = (
            FollowupQuestionGenerator()
        )

        self.report_generator = (
            InterviewReportGenerator()
        )

        self.resume_jd_service = (
            ResumeJDAnalysisService()
        )

    async def start_interview(

            self,

            resume_analysis=None,

            resume_text=None,

            jd_text=None
    ):

        if not resume_analysis:

            resume_analysis = (
                await self.resume_jd_service.analyze(

                    resume_text_input=resume_text,

                    jd_text_input=jd_text
                )
            )

        session_id = (
            self.session_manager.create_session(

                resume_analysis=resume_analysis
            )
        )

        session_data = (
            self.session_manager.get_session(
                session_id
            )
        )

        first_question = (
            await self.question_generator.generate_questions(
                session_data
            )
        )

        self.session_manager.add_question(

            session_id,

            first_question
        )

        self.session_manager.update_question_number(
            session_id
        )

        return {

            "session_id": session_id,

            "resume_analysis": resume_analysis,

            "question": first_question
        }

    async def submit_answer(

            self,

            session_id,

            answer
    ):

        session_data = (
            self.session_manager.get_session(
                session_id
            )
        )

        if not session_data:

            return {

                "error": "Invalid session ID"
            }

        previous_question = session_data[
            "asked_questions"
        ][-1]

        self.session_manager.add_answer(

            session_id,

            answer
        )

        evaluation = (
            await self.answer_evaluator.evaluate_answer(

                question=previous_question,

                candidate_answer=answer,

                session_data=session_data
            )
        )

        self.session_manager.add_evaluation(

            session_id,

            evaluation
        )

        for topic in evaluation.get(
                "weak_topics",
                []
        ):

            self.session_manager.add_weak_topic(

                session_id,

                topic
            )

        for topic in evaluation.get(
                "strong_topics",
                []
        ):

            self.session_manager.add_strong_topic(

                session_id,

                topic
            )

        flow_decision = (
            self.flow_manager.decide_next_step(

                evaluation=evaluation,

                session_data=session_data
            )
        )

        if flow_decision["action"] == "END_INTERVIEW":

            report = (
                await self.report_generator.generate_report(
                    session_data
                )
            )

            return {

                "interview_completed": True,

                "final_report": report
            }

        elif flow_decision["action"] == "FOLLOWUP_QUESTION":

            next_question = (
                await self.followup_generator.generate_followup_question(

                    previous_question=previous_question,

                    candidate_answer=answer,

                    evaluation=evaluation
                )
            )

        else:

            next_question = (
                await self.question_generator.generate_questions(
                    session_data
                )
            )

        self.session_manager.add_question(

            session_id,

            next_question
        )

        self.session_manager.update_question_number(
            session_id
        )

        return {

            "interview_completed": False,

            "evaluation": evaluation,

            "next_question": next_question,

            "current_question_number": session_data[
                "current_question_number"
            ]
        }