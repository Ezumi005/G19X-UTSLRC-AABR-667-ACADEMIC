"""Aplicacion FastAPI principal del Motor de Segmentacion de Clientes.

Ejecutar desde la raiz del proyecto:
    .venv/Scripts/python.exe -m uvicorn src.api.app:app --port 8000
Documentacion interactiva: http://127.0.0.1:8000/docs

La API consume unicamente la capa de persistencia y los procesos ya existentes
(ingesta y segmentacion). Nunca accede al CRM simulado sin su adaptador ni
contiene lógica de ML.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import customers, dashboard, ingestion, segments

DEV_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="Motor Inteligente de Segmentación de Clientes",
        version="0.1.0",
        description="API principal del MVP. Backend único para el frontend React; "
        "orquesta ingesta, segmentación y consulta de resultados.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=DEV_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(ingestion.router)
    app.include_router(customers.router)
    app.include_router(segments.router)
    app.include_router(dashboard.router)

    @app.get("/health", tags=["infra"])
    def health() -> dict:
        return {"status": "ok", "service": "motor-segmentacion"}

    @app.get("/", tags=["infra"])
    def root() -> dict:
        return {
            "service": "Motor Inteligente de Segmentación de Clientes",
            "docs": "/docs",
            "endpoints": [
                "POST /ingestion/sync",
                "GET /customers",
                "GET /customers/{id}",
                "POST /segmentation/run",
                "GET /segments",
                "GET /segments/{id}",
                "POST /segments/{id}/recommendation",
                "GET /dashboard",
            ],
        }

    return app


app = create_app()
