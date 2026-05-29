"use client";

import { isAxiosError } from "axios";
import { useEffect, useState } from "react";

import { Alert, Badge, Button, Card, Input, Textarea } from "@/components/ui";
import { ChipInput } from "@/components/chip-input";
import { getAuth } from "@/lib/auth";
import { getCandidateProfile, saveCandidateProfile, type CandidateProfile } from "@/lib/backend";

function safeParseArray(value: string) {
  return value.trim() ? JSON.parse(value) : [];
}

export default function ProfilePage() {
  const auth = getAuth();
  const [ready, setReady] = useState(false);
  const [message, setMessage] = useState<{ tone: "error" | "success"; text: string } | null>(null);
  const [name, setName] = useState("");
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
  const [rawResumeText, setRawResumeText] = useState("");
  const [structuredResumeJson, setStructuredResumeJson] = useState("{}");

  useEffect(() => {
    if (!auth) return;
    setReady(true);
    getCandidateProfile(auth.user_id)
      .then((profile: CandidateProfile) => {
        setName(profile.name ?? auth.name);
        setMobileNumber(profile.mobile_number ?? "");
        setTitle(profile.title ?? "");
        setSummary(profile.summary ?? "");
        setSkills(profile.skills ?? []);
        setKnownLanguages(profile.known_languages ?? []);
        setTools(profile.tools ?? []);
        setFrameworks(profile.frameworks ?? []);
        setCompaniesWorkedAt(profile.companies_worked_at ?? []);
        setCertifications(profile.certifications ?? []);
        setEducation(JSON.stringify(profile.education ?? [], null, 2));
        setExperience(JSON.stringify(profile.experience ?? [], null, 2));
        setProjects(JSON.stringify(profile.projects ?? [], null, 2));
        setRawResumeText(profile.raw_resume_text ?? "");
        setStructuredResumeJson(JSON.stringify(profile.structured_resume_json ?? {}, null, 2));
      })
      .catch(() => setMessage({ tone: "error", text: "No saved profile found yet." }));
  }, [auth]);

  async function handleSave() {
    if (!auth) return;

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
        education: safeParseArray(education),
        experience: safeParseArray(experience),
        projects: safeParseArray(projects),
        raw_resume_text: rawResumeText || undefined,
        structured_resume_json: JSON.parse(structuredResumeJson || "{}")
      });

      setMessage({ tone: "success", text: "Profile saved successfully!" });
      window.setTimeout(() => setMessage(null), 3000);
    } catch (err) {
      const text = isAxiosError(err) ? (typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Save failed.") : "Save failed.";
      setMessage({ tone: "error", text });
    }
  }

  if (!ready) {
    return null;
  }

  return (
    <div className="grid-2">
      <Card>
        <h2>Your Profile</h2>
        {message ? <Alert tone={message.tone}>{message.text}</Alert> : null}
        <div className="stack">
          <div className="field-group"><label className="field-label">Name</label><Input value={name} onChange={(e) => setName(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Mobile</label><Input value={mobileNumber} onChange={(e) => setMobileNumber(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Title</label><Input value={title} onChange={(e) => setTitle(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Summary</label><Textarea value={summary} onChange={(e) => setSummary(e.target.value)} /></div>
          <ChipInput label="Skills" values={skills} onChange={setSkills} />
          <ChipInput label="Known languages" values={knownLanguages} onChange={setKnownLanguages} />
          <ChipInput label="Tools" values={tools} onChange={setTools} />
          <ChipInput label="Frameworks" values={frameworks} onChange={setFrameworks} />
          <ChipInput label="Companies" values={companiesWorkedAt} onChange={setCompaniesWorkedAt} />
          <ChipInput label="Certifications" values={certifications} onChange={setCertifications} />
          <div className="field-group"><label className="field-label">Education JSON</label><Textarea value={education} onChange={(e) => setEducation(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Experience JSON</label><Textarea value={experience} onChange={(e) => setExperience(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Projects JSON</label><Textarea value={projects} onChange={(e) => setProjects(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Raw resume text</label><Textarea value={rawResumeText} onChange={(e) => setRawResumeText(e.target.value)} /></div>
          <div className="field-group"><label className="field-label">Structured resume JSON</label><Textarea value={structuredResumeJson} onChange={(e) => setStructuredResumeJson(e.target.value)} /></div>
          <div className="grid-2">
            <Button type="button" onClick={handleSave}>Save</Button>
            <Button type="button" variant="secondary" onClick={() => window.location.reload()}>Reload</Button>
          </div>
        </div>
      </Card>

      <Card>
        <h2>Profile Summary</h2>
        <p>Use the saved profile as the source of truth for all downstream flows.</p>
        <div className="stack">
          <Badge>Skills: {skills.length}</Badge>
          <Badge>Languages: {knownLanguages.length}</Badge>
          <Badge>Tools: {tools.length}</Badge>
          <Badge>Frameworks: {frameworks.length}</Badge>
          <Badge>Companies: {companiesWorkedAt.length}</Badge>
          <Badge>Certifications: {certifications.length}</Badge>
        </div>
      </Card>
    </div>
  );
}