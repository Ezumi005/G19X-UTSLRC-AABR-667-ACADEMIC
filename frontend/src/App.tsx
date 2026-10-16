import { useState } from "react";
import { Route, Routes, Link, useLocation } from "react-router-dom";
import { History, LayoutDashboard, Database, PieChart, Settings, Target, Users } from "lucide-react";
import Dashboard from "./pages/Dashboard.tsx";
import Customers from "./pages/Customers.tsx";
import CustomerDetail from "./pages/CustomerDetail.tsx";
import Segments from "./pages/Segments.tsx";
import SegmentDetail from "./pages/SegmentDetail.tsx";
import Runs from "./pages/Runs.tsx";
import Sources from "./pages/Sources.tsx";
import { AudienceDetailPage, AudiencesList } from "./pages/Audiences.tsx";
import Logo from "./Logo.tsx";
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
    { to: "/", label: "Dashboard", icon: LayoutDashboard },
    { to: "/customers", label: "Clientes", icon: Users },
    { to: "/segments", label: "Segmentos", icon: PieChart },
    { to: "/audiences", label: "Audiencias", icon: Target },
    { to: "/sources", label: "Fuentes", icon: Database },
    { to: "/runs", label: "Ejecuciones", icon: History },
  ];
  return (
    <header className="topbar">
      <div className="brand">
        <Logo size={26} />
        Motor de Segmentación de Clientes
      </div>
      <nav>
        {items.map((item) => (
          <Link key={item.to} to={item.to} className={pathname === item.to ? "nav-link active" : "nav-link"}>
            <item.icon size={15} />
            {item.label}
          </Link>
        ))}
        <button
          className="gear"
          aria-label="Configuración"
          onClick={() => setConfigAbierta((v) => !v)}
        >
          <Settings size={16} />
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
          <Route path="/sources" element={<Sources />} />
          <Route path="/runs" element={<Runs />} />
        </Routes>
      </main>
    </div>
  );
}
