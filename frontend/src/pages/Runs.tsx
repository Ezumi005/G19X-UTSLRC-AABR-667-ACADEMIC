import { useEffect, useState } from "react";
import { fetchRuns, fmtDate, fmtNumber } from "../api.ts";
import type { SegmentationRun } from "../types.ts";

export default function Runs() {
  const [runs, setRuns] = useState<SegmentationRun[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRuns()
      .then((r) => setRuns(r.data))
      .catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!runs) return <p className="muted">Cargando…</p>;

  return (
    <section>
      <h1>Ejecuciones de segmentación</h1>
      <p className="muted">Historial con trazabilidad: cada corrida conserva sus métricas (PRD §19/§30).</p>
      <table className="table">
        <thead>
          <tr>
            <th>Run</th>
            <th>Fecha</th>
            <th>Modelo</th>
            <th>k</th>
            <th>Clientes</th>
            <th>Silhouette</th>
            <th>Davies-Bouldin</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.run_id}>
              <td>#{run.run_id}</td>
              <td>{fmtDate(run.started_at)}</td>
              <td>{run.model_name}</td>
              <td>{run.k}</td>
              <td>{fmtNumber(run.n_customers)}</td>
              <td>{run.metrics?.silhouette ?? "—"}</td>
              <td>{run.metrics?.davies_bouldin ?? "—"}</td>
              <td>
                <span className={run.status === "ok" ? "badge" : "badge badge-warn"}>{run.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
