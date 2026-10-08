"""Endpoints de audiencias dinamicas (PRD seccion 16 / RF-18, RF-19).

Las condiciones se almacenan y la membresia se recalcula en cada consulta
contra los datos vigentes (RF-19: actualizar audiencias cuando cambien los datos).
"""

from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field

from src.contracts import ProductCategory
from src.persistence import queries

router = APIRouter(prefix="/audiences", tags=["audiences"])


class AudienceConditions(BaseModel):
    """Condiciones combinables (AND) sobre clientes, features o segmento."""

    segment: str | None = None
    city: str | None = None
    min_frequency: int | None = Field(default=None, ge=0)
    min_days_without_purchase: int | None = Field(default=None, ge=0)
    category: ProductCategory | None = None


class AudienceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str | None = None
    conditions: AudienceConditions


@router.post("")
def create_audience(payload: AudienceCreate) -> dict:
    try:
        audience_id = queries.create_audience(
            payload.name, payload.description, payload.conditions.model_dump()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=409, detail=f"No se pudo crear la audiencia (¿nombre duplicado?): {exc}"
        ) from exc
    return queries.get_audience(audience_id)


@router.get("")
def list_audiences() -> dict:
    data = queries.list_audiences()
    return {"count": len(data), "data": data}


@router.get("/{audience_id}")
def get_audience(
    audience_id: int, limit: int = Query(default=50, ge=1, le=500), offset: int = Query(default=0, ge=0)
) -> dict:
    audiencia = queries.get_audience(audience_id)
    if audiencia is None:
        raise HTTPException(status_code=404, detail=f"Audiencia no encontrada: {audience_id}")
    members, total = queries.audience_members(audiencia["conditions"], limit, offset)
    return {**audiencia, "members": members, "members_total": total}


@router.delete("/{audience_id}")
def delete_audience(audience_id: int) -> dict:
    if not queries.delete_audience(audience_id):
        raise HTTPException(status_code=404, detail=f"Audiencia no encontrada: {audience_id}")
    return {"deleted": audience_id}


@router.get("/{audience_id}/export")
def export_audience(audience_id: int) -> Response:
    """Exporta los miembros actuales de la audiencia en CSV (para campanas)."""
    audiencia = queries.get_audience(audience_id)
    if audiencia is None:
        raise HTTPException(status_code=404, detail=f"Audiencia no encontrada: {audience_id}")
    members, _ = queries.audience_members(audiencia["conditions"])
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["customer_id", "age", "city", "segment_label", "frequency", "last_purchase", "registered_at"])
    for m in members:
        writer.writerow(
            [m["customer_id"], m["age"], m["city"], m["segment_label"], m["frequency"], m["last_purchase"], m["registered_at"]]
        )
    return Response(
        content=buffer.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="audiencia_{audience_id}.csv"'},
    )
