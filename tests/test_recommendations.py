"""Pruebas unitarias del servicio de recomendaciones (sin llamar a Azure)."""

import json
import os

from src.services.recommendations import (
    azure_openai_available,
    build_messages,
    parse_json_loose,
)

PERFIL = {
    "recency_days": 231.81,
    "frequency": 10.89,
    "monetary": 10349.42,
    "avg_ticket": 947.81,
    "web_visits": 1.27,
    "product_views": 0.68,
    "abandoned_carts": 0.09,
    "emails_opened": 0.84,
    "campaign_click_rate": 0.0,
    "tenure_days": 849.93,
}


def prueba_build_messages():
    mensajes = build_messages("Clientes en riesgo de inactividad", "Contexto", 75, PERFIL)
    assert mensajes[0]["role"] == "system" and "JSON" in mensajes[0]["content"]
    user = mensajes[1]["content"]
    assert "Clientes en riesgo de inactividad" in user
    assert "75 clientes" in user
    assert "dias desde la ultima compra: 231.81" in user
    assert "gasto acumulado: 10349.42" in user


def prueba_parse_json_loose():
    limpio = '{"descripcion": "x", "recomendaciones": ["a"]}'
    assert parse_json_loose(limpio) == json.loads(limpio)
    sucio = 'Aqui va el analisis:\n{"descripcion": "y", "recomendaciones": ["b", "c"]}\nGracias'
    assert parse_json_loose(sucio)["recomendaciones"] == ["b", "c"]
    try:
        parse_json_loose("sin json por ningun lado")
        raise AssertionError("Se esperaba ValueError")
    except ValueError:
        pass


def prueba_disponibilidad_configuracion():
    clave, endpoint = os.environ.pop("AZURE_OPENAI_API_KEY", None), os.environ.pop("AZURE_OPENAI_ENDPOINT", None)
    try:
        assert azure_openai_available() is False
        os.environ["AZURE_OPENAI_API_KEY"] = "dummy"
        assert azure_openai_available() is False
        os.environ["AZURE_OPENAI_ENDPOINT"] = "https://dummy.openai.azure.com/"
        assert azure_openai_available() is True
    finally:
        for var, valor in (("AZURE_OPENAI_API_KEY", clave), ("AZURE_OPENAI_ENDPOINT", endpoint)):
            if valor is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = valor


if __name__ == "__main__":
    prueba_build_messages()
    prueba_parse_json_loose()
    prueba_disponibilidad_configuracion()
    print("OK: recomendaciones verificadas (prompt, parseo tolerante y disponibilidad)")
