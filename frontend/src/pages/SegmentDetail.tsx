import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchSegment, fmtNumber, fmtDate, requestRecommendation } from "../api.ts";
import type { SegmentDetail } from "../types.ts";

const PROFILE_LABELS: Record<string, string> = {
  recency_days: "Recencia (días)",
  frequency: "Frecuencia",
  monetary: "Gasto acumulado",
  avg_ticket: "Ticket promedio",
  web_visits: "Visitas web",
  product_views: "Productos vistos",
  abandoned_carts: "Carritos abandonados",
  emails_opened: "Correos abiertos",
  campaign_click_rate: "Tasa de clic en campañas",
  tenure_days: "Antigüedad (días)",
};

export default function SegmentDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<SegmentDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recoState, setRecoState] = useState<"idle" | "loading" | "pending" | "error">("idle");
  const [recoMsg, setRecoMsg] = useState("");

  useEffect(() => {
    fetchSegment(Number(id)).then(setData).catch((e: unknown) => setError(String(e)));
  }, [id]);

  const pedirRecomendacion = async () => {
    setRecoState("loading");
    try {
      await requestRecommendation(Number(id));
    } catch (e) {
      const msg = String(e);
      if (msg.includes("Azure OpenAI")) {
        setRecoState("pending");
        setRecoMsg(msg);
      } else {
        setRecoState("error");
        setRecoMsg(msg);
      }
    }
  };

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  return (
    <section>
      <Link to="/segments" className="back">← Segmentos</Link>
      <h1>{data.label}</h1>
      <p className="muted">
        Cluster {data.cluster_id} · Run #{data.run_id} (k={data.k}, {data.run_status}) · {fmtDate(data.started_at)}
      </p>

      <div className="cards">
        <div className="card">
          <span className="card-label">Clientes</span>
          <span className="card-value">{fmtNumber(data.n_customers)}</span>
        </div>
        <div className="card">
          <span className="card-label">Silhouette</span>
          <span className="card-value">{data.metrics?.silhouette ?? "—"}</span>
        </div>
        <div className="card">
          <span className="card-label">Davies-Bouldin</span>
          <span className="card-value">{data.metrics?.davies_bouldin ?? "—"}</span>
        </div>
        <div className="card">
          <span className="card-label">Inertia</span>
          <span className="card-value">{fmtNumber(data.metrics?.inertia ?? null, 1)}</span>
        </div>
      </div>

      <h2>Descripción comercial</h2>
      <p>{data.description}</p>

      <h2>Perfil del segmento (medias)</h2>
      <table className="table">
        <tbody>
          {Object.entries(data.profile).map(([key, value]) => (
            <tr key={key}>
              <td>{PROFILE_LABELS[key] ?? key}</td>
              <td className="num">{value === null ? "—" : fmtNumber(value, 2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Clientes del segmento (vista previa)</h2>
      <ul className="customer-chips">
        {data.customers_preview.map((c) => (
          <li key={c.customer_id} className="chip">{c.customer_id}</li>
        ))}
      </ul>

      <h2>Recomendación comercial (Azure OpenAI)</h2>
      {recoState === "idle" && (
        <div>
          <p className="muted">
            Generará interpretación y recomendaciones del segmento mediante Azure OpenAI
            (segmento completo, no clientes individuales).
          </p>
          <button onClick={() => void pedirRecomendacion()}>Generar recomendación</button>
        </div>
      )}
      {recoState === "loading" && <p className="muted">Solicitando…</p>}
      {recoState === "pending" && <p className="notice">{recoMsg}</p>}
      {recoState === "error" && <p className="error">{recoMsg}</p>}
    </section>
  );
}
