"""Servicio de scoring del Motor de Segmentacion (Azure App Service).

Expone el mismo contrato que azure/score.py (Azure ML) sobre el MISMO artefacto
(models/kmeans_local.pkl desplegado junto a este archivo). Lo consume unicamente
el backend del Motor de Segmentacion, autenticado con X-API-Key.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, Header, HTTPException

ARTIFACT_PATH = Path(__file__).resolve().parent / "kmeans_local.pkl"
FEATURES = [
    "recency_days",
    "frequency",
    "monetary",
    "web_visits",
    "abandoned_carts",
    "campaign_click_rate",
    "tenure_days",
]

ARTIFACT: dict | None = None
HUELLA: str | None = None
app = FastAPI(title="Scoring Motor de Segmentacion", version="1.1.0")


def huella_centroides(centros) -> str:
    """Misma definicion que src.ml.clustering.centroids_fingerprint: sha256 corto
    de los centroides redondeados. Debe mantenerse sincronizada con ella."""
    blob = np.round(np.asarray(centros, dtype=float), 6).tobytes()
    return hashlib.sha256(blob).hexdigest()[:16]


@app.on_event("startup")
def cargar_artefacto() -> None:
    global ARTIFACT, HUELLA
    try:
        ARTIFACT = joblib.load(ARTIFACT_PATH)
        HUELLA = huella_centroides(ARTIFACT["model"].cluster_centers_)
    except FileNotFoundError:
        # Sin artefacto junto al servicio (p. ej. CI o despliegue incompleto):
        # el servicio arranca y lo declara en /health y /score, en vez de caer.
        ARTIFACT = None
        HUELLA = None


def _verificar_llave(x_api_key: str | None) -> None:
    esperada = os.environ.get("SCORING_API_KEY")
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key invalida o ausente")


@app.get("/health")
def health() -> dict:
    """El servicio se autodescribe: reporta la huella del modelo que REALMENTE
    sirve, para que el backend detecte desfases sin depender de metadatos fijos."""
    return {"status": "ok", "artefacto": ARTIFACT is not None, "huella": HUELLA}


@app.post("/score")
def score(payload: dict, x_api_key: str | None = Header(default=None)) -> dict:
    _verificar_llave(x_api_key)
    if ARTIFACT is None:
        raise HTTPException(
            status_code=503,
            detail="El servicio de scoring arranco sin artefacto: despliega kmeans_local.pkl junto a este servicio.",
        )
    rows = payload.get("customers") or []
    if not rows:
        raise HTTPException(status_code=400, detail="'customers' vacio")
    for row in rows:
        if not isinstance(row, dict) or any(c not in row for c in FEATURES[1:]):
            raise HTTPException(
                status_code=400,
                detail="Cada cliente debe ser un objeto con las features del contrato de scoring.",
            )

    prep = ARTIFACT["preparation"]
    cap = float(prep.get("recency_cap_dias") or 0.0)
    matrix = []
    for posicion, row in enumerate(rows):
        try:
            recency = row.get("recency_days")
            if recency is None:
                recency = cap
            matrix.append([float(recency)] + [float(row[c]) for c in FEATURES[1:]])
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"El cliente en la posicion {posicion} trae features no numericas o nulas: "
                    "las 7 features del contrato de scoring deben ser numeros (recency_days puede ser null)."
                ),
            ) from exc

    x = np.array(matrix, dtype=float)
    for column in prep["log_columns"]:
        index = prep["feature_columns"].index(column)
        x[:, index] = np.log1p(x[:, index])
    xs = ARTIFACT["scaler"].transform(x)
    clusters = ARTIFACT["model"].predict(xs)
    return {"clusters": [int(c) for c in clusters]}
