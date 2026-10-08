import { useEffect, useState } from "react";
import { fetchIngestionRuns, fetchRuns, fmtDate, fmtNumber } from "../api.ts";
import type { IngestionRun, SegmentationRun } from "../types.ts";

const duracion = (inicio: string, fin: string | null): string => {
  if (!fin) return "—";
  const segundos = (new Date(fin).getTime() - new Date(inicio).getTime()) / 1000;
  return `${segundos.toFixed(1)} s`;
};

function IngestionHistory() {
  const [runs, setRuns] = useState<IngestionRun[] | null>(null);
  useEffect(() => {
    fetchIngestionRuns().then((r) => setRuns(r.data)).catch(() => {});
  }, []);
  if (!runs) return null;
  return (
    <>
      <h2>Historial de ingestión</h2>
      <p className="muted">Trazabilidad y calidad por ejecución (PRD §31): leídos/guardados e incidencias.</p>
      <table className="table">
        <thead>
          <tr>
            <th>Run</th>
            <th>Fecha</th>
            <th>Duración</th>
            <th>Clientes</th>
            <th>Transacciones</th>
            <th>Interacciones</th>
            <th>Eventos</th>
            <th>Incidencias</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.run_id}>
              <td>#{run.run_id}</td>
              <td>{fmtDate(run.started_at)}</td>
              <td>{duracion(run.started_at, run.finished_at)}</td>
              <td>{run.customers_saved}/{run.customers_read}</td>
              <td>{fmtNumber(run.transactions_saved)}/{fmtNumber(run.transactions_read)}</td>
              <td>{fmtNumber(run.interactions_saved)}/{fmtNumber(run.interactions_read)}</td>
              <td>{fmtNumber(run.campaign_events_saved)}/{fmtNumber(run.campaign_events_read)}</td>
              <td>{run.incidents}</td>
              <td>
                <span className={run.status === "ok" ? "badge" : "badge badge-warn"}>{run.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

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
      <IngestionHistory />
    </section>
  );
}
