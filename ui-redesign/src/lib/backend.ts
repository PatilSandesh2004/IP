import type { AuthState } from "./auth";
import api from "./api";

export type AuthResponse = AuthState;

export type SignupRequest = {
  name: string;
  email: string;
  password: string;
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type CandidateProfile = {
  id: number;
  user_id: number;
  name?: string;
  mobile_number?: string;
  title?: string;
  summary?: string;
  skills: string[];
  known_languages: string[];
  tools: string[];
  frameworks: string[];
  companies_worked_at: string[];
  certifications: string[];
  education: Array<Record<string, unknown>>;
  experience: Array<Record<string, unknown>>;
  projects: Array<Record<string, unknown>>;
  raw_resume_text?: string;
  structured_resume_json?: Record<string, unknown>;
};

export type CandidateProfilePayload = {
  user_id: number;
  name: string;
  mobile_number?: string;
  title?: string;
  summary?: string;
  skills: string[];
  known_languages: string[];
  tools: string[];
  frameworks: string[];
  companies_worked_at: string[];
  certifications: string[];
  education: Array<Record<string, unknown>>;
  experience: Array<Record<string, unknown>>;
  projects: Array<Record<string, unknown>>;
  raw_resume_text?: string;
  structured_resume_json?: Record<string, unknown>;
  resume_text_input?: string;
};

export type UploadResumeResponse = {
  extracted_text?: string;
};

export type ResumeIngestResponse = {
  message: string;
  candidate_profile_id: number;
};

export type ResumeJdAnalysisResponse = {
  match_score: number;
  ats_score?: number;
  skill_gap_analysis?: string[];
  missing_technologies?: string[];
  recommendations?: string[];
};

export type InterviewQuestion = {
  id: number;
  question: string;
  type?: "behavioral" | "technical";
  difficulty?: "easy" | "medium" | "hard";
};

export type InterviewFeedback = {
  overall_score: number;
  feedback: Array<{
    score: number;
    strength: string;
    improvement: string;
  }>;
};

export async function signup(payload: SignupRequest) {
  const response = await api.post<AuthResponse>("/auth/signup", payload);
  return response.data;
}

export async function login(payload: LoginRequest) {
  const response = await api.post<AuthResponse>("/auth/login", payload);
  return response.data;
}

export async function getCandidateProfile(userId: number) {
  const response = await api.get<CandidateProfile>(`/candidate/${userId}`);
  return response.data;
}

export async function saveCandidateProfile(
  payload: CandidateProfilePayload,
  resumeFile?: File | null
) {
  if (resumeFile || payload.resume_text_input) {
    const formData = new FormData();

    formData.append("user_id", String(payload.user_id));
    formData.append("name", payload.name);

    if (payload.mobile_number) formData.append("mobile_number", payload.mobile_number);
    if (payload.title) formData.append("title", payload.title);
    if (payload.summary) formData.append("summary", payload.summary);
    formData.append("skills", JSON.stringify(payload.skills));
    formData.append("certifications", JSON.stringify(payload.certifications));
    formData.append("known_languages", JSON.stringify(payload.known_languages));
    formData.append("tools", JSON.stringify(payload.tools));
    formData.append("frameworks", JSON.stringify(payload.frameworks));
    formData.append("companies_worked_at", JSON.stringify(payload.companies_worked_at));
    formData.append("education", JSON.stringify(payload.education));
    formData.append("experience", JSON.stringify(payload.experience));
    formData.append("projects", JSON.stringify(payload.projects));

    if (payload.raw_resume_text) formData.append("raw_resume_text", payload.raw_resume_text);
    if (payload.structured_resume_json) formData.append("structured_resume_json", JSON.stringify(payload.structured_resume_json));
    if (payload.resume_text_input) formData.append("resume_text_input", payload.resume_text_input);
    if (resumeFile) formData.append("resume_file", resumeFile);

    const response = await api.post<CandidateProfile>("/candidate/create-profile", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    return response.data;
  }

  const response = await api.post<CandidateProfile>("/candidate/create-profile", payload);
  return response.data;
}

export async function uploadResume(file: File | null, textInput?: string) {
  const formData = new FormData();

  if (file) {
    formData.append("file", file);
  }

  if (textInput) {
    formData.append("text_input", textInput);
  }

  const response = await api.post<UploadResumeResponse>("/resume/upload-resume", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
}

export async function ingestResume(payload: { userId: number; file?: File | null; textInput?: string }) {
  const formData = new FormData();
  formData.append("user_id", String(payload.userId));

  if (payload.file) {
    formData.append("file", payload.file);
  }

  if (payload.textInput) {
    formData.append("text_input", payload.textInput);
  }

  const response = await api.post<ResumeIngestResponse>("/resume/ingest", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
}

export async function analyzeResumeJd(payload: {
  resumeText?: string;
  jdText?: string;
  resumeFile?: File | null;
  jdFile?: File | null;
}) {
  const formData = new FormData();

  if (payload.resumeFile) {
    formData.append("resume_file", payload.resumeFile);
  }
  if (payload.resumeText) {
    formData.append("resume_text_input", payload.resumeText);
  }
  if (payload.jdFile) {
    formData.append("jd_file", payload.jdFile);
  }
  if (payload.jdText) {
    formData.append("jd_text_input", payload.jdText);
  }

  const response = await api.post<ResumeJdAnalysisResponse>("/resume-jd-analysis/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
}