"""Modelos de respuesta (response models) de la API: documentan OpenAPI/Swagger.

Reflejan exactamente lo que devuelven las consultas de src/persistence/queries.py.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CustomerItem(BaseModel):
    customer_id: str
    age: int | None
    city: str | None
    registered_at: datetime
    cluster_id: int | None
    segment_label: str | None


class CustomersResponse(BaseModel):
    total: int
    count: int
    data: list[CustomerItem]


class CustomerStats(BaseModel):
    frequency: int
    monetary: float
    last_purchase: datetime | None
    categories_count: int


class SegmentRef(BaseModel):
    segment_id: int
    label: str
    cluster_id: int | None = None


class CustomerDetailResponse(BaseModel):
    customer_id: str
    age: int | None
    city: str | None
    registered_at: datetime
    stats: CustomerStats
    segment: SegmentRef | None
    features: dict[str, float | None]


class PredictionResponse(BaseModel):
    customer_id: str
    features: dict[str, float | None]
    cluster: int
    segment: SegmentRef | None


class SegmentSummary(BaseModel):
    segment_id: int
    cluster_id: int
    label: str
    description: str | None
    n_customers: int
    profile: dict[str, Any]


class SegmentsResponse(BaseModel):
    run_id: int | None
    count: int
    data: list[SegmentSummary]


class SegmentDetailResponse(SegmentSummary):
    run_id: int
    k: int
    metrics: dict[str, Any] | None
    started_at: datetime
    run_status: str
    customers_preview: list[dict[str, Any]]


class RecommendationResponse(BaseModel):
    recommendation_id: int
    segment_id: int
    model: str
    descripcion: str
    recomendaciones: list[str]


class RecommendationStored(BaseModel):
    recommendation_id: int
    segment_id: int
    model: str
    descripcion: str | None
    recomendaciones: list[str]
    created_at: datetime


class RecommendationQueryResponse(BaseModel):
    recommendation: RecommendationStored | None


class AudienceConditionsModel(BaseModel):
    segment: str | None = None
    city: str | None = None
    min_frequency: int | None = None
    min_days_without_purchase: int | None = None
    category: str | None = None


class AudienceItem(BaseModel):
    audience_id: int
    name: str
    description: str | None
    conditions: AudienceConditionsModel
    created_at: datetime
    n_customers: int


class AudiencesResponse(BaseModel):
    count: int
    data: list[AudienceItem]


class AudienceMemberItem(BaseModel):
    customer_id: str
    age: int | None
    city: str | None
    registered_at: datetime
    segment_label: str | None
    cluster_id: int | None
    frequency: int
    last_purchase: datetime | None


class AudienceDetailResponse(AudienceItem):
    members: list[AudienceMemberItem]
    members_total: int


class SegmentationRunItem(BaseModel):
    run_id: int
    model_name: str
    k: int
    status: str
    n_customers: int
    metrics: dict[str, Any] | None
    started_at: datetime
    finished_at: datetime | None


class SegmentationRunsResponse(BaseModel):
    count: int
    data: list[SegmentationRunItem]


class IngestionRunItem(BaseModel):
    run_id: int
    source: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    customers_read: int
    customers_saved: int
    transactions_read: int
    transactions_saved: int
    interactions_read: int
    interactions_saved: int
    campaign_events_read: int
    campaign_events_saved: int
    incidents: int


class IngestionRunsResponse(BaseModel):
    count: int
    data: list[IngestionRunItem]
