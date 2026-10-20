"""Endpoints de fuentes de datos: adaptacion de archivos CSV sin codigo.

Flujo: subir CSV -> detectar columnas -> mapear a campos del contrato ->
validar en seco -> guardar fuente -> sincronizar al pipeline normal.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from psycopg.types.json import Jsonb
from pydantic import BaseModel, Field

from src.adapters.csv_adapter import (
    DynamicCSVAdapter,
    campos_de_entidad,
    entidades_validas,
    leer_columnas_y_muestra,
    validar_mapeo,
)
from src.persistence.db import connect
from src.persistence.ingest import persist_result
from src.persistence.queries import ingestion_run_summary
from src.services.mapping_suggest import suggest_mapping

router = APIRouter(prefix="/sources", tags=["sources"])

UPLOADS_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"

# La fuente simulada es parte del sistema (no se da de alta ni se borra)
FUENTE_SIMULADA = {
    "source_id": 0,
    "name": "CRM simulado (integrado)",
    "type": "simulada",
    "entity": "todas",
    "detail": "Contrato completo: clientes, transacciones, interacciones y campanas",
}


class MappingPayload(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    entity: str
    upload_token: str = Field(min_length=8, max_length=64)
    mapping: dict[str, str]


def _ruta_upload(token: str) -> Path:
    ruta = UPLOADS_DIR / f"{token}.csv"
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo subido no encontrado; vuelve a subirlo.")
    return ruta


@router.get("")
def list_sources() -> dict:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT source_id, name, type, entity, mapping, created_at, last_sync_at FROM data_sources ORDER BY source_id"
            )
            filas = cur.fetchall()
    importadas = [
        {
            "source_id": f[0],
            "name": f[1],
            "type": f[2],
            "entity": f[3],
            "mapping": f[4],
            "created_at": f[5],
            "last_sync_at": f[6],
        }
        for f in filas
    ]
    return {"count": len(importadas) + 1, "data": [FUENTE_SIMULADA] + importadas}


@router.get("/schema/{entity}")
def entity_schema(entity: str) -> dict:
    """Campos del contrato para una entidad (introspectados; para el asistente)."""
    if entity not in entidades_validas():
        raise HTTPException(status_code=400, detail=f"Entidad desconocida: {entity}")
    return {"entity": entity, "fields": campos_de_entidad(entity)}


@router.post("/csv/upload")
async def upload_csv(archivo: UploadFile) -> dict:
    """Sube un CSV y devuelve token, columnas detectadas y filas de muestra."""
    if not archivo.filename or not archivo.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extension .csv")
    contenido = await archivo.read()
    if len(contenido) > 15_000_000:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande (max 15 MB)")
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:16]
    (UPLOADS_DIR / f"{token}.csv").write_bytes(contenido)
    try:
        columnas, muestra = leer_columnas_y_muestra(UPLOADS_DIR / f"{token}.csv")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el CSV: {exc}") from exc
    if not columnas or len(columnas) < 1:
        raise HTTPException(status_code=400, detail="El CSV no tiene columnas legibles")
    return {"upload_token": token, "filename": archivo.filename, "columns": columnas, "sample_rows": muestra}


class SuggestPayload(BaseModel):
    upload_token: str = Field(min_length=8, max_length=64)


@router.post("/csv/suggest")
def suggest_csv_mapping(payload: SuggestPayload) -> dict:
    """Sugerencia de mapeo con IA (entidad + columnas). El usuario confirma en la UI."""
    ruta = _ruta_upload(payload.upload_token)
    columnas, muestra = leer_columnas_y_muestra(ruta, filas=5)
    try:
        sugerencia = suggest_mapping(columnas, muestra)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Sugerencia IA no disponible: {exc}") from exc
    sugerencia["mapping"] = {
        campo: columna for campo, columna in (sugerencia.get("mapping") or {}).items() if columna in columnas
    }
    sugerencia["columns"] = columnas
    sugerencia["missing_required"] = validar_mapeo(sugerencia["entity"], sugerencia["mapping"])
    return sugerencia


@router.post("/csv/validate")
def validate_csv(payload: MappingPayload) -> dict:
    """Validacion en seco: adapta sin persistir y devuelve conteos e incidencias."""
    errores = validar_mapeo(payload.entity, payload.mapping)
    if errores:
        raise HTTPException(status_code=400, detail="; ".join(errores))
    adaptador = DynamicCSVAdapter(payload.name, payload.entity, _ruta_upload(payload.upload_token), payload.mapping)
    try:
        resultado = adaptador.fetch_normalized()
    except Exception as exc:
        raise HTTPException(
            status_code=422, detail=f"El CSV no se pudo procesar con este mapeo: {str(exc)[:200]}"
        ) from exc
    reporte = resultado.report
    preview: list = []
    entidades = getattr(resultado.dataset, payload.entity)
    for entidad in entidades[:5]:
        preview.append(entidad.model_dump(mode="json"))
    return {
        "read": reporte.read.get(payload.entity, 0),
        "accepted": reporte.accepted.get(payload.entity, 0),
        "rejected": reporte.rejected.get(payload.entity, 0),
        "incidents": [inc.error[:160] for inc in reporte.incidents[:5]],
        "preview": preview,
    }


@router.post("/csv")
def create_csv_source(payload: MappingPayload) -> dict:
    """Crea la fuente con su mapeo (tras validar) lista para sincronizar."""
    errores = validar_mapeo(payload.entity, payload.mapping)
    if errores:
        raise HTTPException(status_code=400, detail="; ".join(errores))
    ruta = _ruta_upload(payload.upload_token)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO data_sources (name, type, entity, filename, mapping)
                   VALUES (%s, 'csv', %s, %s, %s) RETURNING source_id""",
                (payload.name, payload.entity, ruta.name, Jsonb(payload.mapping)),
            )
            return {"source_id": cur.fetchone()[0], "name": payload.name, "entity": payload.entity}


@router.post("/{source_id}/sync")
def sync_source(source_id: int) -> dict:
    """Sincroniza la fuente: adapta el CSV y persiste con trazabilidad."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name, entity, filename, mapping FROM data_sources WHERE source_id = %s",
                (source_id,),
            )
            fila = cur.fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    nombre, entidad, filename, mapping = fila
    adaptador = DynamicCSVAdapter(nombre, entidad, UPLOADS_DIR / filename, mapping)
    try:
        resultado = adaptador.fetch_normalized()
        run_id = persist_result(resultado)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Fallo la sincronizacion: {exc}") from exc
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE data_sources SET last_sync_at = %s WHERE source_id = %s",
                (datetime.now(timezone.utc), source_id),
            )
    return ingestion_run_summary(run_id)


@router.delete("/{source_id}")
def delete_source(source_id: int) -> dict:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM data_sources WHERE source_id = %s", (source_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    return {"deleted": source_id}
