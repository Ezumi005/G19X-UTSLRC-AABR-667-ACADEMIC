import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from "react";

interface Toast {
  id: number;
  tipo: "exito" | "error" | "info";
  mensaje: string;
}

interface Confirmacion {
  id: number;
  titulo: string;
  mensaje: string;
  opcionTexto?: string;
  resolver: (valor: { ok: boolean; conOpcion: boolean }) => void;
}

interface Feedback {
  toast: (mensaje: string, tipo?: Toast["tipo"]) => void;
  confirmar: (titulo: string, mensaje: string) => Promise<boolean>;
  confirmarConOpcion: (
    titulo: string,
    mensaje: string,
    textoOpcion: string,
  ) => Promise<{ ok: boolean; conOpcion: boolean }>;
}

const Ctx = createContext<Feedback | null>(null);

export function FeedbackProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [confirmacion, setConfirmacion] = useState<Confirmacion | null>(null);
  const contador = useRef(0);

  const toast = useCallback((mensaje: string, tipo: Toast["tipo"] = "info") => {
    const id = ++contador.current;
    setToasts((prev) => [...prev, { id, tipo, mensaje }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  const abrir = useCallback(
    (titulo: string, mensaje: string, opcionTexto?: string) =>
      new Promise<{ ok: boolean; conOpcion: boolean }>((resolver) => {
        setConfirmacion({ id: ++contador.current, titulo, mensaje, opcionTexto, resolver });
      }),
    [],
  );

  const confirmar = useCallback(
    async (titulo: string, mensaje: string) => (await abrir(titulo, mensaje)).ok,
    [abrir],
  );

  const confirmarConOpcion = useCallback(
    (titulo: string, mensaje: string, textoOpcion: string) => abrir(titulo, mensaje, textoOpcion),
    [abrir],
  );

  const cerrarConfirmacion = (valor: { ok: boolean; conOpcion: boolean }) => {
    confirmacion?.resolver(valor);
    setConfirmacion(null);
  };

  return (
    <Ctx.Provider value={{ toast, confirmar, confirmarConOpcion }}>
      {children}
      <div className="toast-stack">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast-${t.tipo}`}>
            {t.mensaje}
          </div>
        ))}
      </div>
      {confirmacion && (
        <div className="modal-fondo" onClick={() => cerrarConfirmacion({ ok: false, conOpcion: false })}>
          <div className="modal-caja" onClick={(e) => e.stopPropagation()}>
            <h3>{confirmacion.titulo}</h3>
            <p>{confirmacion.mensaje}</p>
            {confirmacion.opcionTexto && <OpcionModal key={confirmacion.id} texto={confirmacion.opcionTexto} onCerrar={cerrarConfirmacion} />}
            {!confirmacion.opcionTexto && (
              <div className="modal-acciones">
                <button className="btn-secondary" onClick={() => cerrarConfirmacion({ ok: false, conOpcion: false })}>
                  Cancelar
                </button>
                <button onClick={() => cerrarConfirmacion({ ok: true, conOpcion: false })}>Confirmar</button>
              </div>
            )}
          </div>
        </div>
      )}
    </Ctx.Provider>
  );
}

function OpcionModal({
  texto,
  onCerrar,
}: {
  texto: string;
  onCerrar: (v: { ok: boolean; conOpcion: boolean }) => void;
}) {
  const [marcada, setMarcada] = useState(false);
  return (
    <>
      <label className="modal-opcion">
        <input type="checkbox" checked={marcada} onChange={(e) => setMarcada(e.target.checked)} />
        {texto}
      </label>
      <div className="modal-acciones">
        <button className="btn-secondary" onClick={() => onCerrar({ ok: false, conOpcion: false })}>
          Cancelar
        </button>
        <button onClick={() => onCerrar({ ok: true, conOpcion: marcada })}>Confirmar</button>
      </div>
    </>
  );
}

export function useFeedback(): Feedback {
  const feedback = useContext(Ctx);
  if (!feedback) {
    throw new Error("useFeedback debe usarse dentro de FeedbackProvider");
  }
  return feedback;
}
