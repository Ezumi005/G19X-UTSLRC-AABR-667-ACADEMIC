import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchSegments, fmtNumber, runSegmentation } from "../api.ts";
import InfoTip from "../InfoTip.tsx";
import type { SegmentsPage } from "../types.ts";

export default function Segments() {
  const [data, setData] = useState<SegmentsPage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recalculando, setRecalculando] = useState(false);
  const [aviso, setAviso] = useState<string | null>(null);

  const cargar = () => {
    fetchSegments().then(setData).catch((e: unknown) => setError(String(e)));
  };

  useEffect(cargar, []);

  const recalcular = async () => {
    setRecalculando(true);
    setAviso(null);
    try {
      await runSegmentation();
      cargar();
      setAviso("Segmentación recalculada con los datos vigentes.");
    } catch (e) {
      window.alert(`No se pudo recalcular la segmentación: ${String(e)}`);
    } finally {
      setRecalculando(false);
    }
  };

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  const total = data.data.reduce((acc, s) => acc + s.n_customers, 0);

  return (
    <section>
      <h1>Segmentos</h1>
      <p className="muted">
        Grupos descubiertos automáticamente por el modelo <InfoTip termino="cluster" /> con su
        estrategia comercial. {data.run_id ? `${data.count} segmentos · ${fmtNumber(total)} clientes asignados.` : "Aún no hay segmentaciones."}
      </p>
      <div className="actions-bar">
        <button onClick={() => void recalcular()} disabled={recalculando}>
          {recalculando ? "Recalculando…" : "Recalcular segmentos"}
        </button>
        {aviso && <span className="notice">{aviso}</span>}
      </div>
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
