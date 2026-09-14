"""Pruebas del contrato interno V1: entidades validas, rechazos esperados y campos opcionales."""

from datetime import datetime

from pydantic import ValidationError

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


def dataset_valido() -> NormalizedDataset:
    return NormalizedDataset(
        customers=[
            Customer(
                customer_id="C-001",
                age=35,
                city="Monterrey",
                registered_at=datetime(2025, 3, 1, 10, 0, 0),
            )
        ],
        transactions=[
            Transaction(
                transaction_id="T-001",
                customer_id="C-001",
                purchased_at=datetime(2026, 8, 1, 15, 30, 0),
                amount=1250.50,
                category=ProductCategory.ELECTRONICA,
                product_name="Laptop",
            ),
            Transaction(
                transaction_id="T-002",
                customer_id="C-001",
                purchased_at=datetime(2026, 9, 1, 9, 0, 0),
                amount=320.00,
                category="hogar",
            ),
        ],
        interactions=[
            Interaction(
                interaction_id="I-001",
                customer_id="C-001",
                interaction_type=InteractionType.ABANDONED_CART,
                occurred_at=datetime(2026, 9, 5, 18, 45, 0),
                product_name="Monitor",
            )
        ],
        campaign_events=[
            CampaignEvent(
                campaign_id="CMP-01",
                customer_id="C-001",
                event_type=CampaignEventType.OPENED,
                occurred_at=datetime(2026, 9, 2, 8, 15, 0),
            )
        ],
    )


def prueba_dataset_valido():
    ds = dataset_valido()
    assert len(ds.customers) == 1
    assert len(ds.transactions) == 2
    assert ds.transactions[1].category is ProductCategory.HOGAR
    assert ds.interactions[0].interaction_type is InteractionType.ABANDONED_CART
    assert ds.campaign_events[0].event_type is CampaignEventType.OPENED


def prueba_rechazos():
    casos = [
        (
            "monto negativo",
            lambda: Transaction(
                transaction_id="T-X",
                customer_id="C-001",
                purchased_at=datetime(2026, 1, 1),
                amount=-1,
                category="moda",
            ),
        ),
        (
            "categoria fuera del canon",
            lambda: Transaction(
                transaction_id="T-X",
                customer_id="C-001",
                purchased_at=datetime(2026, 1, 1),
                amount=10,
                category="libros",
            ),
        ),
        (
            "edad fuera de rango",
            lambda: Customer(customer_id="C-X", age=200, registered_at=datetime(2026, 1, 1)),
        ),
        (
            "interaction_id vacio",
            lambda: Interaction(
                interaction_id="",
                customer_id="C-001",
                interaction_type="web_visit",
                occurred_at=datetime(2026, 1, 1),
            ),
        ),
        (
            "evento de campana fuera del canon",
            lambda: CampaignEvent(
                campaign_id="CMP",
                customer_id="C-001",
                event_type="bounced",
                occurred_at=datetime(2026, 1, 1),
            ),
        ),
        (
            "fecha invalida",
            lambda: Customer(customer_id="C-X", registered_at="no-es-fecha"),
        ),
    ]
    for nombre, factory in casos:
        try:
            factory()
        except ValidationError:
            continue
        raise AssertionError(f"Se esperaba ValidationError en: {nombre}")


def prueba_campos_opcionales_nulos():
    cliente = Customer(customer_id="C-002", registered_at=datetime(2026, 2, 2))
    assert cliente.age is None
    assert cliente.city is None
    tx = Transaction(
        transaction_id="T-003",
        customer_id="C-002",
        purchased_at=datetime(2026, 2, 2),
        amount=99.9,
        category="alimentos",
    )
    assert tx.product_name is None


if __name__ == "__main__":
    prueba_dataset_valido()
    prueba_rechazos()
    prueba_campos_opcionales_nulos()
    print("OK: contrato interno V1 verificado (entidades, enums, rechazos y opcionales)")
