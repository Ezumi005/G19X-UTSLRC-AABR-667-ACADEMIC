import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  audienceExportUrl,
  createAudience,
  deleteAudience,
  fetchAudience,
  fetchAudiences,
  fetchSegments,
  fmtDate,
  fmtNumber,
} from "../api.ts";
import type { Audience, AudienceConditions, AudienceDetail, SegmentsPage } from "../types.ts";

const CATEGORIAS = ["electronica", "hogar", "moda", "deportes", "belleza", "alimentos", "juguetes", "otros"];

const CONDITIONS_LABELS: Record<string, string> = {
  segment: "segmento",
  city: "ciudad contiene",
  min_frequency: "compras ≥",
  min_days_without_purchase: "días sin comprar ≥",
  category: "ha comprado categoría",
};

function resumenCondiciones(cond: AudienceConditions): string {
  const partes = Object.entries(cond)
    .filter(([, v]) => v !== null && v !== undefined && v !== "")
    .map(([k, v]) => `${CONDITIONS_LABELS[k] ?? k}: ${v}`);
  return partes.length ? partes.join(" · ") : "sin condiciones (todos los clientes)";
}

function FormularioCreacion({ onCreated }: { onCreated: () => void }) {
  const [segments, setSegments] = useState<SegmentsPage | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [segment, setSegment] = useState("");
  const [city, setCity] = useState("");
  const [minFrequency, setMinFrequency] = useState("");
  const [minDays, setMinDays] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [creando, setCreando] = useState(false);

  useEffect(() => {
    fetchSegments().then(setSegments).catch(() => {});
  }, []);

  const crear = async () => {
    if (!name.trim()) {
      setError("La audiencia necesita un nombre.");
      return;
    }
    const conditions: AudienceConditions = {
      segment: segment || undefined,
      city: city.trim() || undefined,
      min_frequency: minFrequency ? Number(minFrequency) : undefined,
      min_days_without_purchase: minDays ? Number(minDays) : undefined,
      category: category || undefined,
    };
    setCreando(true);
    try {
      await createAudience({ name: name.trim(), description: description.trim() || undefined, conditions });
      setName("");
      setDescription("");
      setError(null);
      onCreated();
    } catch (e) {
      setError(String(e));
    } finally {
      setCreando(false);
    }
  };

  return (
    <div className="filter-bar audience-form">
      <input placeholder="Nombre de la audiencia*" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Descripción" value={description} onChange={(e) => setDescription(e.target.value)} />
      <select value={segment} onChange={(e) => setSegment(e.target.value)} aria-label="Segmento">
        <option value="">Segmento: cualquiera</option>
        {segments?.data.map((s) => (
          <option key={s.segment_id} value={s.label}>{s.label}</option>
        ))}
      </select>
      <input placeholder="Ciudad contiene…" value={city} onChange={(e) => setCity(e.target.value)} />
      <input type="number" min={0} placeholder="Compras ≥" value={minFrequency} onChange={(e) => setMinFrequency(e.target.value)} />
      <input type="number" min={0} placeholder="Días sin comprar ≥" value={minDays} onChange={(e) => setMinDays(e.target.value)} />
      <select value={category} onChange={(e) => setCategory(e.target.value)} aria-label="Categoría">
        <option value="">Categoría: cualquiera</option>
        {CATEGORIAS.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
      <button onClick={() => void crear()} disabled={creando}>{creando ? "Creando…" : "Crear audiencia"}</button>
      {error && <span className="error">{error}</span>}
    </div>
  );
}

export function AudiencesList() {
  const [data, setData] = useState<Audience[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const cargar = () => {
    fetchAudiences().then((r) => setData(r.data)).catch((e: unknown) => setError(String(e)));
  };
  useEffect(cargar, []);

  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <h1>Audiencias dinámicas</h1>
      <p className="muted">
        Condiciones combinables sobre segmento, ciudad, frecuencia, inactividad y categorías. El tamaño se
        recalcula contra los datos vigentes en cada consulta (RF-19).
      </p>
      <h2>Crear audiencia</h2>
      <FormularioCreacion onCreated={cargar} />
      {data && data.length > 0 && (
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Condiciones</th>
              <th>Clientes</th>
              <th>Creada</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.map((a) => (
              <tr key={a.audience_id}>
                <td><Link to={`/audiences/${a.audience_id}`}>{a.name}</Link></td>
                <td>{resumenCondiciones(a.conditions)}</td>
                <td>{fmtNumber(a.n_customers)}</td>
                <td>{fmtDate(a.created_at)}</td>
                <td>
                  <button
                    className="btn-secondary"
                    onClick={() => {
                      if (window.confirm(`¿Eliminar la audiencia '${a.name}'?`)) {
                        deleteAudience(a.audience_id).then(cargar).catch((e) => window.alert(String(e)));
                      }
                    }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {data && data.length === 0 && <p className="muted">Aún no hay audiencias. Crea la primera arriba.</p>}
    </section>
  );
}

export function AudienceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<AudienceDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAudience(Number(id)).then(setData).catch((e: unknown) => setError(String(e)));
  }, [id]);

  if (error) return <p className="error">{error}</p>;
  if (!data) return <p className="muted">Cargando…</p>;

  return (
    <section>
      <Link to="/audiences" className="back">← Audiencias</Link>
      <h1>{data.name}</h1>
      {data.description && <p className="muted">{data.description}</p>}
      <p>
        <span className="badge">{fmtNumber(data.n_customers)} clientes</span>{" "}
        <span className="muted">· {resumenCondiciones(data.conditions)}</span>
      </p>
      <p>
        <a className="btn-secondary" href={audienceExportUrl(data.audience_id)}>
          Exportar CSV
        </a>
      </p>
      <h2>Miembros (primeros {data.members.length} de {fmtNumber(data.members_total)})</h2>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ciudad</th>
            <th>Segmento</th>
            <th>Compras</th>
            <th>Última compra</th>
          </tr>
        </thead>
        <tbody>
          {data.members.map((m) => (
            <tr key={m.customer_id}>
              <td><Link to={`/customers/${m.customer_id}`}>{m.customer_id}</Link></td>
              <td>{m.city ?? "—"}</td>
              <td>{m.segment_label ?? <span className="muted">—</span>}</td>
              <td>{fmtNumber(m.frequency)}</td>
              <td>{fmtDate(m.last_purchase)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
