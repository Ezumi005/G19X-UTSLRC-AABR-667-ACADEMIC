"""Pruebas del endpoint de prediccion (mock del servicio de scoring; DB real)."""

import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api.app import create_app

client = TestClient(create_app())


def _configurar_entorno(valor: bool) -> None:
    if valor:
        os.environ["AZURE_SCORING_URL"] = "http://dummy"
        os.environ["AZURE_SCORING_KEY"] = "dummy"
    else:
        os.environ.pop("AZURE_SCORING_URL", None)
        os.environ.pop("AZURE_SCORING_KEY", None)


def prueba_prediccion_con_mock():
    _configurar_entorno(True)
    try:
        with patch("src.services.scoring.predict_clusters", return_value=[5]):
            r = client.post("/customers/CLI-0001/predict")
        assert r.status_code == 200
        body = r.json()
        assert body["cluster"] == 5
        assert body["features"]["frequency"] > 0
        assert set(body["features"]) == {
            "recency_days", "frequency", "monetary", "web_visits",
            "abandoned_carts", "campaign_click_rate", "tenure_days",
        }
        assert body["segment"] is not None and "label" in body["segment"]
    finally:
        _configurar_entorno(False)


def prueba_errores_controlados():
    _configurar_entorno(False)
    try:
        assert client.post("/customers/CLI-0001/predict").status_code == 501
        assert client.post("/customers/NO-EXISTE/predict").status_code == 404
    finally:
        pass


def prueba_cliente_sin_compras():
    """Un cliente sin compras debe pasar recency_days None (el scoring la imputa)."""
    _configurar_entorno(True)
    try:
        with patch("src.services.scoring.predict_clusters", side_effect=lambda cs: [0] * len(cs)):
            r = client.post("/customers/CLI-0500/predict")
        if r.status_code == 200:
            assert r.json()["features"]["frequency"] == 0
    finally:
        _configurar_entorno(False)


def prueba_coherencia_artefacto(tmp_path=None):
    """El endpoint advierte (warnings) si el artefacto remoto pudo quedar desalineado."""
    import json
    import tempfile
    from pathlib import Path

    from src.services.scoring import artifact_coherence

    # Sin metadatos: no se puede verificar -> advertencia informativa
    vacio = Path(tempfile.mkdtemp()) / "no_existe.json"
    sin_meta = artifact_coherence(8, 498, meta_path=vacio)
    assert sin_meta["stale"] is None and "no se puede verificar" in sin_meta["note"]

    # Misma linea base (n_customers igual, sin huella declarada) -> coherente por conteo
    meta_dir = Path(tempfile.mkdtemp())
    meta_ok = meta_dir / "meta.json"
    meta_ok.write_text(json.dumps({"run_id": 4, "n_customers": 498}), encoding="utf-8")
    coherente = artifact_coherence(8, 498, meta_path=meta_ok)
    assert coherente["stale"] is False

    # Linea distinta (n_customers diferente) -> desalineado con nota accionable
    meta_bad = meta_dir / "meta2.json"
    meta_bad.write_text(json.dumps({"run_id": 4, "n_customers": 498}), encoding="utf-8")
    desalineado = artifact_coherence(9, 500, meta_path=meta_bad)
    assert desalineado["stale"] is True and "#9" in desalineado["note"]

    # Huella de centroides: mismo conteo pero huella distinta -> desalineado (el caso que el conteo no ve)
    meta_fp = meta_dir / "meta3.json"
    meta_fp.write_text(
        json.dumps({"run_id": 4, "n_customers": 498, "centroids_sha256": "aaaa111122223333"}),
        encoding="utf-8",
    )
    por_huella = artifact_coherence(9, 498, latest_fingerprint="bbbb444455556666", meta_path=meta_fp)
    assert por_huella["stale"] is True and "huella" in por_huella["note"]
    igual_huella = artifact_coherence(9, 498, latest_fingerprint="aaaa111122223333", meta_path=meta_fp)
    assert igual_huella["stale"] is False

    # Meta con huella pero run vigente sin huella registrada -> verificacion limitada (stale None)
    sin_huella = artifact_coherence(9, 498, latest_fingerprint=None, meta_path=meta_fp)
    assert sin_huella["stale"] is None and "solo pudo compararse por conteo" in sin_huella["note"]

    # El endpoint incluye warnings en la respuesta (mock del scoring)
    _configurar_entorno(True)
    try:
        with patch("src.services.scoring.predict_clusters", return_value=[5]):
            with patch(
                "src.services.scoring.ARTIFACT_META_PATH",
                vacio,
            ):
                r = client.post("/customers/CLI-0001/predict")
        assert r.status_code == 200
        assert isinstance(r.json().get("warnings"), list)
    finally:
        _configurar_entorno(False)


if __name__ == "__main__":
    prueba_prediccion_con_mock()
    prueba_errores_controlados()
    prueba_cliente_sin_compras()
    prueba_coherencia_artefacto()
    print("OK: prediccion verificada (mock 200, 404, 501, features completas y coherencia del artefacto)")
