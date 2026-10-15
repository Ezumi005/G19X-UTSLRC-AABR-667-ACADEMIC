import { Component, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/** Muestra un error amigable en lugar de una pantalla en blanco. */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 24, fontFamily: "Segoe UI, sans-serif", color: "#1c2333" }}>
          <h2>La interfaz encontró un problema</h2>
          <p>Recarga la página. Si persiste, comparte este mensaje para repararlo:</p>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              background: "#fdecea",
              color: "#b3261e",
              padding: 12,
              borderRadius: 8,
              fontSize: 13,
            }}
          >
            {String(this.state.error?.message ?? this.state.error)}
          </pre>
          <button
            onClick={() => window.location.reload()}
            style={{ padding: "8px 16px", borderRadius: 6, border: "none", background: "#2b4acc", color: "#fff", cursor: "pointer" }}
          >
            Recargar
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
