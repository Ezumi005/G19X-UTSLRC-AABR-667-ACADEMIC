"""Pruebas de audiencias dinamicas (creacion, recalculo, exportacion y borrado)."""

from fastapi.testclient import TestClient

from src.api.app import create_app

client = TestClient(create_app())

CONDICIONES = {
    "name": "Prueba QA - nuevos activos",
    "description": "Audiencia de prueba automatizada",
    "conditions": {"segment": "Clientes nuevos", "min_frequency": 1},
}


def prueba_crear_y_detalle():
    r = client.post("/audiences", json=CONDICIONES)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["name"] == CONDICIONES["name"]
    assert body["n_customers"] > 0
    detalle = client.get(f"/audiences/{body['audience_id']}").json()
    assert detalle["members_total"] == detalle["n_customers"]
    for m in detalle["members"]:
        assert m["segment_label"] == "Clientes nuevos"
        assert m["frequency"] >= 1
    return body["audience_id"]


def prueba_listado():
    r = client.get("/audiences")
    assert r.status_code == 200
    assert any(a["name"] == CONDICIONES["name"] for a in r.json()["data"])


def prueba_export_csv():
    listado = client.get("/audiences").json()["data"]
    aid = next(a["audience_id"] for a in listado if a["name"] == CONDICIONES["name"])
    r = client.get(f"/audiences/{aid}/export")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    lineas = r.text.strip().splitlines()
    assert lineas[0].startswith("customer_id")
    assert len(lineas) >= 2


def prueba_validacion_y_errores():
    invalida = {"name": "x", "conditions": {"min_frequency": -1}}
    assert client.post("/audiences", json=invalida).status_code == 422
    assert client.get("/audiences/99999").status_code == 404
    assert client.delete("/audiences/99999").status_code == 404


def prueba_borrado(audience_id: int):
    assert client.delete(f"/audiences/{audience_id}").status_code == 200
    assert client.get(f"/audiences/{audience_id}").status_code == 404


if __name__ == "__main__":
    aid = prueba_crear_y_detalle()
    prueba_listado()
    prueba_export_csv()
    prueba_validacion_y_errores()
    prueba_borrado(aid)
    print("OK: audiencias verificadas (crear, recalcular, exportar CSV, validar y borrar)")
