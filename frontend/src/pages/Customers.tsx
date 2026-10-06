import { useCallback, useEffect, useState } from "react";
import {
  fetchCustomer,
  fetchCustomers,
  fetchSegments,
  fmtNumber,
  fmtDate,
  predictCustomer,
} from "../api.ts";
import type {
  CustomerDetail,
  CustomersPage,
  CustomerRow,
  Prediction,
  SegmentsPage,
} from "../types.ts";

const PAGE_SIZE = 50;

export default function Customers() {
  const [page, setPage] = useState<CustomersPage | null>(null);
  const [offset, setOffset] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [detail, setDetail] = useState<Record<string, CustomerDetail>>({});
  const [predicciones, setPredicciones] = useState<Record<string, Prediction>>({});
  const [prediciendo, setPrediciendo] = useState<string | null>(null);
  const [segments, setSegments] = useState<SegmentsPage | null>(null);

  const [filtroSegmento, setFiltroSegmento] = useState("");
  const [filtroCiudad, setFiltroCiudad] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [filtrosActivos, setFiltrosActivos] = useState<{ segment?: string; city?: string; q?: string }>({});

  useEffect(() => {
    fetchSegments().then(setSegments).catch(() => {});
  }, []);

  useEffect(() => {
    setPage(null);
    fetchCustomers(PAGE_SIZE, offset, filtrosActivos)
      .then(setPage)
      .catch((e: unknown) => setError(String(e)));
  }, [offset, filtrosActivos]);

  const toggle = useCallback(async (row: CustomerRow) => {
    if (expanded === row.customer_id) {
      setExpanded(null);
      return;
    }
    setExpanded(row.customer_id);
    if (!detail[row.customer_id]) {
      const d = await fetchCustomer(row.customer_id);
      setDetail((prev) => ({ ...prev, [row.customer_id]: d }));
    }
  }, [expanded, detail]);

  const predecir = async (customer_id: string) => {
    setPrediciendo(customer_id);
    try {
      const p = await predictCustomer(customer_id);
      setPredicciones((prev) => ({ ...prev, [customer_id]: p }));
    } catch (e) {
      window.alert(`No se pudo predecir: ${String(e)}`);
    } finally {
      setPrediciendo(null);
    }
  };

  const aplicarFiltros = () => {
    setOffset(0);
    setFiltrosActivos({
      segment: filtroSegmento || undefined,
      city: filtroCiudad.trim() || undefined,
      q: busqueda.trim() || undefined,
    });
  };

  const limpiarFiltros = () => {
    setFiltroSegmento("");
    setFiltroCiudad("");
    setBusqueda("");
    setOffset(0);
    setFiltrosActivos({});
  };

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;

  return (
    <section>
      <h1>Clientes</h1>
      <p className="muted">
        {page ? `${fmtNumber(page.total)} clientes · segmento del último run` : "Cargando…"}
      </p>

      <div className="filter-bar">
        <select
          value={filtroSegmento}
          onChange={(e) => setFiltroSegmento(e.target.value)}
          aria-label="Filtrar por segmento"
        >
          <option value="">Todos los segmentos</option>
          {segments?.data.map((s) => (
            <option key={s.segment_id} value={s.label}>{s.label}</option>
          ))}
        </select>
        <input
          placeholder="Ciudad contiene…"
          value={filtroCiudad}
          onChange={(e) => setFiltroCiudad(e.target.value)}
        />
        <input
          placeholder="Buscar ID (p. ej. CLI-01)…"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <button className="btn-secondary" onClick={aplicarFiltros}>Filtrar</button>
        <button className="btn-secondary" onClick={limpiarFiltros}>Limpiar</button>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Edad</th>
            <th>Ciudad</th>
            <th>Registro</th>
            <th>Segmento</th>
          </tr>
        </thead>
        <tbody>
          {page?.data.map((row) => (
            <>
              <tr key={row.customer_id} className="clickable" onClick={() => void toggle(row)}>
                <td>{row.customer_id}</td>
                <td>{row.age ?? "—"}</td>
                <td>{row.city ?? "—"}</td>
                <td>{fmtDate(row.registered_at)}</td>
                <td>
                  {row.segment_label ? (
                    <span className="badge">{row.segment_label}</span>
                  ) : (
                    <span className="muted">sin asignar</span>
                  )}
                </td>
              </tr>
              {expanded === row.customer_id && (
                <tr key={`${row.customer_id}-detail`} className="detail-row">
                  <td colSpan={5}>
                    {detail[row.customer_id] ? (
                      <div className="detail-grid">
                        <span>Compras: <b>{fmtNumber(detail[row.customer_id].stats.frequency)}</b></span>
                        <span>Gasto total: <b>{fmtNumber(detail[row.customer_id].stats.monetary, 2)}</b></span>
                        <span>Última compra: <b>{fmtDate(detail[row.customer_id].stats.last_purchase)}</b></span>
                        <span>Categorías: <b>{fmtNumber(detail[row.customer_id].stats.categories_count)}</b></span>
                      </div>
                    ) : (
                      <span className="muted">Cargando detalle…</span>
                    )}
                    <div className="predict-box">
                      {predicciones[row.customer_id] ? (
                        <span>
                          Predicción (Azure):{" "}
                          <b className="badge">
                            Cluster {predicciones[row.customer_id].cluster} · {predicciones[row.customer_id].segment?.label ?? "sin etiqueta"}
                          </b>
                        </span>
                      ) : (
                        <button
                          disabled={prediciendo === row.customer_id}
                          onClick={() => void predecir(row.customer_id)}
                        >
                          {prediciendo === row.customer_id ? "Consultando Azure…" : "Predecir segmento (Azure)"}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
      <div className="pager">
        <button disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}>
          ← Anterior
        </button>
        <span>
          {page ? `Mostrando ${offset + 1}–${offset + page.count} de ${fmtNumber(page.total)}` : "…"}
        </span>
        <button
          disabled={!page || offset + page.count >= page.total}
          onClick={() => setOffset(offset + PAGE_SIZE)}
        >
          Siguiente →
        </button>
      </div>
    </section>
  );
}
