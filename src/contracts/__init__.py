"""Contrato interno de datos V1 (ver docs/contrato_interno_datos_v1.md)."""

from src.contracts.enums import CampaignEventType, InteractionType, ProductCategory
from src.contracts.models import (
    CampaignEvent,
    Customer,
    Interaction,
    NormalizedDataset,
    Transaction,
)

__all__ = [
    "CampaignEvent",
    "CampaignEventType",
    "Customer",
    "Interaction",
    "InteractionType",
    "NormalizedDataset",
    "ProductCategory",
    "Transaction",
]

__version__ = "1.0.0"
