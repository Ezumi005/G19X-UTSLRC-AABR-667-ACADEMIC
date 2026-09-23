import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchSegments, fmtNumber } from "../api.ts";
import type { SegmentsPage } from "../types.ts";

export default function Segments() {
  const [data, setData] = useState<SegmentsPage | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSegments().then(setData).catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  const total = data.data.reduce((acc, s) => acc + s.n_customers, 0);

  return (
    <section>
      <h1>Segmentos</h1>
      <p className="muted">
        {data.run_id
          ? `Run #${data.run_id} · ${data.count} segmentos · ${fmtNumber(total)} clientes asignados`
          : "Aún no hay segmentaciones."}
      </p>
      <div className="segment-grid">
        {data.data.map((s) => (
          <Link key={s.segment_id} to={`/segments/${s.segment_id}`} className="segment-card">
            <div className="segment-head">
              <span className="badge">{s.label}</span>
              <span className="cluster-tag">Cluster {s.cluster_id}</span>
            </div>
            <div className="segment-n">
              <b>{fmtNumber(s.n_customers)}</b> clientes
              <span className="share"> · {total > 0 ? ((s.n_customers / total) * 100).toFixed(1) : 0}%</span>
            </div>
            <p className="segment-desc">{s.description}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
