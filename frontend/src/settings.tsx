import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type Tema = "claro" | "oscuro";

interface Ajustes {
  tema: Tema;
  setTema: (tema: Tema) => void;
  fmtMoney: (valor: number | null | undefined, decimales?: number) => string;
}

const Ctx = createContext<Ajustes | null>(null);

const formatoPesos = new Intl.NumberFormat("es-MX", {
  style: "currency",
  currency: "MXN",
  maximumFractionDigits: 0,
});

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [tema, setTemaState] = useState<Tema>(() => (localStorage.getItem("tema") as Tema) || "claro");

  useEffect(() => {
    document.documentElement.dataset.tema = tema;
    localStorage.setItem("tema", tema);
  }, [tema]);

  const fmtMoney = (valor: number | null | undefined, decimales = 0): string => {
    if (decimales === 0) {
      return formatoPesos.format(valor ?? 0);
    }
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
      maximumFractionDigits: decimales,
    }).format(valor ?? 0);
  };

  return <Ctx.Provider value={{ tema, setTema: setTemaState, fmtMoney }}>{children}</Ctx.Provider>;
}

export function useSettings(): Ajustes {
  const ajustes = useContext(Ctx);
  if (!ajustes) {
    throw new Error("useSettings debe usarse dentro de SettingsProvider");
  }
  return ajustes;
}
