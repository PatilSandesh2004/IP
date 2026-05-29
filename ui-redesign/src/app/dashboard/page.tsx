"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { Badge, Button, Card } from "@/components/ui";
import { getAuth } from "@/lib/auth";

export default function DashboardPage() {
  const [name, setName] = useState<string | null>(null);

  useEffect(() => {
    setName(getAuth()?.name ?? null);
  }, []);

  return (
    <div className="stack">
      <div className="grid-2">
        <Card>
          <Badge>Welcome back</Badge>
          <h2>{name ? `Welcome back, ${name}` : "Welcome back"}</h2>
          <p>Build interview confidence with adaptive practice and targeted learning.</p>
          <div className="grid-2">
            <Link className="btn btn-primary" href="/job-match">Analyze Resume vs JD</Link>
            <Link className="btn btn-secondary" href="/interview">Start Practice</Link>
          </div>
        </Card>

        <Card>
          <h2>Overview</h2>
          <div className="grid-3">
            <div className="card stat-card"><p>Sessions</p><p className="stat-value">3</p></div>
            <div className="card stat-card"><p>Avg Score</p><p className="stat-value">78%</p></div>
            <div className="card stat-card"><p>Jobs</p><p className="stat-value">5</p></div>
          </div>
        </Card>
      </div>

      <div className="grid-2">
        <Card>
          <h2>Recent activity</h2>
          <div className="stack">
            <div className="feedback-card"><strong>Frontend practice</strong><p>5 qs · 82%</p></div>
            <div className="feedback-card"><strong>Zomato SDE-2 match</strong><p>Match: 76%</p></div>
          </div>
        </Card>

        <Card>
          <h2>Quick actions</h2>
          <div className="stack">
            <Link className="btn btn-primary" href="/profile">Open Profile</Link>
            <Link className="btn btn-secondary" href="/job-match">Job Match</Link>
            <Link className="btn btn-secondary" href="/interview">Practice</Link>
          </div>
        </Card>
      </div>
    </div>
  );
}