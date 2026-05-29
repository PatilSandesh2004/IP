CANDIDATE_PROFILE_EXTRACTION_PROMPT = """
You are an advanced AI Resume Structuring System.

Your task is to extract structured candidate information
from the provided resume text.

==================================================
IMPORTANT EXTRACTION RULES
==================================================

- Extract ONLY information present in resume
- Do NOT hallucinate information
- Do NOT generate fake skills
- Do NOT generate fake experience
- Do NOT assume technologies
- Missing fields should return:
  - empty list []
  - or null

==================================================
FIELDS TO EXTRACT
==================================================

Extract:

- mobile_number
- title
- summary
- skills
- certifications
- known_languages
- tools
- frameworks
- companies_worked_at
- education
- experience
- projects

==================================================
IMPORTANT EXTRACTION BEHAVIOR
==================================================

Skills:
- include technical skills only

Frameworks:
- FastAPI
- Django
- Flask
- TensorFlow
- PyTorch
etc.

Tools:
- Docker
- Git
- Jenkins
- Kubernetes
etc.

Known Languages:
- Python
- Java
- C++
- SQL
etc.

Projects:
Extract:
- title
- description
- technologies_used

Experience:
Extract:
- company_name
- role
- duration
- responsibilities

Education:
Extract:
- degree
- institution
- year

==================================================
OUTPUT RULES
==================================================

Return ONLY valid JSON.

Do NOT:
- generate markdown
- generate explanations
- generate extra text

==================================================
EXPECTED JSON FORMAT
==================================================

{{
  "mobile_number": "",
  "title": "",
  "summary": "",
  "skills": [],
  "certifications": [],
  "known_languages": [],
  "tools": [],
  "frameworks": [],
  "companies_worked_at": [],
  "education": [],
  "experience": [],
  "projects": []
}}

==================================================
RESUME TEXT
==================================================

{resume_text}
"""