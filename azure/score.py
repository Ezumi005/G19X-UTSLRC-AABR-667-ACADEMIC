"""Scoring del endpoint de Azure ML: modelo K-Means del motor de segmentacion.

Entrada (JSON):
{"customers": [{"recency_days": 12.5 o null, "frequency": 3, "monetary": 1500.0,
                "web_visits": 10, "abandoned_carts": 2, "campaign_click_rate": 0.1,
                "tenure_days": 300}, ...]}

Salida (JSON):
{"clusters": [2, 0, ...]}  # cluster del modelo por cliente; la etiqueta comercial
                           # la resuelve el backend contra la tabla segments.

La preparacion (imputacion de recency, log1p, escalado) replica exactamente
src/ml/clustering.py usando la configuracion guardada en el propio artefacto.
"""

import json
import os
from pathlib import Path

import joblib
import numpy as np

ARTIFACT = None


def init():
    global ARTIFACT
    model_dir = os.getenv("AZUREML_MODEL_DIR", ".")
    ARTIFACT = joblib.load(Path(model_dir) / "kmeans_local.pkl")


def run(raw_data):
    try:
        payload = json.loads(raw_data)
        rows = payload["customers"]
        if not rows:
            raise ValueError("lista 'customers' vacia")
    except Exception as exc:
        return json.dumps({"error": f"entrada invalida: {exc}"})

    prep = ARTIFACT["preparation"]
    cap = float(prep.get("recency_cap_dias") or 0.0)
    columns = prep["feature_columns"]

    matrix = []
    for row in rows:
        recency = row.get("recency_days")
        if recency is None:
            recency = cap
        matrix.append([float(recency), float(row["frequency"]), float(row["monetary"]),
                       float(row["web_visits"]), float(row["abandoned_carts"]),
                       float(row["campaign_click_rate"]), float(row["tenure_days"])])

    x = np.array(matrix, dtype=float)
    for column in prep["log_columns"]:
        index = columns.index(column)
        x[:, index] = np.log1p(x[:, index])

    xs = ARTIFACT["scaler"].transform(x)
    clusters = ARTIFACT["model"].predict(xs)
    return json.dumps({"clusters": [int(c) for c in clusters]})
