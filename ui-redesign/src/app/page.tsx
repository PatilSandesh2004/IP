"use client";

import { isAxiosError } from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Alert, Button, Card, Input } from "@/components/ui";
import { getAuth, saveAuth } from "@/lib/auth";
import { login } from "@/lib/backend";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (getAuth()) {
      router.replace("/dashboard");
    }
  }, [router]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const response = await login({ email, password });
      saveAuth(response);
      router.push("/dashboard");
    } catch (err) {
      if (isAxiosError(err)) {
        setError(typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Sign in failed.");
      } else {
        setError("Sign in failed.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <Card className="auth-card">
        <p className="logo"><span>Interview</span><span>OS</span></p>
        <p className="muted">AI-powered interview prep</p>

        <form className="stack" onSubmit={handleSubmit}>
          {error ? <Alert tone="error">{error}</Alert> : null}
          <div className="field-group">
            <label className="field-label">Email</label>
            <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </div>
          <div className="field-group">
            <label className="field-label">Password</label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
          </div>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Signing in..." : "Sign In"}</Button>
          <div className="auth-links">
            <span>or</span>
            <Link href="/signup">Create account</Link>
          </div>
        </form>
      </Card>
    </div>
  );
}