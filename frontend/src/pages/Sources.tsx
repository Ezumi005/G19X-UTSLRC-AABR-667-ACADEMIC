import { useEffect, useRef, useState } from "react";
import {
  CheckCircle2,
  CloudUpload,
  FileSpreadsheet,
  RefreshCw,
  Sparkles,
  Trash2,
  Wand2,
} from "lucide-react";
import {
  createCsvSource,
  deleteSource,
  fetchEntitySchema,
  fetchSources,
  fmtDate,
  suggestCsvMapping,
  syncSource,
  uploadSourceCsv,
  validateCsvMapping,
} from "../api.ts";
import { useFeedback } from "../Feedback.tsx";
import InfoTip from "../InfoTip.tsx";
import { SkeletonRows } from "../Skeleton.tsx";
import type { DataSourceItem, Suggestion, UploadResult, ValidationSummary } from "../types.ts";

const ENTIDADES: { id: string; label: string }[] = [
  { id: "customers", label: "Clientes" },
  { id: "transactions", label: "Transacciones (compras)" },
  { id: "interactions", label: "Interacciones (web)" },
  { id: "campaign_events", label: "Eventos de campaña" },
];

const etiquetaEntidad = (id: string) => ENTIDADES.find((e) => e.id === id)?.label ?? id;
function Wizard({ onCreada }: { onCreada: () => void }) {
  const { toast } = useFeedback();
  const inputArchivo = useRef<HTMLInputElement>(null);

  const [paso, setPaso] = useState<1 | 2 | 3>(1);
  const [subida, setSubida] = useState<UploadResult | null>(null);
  const [nombre, setNombre] = useState("");
  const [entidad, setEntidad] = useState("customers");
  const [campos, setCampos] = useState<Record<string, boolean>>({});
  const [mapeo, setMapeo] = useState<Record<string, string>>({});
  const [sugerencia, setSugerencia] = useState<Suggestion | null>(null);
  const [sugiriendo, setSugiriendo] = useState(false);
  const [validacion, setValidacion] = useState<ValidationSummary | null>(null);
  const [validando, setValidando] = useState(false);
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    fetchEntitySchema(entidad)
      .then((r) => {
        setCampos(r.fields);
        setMapeo((prev) => {
          const nuevo: Record<string, string> = {};
          for (const campo of Object.keys(r.fields)) {
            nuevo[campo] = prev[campo] ?? "";
          }
          return nuevo;
        });
      })
      .catch(() => {});
  }, [entidad]);

  const subir = async (archivo: File) => {
    try {
      const resultado = await uploadSourceCsv(archivo);
      setSubida(resultado);
      setNombre(archivo.name.replace(/\.csv$/i, ""));
      setValidacion(null);
      setSugerencia(null);
      setPaso(2);
      toast(`Archivo listo: ${resultado.columns.length} columnas detectadas.`, "exito");
      void sugerir(resultado.upload_token);
    } catch (e) {
      toast(`No se pudo subir el archivo: ${String(e)}`, "error");
    }
  };

  const sugerir = async (token: string) => {
    setSugiriendo(true);
    try {
      const s = await suggestCsvMapping(token);
      setSugerencia(s);
      setEntidad(s.entity);
      setMapeo((prev) => {
        const nuevo: Record<string, string> = { ...prev };
        for (const [campo, columna] of Object.entries(s.mapping)) {
          nuevo[campo] = columna;
        }
        return nuevo;
      });
      toast("Mapeo sugerido por IA: revísalo y ajusta lo que quieras.", "info");
    } catch (e) {
      toast(`Sugerencia IA no disponible (${String(e)}); mapea manualmente.`, "info");
    } finally {
      setSugiriendo(false);
    }
  };

  const validar = async () => {
    if (!subida) return;
    setValidando(true);
    try {
      const resumen = await validateCsvMapping({
        name: nombre.trim() || subida.filename,
        entity: entidad,
        upload_token: subida.upload_token,
        mapping: mapeo,
      });
      setValidacion(resumen);
      setPaso(3);
    } catch (e) {
      toast(`Validación fallida: ${String(e)}`, "error");
    } finally {
      setValidando(false);
    }
  };

  const guardar = async (sincronizar: boolean) => {
    if (!subida) return;
    setGuardando(true);
    try {
      const creada = await createCsvSource({
        name: nombre.trim() || subida.filename,
        entity: entidad,
        upload_token: subida.upload_token,
        mapping: mapeo,
      });
      if (sincronizar) {
        await syncSource(creada.source_id);
        toast(`Fuente '${creada.name}' creada y sincronizada.`, "exito");
      } else {
        toast(`Fuente '${creada.name}' creada. Sincronízala cuando quieras.`, "exito");
      }
      reiniciar();
      onCreada();
    } catch (e) {
      toast(`No se pudo guardar: ${String(e)}`, "error");
    } finally {
      setGuardando(false);
    }
  };

  const reiniciar = () => {
    setPaso(1);
    setSubida(null);
    setSugerencia(null);
    setValidacion(null);
    setMapeo({});
    setEntidad("customers");
    if (inputArchivo.current) {
      inputArchivo.current.value = "";
    }
  };

  return (
    <div className="chart-card wizard">
      <h3>Nueva fuente CSV {paso > 1 && <span className="muted">· paso {paso} de 3</span>}</h3>

      {paso === 1 && (
        <div className="wizard-subir">
          <p className="muted">
            Sube un archivo .csv con cualquier estructura: la IA sugerirá a qué entidad del
            contrato corresponde y cómo mapear cada columna. Tú confirmas.
          </p>
          <input
            ref={inputArchivo}
            type="file"
            accept=".csv"
            onChange={(e) => {
              const archivo = e.target.files?.[0];
              if (archivo) {
                void subir(archivo);
              }
            }}
          />
        </div>
      )}

      {paso >= 2 && subida && (
        <>
          <div className="wizard-cabecera">
            <span className="badge">
              <FileSpreadsheet size={13} /> {subida.filename}
            </span>
            {sugerencia && (
              <span className="badge">
                <Wand2 size={13} /> Sugerido por IA{sugerencia.confidence !== null ? ` (${sugerencia.confidence}%)` : ""} — revisa y confirma
              </span>
            )}
            <button className="btn-secondary" onClick={reiniciar}>Cambiar archivo</button>
          </div>
          {sugiriendo && <p className="muted">Consultando a la IA por el mejor mapeo…</p>}
          {sugerencia?.notes && <p className="muted">Notas de la IA: {sugerencia.notes}</p>}

          <div className="filter-bar">
            <label>
              Nombre de la fuente{" "}
              <input value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Mis clientes" />
            </label>
            <label>
              Entidad del contrato{" "}
              <select value={entidad} onChange={(e) => setEntidad(e.target.value)}>
                {ENTIDADES.map((e) => (
                  <option key={e.id} value={e.id}>{e.label}</option>
                ))}
              </select>
            </label>
          </div>

          <table className="table">
            <thead>
              <tr>
                <th>Campo del contrato</th>
                <th>Obligatorio</th>
                <th>Columna del CSV</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(campos).map(([campo, obligatorio]) => (
                <tr key={campo}>
                  <td>{campo}</td>
                  <td>{obligatorio ? "Sí" : "—"}</td>
                  <td>
                    <select
                      value={mapeo[campo] ?? ""}
                      onChange={(e) => setMapeo((prev) => ({ ...prev, [campo]: e.target.value }))}
                    >
                      <option value="">— sin asignar —</option>
                      {subida.columns.map((col) => (
                        <option key={col} value={col}>{col}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="actions-bar">
            <button onClick={() => void validar()} disabled={validando}>
              <CheckCircle2 size={15} />
              {validando ? "Validando…" : "Validar mapeo"}
            </button>
          </div>
        </>
      )}

      {paso === 3 && validacion && (
        <div className="wizard-resultado">
          <div className="cards">
            <div className="card">
              <span className="card-label">Filas leídas</span>
              <span className="card-value">{validacion.read}</span>
            </div>
            <div className="card">
              <span className="card-label">Válidas</span>
              <span className="card-value">{validacion.accepted}</span>
            </div>
            <div className="card">
              <span className="card-label">Con incidencias</span>
              <span className="card-value">{validacion.rejected}</span>
            </div>
          </div>
          {validacion.incidents.length > 0 && (
            <div className="notice">
              Primeras incidencias (se excluyen sin romper la carga):
              <ul className="reco-list">
                {validacion.incidents.map((incidente, i) => (
                  <li key={i}>{incidente}</li>
                ))}
              </ul>
            </div>
          )}
          {validacion.preview.length > 0 && (
            <>
              <p className="muted">Vista previa de las primeras filas ya adaptadas al contrato:</p>
              <table className="table">
                <thead>
                  <tr>
                    {Object.keys(validacion.preview[0]).map((clave) => (
                      <th key={clave}>{clave}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {validacion.preview.map((fila, i) => (
                    <tr key={i}>
                      {Object.values(fila).map((valor, j) => (
                        <td key={j}>{String(valor ?? "—")}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
          <div className="actions-bar">
            <button className="btn-secondary" onClick={() => setPaso(2)}>Ajustar mapeo</button>
            <button onClick={() => void guardar(false)} disabled={guardando}>Guardar sin sincronizar</button>
            <button onClick={() => void guardar(true)} disabled={guardando}>
              <CloudUpload size={15} />
              {guardando ? "Procesando…" : "Guardar y sincronizar"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default function Sources() {
  const [data, setData] = useState<DataSourceItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sincronizando, setSincronizando] = useState<number | null>(null);
  const { toast, confirmar } = useFeedback();

  const cargar = () => {
    fetchSources().then((r) => setData(r.data)).catch((e: unknown) => setError(String(e)));
  };
  useEffect(cargar, []);

  const sincronizar = async (fuente: DataSourceItem) => {
    setSincronizando(fuente.source_id);
    try {
      await syncSource(fuente.source_id);
      toast(`Fuente '${fuente.name}' sincronizada.`, "exito");
      cargar();
    } catch (e) {
      toast(`No se pudo sincronizar: ${String(e)}`, "error");
    } finally {
      setSincronizando(null);
    }
  };

  const eliminar = async (fuente: DataSourceItem) => {
    const ok = await confirmar(
      "Eliminar fuente",
      `¿Eliminar la fuente '${fuente.name}'? Los datos ya sincronizados se conservan.`,
    );
    if (!ok) return;
    try {
      await deleteSource(fuente.source_id);
      toast(`Fuente '${fuente.name}' eliminada.`, "exito");
      cargar();
    } catch (e) {
      toast(`No se pudo eliminar: ${String(e)}`, "error");
    }
  };

  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <h1>Fuentes de datos</h1>
      <p className="muted">
        Conecta datos de cualquier origen: sube un CSV y la IA sugiere el mapeo al
        contrato <InfoTip termino="contrato" /> interno; tú confirmas y sincronizas.
        Cambiar de fuente nunca toca el motor.
      </p>

      <Wizard onCreada={cargar} />

      <h2>Fuentes conectadas</h2>
      {!data && <SkeletonRows n={3} columnas={4} />}
      {data && (
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Entidad</th>
              <th>Última sincronización</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.map((fuente) => (
              <tr key={fuente.source_id}>
                <td>{fuente.name}</td>
                <td>
                  <span className="badge">{fuente.type === "simulada" ? "Integrada" : "CSV"}</span>
                </td>
                <td>{fuente.detail ?? etiquetaEntidad(fuente.entity)}</td>
                <td>{fuente.last_sync_at ? fmtDate(fuente.last_sync_at) : "—"}</td>
                <td>
                  {fuente.type !== "simulada" && (
                    <>
                      <button
                        className="btn-secondary"
                        disabled={sincronizando === fuente.source_id}
                        onClick={() => void sincronizar(fuente)}
                      >
                        <RefreshCw size={14} className={sincronizando === fuente.source_id ? "girando" : undefined} />
                        Sincronizar
                      </button>{" "}
                      <button className="btn-secondary" onClick={() => void eliminar(fuente)}>
                        <Trash2 size={14} />
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <p className="muted">
        <Sparkles size={13} /> La sugerencia de la IA es una propuesta: siempre pasa la validación
        del contrato y tu confirmación antes de tocar la base de datos.
      </p>
    </section>
  );
}
