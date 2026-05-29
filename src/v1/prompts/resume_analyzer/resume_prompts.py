RESUME_EXTRACTION_PROMPT = """
You are an expert ATS Resume Analyzer.

Analyze the given resume carefully.

Extract the following information.

Return ONLY valid JSON.

Do not add explanations.
Do not add markdown.
Do not add extra text.

Expected JSON format:

{
  "skills": [],
  "frameworks": [],
  "databases": [],
  "cloud": [],
  "tools": [],
  "experience": {
    "years": 0,
    "roles": [],
    "companies": []
  },
  "projects": [],
  "education": [],
  "certifications": []
}

Rules:
- Extract only technical skills
- Remove duplicate skills
- Normalize skill names
- Experience years should be numeric
- Return empty arrays if not found

Resume:
{resume_text}
"""