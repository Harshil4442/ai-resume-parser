"use client";

import { useState } from "react";
import type { JobMatchResponse } from "../../lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";
export default function JobsPage() {
  const [resumeId, setResumeId] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [jd, setJd] = useState("");
  const [result, setResult] = useState<JobMatchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const payload = {
        user_id: 1,
        resume_id: Number(resumeId),
        job_title: jobTitle,
        company,
        job_description: jd,
      };

      const res = await fetch(`${API_BASE}/job/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.detail || "Match failed");
      setResult(json);
    } catch (err: any) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto py-10 space-y-6">
      <h1 className="text-2xl font-bold">Job Matching</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <input
            className="border rounded px-3 py-2 text-sm"
            placeholder="Resume ID"
            value={resumeId}
            onChange={(e) => setResumeId(e.target.value)}
          />
          <input
            className="border rounded px-3 py-2 text-sm"
            placeholder="Job title"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
          />
        </div>

        <input
          className="border rounded px-3 py-2 text-sm w-full"
          placeholder="Company (optional)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />

        <textarea
          className="border rounded px-3 py-2 text-sm w-full h-44"
          placeholder="Paste job description…"
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />

        <button className="px-4 py-2 rounded bg-black text-white text-sm" disabled={loading}>
          {loading ? "Matching…" : "Compute Match"}
        </button>
      </form>

      {error && <div className="text-sm text-red-600">{error}</div>}
      {result && (
        <div className="border rounded p-4 bg-white space-y-3">
          <div className="text-sm">
            <span className="font-semibold">Match score:</span> {result.match_score.toFixed(1)} / 100
          </div>
          <div>
            <div className="text-sm font-semibold">Missing skills</div>
            <div className="flex flex-wrap gap-2 mt-2">
              {result.missing_skills.map((s) => (
                <span key={s} className="px-2 py-1 rounded bg-red-50 text-xs">{s}</span>
              ))}
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Copy missing skills to the Learning page for a roadmap.
          </div>
        </div>
      )}
    </main>
  );
}
