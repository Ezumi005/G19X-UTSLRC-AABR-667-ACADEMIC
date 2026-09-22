"""Endpoint de ingestion: sincroniza la fuente CRM simulada hacia PostgreSQL."""

from __future__ import annotations

import os

import requests
from fastapi import APIRouter, HTTPException

from src.persistence import queries
from src.persistence.ingest import run_ingestion

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

DEFAULT_SIMULATOR_URL = "http://127.0.0.1:8001"


@router.post("/sync")
def sync_ingestion() -> dict:
    """Ejecuta una ingesta completa: simulador -> adaptador -> PostgreSQL.

    Requiere la API CRM simulada encendida (SIMULATOR_URL o 127.0.0.1:8001).
    """
    base_url = os.environ.get("SIMULATOR_URL", DEFAULT_SIMULATOR_URL)
    try:
        run_id = run_ingestion(base_url)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Fuente CRM simulada no disponible en {base_url}: {exc}",
        ) from exc
    return queries.ingestion_run_summary(run_id)
