import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchCustomer, fmtNumber, fmtDate, predictCustomer } from "../api.ts";
import type { CustomerDetail, Prediction } from "../types.ts";

const FEATURE_LABELS: Record<string, string> = {
  recency_days: "Días desde la última compra",
  frequency: "Compras",
  monetary: "Gasto acumulado",
  avg_ticket: "Ticket promedio",
  web_visits: "Visitas web",
  product_views: "Productos vistos",
  abandoned_carts: "Carritos abandonados",
  emails_opened: "Correos abiertos",
  campaign_click_rate: "Tasa de clic en campañas",
  tenure_days: "Antigüedad (días)",
};

export default function CustomerDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<CustomerDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [prediccion, setPrediccion] = useState<Prediction | null>(null);
  const [prediciendo, setPrediciendo] = useState(false);

  useEffect(() => {
    fetchCustomer(id ?? "").then(setData).catch((e: unknown) => setError(String(e)));
  }, [id]);

  const predecir = async () => {
    setPrediciendo(true);
    try {
      setPrediccion(await predictCustomer(id ?? ""));
    } catch (e) {
      window.alert(`No se pudo predecir: ${String(e)}`);
    } finally {
      setPrediciendo(false);
    }
  };

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  return (
    <section>
      <Link to="/customers" className="back">← Clientes</Link>
      <h1>{data.customer_id}</h1>
      <p className="muted">
        {data.city ?? "—"} · {data.age ?? "—"} años · registrado el {fmtDate(data.registered_at)}
      </p>

      <div className="cards">
        <div className="card">
          <span className="card-label">Compras</span>
          <span className="card-value">{fmtNumber(data.stats.frequency)}</span>
        </div>
        <div className="card">
          <span className="card-label">Gasto total</span>
          <span className="card-value">{fmtNumber(data.stats.monetary, 2)}</span>
        </div>
        <div className="card">
          <span className="card-label">Última compra</span>
          <span className="card-value">{fmtDate(data.stats.last_purchase)}</span>
        </div>
        <div className="card">
          <span className="card-label">Segmento asignado</span>
          <span className="card-value">
            {data.segment ? <span className="badge">{data.segment.label}</span> : "sin asignar"}
          </span>
        </div>
      </div>

      <h2>Predicción de segmento (inferencia en Azure)</h2>
      {prediccion ? (
        <p className="reco-card">
          Cluster <b>{prediccion.cluster}</b> ·{" "}
          <b>{prediccion.segment?.label ?? "sin etiqueta"}</b>{" "}
          <button className="btn-secondary" onClick={() => void predecir()} disabled={prediciendo}>
            Recalcular
          </button>
        </p>
      ) : (
        <button onClick={() => void predecir()} disabled={prediciendo}>
          {prediciendo ? "Consultando Azure…" : "Predecir segmento (Azure)"}
        </button>
      )}

      <h2>Perfil del cliente (features)</h2>
      <table className="table">
        <tbody>
          {Object.entries(data.features ?? {}).map(([key, value]) => (
            <tr key={key}>
              <td>{FEATURE_LABELS[key] ?? key}</td>
              <td className="num">{value === null ? "—" : fmtNumber(value, 2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
