import json
import re


from infrastructure.clients.llm.groq_llm_client import (
    GroqLLMClient
)

from prompts.resume_ingestion.candidate_profile_extraction_prompt import (
    CANDIDATE_PROFILE_EXTRACTION_PROMPT
)

from schemas.resume_ingestion.candidate_profile_schema import (
    CandidateProfileSchema
)


class CandidateProfileExtractor:
    """
    Service to extract structured candidate profile information from resume text.
    """

    def __init__(self):

        self.llm_client = (
            GroqLLMClient()
        )

    def _strip_markdown(
            self,
            response
    ):

        response = re.sub(
            r'^```json\s*',
            '',
            response.strip(),
            flags=re.IGNORECASE
        )

        response = re.sub(
            r'^```\s*',
            '',
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r'\s*```$',
            '',
            response
        )

        return response.strip()

    def _parse_llm_json(
            self,
            response
    ):

        cleaned_response = self._strip_markdown(
            response
        )

        try:

            return json.loads(
                cleaned_response
            )

        except json.JSONDecodeError:

            start_index = cleaned_response.find(
                "{"
            )

            end_index = cleaned_response.rfind(
                "}"
            )

            if (
                start_index == -1
                or end_index == -1
                or end_index <= start_index
            ):

                raise

            return json.loads(
                cleaned_response[
                    start_index:end_index + 1
                ]
            )

    async def extract_candidate_profile(
            self,
            user_id,
            resume_text
    ):

        return await self.extract_candiate_profile(
            user_id=user_id,
            resume_text=resume_text
        )

    async def extract_candiate_profile(
            self,
            user_id,
            resume_text
    ):
        
        prompt=(
            CANDIDATE_PROFILE_EXTRACTION_PROMPT.format(
                resume_text=resume_text
            )
        )


        response = (
            await self.llm_client.generate_response(
                prompt=prompt,
                temperature=0.2,
            )
        )

        structured_response = (
            self._parse_llm_json(
                response
            )
        )


        validated_profile = (
            CandidateProfileSchema(

                user_id=user_id,

                resume_text=resume_text,

                structured_resume=structured_response,

                **structured_response
            )
        )

        return validated_profile