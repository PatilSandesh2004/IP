import type { Metadata } from "next";
import { DM_Sans, Syne } from "next/font/google";

import { Shell } from "@/components/shell";

import "./globals.css";

const syne = Syne({ subsets: ["latin"], variable: "--font-syne" });
const dmSans = DM_Sans({ subsets: ["latin"], variable: "--font-dm-sans" });

export const metadata: Metadata = {
  title: "InterviewOS Redesign",
  description: "Separate InterviewOS UI for the new design spec"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${syne.variable} ${dmSans.variable}`}>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}