import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchDashboard, fmtNumber } from "../api.ts";
import InfoTip from "../InfoTip.tsx";
import { SkeletonBlocks, SkeletonCards } from "../Skeleton.tsx";
import { useSettings } from "../settings.tsx";
import type { Dashboard as DashboardData } from "../types.ts";

const PALETA = ["#4f8cff", "#7a6bff", "#2bb673", "#f59e0b", "#ef5da8", "#26c3d6"];

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

interface PropsTip {
  active?: boolean;
  payload?: Array<{ payload: Record<string, string | number | null> }>;
  formatear: (fila: Record<string, string | number | null>) => string;
}

function TipGrafica({ active, payload, formatear }: PropsTip) {
  if (!active || !payload?.length) {
    return null;
  }
  const fila = payload[0].payload;
  return (
    <div className="tip-grafica">
      <b>{String(fila.nombre)}</b>
      <span>{formatear(fila)}</span>
    </div>
  );
}

function ChartCard({ titulo, children }: { titulo: React.ReactNode; children: React.ReactNode }) {
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
  const navegar = useNavigate();

  useEffect(() => {
    fetchDashboard().then(setData).catch((e: unknown) => setError(String(e)));
  }, []);

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;
  if (!data) {
    return (
      <section>
        <h1>Dashboard</h1>
        <SkeletonCards n={4} />
        <SkeletonBlocks n={4} />
      </section>
    );
  }

  const idPorSegmento = new Map(
    data.segments_distribution.map((s, i) => [i, s.segment_id]),
  );
  const irASegmento = (indice: number) => {
    const id = idPorSegmento.get(indice);
    if (id) {
      navegar(`/segments/${id}`);
    }
  };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const alClickBarra: any = (dato: { indice?: number }) => {
    if (dato?.indice !== undefined) {
      irASegmento(dato.indice);
    }
  };

  const distribucion = data.segments_distribution.map((s, i) => ({
    nombre: s.label,
    clientes: s.n_customers,
    indice: i,
  }));
  const gasto = data.segments_profile.map((s, i) => ({
    nombre: s.label,
    gasto: Math.round(s.monetary ?? 0),
    indice: i,
  }));
  const recencia = data.segments_profile.map((s, i) => ({
    nombre: s.label,
    dias: s.recency_days === null ? null : Math.round(s.recency_days),
    indice: i,
  }));
  const categorias = data.top_categories.map((c) => ({
    categoria: c.category,
    compras: c.n,
  }));

  return (
    <section>
      <h1>Dashboard</h1>
      <p className="muted">
        Panorama general: cuántos clientes hay, cómo se distribuyen sus segmentos y cómo compran.
      </p>
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
          <span className="card-label">
            Ticket promedio <InfoTip termino="ticket" />
          </span>
          <span className="card-value">{fmtMoney(data.avg_ticket)}</span>
        </div>
      </div>

      <div className="chart-grid">
        <ChartCard titulo="Clientes por segmento (clic para ver el detalle)">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={distribucion} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis type="number" stroke="var(--texto-suave)" />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip content={<TipGrafica formatear={(f) => `${fmtNumber(Number(f.clientes))} clientes`} />} />
              <Bar
                dataKey="clientes"
                radius={[0, 4, 4, 0]}
                className="barra-clicable"
                onClick={alClickBarra}
              >
                {distribucion.map((_fila, i) => (
                  <Cell key={i} fill={PALETA[i % PALETA.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Gasto promedio por cliente del segmento">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={gasto} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis
                type="number"
                stroke="var(--texto-suave)"
                tickFormatter={(v: number) => `${Math.round(v / 1000)}k`}
              />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip content={<TipGrafica formatear={(f) => fmtMoney(Number(f.gasto))} />} />
              <Bar
                dataKey="gasto"
                radius={[0, 4, 4, 0]}
                className="barra-clicable"
                onClick={alClickBarra}
              >
                {gasto.map((_fila, i) => (
                  <Cell key={i} fill={PALETA[i % PALETA.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo={<>Días desde la última compra (promedio) <InfoTip termino="recencia" /></>}>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={recencia} layout="vertical" margin={{ left: 8, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" horizontal={false} />
              <XAxis type="number" stroke="var(--texto-suave)" />
              <YAxis type="category" dataKey="nombre" width={190} tickLine={false} tick={tickEje} />
              <Tooltip
                content={
                  <TipGrafica
                    formatear={(f) => (f.dias === null ? "Sin compras registradas" : `${f.dias} días en promedio`)}
                  />
                }
              />
              <Bar
                dataKey="dias"
                radius={[0, 4, 4, 0]}
                className="barra-clicable"
                onClick={alClickBarra}
              >
                {recencia.map((_fila, i) => (
                  <Cell key={i} fill={PALETA[i % PALETA.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard titulo="Compras por categoría (top 8)">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={categorias} margin={{ left: 0, right: 8, bottom: 34 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--borde)" vertical={false} />
              <XAxis dataKey="categoria" tick={{ fontSize: 11, fill: "var(--texto-suave)" }} angle={-25} textAnchor="end" />
              <YAxis stroke="var(--texto-suave)" />
              <Tooltip
                content={
                  <TipGrafica
                    formatear={(f) => `${fmtNumber(Number(f.compras))} compras (${f.categoria})`}
                  />
                }
              />
              <Bar dataKey="compras" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </section>
  );
}
