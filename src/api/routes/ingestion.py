"""Endpoint de ingestion: sincroniza la fuente CRM simulada hacia PostgreSQL."""

from __future__ import annotations

import logging
import os

import requests
from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import IngestionRunsResponse
from src.ml.segmentation import run_segmentation_si_hay_datos
from src.persistence import queries
from src.persistence.ingest import run_ingestion

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

DEFAULT_SIMULATOR_URL = "http://127.0.0.1:8001"


@router.get("/runs", response_model=IngestionRunsResponse)
def list_ingestion_runs(limit: int = Query(default=10, ge=1, le=50)) -> dict:
    """Historial de ingestiones con duracion, conteos e incidencias (PRD seccion 31)."""
    data = queries.list_ingestion_runs(limit)
    return {"count": len(data), "data": data}


@router.post("/sync")
def sync_ingestion() -> dict:
    """Ejecuta una ingesta completa: simulador -> adaptador -> PostgreSQL.

    Requiere la API CRM simulada encendida (SIMULATOR_URL o 127.0.0.1:8001).
    """
    base_url = os.environ.get("SIMULATOR_URL", DEFAULT_SIMULATOR_URL)
    try:
        run_id = run_ingestion(base_url)
    except requests.RequestException as exc:
        logger.exception("CRM simulado no alcanzable en %s", base_url)
        raise HTTPException(
            status_code=502,
            detail=(
                f"La fuente CRM simulada no esta disponible en {base_url} (no responde). "
                "Levantala o revisa SIMULATOR_URL; el detalle tecnico quedo en el log del servidor."
            ),
        ) from exc
    resumen = queries.ingestion_run_summary(run_id)
    # Segmentos siempre vigentes: se regeneran con los datos que acaban de entrar.
    try:
        resumen["segmentation_run"] = run_segmentation_si_hay_datos()
    except Exception as exc:
        resumen["segmentation_run"] = None
        resumen["segmentation_error"] = str(exc)[:200]
    return resumen
