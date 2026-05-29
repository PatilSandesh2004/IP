"use client";

import { isAxiosError } from "axios";
import { UploadCloud, Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { ChangeEvent, useState } from "react";

import { Alert, Badge, Button, Card, Input, Textarea } from "@/components/ui";
import { analyzeResumeJd } from "@/lib/backend";
import type { ResumeJdAnalysisResponse } from "@/lib/backend";

function AnalysisPane({ label, mode, setMode, text, setText, file, setFile }: {
  label: string;
  mode: "text" | "file";
  setMode: (mode: "text" | "file") => void;
  text: string;
  setText: (value: string) => void;
  file: File | null;
  setFile: (value: File | null) => void;
}) {
  return (
    <Card>
      <div className="grid gap-4">
        <div>
          <h2>{label}</h2>
          <div className="grid-2" style={{ marginTop: 12 }}>
            <Button variant={mode === "text" ? "primary" : "outline"} onClick={() => setMode("text")}>Paste</Button>
            <Button variant={mode === "file" ? "primary" : "outline"} onClick={() => setMode("file")}>Upload</Button>
          </div>
        </div>
        {mode === "text" ? (
          <Textarea value={text} onChange={(e) => setText(e.target.value)} placeholder={`Paste ${label.toLowerCase()} here...`} />
        ) : (
          <div className="upload-zone">
            <Input type="file" accept=".pdf,.doc,.docx,.txt" onChange={(e: ChangeEvent<HTMLInputElement>) => setFile(e.target.files?.[0] ?? null)} />
            <p>{file ? file.name : `Choose a ${label.toLowerCase()} file`}</p>
          </div>
        )}
      </div>
    </Card>
  );
}

export default function JobMatchPage() {
  const router = useRouter();
  const [resumeMode, setResumeMode] = useState<"text" | "file">("text");
  const [jdMode, setJdMode] = useState<"text" | "file">("text");
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ResumeJdAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    setError(null);
    setLoading(true);

    try {
      const response = await analyzeResumeJd({
        resumeText: resumeMode === "text" ? resumeText : undefined,
        resumeFile: resumeMode === "file" ? resumeFile : null,
        jdText: jdMode === "text" ? jdText : undefined,
        jdFile: jdMode === "file" ? jdFile : null
      });
      setResult(response);
    } catch (err) {
      const message = isAxiosError(err) ? (typeof err.response?.data?.error === "string" ? err.response.data.error : "Analysis failed.") : "Analysis failed.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  const practiceRole = (jdText.split("\n").find(Boolean) ?? "Practice this role").slice(0, 60);

  return (
    <div className="stack">
      {error ? <Alert tone="error">{error}</Alert> : null}

      <div className="grid-2">
        <AnalysisPane label="Resume" mode={resumeMode} setMode={setResumeMode} text={resumeText} setText={setResumeText} file={resumeFile} setFile={setResumeFile} />
        <AnalysisPane label="Job Description" mode={jdMode} setMode={setJdMode} text={jdText} setText={setJdText} file={jdFile} setFile={setJdFile} />
      </div>

      <Card>
        <div className="grid-2">
          <div>
            <h2>Results</h2>
            <p>All fields returned by the analysis endpoint are shown below.</p>
          </div>
          <Button onClick={handleAnalyze} disabled={loading}>{loading ? "Analyzing..." : (<><Search size={16} /> Analyze Match</>)}</Button>
        </div>

        <div className="grid-3" style={{ marginTop: 18 }}>
          <div className="card stat-card"><p>Match</p><p className="stat-value">{result?.match_score ?? 0}%</p></div>
          <div className="card stat-card"><p>ATS</p><p className="stat-value">{result?.ats_score ?? 0}%</p></div>
          <div className="card stat-card"><p>Missing</p><p className="stat-value">{result?.missing_technologies?.length ?? 0}</p></div>
        </div>

        <div className="grid-2" style={{ marginTop: 18 }}>
          <div>
            <h3>Missing technologies</h3>
            <div className="stack">{result?.missing_technologies?.length ? result.missing_technologies.map((item) => <Badge key={item}>{item}</Badge>) : <p className="muted">No missing technologies reported yet.</p>}</div>
          </div>
          <div>
            <h3>Recommendations</h3>
            <div className="stack">{result?.recommendations?.length ? result.recommendations.map((item) => <div key={item} className="feedback-card">{item}</div>) : <p className="muted">Recommendations will appear after analysis.</p>}</div>
          </div>
        </div>

        <Button variant="secondary" onClick={() => router.push(`/interview?role=${encodeURIComponent(practiceRole)}`)} style={{ marginTop: 18 }}>Practice for this role</Button>
      </Card>
    </div>
  );
}