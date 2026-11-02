"""Repositorio: persiste entidades del contrato interno en PostgreSQL.

Los upserts son idempotentes: re-sincronizar no duplica registros
(RF-MVP-18). Recibe entidades Pydantic del contrato, sin conocer
ningun formato externo.

Cada fila guarda `source_id` (procedencia): 0 = CRM simulado, N = fuente
CSV de la vista Fuentes, NULL = dato anterior a la migracion. Eso permite
gestionar el ciclo de vida completo desde la plataforma (reemplazar y
eliminar una fuente junto con sus datos).
"""

from __future__ import annotations

import psycopg

from src.contracts import NormalizedDataset

UPSERT_CUSTOMER = """
INSERT INTO customers (customer_id, age, city, registered_at, source_id)
VALUES (%(customer_id)s, %(age)s, %(city)s, %(registered_at)s, %(source_id)s)
ON CONFLICT (customer_id) DO UPDATE SET
    age = EXCLUDED.age,
    city = EXCLUDED.city,
    registered_at = EXCLUDED.registered_at,
    source_id = EXCLUDED.source_id,
    updated_at = now()
"""

UPSERT_TRANSACTION = """
INSERT INTO transactions (transaction_id, customer_id, purchased_at, amount, category, product_name, source_id)
VALUES (%(transaction_id)s, %(customer_id)s, %(purchased_at)s, %(amount)s, %(category)s, %(product_name)s, %(source_id)s)
ON CONFLICT (transaction_id) DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    purchased_at = EXCLUDED.purchased_at,
    amount = EXCLUDED.amount,
    category = EXCLUDED.category,
    product_name = EXCLUDED.product_name,
    source_id = EXCLUDED.source_id,
    updated_at = now()
"""

UPSERT_INTERACTION = """
INSERT INTO interactions (interaction_id, customer_id, interaction_type, occurred_at, product_name, source_id)
VALUES (%(interaction_id)s, %(customer_id)s, %(interaction_type)s, %(occurred_at)s, %(product_name)s, %(source_id)s)
ON CONFLICT (interaction_id) DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    interaction_type = EXCLUDED.interaction_type,
    occurred_at = EXCLUDED.occurred_at,
    product_name = EXCLUDED.product_name,
    source_id = EXCLUDED.source_id,
    updated_at = now()
"""

UPSERT_CAMPAIGN_EVENT = """
INSERT INTO campaign_events (campaign_id, customer_id, event_type, occurred_at, source_id)
VALUES (%(campaign_id)s, %(customer_id)s, %(event_type)s, %(occurred_at)s, %(source_id)s)
ON CONFLICT (campaign_id, customer_id, event_type, occurred_at) DO UPDATE SET
    source_id = EXCLUDED.source_id
"""


def save_dataset(
    conn: psycopg.Connection, dataset: NormalizedDataset, source_id: int | None = None
) -> dict[str, int]:
    """Persiste el dataset completo en una sola transaccion, sellando la procedencia."""
    def con_fuente(entidad) -> dict:
        registro = entidad.model_dump(mode="json")
        registro["source_id"] = source_id
        return registro

    with conn.transaction():
        with conn.cursor() as cur:
            cur.executemany(UPSERT_CUSTOMER, [con_fuente(c) for c in dataset.customers])
            cur.executemany(UPSERT_TRANSACTION, [con_fuente(t) for t in dataset.transactions])
            cur.executemany(UPSERT_INTERACTION, [con_fuente(i) for i in dataset.interactions])
            cur.executemany(UPSERT_CAMPAIGN_EVENT, [con_fuente(e) for e in dataset.campaign_events])
    return {
        "customers": len(dataset.customers),
        "transactions": len(dataset.transactions),
        "interactions": len(dataset.interactions),
        "campaign_events": len(dataset.campaign_events),
    }
