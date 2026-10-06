import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchDashboard, fmtNumber, fmtDate } from "../api.ts";
import type { Dashboard as DashboardData } from "../types.ts";

const corto = (texto: string, max = 22) => (texto.length > max ? `${texto.slice(0, max)}…` : texto);

function ChartCard({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <div className="chart-card">
      <h3>{titulo}</h3>
      <div className="chart-body">{children}</div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard().then(setData).catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  const distribucion = data.segments_distribution.map((s) => ({
    nombre: corto(s.label),
    clientes: s.n_customers,
  }));
  const gasto = data.segments_profile.map((s) => ({
    nombre: corto(s.label),
    gasto: Math.round((s.monetary ?? 0) / 1000),
  }));
  const recencia = data.segments_profile.map((s) => ({
    nombre: corto(s.label),
    dias: s.recency_days === null ? null : Math.round(s.recency_days),
  }));
  const categorias = data.top_categories.map((c) => ({
    categoria: corto(c.category, 14),
    compras: c.n,
  }));

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

      <div className="chart-grid">
        <ChartCard titulo="Clientes por segmento">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={distribucion} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" />
              <YAxis type="category" dataKey="nombre" width={150} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="clientes" fill="#4f8cff" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Gasto acumulado promedio por segmento (miles)">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={gasto} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" />
              <YAxis type="category" dataKey="nombre" width={150} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="gasto" fill="#7a6bff" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Días desde la última compra (promedio)">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={recencia} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" />
              <YAxis type="category" dataKey="nombre" width={150} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="dias" fill="#2bb673" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Compras por categoría (top 8)">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={categorias} margin={{ left: 0, right: 8, bottom: 24 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="categoria" tick={{ fontSize: 11 }} angle={-30} textAnchor="end" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="compras" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
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
