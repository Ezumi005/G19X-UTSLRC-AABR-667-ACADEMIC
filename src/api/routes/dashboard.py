"""Resumen del dashboard para el frontend."""

from __future__ import annotations

from fastapi import APIRouter

from src.persistence import queries

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def dashboard() -> dict:
    """Totales e indicadores generales para la vista Dashboard (MVP seccion 16)."""
    return queries.dashboard_summary()
