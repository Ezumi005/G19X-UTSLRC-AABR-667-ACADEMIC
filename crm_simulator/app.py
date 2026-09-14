"""API del CRM simulado: fuente EXTERNA de datos para el Motor de Segmentacion.

Este servicio representa un sistema externo independiente del backend principal.
Entrega los datos en su formato externo propio (ver crm_simulator/generate_data.py),
que NO es el contrato interno: el backend debe consumirla unicamente a traves
del SimulatedCRMAdapter.

Ejecutar desde la raiz del proyecto:
    .venv/Scripts/python.exe -m uvicorn crm_simulator.app:app --port 8001
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

app = FastAPI(
    title="CRM Simulado (PluriOne)",
    version="1.0.0",
    description="Fuente externa de datos para el Motor Inteligente de Segmentacion de Clientes. "
    "Formato propio del CRM; NO es el contrato interno del motor.",
)

_CACHE: dict[str, list] = {}


def _load(name: str) -> list:
    if name not in _CACHE:
        path = DATA_DIR / name
        if not path.exists():
            raise HTTPException(
                status_code=503,
                detail="Dataset no generado. Ejecuta: .venv/Scripts/python.exe -m crm_simulator.generate_data",
            )
        _CACHE[name] = json.loads(path.read_text(encoding="utf-8"))
    return _CACHE[name]


def _paged(items: list, limit: int, offset: int) -> dict:
    page = items[offset:] if limit <= 0 else items[offset : offset + limit]
    return {"total": len(items), "count": len(page), "data": page}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "crm-simulado"}


@app.get("/crm/customers")
def get_customers(limit: int = Query(default=0, ge=0), offset: int = Query(default=0, ge=0)) -> dict:
    return _paged(_load("customers.json"), limit, offset)


@app.get("/crm/transactions")
def get_transactions(limit: int = Query(default=0, ge=0), offset: int = Query(default=0, ge=0)) -> dict:
    return _paged(_load("transactions.json"), limit, offset)


@app.get("/crm/interactions")
def get_interactions(limit: int = Query(default=0, ge=0), offset: int = Query(default=0, ge=0)) -> dict:
    return _paged(_load("interactions.json"), limit, offset)


@app.get("/crm/campaign-events")
def get_campaign_events(limit: int = Query(default=0, ge=0), offset: int = Query(default=0, ge=0)) -> dict:
    return _paged(_load("campaign_events.json"), limit, offset)
