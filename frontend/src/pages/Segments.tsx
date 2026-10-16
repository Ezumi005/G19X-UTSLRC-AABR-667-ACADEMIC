import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchSegments, fmtNumber, runSegmentation } from "../api.ts";
import { useFeedback } from "../Feedback.tsx";
import InfoTip from "../InfoTip.tsx";
import { SkeletonCards } from "../Skeleton.tsx";
import type { SegmentsPage } from "../types.ts";
import { RefreshCw } from "lucide-react";

export default function Segments() {
  const [data, setData] = useState<SegmentsPage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recalculando, setRecalculando] = useState(false);
  const { toast } = useFeedback();

  const cargar = () => {
    fetchSegments().then(setData).catch((e: unknown) => setError(String(e)));
  };

  useEffect(cargar, []);

  const recalcular = async () => {
    setRecalculando(true);
    try {
      const resultado = await runSegmentation();
      cargar();
      toast(`Segmentación recalculada (run #${resultado.run_id}) con los datos vigentes.`, "exito");
    } catch (e) {
      toast(`No se pudo recalcular: ${String(e)}`, "error");
    } finally {
      setRecalculando(false);
    }
  };

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) {
    return (
      <section>
        <h1>Segmentos</h1>
        <SkeletonCards n={6} alto={140} />
      </section>
    );
  }

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
          <RefreshCw size={15} className={recalculando ? "girando" : undefined} />
          {recalculando ? "Recalculando…" : "Recalcular segmentos"}
        </button>
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
