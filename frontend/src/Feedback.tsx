import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from "react";

interface Toast {
  id: number;
  tipo: "exito" | "error" | "info";
  mensaje: string;
}

interface Confirmacion {
  titulo: string;
  mensaje: string;
  resolver: (valor: boolean) => void;
}

interface Feedback {
  toast: (mensaje: string, tipo?: Toast["tipo"]) => void;
  confirmar: (titulo: string, mensaje: string) => Promise<boolean>;
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

  const confirmar = useCallback(
    (titulo: string, mensaje: string) =>
      new Promise<boolean>((resolver) => {
        setConfirmacion({ titulo, mensaje, resolver });
      }),
    [],
  );

  const cerrarConfirmacion = (valor: boolean) => {
    confirmacion?.resolver(valor);
    setConfirmacion(null);
  };

  return (
    <Ctx.Provider value={{ toast, confirmar }}>
      {children}
      <div className="toast-stack">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast-${t.tipo}`}>
            {t.mensaje}
          </div>
        ))}
      </div>
      {confirmacion && (
        <div className="modal-fondo" onClick={() => cerrarConfirmacion(false)}>
          <div className="modal-caja" onClick={(e) => e.stopPropagation()}>
            <h3>{confirmacion.titulo}</h3>
            <p>{confirmacion.mensaje}</p>
            <div className="modal-acciones">
              <button className="btn-secondary" onClick={() => cerrarConfirmacion(false)}>
                Cancelar
              </button>
              <button onClick={() => cerrarConfirmacion(true)}>Confirmar</button>
            </div>
          </div>
        </div>
      )}
    </Ctx.Provider>
  );
}

export function useFeedback(): Feedback {
  const feedback = useContext(Ctx);
  if (!feedback) {
    throw new Error("useFeedback debe usarse dentro de FeedbackProvider");
  }
  return feedback;
}
