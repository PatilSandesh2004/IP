"use client";

import { isAxiosError } from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Alert, Button, Card, Input } from "@/components/ui";
import { getAuth, saveAuth } from "@/lib/auth";
import { signup } from "@/lib/backend";

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState("");
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
      const response = await signup({ name, email, password });
      saveAuth(response);
      router.push("/onboarding");
    } catch (err) {
      if (isAxiosError(err)) {
        setError(typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Create account failed.");
      } else {
        setError("Create account failed.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <Card className="auth-card">
        <p className="logo"><span>Interview</span><span>OS</span></p>
        <p className="muted">Create your account</p>

        <form className="stack" onSubmit={handleSubmit}>
          {error ? <Alert tone="error">{error}</Alert> : null}
          <div className="field-group">
            <label className="field-label">Full Name</label>
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Sandesh Kumar" />
          </div>
          <div className="field-group">
            <label className="field-label">Email</label>
            <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </div>
          <div className="field-group">
            <label className="field-label">Password</label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••••" />
          </div>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Creating..." : "Create Account"}</Button>
          <Link href="/">Back to Login</Link>
        </form>
      </Card>
    </div>
  );
}