import { useEffect, useState } from "react";
import { fetchIngestionRuns, fetchRuns, fmtDate, fmtNumber } from "../api.ts";
import InfoTip from "../InfoTip.tsx";
import { SkeletonRows } from "../Skeleton.tsx";
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
      <h2>Historial de ingestión <InfoTip termino="ingesta" /></h2>
      <p className="muted">
        Qué datos entraron y con qué calidad. Se muestra guardados/leídos por tipo de registro.
      </p>
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
            <th>Incidencias <InfoTip termino="incidencias" /></th>
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
  if (!runs) {
    return (
      <section>
        <h1>Ejecuciones</h1>
        <SkeletonRows n={5} columnas={8} />
      </section>
    );
  }

  return (
    <section>
      <h1>Ejecuciones</h1>
      <p className="muted">
        Historial de confianza: qué ejecutó el sistema, cuándo y con qué calidad. Vista de soporte.
      </p>
      <table className="table">
        <thead>
          <tr>
            <th>Run</th>
            <th>Fecha</th>
            <th>Modelo</th>
            <th>k <InfoTip termino="k" /></th>
            <th>Clientes</th>
            <th>Silhouette <InfoTip termino="silhouette" /></th>
            <th>Davies-Bouldin <InfoTip termino="davies" /></th>
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
