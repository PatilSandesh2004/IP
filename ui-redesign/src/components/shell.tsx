"use client";

import { LayoutDashboard, LogOut, MessageSquare, UserCircle2, FileText, FileSearch, Mic2 } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { clearAuth, getAuth } from "@/lib/auth";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/profile", label: "Profile", icon: UserCircle2 },
  { href: "/job-match", label: "Job Match", icon: FileSearch },
  { href: "/interview", label: "Practice", icon: Mic2 }
];

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const auth = typeof window !== "undefined" ? getAuth() : null;

  if (pathname === "/" || pathname === "/signup" || pathname === "/onboarding") {
    return <>{children}</>;
  }

  const title = pathname === "/job-match" ? "Job Match" : pathname === "/profile" ? "Profile" : pathname === "/interview" ? "Practice" : "Dashboard";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">Interview</div>
          <div className="brand-wordmark"><span>Interview</span><strong>OS</strong></div>
        </div>

        <nav className="nav-stack">
          {navItems.map((item) => {
            const active = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link key={item.href} href={item.href} className={active ? "nav-item active" : "nav-item"}>
                <Icon size={16} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <p className="muted-label">Adaptive coaching</p>
          <p>{auth?.name ? `${auth.name}, your next round will track weak areas.` : "Track weak areas after each practice round."}</p>
        </div>
      </aside>

      <div className="content-shell">
        <header className="topbar">
          <div>
            <p className="eyebrow">AI interview preparation</p>
            <h1>{title}</h1>
          </div>
          <div className="topbar-actions">
            <div className="avatar-circle">{auth?.name?.[0] ?? "S"}</div>
            <div className="topbar-user">
              <strong>{auth?.name ?? "Guest"}</strong>
              <span>{auth?.email ?? "Not signed in"}</span>
            </div>
            <button
              className="icon-button"
              onClick={() => {
                clearAuth();
                router.push("/");
              }}
              type="button"
              aria-label="Logout"
            >
              <LogOut size={16} />
            </button>
          </div>
        </header>

        <main className="page-main">{children}</main>
      </div>
    </div>
  );
}