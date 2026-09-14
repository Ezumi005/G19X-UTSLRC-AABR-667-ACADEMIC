"""Enumeraciones canonicas del contrato interno de datos V1 (ver docs/contrato_interno_datos_v1.md, seccion 4)."""

from enum import Enum


class ProductCategory(str, Enum):
    """Categorias canonicas de producto. Mapeo del adaptador: valor externo sin equivalente -> OTROS."""

    ELECTRONICA = "electronica"
    HOGAR = "hogar"
    MODA = "moda"
    DEPORTES = "deportes"
    BELLEZA = "belleza"
    ALIMENTOS = "alimentos"
    JUGUETES = "juguetes"
    OTROS = "otros"


class InteractionType(str, Enum):
    """Interacciones digitales fuera de campanas de marketing."""

    WEB_VISIT = "web_visit"
    PRODUCT_VIEW = "product_view"
    ABANDONED_CART = "abandoned_cart"


class CampaignEventType(str, Enum):
    """Eventos del embudo de campanas de marketing."""

    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
