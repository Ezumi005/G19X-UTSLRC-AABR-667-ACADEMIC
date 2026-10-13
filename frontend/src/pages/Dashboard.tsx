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
import { fetchDashboard, fmtNumber } from "../api.ts";
import { useSettings } from "../settings.tsx";
import type { Dashboard as DashboardData } from "../types.ts";

function envolver(texto: string, ancho = 20): string[] {
  const palabras = texto.split(" ");
  const lineas: string[] = [];
  let actual = "";
  for (const palabra of palabras) {
    if (actual && (actual + " " + palabra).length > ancho) {
      lineas.push(actual);
      actual = palabra;
    } else {
      actual = actual ? `${actual} ${palabra}` : palabra;
    }
  }
  if (actual) lineas.push(actual);
  return lineas;
}

type PropsTick = { x?: number; y?: number; payload?: { value?: string } };

function EtiquetaEje({ x = 0, y = 0, payload }: PropsTick) {
  const lineas = envolver(payload?.value ?? "");
  return (
    <g transform={`translate(${x},${y})`}>
      {lineas.map((linea, i) => (
        <text
          key={i}
          x={0}
          y={(i - (lineas.length - 1) / 2) * 13}
          textAnchor="end"
          fill="var(--texto-suave)"
          fontSize={11.5}
        >
          {linea}
        </text>
      ))}
    </g>
  );
}

const tickEje = (props: unknown) => EtiquetaEje(props as PropsTick);

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
  const { fmtMoney } = useSettings();

  useEffect(() => {
    fetchDashboard().then(setData).catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) return <p className="muted">Cargandoâ€¦</p>;

  const distribucion = data.segments_distribution.map((s) => ({ nombre: s.label, clientes: s.n_customers }));
  const gasto = data.segments_profile.map((s) => ({
    nombre: s.label,
    gasto: Math.round((s.monetary ?? 0) / 1000),
  }));
  const recencia = data.segments_profile.map((s) => ({
    nombre: s.label,
    dias: s.recency_days === null ? null : Math.round(s.recency_days),
  }));
  const categorias = data.top_categories.map((c) => ({ categoria: c.category, compras: c.n }));

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
          <span className="card-value">{fmtMoney(data.total_spend)}</span>
        </div>
        <div className="card">
          <span className="card-label">Ticket promedio</span>
          <span className="card-value">{fmtMoney(data.avg_ticket)}</span>
        </div>
      </div>

      <div className="chart-grid">
        <ChartCard titulo="Clientes por segmento">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={distribucion} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis type="number" stroke="var(--texto-suave)" />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip />
              <Bar dataKey="clientes" fill="#4f8cff" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Gasto acumulado promedio por segmento (miles)">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={gasto} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis type="number" stroke="var(--texto-suave)" />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip />
              <Bar dataKey="gasto" fill="#7a6bff" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="DÃ­as desde la Ãºltima compra (promedio)">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={recencia} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis type="number" stroke="var(--texto-suave)" />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip />
              <Bar dataKey="dias" fill="#2bb673" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Compras por categorÃ­a (top 8)">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={categorias} margin={{ left: 0, right: 8, bottom: 34 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" vertical={false} />
              <XAxis dataKey="categoria" tick={{ fontSize: 11, fill: "var(--texto-suave)" }} angle={-25} textAnchor="end" />
              <YAxis stroke="var(--texto-suave)" />
              <Tooltip />
              <Bar dataKey="compras" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </section>
  );
}

