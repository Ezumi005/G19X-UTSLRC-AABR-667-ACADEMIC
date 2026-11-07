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
    assert "segmentation_run" in cuerpo, "sincronizar debe intentar re-segmentar con los datos vigentes"

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


def prueba_ciclo_de_vida_completo():
    """Reemplazar el archivo de una fuente, sincronizar, medir impacto y borrarla con sus datos."""
    csv_a = io.BytesIO("ident,edad,ciudad,alta\nR-1,30,Morelia,2024-01-01\nR-2,41,Toluca,2023-05-05\n".encode("utf-8"))
    subida_a = client.post("/sources/csv/upload", files={"archivo": ("a.csv", csv_a, "text/csv")})
    token_a = subida_a.json()["upload_token"]
    creacion = client.post("/sources/csv", json={"name": "Ciclo vida", "entity": "customers", "upload_token": token_a, "mapping": MAPEO})
    sid = creacion.json()["source_id"]
    assert client.post(f"/sources/{sid}/sync").status_code == 200

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT city, source_id FROM customers WHERE customer_id = 'R-1'")
            ciudad, fuente = cur.fetchone()
    assert ciudad == "Morelia" and fuente == sid, "la fila debe quedar sellada con su fuente"

    csv_b = io.BytesIO(
        "ident,edad,ciudad,alta\nR-1,30,Morelia Norte,2024-01-01\nR-2,41,Toluca,2023-05-05\nR-3,22,Puebla,2025-02-02\n".encode("utf-8")
    )
    subida_b = client.post("/sources/csv/upload", files={"archivo": ("b.csv", csv_b, "text/csv")})
    token_b = subida_b.json()["upload_token"]
    reemplazo = client.post(f"/sources/{sid}/replace", json={"upload_token": token_b, "mapping": MAPEO})
    assert reemplazo.status_code == 200, reemplazo.text
    assert client.post(f"/sources/{sid}/sync").status_code == 200

    impacto = client.get(f"/sources/{sid}/impact").json()
    assert impacto["customers"] == 3, impacto

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT city FROM customers WHERE customer_id = 'R-1'")
            assert cur.fetchone()[0] == "Morelia Norte", "el reemplazo debe actualizar al sincronizar"

    borrado = client.delete(f"/sources/{sid}")
    assert borrado.status_code == 200, borrado.text
    assert borrado.json()["rows_removed"]["customers"] == 3, "eliminar debe retirar tambien los datos de la fuente"
    assert "segmentation_run" in borrado.json(), "tras retirar datos, los segmentos se regeneran con lo que queda"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM customers WHERE customer_id IN ('R-1','R-2','R-3')")
            assert cur.fetchone()[0] == 0, "borrar con datos debe retirar las filas de la fuente"
    assert client.get(f"/sources/{sid}/impact").status_code == 200


def prueba_impacto_y_fuente_inexistente():
    """El impacto de la fuente integrada es de solo lectura; una fuente inexistente da 404."""
    impacto = client.get("/sources/0/impact").json()
    assert set(impacto) == {"customers", "transactions", "interactions", "campaign_events"}
    assert client.get("/sources/999999/impact").json() == {
        "customers": 0,
        "transactions": 0,
        "interactions": 0,
        "campaign_events": 0,
    }
    assert client.delete("/sources/999999").status_code == 404


def prueba_excel_subida_y_flujo():
    """Un .xlsx sube, se convierte y recorre el mismo flujo que un CSV (validar, crear, sincronizar, borrar)."""
    import io as _io

    import pandas as pd

    df = pd.DataFrame(
        [
            {"ident": "C-XLSX-1", "edad": 30, "ciudad": "Guadalajara", "alta": "2025-05-10"},
            {"ident": "C-XLSX-2", "edad": None, "ciudad": "Merida", "alta": "2024-01-15"},
            {"ident": "BAD", "edad": 999, "ciudad": "CDMX", "alta": "fecha-mala"},
        ]
    )
    buffer = _io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    subida = client.post(
        "/sources/csv/upload",
        files={"archivo": ("clientes.xlsx", buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert subida.status_code == 200, subida.text
    cuerpo = subida.json()
    assert cuerpo["filename"] == "clientes.xlsx"
    assert set(MAPEO.values()) <= set(cuerpo["columns"])

    validacion = client.post(
        "/sources/csv/validate",
        json={"name": "QA excel", "entity": "customers", "upload_token": cuerpo["upload_token"], "mapping": MAPEO},
    )
    assert validacion.status_code == 200, validacion.text
    assert validacion.json()["read"] == 3 and validacion.json()["accepted"] == 2

    creacion = client.post(
        "/sources/csv",
        json={"name": "QA excel", "entity": "customers", "upload_token": cuerpo["upload_token"], "mapping": MAPEO},
    )
    sid = creacion.json()["source_id"]
    assert client.post(f"/sources/{sid}/sync").status_code == 200
    borrado = client.delete(f"/sources/{sid}")
    assert borrado.status_code == 200
    assert borrado.json()["rows_removed"]["customers"] == 2


def prueba_extension_rechazada():
    r = client.post("/sources/csv/upload", files={"archivo": ("datos.txt", io.BytesIO(b"a,b\n1,2\n"), "text/plain")})
    assert r.status_code == 400
    assert ".csv o .xlsx" in r.json()["detail"]


def prueba_incidencias_legibles():
    """Las incidencias del CSV mencionan el campo y el motivo completo, sin volcado Pydantic truncado."""
    csv_malo = io.BytesIO("ident,edad,ciudad,alta\nC-LEG-1,30,Guadalajara,ayer\n".encode("utf-8"))
    subida = client.post("/sources/csv/upload", files={"archivo": ("legible.csv", csv_malo, "text/csv")})
    token = subida.json()["upload_token"]
    r = client.post(
        "/sources/csv/validate",
        json={"name": "x", "entity": "customers", "upload_token": token, "mapping": MAPEO},
    )
    assert r.status_code == 200, r.text
    incidencias = r.json()["incidents"]
    assert len(incidencias) == 1
    texto = incidencias[0]
    assert "Campo 'registered_at'" in texto, texto
    assert "validation error for" not in texto
    assert len(texto) < 300


if __name__ == "__main__":
    prueba_mapeo_incompleto_rechazado()
    prueba_token_invalido_controlado()
    prueba_csv_mal_estructurado_controlado()
    sid = prueba_listado_y_sync()
    prueba_limpieza(sid)
    prueba_sugerencia_ia_con_mock()
    prueba_sugerencia_ia_no_disponible()
    prueba_ciclo_de_vida_completo()
    prueba_impacto_y_fuente_inexistente()
    prueba_excel_subida_y_flujo()
    prueba_extension_rechazada()
    prueba_incidencias_legibles()
    print("OK: fuentes CSV verificadas (manual + token seguro + 422 controlado + IA con mock + degradacion 503 + ciclo de vida completo con borrado total + Excel xlsx + incidencias legibles)")
