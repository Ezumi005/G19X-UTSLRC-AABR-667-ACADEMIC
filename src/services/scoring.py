"""Cliente del servicio de scoring de inferencia en Azure (App Service).

El backend es el unico consumidor del endpoint remoto (React nunca lo toca,
README seccion 7). Degrada de forma controlada: sin configuracion -> la API
responde 501 informativo; con el servicio caido -> 502.
"""

from __future__ import annotations

import os

import requests


def scoring_available() -> bool:
    return bool(os.environ.get("AZURE_SCORING_URL") and os.environ.get("AZURE_SCORING_KEY"))


def predict_clusters(customers: list[dict]) -> list[int]:
    """Envia las features (unidades originales) de cada cliente y devuelve su cluster."""
    response = requests.post(
        f"{os.environ['AZURE_SCORING_URL'].rstrip('/')}/score",
        json={"customers": customers},
        headers={"X-API-Key": os.environ["AZURE_SCORING_KEY"]},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["clusters"]
