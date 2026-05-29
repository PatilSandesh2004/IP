# RESUME_JD_ANALYSIS_PROMPT = """
# You are an expert ATS Resume Analyzer and Technical Hiring Assistant.

# Your task is to deeply analyze the candidate resume against the given job description.

# You must identify:
# - matching technical skills
# - missing technical skills
# - matching tools and frameworks
# - relevant projects
# - candidate strengths
# - candidate weaknesses
# - experience alignment
# - learning recommendations

# IMPORTANT:
# Do NOT generate random scores.
# The backend system will calculate scores separately.

# Return ONLY valid JSON.

# Do not add explanations.
# Do not add markdown.
# Do not add extra text.

# Expected JSON format:

# {
#   "matched_skills": [],
#   "missing_skills": [],
#   "matched_frameworks": [],
#   "missing_frameworks": [],
#   "matched_tools": [],
#   "missing_tools": [],
#   "matched_databases": [],
#   "missing_databases": [],
#   "matched_cloud_technologies": [],
#   "missing_cloud_technologies": [],

#   "experience_analysis": {
#     "required_years": 0,
#     "candidate_years": 0,
#     "experience_match_percentage": 0,
#     "status": ""
#   },

#   "project_relevance": {
#     "relevant_projects": [],
#     "relevance_percentage": 0
#   },

#   "resume_quality": {
#     "quality_percentage": 0,
#     "issues": []
#   },

#   "strengths": [],

#   "weaknesses": [],

#   "recommendations": []
# }

# Rules:
# - Extract ONLY technical information
# - Normalize skill names
# - Remove duplicate skills
# - Compare resume technologies with JD technologies
# - Recommendations should focus on improving missing skills
# - experience_match_percentage should be between 0 and 100
# - relevance_percentage should be between 0 and 100
# - quality_percentage should be between 0 and 100
# - Status should be one of:
#   - "Matched"
#   - "Partially Matched"
#   - "Not Matched"

# Resume:
# {resume_text}

# Job Description:
# {jd_text}
# """



import json
import re

from infrastructure.clients.llm.groq_llm_client import GroqLLMClient
# from prompts.resume_analyzer.recommendation_prompts import RESUME_JD_ANALYSIS_PROMPT
# from

from prompts.resume_jd_analysis.resume_jd_analysis_prompt import (
    RESUME_JD_ANALYSIS_PROMPT
)

class ResumeJDAnalyzer:

    def __init__(self):

        self.llm_client = GroqLLMClient()

    def _strip_markdown(self, response):

        response = response.strip()

        response = re.sub(r'^```(?:json)?\s*', '', response)

        response = re.sub(r'\s*```$', '', response)

        return response.strip()

    async def analyze(
            self,
            resume_text,
            jd_text,
    ):
        prompt = RESUME_JD_ANALYSIS_PROMPT.format(
            resume_text=resume_text,
            jd_text=jd_text
        )

        response = await self.llm_client.generate_response(

            prompt=prompt,
            temperature=0.2,
            max_tokens=8000,
        )

        cleaned_response = self._strip_markdown(response)

        analyzed_data = json.loads(
            cleaned_response
        )

        return analyzed_data