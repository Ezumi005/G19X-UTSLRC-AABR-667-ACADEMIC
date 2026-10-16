"""Adaptador CSV dinamico: adapta cualquier archivo CSV al contrato V1 sin codigo.

El usuario sube un CSV desde la web y define el mapeo columna -> campo del
contrato (por entidad). Este adaptador implementa la MISMA interfaz BaseAdapter
que el SimulatedCRMAdapter: el motor no distingue la fuente.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from src.adapters.base import AdapterReport, AdapterResult, BaseAdapter, Incident
from src.contracts import (
    CampaignEvent,
    Customer,
    Interaction,
    NormalizedDataset,
    Transaction,
)

ENTITY_MODELS: dict[str, type] = {
    "customers": Customer,
    "transactions": Transaction,
    "interactions": Interaction,
    "campaign_events": CampaignEvent,
}


def entidades_validas() -> list[str]:
    return list(ENTITY_MODELS.keys())


def campos_de_entidad(entity: str) -> dict[str, bool]:
    """Campos del contrato por introspeccion (unica fuente de verdad): campo -> obligatorio.

    Los campos requeridos se derivan del propio modelo Pydantic del contrato;
    agregar un campo al contrato lo hace aparecer aqui, en la UI y en el
    prompt de la IA sin tocar nada mas.
    """
    modelo = ENTITY_MODELS.get(entity)
    if modelo is None:
        raise ValueError(f"Entidad desconocida: {entity}")
    return {nombre: info.is_required() for nombre, info in modelo.model_fields.items()}


def leer_columnas_y_muestra(filepath: str | Path, filas: int = 3) -> tuple[list[str], list[dict]]:
    """Columnas detectadas y unas filas de muestra para el asistente de mapeo."""
    df = pd.read_csv(filepath, nrows=filas, dtype=str, keep_default_na=False)
    columnas = df.columns.tolist()
    muestra = df.to_dict("records")
    return columnas, muestra


def validar_mapeo(entity: str, mapping: dict[str, str]) -> list[str]:
    """Errores de un mapeo antes de usarlo (campos obligatorios sin columna)."""
    errores: list[str] = []
    for campo, obligatorio in campos_de_entidad(entity).items():
        columna = mapping.get(campo)
        if obligatorio and not columna:
            errores.append(f"Falta asignar columna para el campo obligatorio '{campo}'")
    return errores


class DynamicCSVAdapter(BaseAdapter):
    """Adapta un CSV con mapeo declarado a la entidad del contrato indicada."""

    def __init__(self, name: str, entity: str, filepath: str | Path, mapping: dict[str, str]) -> None:
        self.name = name
        self.entity = entity
        self.filepath = Path(filepath)
        self.mapping = {campo: columna for campo, columna in mapping.items() if columna}

    def _filas(self) -> list[dict]:
        df = pd.read_csv(self.filepath, dtype=str, keep_default_na=False, skipinitialspace=True)
        filas: list[dict] = []
        for _, fila in df.iterrows():
            registro = {
                campo: fila[columna].strip()
                for campo, columna in self.mapping.items()
                if columna in fila and str(fila[columna]).strip() != ""
            }
            filas.append(registro)
        return filas

    def fetch_normalized(self) -> AdapterResult:
        modelo = ENTITY_MODELS[self.entity]
        reporte = AdapterReport(source=self.name)
        aceptados: list = []
        incidentes: list[Incident] = []
        for indice, registro in enumerate(self._filas(), start=2):
            identificador = registro.get("customer_id") or registro.get("transaction_id") or registro.get("interaction_id") or registro.get("campaign_id") or f"fila {indice}"
            try:
                aceptados.append(modelo.model_validate(registro))
            except ValidationError as exc:
                errores = exc.errors()
                campo = ".".join(str(parte) for parte in errores[0]["loc"]) if errores and errores[0].get("loc") else None
                incidentes.append(Incident(self.entity, str(identificador), str(exc).replace("\n", " ")[:200], campo))
        reporte.add(self.entity, len(aceptados) + len(incidentes), len(aceptados), incidentes)

        dataset = NormalizedDataset()
        setattr(dataset, self.entity, aceptados)
        return AdapterResult(dataset, reporte)
