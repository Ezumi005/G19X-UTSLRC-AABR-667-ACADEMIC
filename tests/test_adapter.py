"""Pruebas unitarias del SimulatedCRMAdapter (sin necesidad de la API encendida).

Cubren: mapeo de campos externos al contrato, conversion de tipos, enums
canonicos (incluido el escape a OTROS), descarte de valores desconocidos y
reporte de registros invalidos.
"""

from datetime import datetime, timezone

from src.adapters.base import AdapterReport
from src.adapters.simulated_crm_adapter import (
    _convert,
    transform_campaign_event,
    transform_customer,
    transform_interaction,
    transform_transaction,
)
from src.contracts import CampaignEventType, InteractionType, ProductCategory

UTC = timezone.utc

CLIENTE = {
    "clientId": "CLI-0001",
    "demographics": {"age": 35, "city": "Monterrey"},
    "memberSince": "2023-10-22",
}

TRANSACCION = {
    "opId": "TRX-00001",
    "clientId": "CLI-0001",
    "ts": "2026-07-14T15:30:00Z",
    "totalAmount": "1250.50",
    "productLine": "ELECTRONICS",
    "itemName": "Laptop X14",
}

INTERACCION = {
    "eventId": "EVT-000001",
    "clientId": "CLI-0001",
    "kind": "PRODUCT_CONSULT",
    "eventTs": "2026-08-14T19:30:19Z",
    "item": "Monitor 27",
}

EVENTO = {
    "campId": "CAMP-2026-09",
    "clientId": "CLI-0001",
    "action": "OPEN",
    "actionTs": "2026-09-05T10:17:00Z",
}


def prueba_mapeo_cliente():
    c = transform_customer(CLIENTE)
    assert c.customer_id == "CLI-0001"
    assert c.age == 35
    assert c.city == "Monterrey"
    assert c.registered_at == datetime(2023, 10, 22, tzinfo=UTC)
    sin_demo = {"clientId": "CLI-2", "memberSince": "2024-01-05"}
    c2 = transform_customer(sin_demo)
    assert c2.age is None and c2.city is None


def prueba_mapeo_transaccion():
    t = transform_transaction(TRANSACCION)
    assert t.transaction_id == "TRX-00001"
    assert t.customer_id == "CLI-0001"
    assert t.purchased_at == datetime(2026, 7, 14, 15, 30, tzinfo=UTC)
    assert isinstance(t.amount, float) and t.amount == 1250.50
    assert t.category is ProductCategory.ELECTRONICA
    assert t.product_name == "Laptop X14"


def prueba_escape_categorias():
    casos = {
        "BOOKS": ProductCategory.OTROS,
        "GARDEN_TOOLS": ProductCategory.OTROS,
        "CRYPTO": ProductCategory.OTROS,
        "GROCERIES": ProductCategory.ALIMENTOS,
        "TOYS": ProductCategory.JUGUETES,
    }
    for externo, esperado in casos.items():
        crudo = dict(TRANSACCION, productLine=externo)
        assert transform_transaction(crudo).category is esperado, externo


def prueba_mapeo_interaccion():
    tipos = {
        "WEB_SESSION": InteractionType.WEB_VISIT,
        "PRODUCT_CONSULT": InteractionType.PRODUCT_VIEW,
        "CART_LEFT": InteractionType.ABANDONED_CART,
    }
    for externo, esperado in tipos.items():
        crudo = dict(INTERACCION, kind=externo)
        assert transform_interaction(crudo).interaction_type is esperado, externo
    assert transform_interaction(INTERACCION).product_name == "Monitor 27"
    sin_item = {k: v for k, v in INTERACCION.items() if k != "item"}
    assert transform_interaction(sin_item).product_name is None
    try:
        transform_interaction(dict(INTERACCION, kind="PHONE_CALL"))
        raise AssertionError("Se esperaba rechazo por kind desconocido")
    except ValueError:
        pass


def prueba_mapeo_evento_campana():
    acciones = {
        "SEND": CampaignEventType.SENT,
        "DELIVER": CampaignEventType.DELIVERED,
        "OPEN": CampaignEventType.OPENED,
        "CLICK": CampaignEventType.CLICKED,
    }
    for externo, esperado in acciones.items():
        crudo = dict(EVENTO, action=externo)
        assert transform_campaign_event(crudo).event_type is esperado, externo
    try:
        transform_campaign_event(dict(EVENTO, action="BOUNCED"))
        raise AssertionError("Se esperaba rechazo por action desconocida")
    except ValueError:
        pass


def prueba_registros_invalidos_reportados():
    tx_crudas = [
        TRANSACCION,
        dict(TRANSACCION, opId="TRX-BAD-1", totalAmount="-50.00"),
        {k: v for k, v in dict(TRANSACCION, opId="TRX-BAD-2").items() if k != "clientId"},
        dict(TRANSACCION, opId="TRX-BAD-3", ts="fecha-invalida"),
    ]
    aceptadas, incidencias = _convert(tx_crudas, "transactions", transform_transaction)
    assert len(aceptadas) == 1
    assert len(incidencias) == 3
    entidades = {inc.entity for inc in incidencias}
    assert entidades == {"transactions"}

    clientes_crudos = [
        CLIENTE,
        dict(CLIENTE, clientId="CLI-BAD-1", demographics={"age": 999, "city": "CDMX"}),
        dict(CLIENTE, clientId="CLI-BAD-2", memberSince="2025-02-31"),
    ]
    aceptados, inc_clientes = _convert(clientes_crudos, "customers", transform_customer)
    assert len(aceptados) == 1
    assert len(inc_clientes) == 2

    interacciones_crudas = [INTERACCION, dict(INTERACCION, eventId="EVT-BAD-1", kind="PUSH_NOTIFICATION")]
    _, inc_inter = _convert(interacciones_crudas, "interactions", transform_interaction)
    assert len(inc_inter) == 1


def prueba_reporte():
    reporte = AdapterReport(source="prueba")
    aceptadas, incidencias = _convert(
        [TRANSACCION, dict(TRANSACCION, opId="TRX-BAD-1", totalAmount="-1.00")],
        "transactions",
        transform_transaction,
    )
    reporte.add("transactions", 2, len(aceptadas), incidencias)
    assert reporte.read["transactions"] == 2
    assert reporte.accepted["transactions"] == 1
    assert reporte.rejected["transactions"] == 1
    assert reporte.total_rejected == 1
    resumen = reporte.summary()
    assert "transactions" in resumen and "total incidencias: 1" in resumen


if __name__ == "__main__":
    prueba_mapeo_cliente()
    prueba_mapeo_transaccion()
    prueba_escape_categorias()
    prueba_mapeo_interaccion()
    prueba_mapeo_evento_campana()
    prueba_registros_invalidos_reportados()
    prueba_reporte()
    print("OK: SimulatedCRMAdapter verificado (mapeos, enums, escape a otros, invalidos y reporte)")
