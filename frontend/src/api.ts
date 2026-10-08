const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? "http://127.0.0.1:8000";

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`GET ${path} -> HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function postJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { method: "POST" });
  const body = (await res.json().catch(() => null)) as { detail?: string } | null;
  if (!res.ok) {
    throw new Error(body?.detail ?? `POST ${path} -> HTTP ${res.status}`);
  }
  return body as T;
}

export const fetchDashboard = () => getJson<import("./types.ts").Dashboard>("/dashboard");
export interface CustomerFilters {
  segment?: string;
  city?: string;
  q?: string;
}

export async function fetchCustomers(
  limit: number,
  offset: number,
  filters: CustomerFilters = {},
): Promise<import("./types.ts").CustomersPage> {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (filters.segment) params.set("segment", filters.segment);
  if (filters.city) params.set("city", filters.city);
  if (filters.q) params.set("q", filters.q);
  return getJson(`/customers?${params.toString()}`);
}

export const fetchCustomer = (id: string) =>
  getJson<import("./types.ts").CustomerDetail>(`/customers/${encodeURIComponent(id)}`);
async function postJsonBody<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = (await res.json().catch(() => null)) as { detail?: string } | null;
  if (!res.ok) {
    throw new Error(data?.detail ?? `POST ${path} -> HTTP ${res.status}`);
  }
  return data as T;
}

async function delJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { method: "DELETE" });
  if (!res.ok) {
    const data = (await res.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(data?.detail ?? `DELETE ${path} -> HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const predictCustomer = (id: string) =>
  postJson<import("./types.ts").Prediction>(`/customers/${encodeURIComponent(id)}/predict`);
export const fetchRuns = () =>
  getJson<{ count: number; data: import("./types.ts").SegmentationRun[] }>("/segmentation/runs");
export const fetchIngestionRuns = () =>
  getJson<{ count: number; data: import("./types.ts").IngestionRun[] }>("/ingestion/runs");
export const fetchAudiences = () =>
  getJson<{ count: number; data: import("./types.ts").Audience[] }>("/audiences");
export const fetchAudience = (id: number) =>
  getJson<import("./types.ts").AudienceDetail>(`/audiences/${id}`);
export const createAudience = (payload: {
  name: string;
  description?: string;
  conditions: import("./types.ts").AudienceConditions;
}) => postJsonBody<import("./types.ts").Audience>("/audiences", payload);
export const deleteAudience = (id: number) => delJson<{ deleted: number }>(`/audiences/${id}`);
export const audienceExportUrl = (id: number) => `${API_BASE}/audiences/${id}/export`;
export const fetchSegments = () => getJson<import("./types.ts").SegmentsPage>("/segments");
export const fetchSegment = (id: number) =>
  getJson<import("./types.ts").SegmentDetail>(`/segments/${id}`);
export const fetchRecommendation = (id: number) =>
  getJson<{ recommendation: import("./types.ts").Recommendation | null }>(`/segments/${id}/recommendation`);
export const requestRecommendation = (id: number) =>
  postJson<import("./types.ts").Recommendation>(`/segments/${id}/recommendation`);

export const fmtNumber = (n: number | null | undefined, digits = 0): string =>
  n === null || n === undefined ? "—" : new Intl.NumberFormat("es-MX", { maximumFractionDigits: digits }).format(n);

export const fmtDate = (iso: string | null | undefined): string =>
  iso ? new Date(iso).toLocaleString("es-MX", { dateStyle: "medium", timeStyle: "short" }) : "—";
