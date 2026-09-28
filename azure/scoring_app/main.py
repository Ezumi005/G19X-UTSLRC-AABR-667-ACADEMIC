"""Servicio de scoring del Motor de Segmentacion (Azure App Service).

Expone el mismo contrato que azure/score.py (Azure ML) sobre el MISMO artefacto
(models/kmeans_local.pkl desplegado junto a este archivo). Lo consume unicamente
el backend del Motor de Segmentacion, autenticado con X-API-Key.
"""

from __future__ import annotations

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
app = FastAPI(title="Scoring Motor de Segmentacion", version="1.0.0")


@app.on_event("startup")
def cargar_artefacto() -> None:
    global ARTIFACT
    ARTIFACT = joblib.load(ARTIFACT_PATH)


def _verificar_llave(x_api_key: str | None) -> None:
    esperada = os.environ.get("SCORING_API_KEY")
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key invalida o ausente")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "artefacto": ARTIFACT is not None}


@app.post("/score")
def score(payload: dict, x_api_key: str | None = Header(default=None)) -> dict:
    _verificar_llave(x_api_key)
    rows = payload.get("customers") or []
    if not rows:
        raise HTTPException(status_code=400, detail="'customers' vacio")

    prep = ARTIFACT["preparation"]
    cap = float(prep.get("recency_cap_dias") or 0.0)
    matrix = []
    for row in rows:
        recency = row.get("recency_days")
        if recency is None:
            recency = cap
        matrix.append([float(recency)] + [float(row[c]) for c in FEATURES[1:]])

    x = np.array(matrix, dtype=float)
    for column in prep["log_columns"]:
        index = prep["feature_columns"].index(column)
        x[:, index] = np.log1p(x[:, index])
    xs = ARTIFACT["scaler"].transform(x)
    clusters = ARTIFACT["model"].predict(xs)
    return {"clusters": [int(c) for c in clusters]}
