import { useEffect, useState } from "react";
import { fetchDashboard, fmtNumber, fmtDate } from "../api.ts";
import type { Dashboard as DashboardData } from "../types.ts";

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard().then(setData).catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  const maxN = Math.max(...data.segments_distribution.map((s) => s.n_customers), 1);

  return (
    <section>
      <h1>Dashboard</h1>
      <div className="cards">
        <div className="card">
          <span className="card-label">Clientes</span>
          <span className="card-value">{fmtNumber(data.total_customers)}</span>
        </div>
        <div className="card">
          <span className="card-label">Transacciones</span>
          <span className="card-value">{fmtNumber(data.total_transactions)}</span>
        </div>
        <div className="card">
          <span className="card-label">Gasto total</span>
          <span className="card-value">{fmtNumber(data.total_spend)}</span>
        </div>
        <div className="card">
          <span className="card-label">Ticket promedio</span>
          <span className="card-value">{fmtNumber(data.avg_ticket, 2)}</span>
        </div>
      </div>

      <h2>Distribución de segmentos</h2>
      {data.segments_distribution.length === 0 && (
        <p className="muted">Sin segmentaciones todavía. Ejecuta el backend y corre una segmentación.</p>
      )}
      <div className="distribution">
        {data.segments_distribution.map((s) => (
          <div key={s.segment_id} className="dist-row">
            <span className="dist-label" title={s.label}>{s.label}</span>
            <div className="dist-bar-track">
              <div className="dist-bar" style={{ width: `${(s.n_customers / maxN) * 100}%` }} />
            </div>
            <span className="dist-n">{fmtNumber(s.n_customers)}</span>
          </div>
        ))}
      </div>

      <h2>Últimas ejecuciones</h2>
      <div className="cards">
        <div className="card">
          <span className="card-label">Última ingesta</span>
          <span className="card-sub">
            {data.last_ingestion
              ? `Run #${data.last_ingestion.run_id} · ${data.last_ingestion.status} · ${fmtDate(data.last_ingestion.finished_at)}`
              : "—"}
          </span>
        </div>
        <div className="card">
          <span className="card-label">Última segmentación</span>
          <span className="card-sub">
            {data.last_segmentation
              ? `Run #${data.last_segmentation.run_id} · k=${data.last_segmentation.k} · ${fmtNumber(data.last_segmentation.n_customers)} clientes · ${fmtDate(data.last_segmentation.started_at)}`
              : "—"}
          </span>
        </div>
      </div>
    </section>
  );
}
