import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type Tema = "claro" | "oscuro";

export const MONEDAS = ["MXN", "USD", "EUR", "COP", "ARS", "CLP", "PEN"];

interface Ajustes {
  tema: Tema;
  moneda: string;
  setTema: (tema: Tema) => void;
  setMoneda: (moneda: string) => void;
  fmtMoney: (valor: number | null | undefined, decimales?: number) => string;
}

const Ctx = createContext<Ajustes | null>(null);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [tema, setTemaState] = useState<Tema>(() => (localStorage.getItem("tema") as Tema) || "claro");
  const [moneda, setMonedaState] = useState<string>(() => localStorage.getItem("moneda") || "MXN");

  useEffect(() => {
    document.documentElement.dataset.tema = tema;
    localStorage.setItem("tema", tema);
  }, [tema]);

  useEffect(() => {
    localStorage.setItem("moneda", moneda);
  }, [moneda]);

  const fmtMoney = (valor: number | null | undefined, decimales = 0): string =>
    new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: moneda,
      maximumFractionDigits: decimales,
    }).format(valor ?? 0);

  return (
    <Ctx.Provider
      value={{ tema, moneda, setTema: setTemaState, setMoneda: setMonedaState, fmtMoney }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useSettings(): Ajustes {
  const ajustes = useContext(Ctx);
  if (!ajustes) {
    throw new Error("useSettings debe usarse dentro de SettingsProvider");
  }
  return ajustes;
}
