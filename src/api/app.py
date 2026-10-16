"""Aplicacion FastAPI principal del Motor de Segmentacion de Clientes.

Ejecutar desde la raiz del proyecto:
    .venv/Scripts/python.exe -m uvicorn src.api.app:app --port 8000
Documentacion interactiva: http://127.0.0.1:8000/docs

La API consume unicamente la capa de persistencia y los procesos ya existentes
(ingesta y segmentacion). Nunca accede al CRM simulado sin su adaptador ni
contiene lógica de ML.
"""

from __future__ import annotations

import logging
import os

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import audiences, customers, dashboard, ingestion, segments

logger = logging.getLogger("motor-segmentacion")

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
    app.include_router(audiences.router)

    @app.exception_handler(Exception)
    async def error_no_controlado(request: Request, exc: Exception) -> JSONResponse:
        """Errores inesperados: respuesta controlada sin filtrar detalles internos."""
        logger.exception("Error no controlado en %s", request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})

    @app.get("/health", tags=["infra"])
    def health() -> dict:
        """Estado del servicio y de sus dependencias (PostgreSQL, Azure)."""
        reporte: dict = {"status": "ok", "service": "motor-segmentacion", "dependencies": {}}

        def revisar(nombre: str, chequeo) -> None:
            try:
                detalle = chequeo()
                reporte["dependencies"][nombre] = detalle or "ok"
            except Exception as exc:  # noqa: BLE001
                reporte["dependencies"][nombre] = f"error: {str(exc)[:140]}"
                reporte["status"] = "degradado"

        def _postgres():
            from src.persistence.db import connect

            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")

        def _scoring():
            url = os.environ.get("AZURE_SCORING_URL")
            if not url:
                return "no configurado"
            respuesta = requests.get(f"{url.rstrip('/')}/health", timeout=8)
            respuesta.raise_for_status()
            return "ok"

        def _openai():
            if not (os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT")):
                return "no configurado"
            return "configurado"

        revisar("postgresql", _postgres)
        revisar("azure_scoring", _scoring)
        revisar("azure_openai", _openai)
        return reporte

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
