"""Endpoints de clientes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.persistence import queries
from src.services import scoring as scoring_service

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


@router.post("/customers/{customer_id}/predict")
def predict_customer(customer_id: str) -> dict:
    """Predice el cluster de un cliente con el modelo servido en Azure.

    Flujo (etapa 11): features desde PostgreSQL -> endpoint de scoring en
    Azure App Service (artefacto registrado en Azure ML) -> cluster + etiqueta
    del ultimo run exitoso.
    """
    if queries.get_customer(customer_id) is None:
        raise HTTPException(status_code=404, detail=f"Cliente no encontrado: {customer_id}")
    if not scoring_service.scoring_available():
        raise HTTPException(
            status_code=501,
            detail="Servicio de scoring en Azure no configurado: faltan AZURE_SCORING_* en el .env.",
        )
    features = queries.customer_features(customer_id)
    try:
        clusters = scoring_service.predict_clusters([features])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Servicio de scoring no disponible: {exc}") from exc
    cluster = int(clusters[0])
    _, segments = queries.latest_segments()
    segment = next(
        ({"segment_id": s["segment_id"], "label": s["label"]} for s in segments if s["cluster_id"] == cluster),
        None,
    )
    return {"customer_id": customer_id, "features": features, "cluster": cluster, "segment": segment}
