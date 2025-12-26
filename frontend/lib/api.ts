const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";
if (!API_BASE) {
  console.warn("NEXT_PUBLIC_API_BASE_URL is not set. Add it to .env.local");
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return (await res.json()) as T;
}

export async function apiPostJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = (data?.detail || data?.error || "Request failed") as string;
    throw new Error(msg);
  }
  return data as T;
}
