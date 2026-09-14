"""Contrato interno de datos V1 codificado con Pydantic.

Fuente de verdad documental: docs/contrato_interno_datos_v1.md
Toda fuente externa debe adaptarse a estas entidades antes de entrar al nucleo del sistema.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from src.contracts.enums import CampaignEventType, InteractionType, ProductCategory


class Customer(BaseModel):
    """Cliente. Campos obligatorios: customer_id, registered_at."""

    customer_id: str = Field(min_length=1)
    age: int | None = Field(default=None, ge=0, le=120)
    city: str | None = Field(default=None, min_length=1)
    registered_at: datetime


class Transaction(BaseModel):
    """Compra. Campos obligatorios: transaction_id, customer_id, purchased_at, amount (>=0), category."""

    transaction_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    purchased_at: datetime
    amount: float = Field(ge=0)
    category: ProductCategory
    product_name: str | None = Field(default=None, min_length=1)


class Interaction(BaseModel):
    """Interaccion digital fuera de campanas (web_visit, product_view, abandoned_cart)."""

    interaction_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    interaction_type: InteractionType
    occurred_at: datetime
    product_name: str | None = Field(default=None, min_length=1)


class CampaignEvent(BaseModel):
    """Evento de embudo de campana (sent, delivered, opened, clicked). Sin ID propio: identidad compuesta."""

    campaign_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    event_type: CampaignEventType
    occurred_at: datetime


class NormalizedDataset(BaseModel):
    """Salida completa de un adaptador: datos normalizados listos para validacion y persistencia."""

    customers: list[Customer] = Field(default_factory=list)
    transactions: list[Transaction] = Field(default_factory=list)
    interactions: list[Interaction] = Field(default_factory=list)
    campaign_events: list[CampaignEvent] = Field(default_factory=list)
