"""Interfaz comun y estructuras de reporte para todos los adaptadores.

Cada fuente externa (CRM simulado, HubSpot, CSV, base de datos, ...) implementa
BaseAdapter y entrega un AdapterResult: un NormalizedDataset valido segun el
contrato interno + un reporte de incidencias de los registros excluidos.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.contracts import NormalizedDataset


@dataclass
class Incident:
    """Registro externo excluido del dataset, con la causa."""

    entity: str
    external_id: str
    error: str
    field: str | None = None


@dataclass
class AdapterReport:
    """Resumen de una ejecucion del adaptador: leidos / aceptados / rechazados."""

    source: str
    read: dict[str, int] = field(default_factory=dict)
    accepted: dict[str, int] = field(default_factory=dict)
    rejected: dict[str, int] = field(default_factory=dict)
    incidents: list[Incident] = field(default_factory=list)

    def add(self, entity: str, read: int, accepted: int, incidents: list[Incident]) -> None:
        self.read[entity] = read
        self.accepted[entity] = accepted
        self.rejected[entity] = read - accepted
        self.incidents.extend(incidents)

    @property
    def total_rejected(self) -> int:
        return sum(self.rejected.values())

    def summary(self) -> str:
        lines = [f"Reporte del adaptador [{self.source}]"]
        for entity in self.read:
            lines.append(
                f"  {entity}: leidos={self.read[entity]} "
                f"aceptados={self.accepted[entity]} rechazados={self.rejected[entity]}"
            )
        lines.append(f"  total incidencias: {len(self.incidents)}")
        for inc in self.incidents:
            detail = f"{inc.entity} {inc.external_id}"
            if inc.field:
                detail += f" (campo {inc.field})"
            lines.append(f"    - {detail}: {inc.error}")
        return "\n".join(lines)


@dataclass
class AdapterResult:
    """Salida estandar de un adaptador."""

    dataset: NormalizedDataset
    report: AdapterReport


class BaseAdapter(ABC):
    """Interfaz que debe implementar todo adaptador de fuente externa."""

    @abstractmethod
    def fetch_normalized(self) -> AdapterResult:
        """Obtiene los datos de la fuente y los entrega ya normalizados."""
