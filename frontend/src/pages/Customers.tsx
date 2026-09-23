import { useCallback, useEffect, useState } from "react";
import { fetchCustomer, fetchCustomers, fmtNumber, fmtDate } from "../api.ts";
import type { CustomerDetail, CustomersPage, CustomerRow } from "../types.ts";

const PAGE_SIZE = 50;

export default function Customers() {
  const [page, setPage] = useState<CustomersPage | null>(null);
  const [offset, setOffset] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [detail, setDetail] = useState<Record<string, CustomerDetail>>({});

  useEffect(() => {
    setPage(null);
    fetchCustomers(PAGE_SIZE, offset)
      .then(setPage)
      .catch((e: unknown) => setError(String(e)));
  }, [offset]);

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

  if (error) return <p className="error">No se pudo conectar con el backend: {error}</p>;

  return (
    <section>
      <h1>Clientes</h1>
      <p className="muted">{page ? `${fmtNumber(page.total)} clientes · segmento del último run` : "Cargando…"}</p>
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
