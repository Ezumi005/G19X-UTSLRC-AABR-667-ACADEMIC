"""Pruebas de integracion de la API principal (requieren PostgreSQL con datos y .env).

Cubren los 8 endpoints del MVP, incluidos los casos de error (404, 501 y 502
cuando el simulador no esta disponible).
"""

from fastapi.testclient import TestClient

from src.api.app import create_app

client = TestClient(create_app())

ETIQUETAS_ESPERADAS = {
    "Clientes frecuentes de alto valor",
    "Navegadores sin compra",
    "Compradores ocasionales",
    "Clientes nuevos",
    "Navegadores con compra esporádica",
    "Clientes en riesgo de inactividad",
}


def prueba_health_y_raiz():
    assert client.get("/health").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    raiz = client.get("/").json()
    assert "endpoints" in raiz


def prueba_clientes():
    r = client.get("/customers", params={"limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 5 and body["total"] >= 498
    fila = body["data"][0]
    assert {"customer_id", "age", "city", "registered_at", "segment_label"} <= set(fila)


def prueba_filtros_clientes():
    r = client.get("/customers", params={"segment": "Clientes nuevos", "limit": 100})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] > 0
    assert all(f["segment_label"] == "Clientes nuevos" for f in body["data"])
    r2 = client.get("/customers", params={"q": "CLI-01", "limit": 500})
    assert r2.status_code == 200
    assert all(f["customer_id"].startswith("CLI-01") for f in r2.json()["data"])
    r3 = client.get("/customers", params={"city": "Monterrey", "limit": 100})
    assert r3.status_code == 200
    assert all(f["city"] == "Monterrey" for f in r3.json()["data"])


def prueba_runs_segmentacion():
    r = client.get("/segmentation/runs")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    run = body["data"][0]
    assert {"run_id", "k", "status", "n_customers", "metrics", "started_at"} <= set(run)
    assert run["metrics"]["silhouette"] > 0


def prueba_detalle_cliente():
    r = client.get("/customers/CLI-0001")
    assert r.status_code == 200
    body = r.json()
    assert body["stats"]["frequency"] > 0
    assert body["segment"] is not None and "label" in body["segment"]
    assert client.get("/customers/NO-EXISTE").status_code == 404


def prueba_segmentos():
    r = client.get("/segments")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 6 and body["run_id"] is not None
    assert {s["label"] for s in body["data"]} == ETIQUETAS_ESPERADAS
    detalle = client.get("/segments/1").json()
    assert "profile" in detalle and "customers_preview" in detalle
    assert client.get("/segments/9999").status_code == 404


def prueba_recomendaciones():
    r = client.get("/segments/1/recommendation")
    assert r.status_code == 200
    assert "recommendation" in r.json()
    assert client.get("/segments/9999/recommendation").status_code == 404
    assert client.post("/segments/9999/recommendation").status_code == 404


def prueba_ingestion_sin_simulador():
    """Sin simulador en 8001, la ingesta debe responder 502 (error controlado)."""
    r = client.post("/ingestion/sync")
    assert r.status_code == 502
    assert "no disponible" in r.json()["detail"].lower()


def prueba_dashboard():
    body = client.get("/dashboard").json()
    assert body["total_customers"] >= 498
    assert body["total_transactions"] > 0
    assert len(body["segments_distribution"]) == 6
    assert body["last_segmentation"] is not None
    assert len(body["segments_profile"]) == 6
    assert "monetary" in body["segments_profile"][0]
    assert len(body["top_categories"]) > 0


def prueba_error_interno_controlado():
    """Un fallo inesperado debe responder 500 controlado, sin filtrar stack traces."""
    from unittest.mock import patch

    import src.api.routes.customers as customers_route
    from src.api.app import create_app

    cliente_500 = TestClient(create_app(), raise_server_exceptions=False)
    with patch.object(customers_route.queries, "list_customers", side_effect=RuntimeError("boom interno")):
        r = cliente_500.get("/customers")
    assert r.status_code == 500
    assert r.json() == {"detail": "Error interno del servidor"}


if __name__ == "__main__":
    prueba_health_y_raiz()
    prueba_clientes()
    prueba_filtros_clientes()
    prueba_runs_segmentacion()
    prueba_detalle_cliente()
    prueba_segmentos()
    prueba_recomendaciones()
    prueba_ingestion_sin_simulador()
    prueba_dashboard()
    prueba_error_interno_controlado()
    print("OK: API verificada (health, clientes, filtros, runs, segmentos, recomendaciones, 404/502, dashboard, 500)")
