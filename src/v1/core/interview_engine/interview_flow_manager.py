class InterviewFlowManager:
    """
    Controls interview flow
    and adaptive interview logic.
    """

    def decide_next_step(

            self,

            evaluation,

            session_data
    ):

        score = evaluation.get(
            "score",
            0
        )

        followup_required = evaluation.get(
            "followup_required",
            False
        )

        current_question_number = session_data.get(
            "current_question_number",
            0
        )

        if current_question_number >= 15:

            return {
                "action": "END_INTERVIEW"
            }

        if followup_required:

            return {

                "action": "FOLLOWUP_QUESTION",

                "reason": evaluation.get(
                    "followup_reason"
                )
            }

        if score >= 8:

            return {

                "action": "INCREASE_DIFFICULTY"
            }

        if score >= 5:

            return {

                "action": "NEXT_QUESTION"
            }

        return {

            "action": "ASK_WEAK_TOPIC_QUESTION"
        }