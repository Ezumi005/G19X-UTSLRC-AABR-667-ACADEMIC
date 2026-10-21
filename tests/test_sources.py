"""Pruebas de fuentes CSV dinamicas (subir, mapear, validar, sincronizar, borrar)."""

import io
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.persistence.db import connect

client = TestClient(create_app())

CSV_CLIENTES = io.BytesIO(
    "ident,edad,ciudad,alta\nC-TEST-1,30,Guadalajara,2025-05-10\nC-TEST-2,,Merida,2024-01-15\nBAD,999,CDMX,fecha-mala\n".encode(
        "utf-8"
    )
)
MAPEO = {"customer_id": "ident", "age": "edad", "city": "ciudad", "registered_at": "alta"}


def _subir_y_crear() -> int:
    r = client.post("/sources/csv/upload", files={"archivo": ("clientes.csv", CSV_CLIENTES, "text/csv")})
    assert r.status_code == 200, r.text
    subida = r.json()
    assert set(MAPEO.values()) <= set(subida["columns"])
    token = subida["upload_token"]

    validacion = client.post("/sources/csv/validate", json={"name": "QA clientes", "entity": "customers", "upload_token": token, "mapping": MAPEO})
    assert validacion.status_code == 200, validacion.text
    detalle = validacion.json()
    assert detalle["read"] == 3 and detalle["accepted"] == 2 and detalle["rejected"] == 1
    assert len(detalle["preview"]) == 2

    creacion = client.post("/sources/csv", json={"name": "QA clientes", "entity": "customers", "upload_token": token, "mapping": MAPEO})
    assert creacion.status_code == 200, creacion.text
    return creacion.json()["source_id"]


def prueba_mapeo_incompleto_rechazado():
    r = client.post(
        "/sources/csv/validate",
        json={"name": "x", "entity": "customers", "upload_token": "tokeninexistente1", "mapping": {"age": "edad"}},
    )
    assert r.status_code == 400
    assert "obligatorio" in r.json()["detail"]


def prueba_listado_y_sync():
    source_id = _subir_y_crear()
    listado = client.get("/sources").json()
    assert any(s["source_id"] == source_id for s in listado["data"])
    assert listado["data"][0]["type"] == "simulada"

    sync = client.post(f"/sources/{source_id}/sync")
    assert sync.status_code == 200, sync.text
    cuerpo = sync.json()
    assert cuerpo["customers_read"] == 3 and cuerpo["customers_saved"] == 2

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT customer_id, city FROM customers WHERE customer_id IN ('C-TEST-1','C-TEST-2') ORDER BY customer_id")
            filas = cur.fetchall()
    assert filas == [("C-TEST-1", "Guadalajara"), ("C-TEST-2", "Merida")]

    detalle = client.get("/sources").json()
    fuente = next(s for s in detalle["data"] if s["source_id"] == source_id)
    assert fuente["last_sync_at"] is not None
    return source_id


def prueba_limpieza(source_id: int):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM customers WHERE customer_id LIKE 'C-TEST-%'")
    assert client.delete(f"/sources/{source_id}").status_code == 200
    assert client.delete(f"/sources/{source_id}").status_code == 404


def prueba_sugerencia_ia_con_mock():
    """La sugerencia de la IA se filtra por columnas existentes y llega normalizada."""
    r = client.post("/sources/csv/upload", files={"archivo": ("clientes.csv", CSV_CLIENTES, "text/csv")})
    token = r.json()["upload_token"]

    def ia_fake(columns, sample_rows):
        return {
            "entity": "customers",
            "mapping": {"customer_id": "ident", "registered_at": "alta", "city": "ciudad", "age": "edad", "customer_note": "columna_inexistente"},
            "unused_columns": ["columna_rara"],
            "confidence": 92,
            "notes": "ok",
        }

    with patch("src.api.routes.sources.suggest_mapping", side_effect=ia_fake):
        respuesta = client.post("/sources/csv/suggest", json={"upload_token": token})
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["entity"] == "customers"
    assert cuerpo["mapping"] == {"customer_id": "ident", "registered_at": "alta", "city": "ciudad", "age": "edad"}
    assert cuerpo["missing_required"] == []
    assert "columna_inexistente" not in cuerpo["mapping"]


def prueba_sugerencia_ia_no_disponible():
    """Sin IA disponible, el endpoint responde 503 y el flujo manual sigue vivo."""
    csv_fresco = io.BytesIO(b"ident,alta\nC-1,2025-01-01\n")
    subida = client.post("/sources/csv/upload", files={"archivo": ("x.csv", csv_fresco, "text/csv")})
    token = subida.json()["upload_token"]
    with patch("src.api.routes.sources.suggest_mapping", side_effect=RuntimeError("Azure OpenAI no configurado")):
        r = client.post("/sources/csv/suggest", json={"upload_token": token})
    assert r.status_code == 503
    assert "no configurado" in r.json()["detail"]


def prueba_csv_mal_estructurado_controlado():
    """Un CSV con fila rota despues de la muestra responde 422 en la validacion en seco, no 500."""
    buenas = "\n".join(["ident,edad,ciudad,alta"] + [f"C-{i},30,Guadalajara,2025-05-10" for i in range(1, 6)])
    roto = io.BytesIO((buenas + "\nC-6,30,Guadalajara,2025-05-10,campoextra\n").encode("utf-8"))
    subida = client.post("/sources/csv/upload", files={"archivo": ("roto.csv", roto, "text/csv")})
    assert subida.status_code == 200, subida.text
    token = subida.json()["upload_token"]
    r = client.post(
        "/sources/csv/validate",
        json={"name": "x", "entity": "customers", "upload_token": token, "mapping": MAPEO},
    )
    assert r.status_code == 422, r.text
    assert "no se pudo procesar" in r.json()["detail"]


def prueba_token_invalido_controlado():
    """Un upload_token malicioso (path traversal) se rechaza con 400, nunca llega al filesystem."""
    for malo in ["../../.envx", "../secretos", "..\\..\\windows"]:
        r = client.post(
            "/sources/csv/validate",
            json={"name": "x", "entity": "customers", "upload_token": malo, "mapping": MAPEO},
        )
        assert r.status_code == 400, f"{malo}: {r.status_code}"
        assert "Token" in r.json()["detail"]


if __name__ == "__main__":
    prueba_mapeo_incompleto_rechazado()
    prueba_token_invalido_controlado()
    prueba_csv_mal_estructurado_controlado()
    sid = prueba_listado_y_sync()
    prueba_limpieza(sid)
    prueba_sugerencia_ia_con_mock()
    prueba_sugerencia_ia_no_disponible()
    print("OK: fuentes CSV verificadas (manual + token seguro + 422 controlado + IA con mock + degradacion 503)")
