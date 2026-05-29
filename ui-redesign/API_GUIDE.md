# InterviewOS API Guide for the Redesign UI

Use this guide as the UI contract for the separate redesign app.

Backend base URL: `http://localhost:8100`

## Authentication

### `POST /auth/signup`

Create a new account.

Request:

```json
{ "name": "Sandesh", "email": "sandesh@example.com", "password": "password123" }
```

Response:

```json
{ "user_id": 1, "name": "Sandesh", "email": "sandesh@example.com", "access_token": "token" }
```

### `POST /auth/login`

Sign in an existing account.

Request:

```json
{ "email": "sandesh@example.com", "password": "password123" }
```

Response matches signup.

## Candidate Profile

### `GET /candidate/{user_id}`

Load the saved profile for the logged-in user.

Fields returned:

- `name`
- `mobile_number`
- `title`
- `summary`
- `skills`
- `known_languages`
- `tools`
- `frameworks`
- `companies_worked_at`
- `certifications`
- `education`
- `experience`
- `projects`
- `raw_resume_text`
- `structured_resume_json`

### `POST /candidate/create-profile`

Save the editable profile form.
This endpoint can also accept a resume file or pasted resume text and will extract profile details before saving.

Request type:

- `application/json` for manual profile save
- `multipart/form-data` for profile save with resume upload or pasted resume text

Important: send arrays as arrays, not comma strings.

Multipart fields:

- `user_id`
- `name`
- `mobile_number`
- `title`
- `summary`
- `skills`
- `certifications`
- `known_languages`
- `tools`
- `frameworks`
- `companies_worked_at`
- `education`
- `experience`
- `projects`
- `raw_resume_text`
- `structured_resume_json`
- `resume_text_input`
- `resume_file`

## Resume Upload and Ingestion

### `POST /resume/upload-resume`

Use to extract resume text from either a file or pasted text.

Fields:

- `file` optional
- `text_input` optional

### `POST /resume/ingest`

Use to structure and persist the resume for the current user.

Fields:

- `user_id` required
- `file` optional
- `text_input` optional

## Resume vs JD Analysis

### `POST /resume-jd-analysis/analyze`

Compare resume to JD.

Fields:

- `resume_file` optional
- `resume_text_input` optional
- `jd_file` optional
- `jd_text_input` optional

Use one input style per side.

## Recommended UI Flow

1. Signup or login.
2. Store auth response in local storage.
3. Load candidate profile with `GET /candidate/{user_id}`.
4. Edit and save profile with `POST /candidate/create-profile`.
5. If a resume is available, send it through the same create-profile call so the backend can extract details.
6. Run resume vs JD analysis.
