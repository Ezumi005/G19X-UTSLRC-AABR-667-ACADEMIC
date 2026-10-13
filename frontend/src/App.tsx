import { useState } from "react";
import { Route, Routes, Link, useLocation } from "react-router-dom";
import Dashboard from "./pages/Dashboard.tsx";
import Customers from "./pages/Customers.tsx";
import CustomerDetail from "./pages/CustomerDetail.tsx";
import Segments from "./pages/Segments.tsx";
import SegmentDetail from "./pages/SegmentDetail.tsx";
import Runs from "./pages/Runs.tsx";
import { AudienceDetailPage, AudiencesList } from "./pages/Audiences.tsx";
import { useSettings } from "./settings.tsx";

function PanelConfiguracion({ alCerrar }: { alCerrar: () => void }) {
  const { tema, setTema } = useSettings();
  return (
    <div className="settings-panel">
      <div className="settings-row">
        <span>Tema</span>
        <select value={tema} onChange={(e) => setTema(e.target.value as "claro" | "oscuro")}>
          <option value="claro">Claro</option>
          <option value="oscuro">Oscuro</option>
        </select>
      </div>
      <button className="btn-secondary" onClick={alCerrar}>Listo</button>
    </div>
  );
}

function Nav() {
  const { pathname } = useLocation();
  const [configAbierta, setConfigAbierta] = useState(false);
  const items = [
    { to: "/", label: "Dashboard" },
    { to: "/customers", label: "Clientes" },
    { to: "/segments", label: "Segmentos" },
    { to: "/audiences", label: "Audiencias" },
    { to: "/runs", label: "Ejecuciones" },
  ];
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-dot" />
        Motor de Segmentación de Clientes
      </div>
      <nav>
        {items.map((item) => (
          <Link key={item.to} to={item.to} className={pathname === item.to ? "nav-link active" : "nav-link"}>
            {item.label}
          </Link>
        ))}
        <button
          className="gear"
          aria-label="Configuración"
          onClick={() => setConfigAbierta((v) => !v)}
        >
          ⚙
        </button>
      </nav>
      {configAbierta && <PanelConfiguracion alCerrar={() => setConfigAbierta(false)} />}
    </header>
  );
}

export default function App() {
  return (
    <div className="app">
      <Nav />
      <main className="content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/customers/:id" element={<CustomerDetail />} />
          <Route path="/segments" element={<Segments />} />
          <Route path="/segments/:id" element={<SegmentDetail />} />
          <Route path="/audiences" element={<AudiencesList />} />
          <Route path="/audiences/:id" element={<AudienceDetailPage />} />
          <Route path="/runs" element={<Runs />} />
        </Routes>
      </main>
      <footer className="footer">
        Motor de Segmentación de Clientes · MVP con datos simulados
      </footer>
    </div>
  );
}
