import { Route, Routes, Link, useLocation } from "react-router-dom";
import Dashboard from "./pages/Dashboard.tsx";
import Customers from "./pages/Customers.tsx";
import Segments from "./pages/Segments.tsx";
import SegmentDetail from "./pages/SegmentDetail.tsx";
import Runs from "./pages/Runs.tsx";

function Nav() {
  const { pathname } = useLocation();
  const items = [
    { to: "/", label: "Dashboard" },
    { to: "/customers", label: "Clientes" },
    { to: "/segments", label: "Segmentos" },
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
      </nav>
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
          <Route path="/segments" element={<Segments />} />
          <Route path="/segments/:id" element={<SegmentDetail />} />
          <Route path="/runs" element={<Runs />} />
        </Routes>
      </main>
      <footer className="footer">
        MVP con datos simulados · el frontend consume únicamente la API del backend (puerto 8000)
      </footer>
    </div>
  );
}
