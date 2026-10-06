"""Endpoints de segmentacion y segmentos."""

from __future__ import annotations

import os

from fastapi import APIRouter, HTTPException, Query

from src.ml.segmentation import run_segmentation
from src.persistence import queries
from src.services import recommendations as reco_service

router = APIRouter(tags=["segmentation"])


@router.post("/segmentation/run")
def run_segmentation_endpoint() -> dict:
    """Ejecuta una segmentacion completa (features -> K-Means k=6 -> etiquetas -> PostgreSQL)."""
    run_id = run_segmentation()
    return queries.segmentation_run_summary(run_id)


@router.get("/segmentation/runs")
def list_runs(limit: int = Query(default=20, ge=1, le=100)) -> dict:
    """Historial de ejecuciones de segmentacion con sus metricas (PRD seccion 19)."""
    runs = queries.list_segmentation_runs(limit)
    return {"count": len(runs), "data": runs}


@router.get("/segments")
def list_segments() -> dict:
    """Segmentos del ultimo run de segmentacion exitoso."""
    run_id, segments = queries.latest_segments()
    return {"run_id": run_id, "count": len(segments), "data": segments}


@router.get("/segments/{segment_id}")
def get_segment(segment_id: int) -> dict:
    """Detalle de un segmento: perfil, metricas del run y vista previa de clientes."""
    segment = queries.get_segment(segment_id)
    if segment is None:
        raise HTTPException(status_code=404, detail=f"Segmento no encontrado: {segment_id}")
    return segment


@router.get("/segments/{segment_id}/recommendation")
def get_recommendation(segment_id: int) -> dict:
    """Ultima recomendacion generada para el segmento (o null si nunca se genero)."""
    if queries.get_segment(segment_id) is None:
        raise HTTPException(status_code=404, detail=f"Segmento no encontrado: {segment_id}")
    return {"recommendation": queries.latest_recommendation(segment_id)}


@router.post("/segments/{segment_id}/recommendation")
def create_recommendation(segment_id: int) -> dict:
    """Genera (con Azure OpenAI) y persiste la recomendacion comercial del segmento.

    Recibe unicamente agregados del segmento: Azure OpenAI no decide clusters
    ni ve clientes individuales (PRD seccion 17).
    """
    segment = queries.get_segment(segment_id)
    if segment is None:
        raise HTTPException(status_code=404, detail=f"Segmento no encontrado: {segment_id}")
    if not reco_service.azure_openai_available():
        raise HTTPException(
            status_code=501,
            detail="Azure OpenAI no configurado: faltan AZURE_OPENAI_* en el .env del backend.",
        )
    model = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5-4-mini")
    try:
        resultado = reco_service.generate_recommendation(
            label=segment["label"],
            description=segment.get("description"),
            n_customers=segment["n_customers"],
            profile=segment.get("profile") or {},
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Azure OpenAI no disponible: {exc}") from exc
    recommendation_id = queries.save_recommendation(segment_id, model, resultado)
    return {
        "recommendation_id": recommendation_id,
        "segment_id": segment_id,
        "model": model,
        "descripcion": resultado["descripcion"],
        "recomendaciones": resultado["recomendaciones"],
    }
