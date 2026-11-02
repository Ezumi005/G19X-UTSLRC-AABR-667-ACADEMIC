import type { ReactNode } from "react";
import { Inbox } from "lucide-react";

export default function EmptyState({
  titulo,
  children,
  accion,
}: {
  titulo: string;
  children?: ReactNode;
  accion?: ReactNode;
}) {
  return (
    <div className="empty-state">
      <Inbox size={30} />
      <h3>{titulo}</h3>
      {children && <p className="muted">{children}</p>}
      {accion && <div className="actions-bar">{accion}</div>}
    </div>
  );
}
