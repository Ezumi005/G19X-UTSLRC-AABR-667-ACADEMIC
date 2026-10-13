"""Cliente del servicio de scoring de inferencia en Azure (App Service).

El backend es el unico consumidor del endpoint remoto (React nunca lo toca,
README seccion 7). Degrada de forma controlada: sin configuracion -> la API
responde 501 informativo; con el servicio caido -> 502.

Nota: el plan gratuito (F1) "duerme" la app tras un rato sin uso; el primer
request puede tardar decenas de segundos (arranque en frio). Por eso se usa
un timeout largo y un reintento automatico.
"""

from __future__ import annotations

import os

import requests

TIMEOUT_SEGUNDOS = 90
INTENTOS = 2


def scoring_available() -> bool:
    return bool(os.environ.get("AZURE_SCORING_URL") and os.environ.get("AZURE_SCORING_KEY"))


def predict_clusters(customers: list[dict]) -> list[int]:
    """Envia las features (unidades originales) de cada cliente y devuelve su cluster."""
    url = f"{os.environ['AZURE_SCORING_URL'].rstrip('/')}/score"
    ultimo_error: Exception | None = None
    for _ in range(INTENTOS):
        try:
            response = requests.post(
                url,
                json={"customers": customers},
                headers={"X-API-Key": os.environ["AZURE_SCORING_KEY"]},
                timeout=TIMEOUT_SEGUNDOS,
            )
            response.raise_for_status()
            return response.json()["clusters"]
        except requests.RequestException as exc:
            ultimo_error = exc
    raise ultimo_error
