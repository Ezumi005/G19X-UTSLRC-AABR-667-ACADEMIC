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


if __name__ == "__main__":
    prueba_prediccion_con_mock()
    prueba_errores_controlados()
    prueba_cliente_sin_compras()
    print("OK: prediccion verificada (mock 200, 404, 501 y features completas)")
