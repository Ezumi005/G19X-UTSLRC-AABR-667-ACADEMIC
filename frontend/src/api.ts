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
export const fetchCustomers = (limit: number, offset: number) =>
  getJson<import("./types.ts").CustomersPage>(`/customers?limit=${limit}&offset=${offset}`);
export const fetchCustomer = (id: string) =>
  getJson<import("./types.ts").CustomerDetail>(`/customers/${encodeURIComponent(id)}`);
export const fetchSegments = () => getJson<import("./types.ts").SegmentsPage>("/segments");
export const fetchSegment = (id: number) =>
  getJson<import("./types.ts").SegmentDetail>(`/segments/${id}`);
export const requestRecommendation = (id: number) =>
  postJson<unknown>(`/segments/${id}/recommendation`);

export const fmtNumber = (n: number | null | undefined, digits = 0): string =>
  n === null || n === undefined ? "—" : new Intl.NumberFormat("es-MX", { maximumFractionDigits: digits }).format(n);

export const fmtDate = (iso: string | null | undefined): string =>
  iso ? new Date(iso).toLocaleString("es-MX", { dateStyle: "medium", timeStyle: "short" }) : "—";
