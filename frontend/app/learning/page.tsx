"use client";

import { useState } from "react";
import { apiPostJson } from "../../lib/api";

type RoadmapItem = {
  id: number;
  title: string;
  url: string;
  skills: string[];
  level: string;
  type: string;
};

export default function LearningPage() {
  const [missing, setMissing] = useState("");
  const [items, setItems] = useState<RoadmapItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setItems([]);
    setLoading(true);

    const skills = missing.split(",").map((s) => s.trim()).filter(Boolean);
    try {
      const res = await apiPostJson<{ roadmap: RoadmapItem[] }>("/recommendations/gaps", skills);
      setItems(res.roadmap || []);
    } catch (err: any) {
      setError(err.message || "Failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto py-10 space-y-6">
      <h1 className="text-2xl font-bold">Learning Path</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <textarea
          className="border rounded px-3 py-2 text-sm w-full h-24"
          placeholder="Comma-separated missing skills (e.g., docker, pytorch, sql)"
          value={missing}
          onChange={(e) => setMissing(e.target.value)}
        />
        <button className="px-4 py-2 rounded bg-black text-white text-sm" disabled={loading}>
          {loading ? "Generating…" : "Generate Roadmap"}
        </button>
      </form>

      {error && <div className="text-sm text-red-600">{error}</div>}
      {items.length > 0 && (
        <div className="space-y-3">
          {items.map((it) => (
            <div key={it.id} className="border rounded p-4 bg-white">
              <div className="font-semibold">{it.title}</div>
              <div className="text-xs text-gray-500 mt-1">
                Level: {it.level} • Type: {it.type}
              </div>
              <div className="text-xs text-gray-600 mt-2">Covers: {it.skills.join(", ")}</div>
              <a className="text-xs text-blue-600 underline mt-2 inline-block" href={it.url} target="_blank">
                Open resource
              </a>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
