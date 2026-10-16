import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./styles.css";
import App from "./App.tsx";
import ErrorBoundary from "./ErrorBoundary.tsx";
import { FeedbackProvider } from "./Feedback.tsx";
import { SettingsProvider } from "./settings.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <FeedbackProvider>
        <SettingsProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </SettingsProvider>
      </FeedbackProvider>
    </ErrorBoundary>
  </StrictMode>,
);
