"use client";

import { isAxiosError } from "axios";
import { Mic2, ArrowRight, RotateCcw } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { Alert, Badge, Button, Card, Input, Textarea } from "@/components/ui";
import api from "@/lib/api";

type StartResponse = {
  session_id: string;
  question: { id?: number; question?: string } | string;
  resume_analysis?: unknown;
};

type AnswerResponse = {
  interview_completed: boolean;
  next_question?: { id?: number; question?: string } | string;
  evaluation?: unknown;
  final_report?: unknown;
  current_question_number?: number;
};

function normalizeQuestion(question: unknown) {
  if (typeof question === "string") return question;
  if (question && typeof question === "object" && "question" in question) return String((question as { question?: string }).question ?? "");
  return "";
}

export default function InterviewPage() {
  const params = useSearchParams();
  const defaultRole = params.get("role") ?? "Backend Engineer";
  const [role, setRole] = useState(defaultRole);
  const [questionsCount] = useState(5);
  const [focusArea, setFocusArea] = useState("All areas");
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);
  const [stage, setStage] = useState<"setup" | "active" | "results">("setup");
  const [currentQuestionNumber, setCurrentQuestionNumber] = useState(1);

  useEffect(() => {
    setRole(defaultRole);
  }, [defaultRole]);

  const questionLabel = useMemo(() => (question ? `Question ${currentQuestionNumber}` : "Question"), [currentQuestionNumber, question]);

  async function startInterview() {
    setError(null);
    try {
      const response = await api.post<StartResponse>("/interview/start", {
        resume_text: resumeText || undefined,
        jd_text: jdText || undefined,
        resume_analysis: undefined
      });
      setSessionId(response.data.session_id);
      setQuestion(normalizeQuestion(response.data.question));
      setStage("active");
      setCurrentQuestionNumber(1);
    } catch (err) {
      const message = isAxiosError(err) ? (typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Interview start failed.") : "Interview start failed.";
      setError(message);
    }
  }

  async function submitAnswer() {
    if (!sessionId) return;
    setError(null);

    try {
      const response = await api.post<AnswerResponse>("/interview/answer", {
        session_id: sessionId,
        answer
      });

      if (response.data.interview_completed) {
        setResult(response.data.final_report ?? response.data);
        setStage("results");
      } else {
        setQuestion(normalizeQuestion(response.data.next_question));
        setCurrentQuestionNumber(response.data.current_question_number ?? currentQuestionNumber + 1);
        setAnswer("");
      }
    } catch (err) {
      const message = isAxiosError(err) ? (typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Answer submit failed.") : "Answer submit failed.";
      setError(message);
    }
  }

  return (
    <div className="stack">
      {error ? <Alert tone="error">{error}</Alert> : null}

      {stage === "setup" ? (
        <div className="grid-2">
          <Card>
            <h2>Interview Setup</h2>
            <div className="stack">
              <div className="field-group"><label className="field-label">Role / Title</label><Input value={role} onChange={(e) => setRole(e.target.value)} /></div>
              <div className="field-group"><label className="field-label">Questions</label><Input value={String(questionsCount)} readOnly /></div>
              <div className="field-group"><label className="field-label">Focus Area</label><Input value={focusArea} onChange={(e) => setFocusArea(e.target.value)} /></div>
              <div className="field-group"><label className="field-label">Resume text</label><Textarea value={resumeText} onChange={(e) => setResumeText(e.target.value)} /></div>
              <div className="field-group"><label className="field-label">Job description</label><Textarea value={jdText} onChange={(e) => setJdText(e.target.value)} /></div>
              <Button onClick={startInterview}><Mic2 size={16} /> Start Interview</Button>
            </div>
          </Card>

          <Card>
            <h2>What this page does</h2>
            <p>The backend will generate questions from the resume/JD context and keep the session state server-side.</p>
            <div className="stack">
              <div className="feedback-card">Continuous mic support can be added on top of the current text flow.</div>
              <div className="feedback-card">Results are shown after the backend ends the interview session.</div>
            </div>
          </Card>
        </div>
      ) : null}

      {stage === "active" ? (
        <div className="grid-2">
          <Card>
            <Badge>Interview in progress</Badge>
            <h2 style={{ marginTop: 12 }}>{role}</h2>
            <p>{questionLabel} of {questionsCount}</p>
            <div className="card stat-card" style={{ marginTop: 18 }}>
              <p>{question}</p>
            </div>
            <div className="field-group" style={{ marginTop: 18 }}>
              <label className="field-label">Your answer</label>
              <Textarea value={answer} onChange={(e) => setAnswer(e.target.value)} />
            </div>
            <div className="grid-2" style={{ marginTop: 18 }}>
              <Button variant="secondary" onClick={() => setAnswer("")}><RotateCcw size={16} /> Reset answer</Button>
              <Button onClick={submitAnswer}><ArrowRight size={16} /> Next</Button>
            </div>
          </Card>

          <Card>
            <h2>Live tips</h2>
            <div className="stack">
              <div className="feedback-card">Keep the answer tight, then add one concrete metric.</div>
              <div className="feedback-card">Use the role title to anchor your example selection.</div>
            </div>
          </Card>
        </div>
      ) : null}

      {stage === "results" ? (
        <Card>
          <h2>Interview Complete</h2>
          <p>The backend completed the session and returned the final report.</p>
          <pre className="card stat-card" style={{ overflowX: "auto", whiteSpace: "pre-wrap" }}>{JSON.stringify(result, null, 2)}</pre>
          <div className="grid-2">
            <Button onClick={() => window.location.reload()}>Again</Button>
            <Button variant="secondary" onClick={() => setStage("setup")}>Jobs</Button>
          </div>
        </Card>
      ) : null}
    </div>
  );
}