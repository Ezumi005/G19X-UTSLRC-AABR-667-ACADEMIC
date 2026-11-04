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
import time
from pathlib import Path

import requests

TIMEOUT_SEGUNDOS = 90
INTENTOS = 2

# Metadatos del artefacto desplegado en Azure App Service (versionado: describe
# con que run/linea de datos se entreno el modelo remoto que sirve /score).
ARTIFACT_META_PATH = Path(__file__).resolve().parents[2] / "models" / "artefacto_desplegado.json"

# Caché corta de la huella que el servicio de scoring reporta de sí mismo.
_CACHE_HUELLA: dict = {"ts": 0.0, "valor": None}
TTL_HUELLA_SEGUNDOS = 60


def scoring_available() -> bool:
    return bool(os.environ.get("AZURE_SCORING_URL") and os.environ.get("AZURE_SCORING_KEY"))


def remote_fingerprint(ttl_segundos: int = TTL_HUELLA_SEGUNDOS) -> str | None:
    """Huella de centroides que el servicio de scoring REALMENTE sirve (su /health).

    Hace autodescriptiva la comprobacion de coherencia: funciona igual contra el
    App Service de Azure que contra una instancia local del mismo servicio, sin
    depender de metadatos fijos en el repositorio. Si el servicio no la reporta
    (despliegues anteriores) o no responde, devuelve None y se usa el respaldo.
    """
    if not scoring_available():
        return None
    ahora = time.time()
    if ahora - _CACHE_HUELLA["ts"] < ttl_segundos:
        return _CACHE_HUELLA["valor"]
    valor = None
    try:
        respuesta = requests.get(f"{os.environ['AZURE_SCORING_URL'].rstrip('/')}/health", timeout=10)
        if respuesta.ok:
            valor = respuesta.json().get("huella")
    except (requests.RequestException, ValueError):
        valor = None
    _CACHE_HUELLA["ts"] = ahora
    _CACHE_HUELLA["valor"] = valor
    return valor


def artifact_coherence(
    latest_run_id: int | None,
    latest_n_customers: int | None,
    latest_fingerprint: str | None = None,
    remote_huella: str | None = None,
    meta_path: Path | None = None,
) -> dict:
    """Compara el run vigente con el modelo que REALMENTE sirve las predicciones.

    Prioridad: la huella que el propio servicio reporta (/health). Si el servicio
    no la declara (despliegues anteriores), respaldo con models/artefacto_desplegado.json
    (conteo de clientes y huella declarada). Nunca se oculta el desfase: se advierte.
    """
    if latest_run_id is None:
        return {"stale": None, "note": "Sin segmentacion vigente con la que comparar."}
    if remote_huella and latest_fingerprint:
        if remote_huella == latest_fingerprint:
            return {
                "stale": False,
                "note": "El servicio de scoring sirve el mismo modelo que el run vigente (huella coincidente).",
            }
        return {
            "stale": True,
            "note": (
                f"El servicio de scoring sirve un modelo con huella {remote_huella} y el run vigente "
                f"#{latest_run_id} tiene huella {latest_fingerprint}: los datos cambiaron desde el "
                "exporte del artefacto y el cluster puede no corresponder. Realinea re-exportando el "
                "artefacto y redesplegando el servicio de scoring (README seccion 7)."
            ),
        }
    if remote_huella and not latest_fingerprint:
        return {
            "stale": None,
            "note": (
                f"El run vigente #{latest_run_id} no registro huella de centroides: la coherencia con el "
                "servicio de scoring no pudo verificarse por huella."
            ),
        }
    ruta = meta_path or ARTIFACT_META_PATH
    if not ruta.exists():
        return {
            "stale": None,
            "note": (
                "El servicio de scoring no reporta su huella y no hay metadatos del artefacto desplegado "
                "(models/artefacto_desplegado.json): no se puede verificar la coherencia del modelo remoto."
            ),
        }
    meta = json.loads(ruta.read_text(encoding="utf-8"))
    base_run = meta.get("run_id")
    base_n = meta.get("n_customers")
    base_fp = meta.get("centroids_sha256")
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
    if base_fp and latest_fingerprint and base_fp != latest_fingerprint:
        return {
            "stale": True,
            "note": (
                f"La huella de centroides del run vigente #{latest_run_id} ({latest_fingerprint}) difiere de la "
                f"del artefacto desplegado ({base_fp}, entrenado con el run #{base_run}): los datos cambiaron "
                "aunque el numero de clientes sea el mismo, y el cluster de Azure puede no corresponder. "
                "Realinea re-exportando el artefacto y redesplegando (README seccion 7)."
            ),
        }
    if base_fp and not latest_fingerprint:
        return {
            "stale": None,
            "note": (
                f"El run vigente #{latest_run_id} no registro huella de centroides: la coherencia con el "
                "artefacto de Azure solo pudo compararse por conteo de clientes."
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
