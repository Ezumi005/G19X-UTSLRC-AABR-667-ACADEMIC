import { useState } from "react";
import { GLOSARIO } from "./glossary.ts";

export default function InfoTip({ termino }: { termino: string }) {
  const [abierto, setAbierto] = useState(false);
  const entrada = GLOSARIO[termino];
  if (!entrada) {
    return null;
  }
  return (
    <span className="infotip">
      <button
        className="infotip-btn"
        aria-label={`Qué significa: ${entrada.titulo}`}
        onClick={() => setAbierto((valor) => !valor)}
      >
        ?
      </button>
      {abierto && (
        <span className="infotip-panel" role="tooltip">
          <b>{entrada.titulo}</b>
          <span>{entrada.descripcion}</span>
          <button className="btn-secondary infotip-close" onClick={() => setAbierto(false)}>
            Entendido
          </button>
        </span>
      )}
    </span>
  );
}
