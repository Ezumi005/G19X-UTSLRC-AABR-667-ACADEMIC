"""Cliente del servicio de scoring de inferencia en Azure (App Service).

El backend es el unico consumidor del endpoint remoto (React nunca lo toca,
README seccion 7). Degrada de forma controlada: sin configuracion -> la API
responde 501 informativo; con el servicio caido -> 502.

Nota: el plan gratuito (F1) "duerme" la app tras un rato sin uso; el primer
request puede tardar decenas de segundos (arranque en frio). Por eso se usa
un timeout largo y un reintento automatico.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

TIMEOUT_SEGUNDOS = 90
INTENTOS = 2

# Metadatos del artefacto desplegado en Azure App Service (versionado: describe
# con que run/linea de datos se entreno el modelo remoto que sirve /score).
ARTIFACT_META_PATH = Path(__file__).resolve().parents[2] / "models" / "artefacto_desplegado.json"


def scoring_available() -> bool:
    return bool(os.environ.get("AZURE_SCORING_URL") and os.environ.get("AZURE_SCORING_KEY"))


def artifact_coherence(
    latest_run_id: int | None,
    latest_n_customers: int | None,
    meta_path: Path | None = None,
) -> dict:
    """Compara el run vigente con el run que entreno el artefacto desplegado.

    El artefacto remoto NO se reentrena al pulsar "Recalcular segmentos" (que
    reentrena en local): si los datos cambian, el cluster devuelto por Azure
    puede dejar de corresponder con los segmentos vigentes. Esta funcion lo
    detecta para que la API pueda advertirlo en la respuesta (nunca ocultarlo).
    """
    ruta = meta_path or ARTIFACT_META_PATH
    if not ruta.exists():
        return {
            "stale": None,
            "note": (
                "No hay metadatos del artefacto desplegado (models/artefacto_desplegado.json): "
                "no se puede verificar que el modelo de Azure corresponda al run vigente."
            ),
        }
    meta = json.loads(ruta.read_text(encoding="utf-8"))
    base_run = meta.get("run_id")
    base_n = meta.get("n_customers")
    if latest_run_id is None:
        return {"stale": None, "note": "Sin segmentacion vigente con la que comparar."}
    if base_n is not None and latest_n_customers is not None and int(base_n) != int(latest_n_customers):
        return {
            "stale": True,
            "note": (
                f"El artefacto de Azure se entreno con el run #{base_run} ({base_n} clientes) y el run "
                f"vigente es el #{latest_run_id} ({latest_n_customers} clientes): el cluster puede no "
                "corresponder con los segmentos vigentes. Realinea re-exportando el artefacto y "
                "redesplegando (README seccion 7)."
            ),
        }
    return {
        "stale": False,
        "note": f"Artefacto entrenado con la misma linea base del run vigente (run #{base_run}, {base_n} clientes).",
    }


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


def export_metadata(run_id: int | None, n_customers: int | None) -> dict:
    """Contexto que acompagna a un artefacto recien exportado (save_artifact lo escribe junto al .pkl)."""
    return {
        "run_id": run_id,
        "n_customers": n_customers,
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }
