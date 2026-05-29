"use client";

import { isAxiosError } from "axios";
import { Upload, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";

import { Alert, Badge, Button, Card, Input, Textarea } from "@/components/ui";
import { ChipInput } from "@/components/chip-input";
import { getAuth, saveAuth } from "@/lib/auth";
import { getCandidateProfile, saveCandidateProfile, uploadResume } from "@/lib/backend";

function parseJsonArray(value: string) {
  return value.trim() ? JSON.parse(value) : [];
}

function stringify(value: unknown) {
  return JSON.stringify(value ?? {}, null, 2);
}

export default function OnboardingPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [authReady, setAuthReady] = useState(false);
  const auth = getAuth();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [rawResumeText, setRawResumeText] = useState("");
  const [structuredJson, setStructuredJson] = useState("{}");
  const [name, setName] = useState(auth?.name ?? "");
  const [mobileNumber, setMobileNumber] = useState("");
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [skills, setSkills] = useState<string[]>([]);
  const [knownLanguages, setKnownLanguages] = useState<string[]>([]);
  const [tools, setTools] = useState<string[]>([]);
  const [frameworks, setFrameworks] = useState<string[]>([]);
  const [companiesWorkedAt, setCompaniesWorkedAt] = useState<string[]>([]);
  const [certifications, setCertifications] = useState<string[]>([]);
  const [education, setEducation] = useState("[]");
  const [experience, setExperience] = useState("[]");
  const [projects, setProjects] = useState("[]");

  useEffect(() => {
    if (!auth) {
      router.replace("/");
    } else {
      setAuthReady(true);
    }
  }, [auth, router]);

  async function handleResumeUpload() {
    if (!file) {
      setError("Choose a resume file first.");
      return;
    }

    setError(null);
    try {
      const response = await uploadResume(file, rawResumeText.trim() || undefined);
      setRawResumeText(response.extracted_text ?? rawResumeText);
      setSuccess("Resume extracted. Review the fields and save.");
    } catch (err) {
      setError(isAxiosError(err) && typeof err.response?.data?.error === "string" ? err.response.data.error : "Resume upload failed.");
    }
  }

  async function handleSave() {
    if (!auth) {
      return;
    }

    setError(null);
    try {
      await saveCandidateProfile({
        user_id: auth.user_id,
        name,
        mobile_number: mobileNumber || undefined,
        title: title || undefined,
        summary: summary || undefined,
        skills,
        known_languages: knownLanguages,
        tools,
        frameworks,
        companies_worked_at: companiesWorkedAt,
        certifications,
        education: parseJsonArray(education),
        experience: parseJsonArray(experience),
        projects: parseJsonArray(projects),
        raw_resume_text: rawResumeText || undefined,
        structured_resume_json: JSON.parse(structuredJson || "{}"),
        resume_text_input: rawResumeText || undefined
      }, file);

      const refreshed = await getCandidateProfile(auth.user_id);
      saveAuth({ ...auth, name: refreshed.name ?? auth.name });
      setSuccess("Profile saved successfully.");
      router.push("/dashboard");
    } catch (err) {
      const message = isAxiosError(err)
        ? typeof err.response?.data?.detail === "string"
          ? err.response.data.detail
          : typeof err.response?.data?.error === "string"
            ? err.response.data.error
            : "Save failed."
        : "Save failed.";
      setError(message);
    }
  }

  const completion = useMemo(() => {
    const fields = [name, mobileNumber, title, summary, rawResumeText, structuredJson];
    return Math.round((fields.filter(Boolean).length / fields.length) * 100);
  }, [name, mobileNumber, title, summary, rawResumeText, structuredJson]);

  if (!authReady) {
    return null;
  }

  return (
    <div className="stack">
      {error ? <Alert tone="error">{error}</Alert> : null}
      {success ? <Alert tone="success">{success}</Alert> : null}

      <div className="grid-2">
        <Card>
          <h2>Build your profile</h2>
          <p>Upload a resume or fill manually. The backend schema stays the source of truth.</p>

          <div className="stack">
            <div className="field-group">
              <label className="field-label">Name</label>
              <Input value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="field-group">
              <label className="field-label">Mobile</label>
              <Input value={mobileNumber} onChange={(e) => setMobileNumber(e.target.value)} />
            </div>
            <div className="field-group">
              <label className="field-label">Title</label>
              <Input value={title} onChange={(e) => setTitle(e.target.value)} />
            </div>
            <div className="field-group">
              <label className="field-label">Summary</label>
              <Textarea value={summary} onChange={(e) => setSummary(e.target.value)} />
            </div>

            <ChipInput label="Skills" values={skills} onChange={setSkills} placeholder="Press Enter to add" />
            <ChipInput label="Known languages" values={knownLanguages} onChange={setKnownLanguages} placeholder="English, Hindi" />
            <ChipInput label="Tools" values={tools} onChange={setTools} />
            <ChipInput label="Frameworks" values={frameworks} onChange={setFrameworks} />
            <ChipInput label="Companies worked at" values={companiesWorkedAt} onChange={setCompaniesWorkedAt} />
            <ChipInput label="Certifications" values={certifications} onChange={setCertifications} />

            <div className="field-group">
              <label className="field-label">Education JSON</label>
              <Textarea value={education} onChange={(e) => setEducation(e.target.value)} placeholder='[{"degree":"B.Tech"}]' />
            </div>
            <div className="field-group">
              <label className="field-label">Experience JSON</label>
              <Textarea value={experience} onChange={(e) => setExperience(e.target.value)} placeholder='[{"company":"..."}]' />
            </div>
            <div className="field-group">
              <label className="field-label">Projects JSON</label>
              <Textarea value={projects} onChange={(e) => setProjects(e.target.value)} placeholder='[{"name":"..."}]' />
            </div>
            <div className="field-group">
              <label className="field-label">Structured resume JSON</label>
              <Textarea value={structuredJson} onChange={(e) => setStructuredJson(e.target.value)} placeholder="{}" />
            </div>

            <div className="grid-2">
              <Button type="button" variant="secondary" onClick={() => fileInputRef.current?.click()}>
                <Upload size={16} /> Upload resume
              </Button>
              <Button type="button" onClick={handleSave}>
                Save & Go <ArrowRight size={16} />
              </Button>
            </div>
            <p className="muted">Profile completion: {completion}%</p>
          </div>
        </Card>

        <Card>
          <h2>Resume upload</h2>
          <p>Upload PDF, DOCX, or TXT. The backend extracts text and structures it for this user.</p>

          <div className="upload-zone" onClick={() => fileInputRef.current?.click()} onDragOver={(e) => e.preventDefault()} onDrop={(e) => {
            e.preventDefault();
            const nextFile = e.dataTransfer.files?.[0] ?? null;
            setFile(nextFile);
          }}>
            <input ref={fileInputRef} type="file" accept=".pdf,.doc,.docx,.txt" hidden onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
            <p><strong>Drop or browse your resume</strong></p>
            <p>{file ? file.name : "Click to choose a file"}</p>
            <Button type="button" variant="outline" onClick={(e) => { e.stopPropagation(); handleResumeUpload(); }}>Preview extraction</Button>
          </div>

          <div className="field-group">
            <label className="field-label">Raw resume text</label>
            <Textarea value={rawResumeText} onChange={(e) => setRawResumeText(e.target.value)} />
          </div>

          <div className="stack">
            <Badge>Use /resume/upload-resume for preview text</Badge>
            <Badge>Use /resume/ingest to save the structured profile</Badge>
          </div>
        </Card>
      </div>
    </div>
  );
}