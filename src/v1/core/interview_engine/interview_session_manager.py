import uuid


INTERVIEW_SESSIONS = {}


class InterviewSessionManager:
    """
    Handles interview session memory
    and conversation state.
    """

    def create_session(

            self,

            resume_analysis,

            interview_type="technical"
    ):

        session_id = str(
            uuid.uuid4()
        )

        INTERVIEW_SESSIONS[session_id] = {

            "session_id": session_id,

            "interview_type": interview_type,

            "current_question_number": 0,

            "resume_analysis": resume_analysis,

            "asked_questions": [],

            "candidate_answers": [],

            "answer_evaluations": [],

            "weak_topics": [],

            "strong_topics": [],

            "conversation_history": [],

            "overall_score": 0,

            "followup_required": False
        }

        return session_id

    def get_session(
            self,
            session_id
    ):

        return INTERVIEW_SESSIONS.get(
            session_id
        )

    def add_question(

            self,

            session_id,

            question
    ):

        INTERVIEW_SESSIONS[session_id][
            "asked_questions"
        ].append(question)

    def add_answer(

            self,

            session_id,

            answer
    ):

        INTERVIEW_SESSIONS[session_id][
            "candidate_answers"
        ].append(answer)

    def add_evaluation(

            self,

            session_id,

            evaluation
    ):

        INTERVIEW_SESSIONS[session_id][
            "answer_evaluations"
        ].append(evaluation)

    def add_weak_topic(

            self,

            session_id,

            topic
    ):

        INTERVIEW_SESSIONS[session_id][
            "weak_topics"
        ].append(topic)

    def add_strong_topic(

            self,

            session_id,

            topic
    ):

        INTERVIEW_SESSIONS[session_id][
            "strong_topics"
        ].append(topic)

    def update_question_number(
            self,
            session_id
    ):

        INTERVIEW_SESSIONS[session_id][
            "current_question_number"
        ] += 1

    def add_conversation_history(

            self,

            session_id,

            role,

            content
    ):

        INTERVIEW_SESSIONS[session_id][
            "conversation_history"
        ].append({

            "role": role,

            "content": content
        })

    def set_followup_required(

            self,

            session_id,

            status
    ):

        INTERVIEW_SESSIONS[session_id][
            "followup_required"
        ] = status