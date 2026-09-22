"""SimulatedCRMAdapter: traduce el formato externo del CRM simulado al Contrato Interno V1.

Fuente: crm_simulator/app.py (puerto 8001), formato externo propio.

Reglas del contrato (docs/contrato_interno_datos_v1.md, seccion 4):
- categoria externa sin equivalente en el canon -> ProductCategory.OTROS;
- tipo de interaccion o evento desconocido -> se descarta y se reporta;
- registro que no valida contra el contrato -> se excluye y se reporta.

Este modulo NO contiene logica de negocio ni de ML: solo mapeo, conversion
de tipos, validacion y reporte.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import requests
from pydantic import ValidationError

from src.adapters.base import AdapterReport, AdapterResult, BaseAdapter, Incident
from src.contracts import (
    CampaignEvent,
    CampaignEventType,
    Customer,
    Interaction,
    InteractionType,
    NormalizedDataset,
    ProductCategory,
    Transaction,
)

DEFAULT_BASE_URL = "http://127.0.0.1:8001"

CATEGORY_MAP: dict[str, ProductCategory] = {
    "ELECTRONICS": ProductCategory.ELECTRONICA,
    "HOME_APPLIANCES": ProductCategory.HOGAR,
    "FASHION": ProductCategory.MODA,
    "SPORTS": ProductCategory.DEPORTES,
    "BEAUTY": ProductCategory.BELLEZA,
    "GROCERIES": ProductCategory.ALIMENTOS,
    "TOYS": ProductCategory.JUGUETES,
    "BOOKS": ProductCategory.OTROS,
    "GARDEN_TOOLS": ProductCategory.OTROS,
}

INTERACTION_MAP: dict[str, InteractionType] = {
    "WEB_SESSION": InteractionType.WEB_VISIT,
    "PRODUCT_CONSULT": InteractionType.PRODUCT_VIEW,
    "CART_LEFT": InteractionType.ABANDONED_CART,
}

EVENT_MAP: dict[str, CampaignEventType] = {
    "SEND": CampaignEventType.SENT,
    "DELIVER": CampaignEventType.DELIVERED,
    "OPEN": CampaignEventType.OPENED,
    "CLICK": CampaignEventType.CLICKED,
}


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _parse_date_only(value: str) -> datetime:
    day = date.fromisoformat(value)
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)


def transform_customer(raw: dict) -> Customer:
    demographics = raw.get("demographics") or {}
    return Customer(
        customer_id=raw["clientId"],
        age=demographics.get("age"),
        city=demographics.get("city"),
        registered_at=_parse_date_only(raw["memberSince"]),
    )


def transform_transaction(raw: dict) -> Transaction:
    return Transaction(
        transaction_id=raw["opId"],
        customer_id=raw["clientId"],
        purchased_at=_parse_ts(raw["ts"]),
        amount=float(raw["totalAmount"]),
        category=CATEGORY_MAP.get(raw["productLine"], ProductCategory.OTROS),
        product_name=raw.get("itemName"),
    )


def transform_interaction(raw: dict) -> Interaction:
    kind = INTERACTION_MAP.get(raw.get("kind"))
    if kind is None:
        raise ValueError(f"tipo de interaccion desconocido: {raw.get('kind')!r} (se descarta)")
    return Interaction(
        interaction_id=raw["eventId"],
        customer_id=raw["clientId"],
        interaction_type=kind,
        occurred_at=_parse_ts(raw["eventTs"]),
        product_name=raw.get("item"),
    )


def transform_campaign_event(raw: dict) -> CampaignEvent:
    action = EVENT_MAP.get(raw.get("action"))
    if action is None:
        raise ValueError(f"tipo de evento de campana desconocido: {raw.get('action')!r} (se descarta)")
    return CampaignEvent(
        campaign_id=raw["campId"],
        customer_id=raw["clientId"],
        event_type=action,
        occurred_at=_parse_ts(raw["actionTs"]),
    )


def _short(exc: Exception) -> str:
    return str(exc).replace("\n", " ")[:200]


def _external_id(raw: dict) -> str:
    return str(raw.get("clientId") or raw.get("opId") or raw.get("eventId") or raw.get("campId") or "?")


def _convert(records: list[dict], entity: str, transform) -> tuple[list, list[Incident]]:
    accepted: list = []
    incidents: list[Incident] = []
    for raw in records:
        ext_id = _external_id(raw)
        try:
            accepted.append(transform(raw))
        except ValidationError as exc:
            errors = exc.errors()
            field = ".".join(str(part) for part in errors[0]["loc"]) if errors and errors[0].get("loc") else None
            incidents.append(Incident(entity, ext_id, _short(exc), field))
        except (KeyError, ValueError, TypeError) as exc:
            field = str(exc.args[0]) if isinstance(exc, KeyError) and exc.args else None
            incidents.append(Incident(entity, ext_id, _short(exc), field))
    return accepted, incidents


class SimulatedCRMAdapter(BaseAdapter):
    """Adaptador de la API CRM simulada (crm_simulator)."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 15.0, page_size: int = 1000) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.page_size = page_size

    def _fetch_all(self, path: str) -> list[dict]:
        records: list[dict] = []
        offset = 0
        while True:
            response = requests.get(
                f"{self.base_url}{path}",
                params={"limit": self.page_size, "offset": offset},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            batch = payload.get("data", [])
            records.extend(batch)
            offset += len(batch)
            if not batch or offset >= payload.get("total", 0):
                return records

    def fetch_normalized(self) -> AdapterResult:
        report = AdapterReport(source="crm_simulado")

        raw = self._fetch_all("/crm/customers")
        customers, incidents = _convert(raw, "customers", transform_customer)
        report.add("customers", len(raw), len(customers), incidents)

        raw = self._fetch_all("/crm/transactions")
        transactions, incidents = _convert(raw, "transactions", transform_transaction)
        report.add("transactions", len(raw), len(transactions), incidents)

        raw = self._fetch_all("/crm/interactions")
        interactions, incidents = _convert(raw, "interactions", transform_interaction)
        report.add("interactions", len(raw), len(interactions), incidents)

        raw = self._fetch_all("/crm/campaign-events")
        campaign_events, incidents = _convert(raw, "campaign_events", transform_campaign_event)
        report.add("campaign_events", len(raw), len(campaign_events), incidents)

        dataset = NormalizedDataset(
            customers=customers,
            transactions=transactions,
            interactions=interactions,
            campaign_events=campaign_events,
        )
        return AdapterResult(dataset, report)
