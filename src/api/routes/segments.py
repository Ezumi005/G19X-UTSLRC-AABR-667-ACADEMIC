"""Endpoints de segmentacion y segmentos."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.ml.segmentation import run_segmentation
from src.persistence import queries

router = APIRouter(tags=["segmentation"])


@router.post("/segmentation/run")
def run_segmentation_endpoint() -> dict:
    """Ejecuta una segmentacion completa (features -> K-Means k=6 -> etiquetas -> PostgreSQL)."""
    run_id = run_segmentation()
    return queries.segmentation_run_summary(run_id)


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


@router.post("/segments/{segment_id}/recommendation")
def create_recommendation(segment_id: int) -> dict:
    """Generara la recomendacion comercial del segmento mediante Azure OpenAI.

    Endpoint reservado: se implementara en la etapa de integracion de Azure OpenAI
    (el motor de segmentacion NO depende de el).
    """
    raise HTTPException(
        status_code=501,
        detail="Recomendaciones con Azure OpenAI: pendiente de la etapa correspondiente del plan.",
    )
