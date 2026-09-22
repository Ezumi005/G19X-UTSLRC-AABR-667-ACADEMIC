"""Endpoints de clientes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.persistence import queries

router = APIRouter(tags=["customers"])


@router.get("/customers")
def list_customers(limit: int = Query(default=50, ge=1, le=500), offset: int = Query(default=0, ge=0)) -> dict:
    """Clientes con paginacion y etiqueta de segmento del ultimo run exitoso."""
    items, total = queries.list_customers(limit, offset)
    return {"total": total, "count": len(items), "data": items}


@router.get("/customers/{customer_id}")
def get_customer(customer_id: str) -> dict:
    """Detalle de un cliente: datos, estadisticas de compra y segmento asignado."""
    customer = queries.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Cliente no encontrado: {customer_id}")
    return customer
