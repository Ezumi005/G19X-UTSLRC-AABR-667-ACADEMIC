import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./styles.css";
import App from "./App.tsx";
import { SettingsProvider } from "./settings.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <SettingsProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </SettingsProvider>
  </StrictMode>,
);
