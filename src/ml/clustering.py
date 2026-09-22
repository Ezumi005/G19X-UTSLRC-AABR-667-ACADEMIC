"""Clustering K-Means local sobre las features RFM + engagement.

Flujo (etapa 7 del orden de desarrollo):
1. Recomputa las features desde PostgreSQL (unica fuente: src/features/rfm.py).
2. Prepara la matriz: imputacion de recency nulo (cap al maximo observado),
   log1p en variables sesgadas y StandardScaler.
3. Evalua k en 2..10 con Silhouette (primario), Inertia (codo) y Davies-Bouldin.
4. Regla pre-declarada de seleccion: mejor Silhouette; empate (dif <= 0.01) -> menor k.
5. Entrena el modelo final, verifica estabilidad (ARI entre semillas) y perfila
   los clusters en unidades originales.
6. Contrasta contra los perfiles reales del simulador (ground truth de
   data/meta.json, solo para validacion).
7. Guarda el artefacto en models/ (no versionado, regenerable con semilla fija).

Los clusters se mantienen como "Cluster 0..N": las etiquetas comerciales se
asignan despues de analizar los resultados (README seccion 6).

Uso (desde la raiz, requiere .env y base con datos):
    .venv/Scripts/python.exe -m src.ml.clustering
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from src.features.rfm import build_features, load_from_postgres

ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data"

SEED = 42
K_RANGE = range(2, 11)

FEATURE_COLUMNS = [
    "recency_days",
    "frequency",
    "monetary",
    "web_visits",
    "abandoned_carts",
    "campaign_click_rate",
    "tenure_days",
]
LOG_COLUMNS = ["frequency", "monetary", "web_visits", "abandoned_carts"]

PROFILE_COLUMNS = FEATURE_COLUMNS + ["avg_ticket", "product_views", "emails_opened"]


def prepare_matrix(
    features: pd.DataFrame,
    feature_columns: list[str] = FEATURE_COLUMNS,
    log_columns: list[str] = LOG_COLUMNS,
) -> tuple[np.ndarray, StandardScaler, dict]:
    """Features -> matriz escalada. Devuelve (X, scaler, info) con el reporte de imputacion."""
    df = features[feature_columns].copy()
    n_null = int(df["recency_days"].isna().sum())
    cap = float(df["recency_days"].max())
    df["recency_days"] = df["recency_days"].fillna(cap)
    for column in log_columns:
        df[column] = np.log1p(df[column])
    x = df.to_numpy(dtype=float)
    scaler = StandardScaler().fit(x)
    xs = scaler.transform(x)
    info = {
        "recency_imputados": n_null,
        "recency_cap_dias": round(cap, 2),
        "feature_columns": feature_columns,
        "log_columns": log_columns,
        "clientes": int(len(df)),
    }
    return xs, scaler, info


def evaluate_ks(xs: np.ndarray, k_range: range = K_RANGE) -> pd.DataFrame:
    """Metricas por k. Regla de seleccion: mejor Silhouette (empate <= 0.01 -> menor k)."""
    rows = []
    for k in k_range:
        model = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(xs)
        rows.append(
            {
                "k": k,
                "silhouette": round(float(silhouette_score(xs, model.labels_)), 4),
                "inertia": round(float(model.inertia_), 1),
                "davies_bouldin": round(float(davies_bouldin_score(xs, model.labels_)), 4),
            }
        )
    return pd.DataFrame(rows)


def choose_k(metrics: pd.DataFrame) -> int:
    best_sil = metrics["silhouette"].max()
    candidatos = metrics[metrics["silhouette"] >= best_sil - 0.01]
    return int(candidatos["k"].min())


def train_kmeans(xs: np.ndarray, k: int, seed: int = SEED) -> KMeans:
    return KMeans(n_clusters=k, random_state=seed, n_init=10).fit(xs)


def stability(xs: np.ndarray, k: int, seeds: tuple[int, ...] = (0, 1, 2, 3, 4)) -> float:
    """ARI promedio entre el modelo de referencia y reentrenamientos con otras semillas."""
    base = train_kmeans(xs, k).labels_
    aris = [adjusted_rand_score(base, train_kmeans(xs, k, seed=s).labels_) for s in seeds]
    return float(np.mean(aris))


def cluster_profiles(features: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """Medias por cluster en unidades originales + tamano. Solo para analisis/interpretacion."""
    out = features.copy()
    out["cluster"] = labels
    grouped = out.groupby("cluster")
    profiles = grouped[PROFILE_COLUMNS].mean().round(2)
    profiles.insert(0, "clientes", grouped.size())
    return profiles


def _ground_truth(features: pd.DataFrame) -> pd.Series | None:
    meta_path = DATA_DIR / "meta.json"
    if not meta_path.exists():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    truth = pd.Series(meta["ground_truth"], name="profile")
    return truth.reindex(features["customer_id"].to_numpy()).to_numpy()


def validate_against_truth(features: pd.DataFrame, labels: np.ndarray) -> tuple[pd.DataFrame, float] | None:
    """Crosstab cluster x perfil real + ARI (validacion analitica, no entrena nada)."""
    truth = _ground_truth(features)
    if truth is None:
        return None
    table = pd.crosstab(pd.Series(labels, name="cluster"), pd.Series(truth, name="perfil_real"))
    ari = adjusted_rand_score(pd.Series(truth).astype("category").cat.codes, labels)
    return table, float(ari)


def save_artifact(model: KMeans, scaler: StandardScaler, info: dict, k: int, metrics_row: dict, stability_ari: float) -> Path:
    MODELS_DIR.mkdir(exist_ok=True)
    path = MODELS_DIR / "kmeans_local.pkl"
    joblib.dump(
        {
            "model": model,
            "scaler": scaler,
            "k": k,
            "metrics": metrics_row,
            "stability_ari": stability_ari,
            "preparation": info,
        },
        path,
    )
    return path


def main() -> None:
    print("--- Features (recomputadas desde PostgreSQL) ---")
    frames = load_from_postgres()
    features = build_features(**frames)

    print("\n--- Correlaciones (justificacion de la seleccion de features) ---")
    print(features[PROFILE_COLUMNS].corr().round(2).to_string())

    xs, scaler, info = prepare_matrix(features)
    print(f"\n--- Preparacion --- {info}")

    metrics = evaluate_ks(xs)
    print("\n--- Metricas por k ---")
    print(metrics.to_string(index=False))

    k = choose_k(metrics)
    ari_stability = stability(xs, k)
    print(f"\nk elegido (mejor Silhouette, empate -> menor k): {k}")
    print(f"estabilidad (ARI promedio entre semillas): {ari_stability:.3f}")

    model = train_kmeans(xs, k)
    labels = model.labels_

    print("\n--- Perfil de clusters (medias en unidades originales) ---")
    print(cluster_profiles(features, labels).to_string())

    validacion = validate_against_truth(features, labels)
    if validacion is not None:
        table, ari = validacion
        print("\n--- Validacion contra perfiles reales (crosstab) ---")
        print(table.to_string())
        print(f"ARI contra perfiles reales: {ari:.3f}")

    row = metrics[metrics["k"] == k].iloc[0].to_dict()
    path = save_artifact(model, scaler, info, k, row, ari_stability)
    print(f"\nArtefacto guardado: {path}")


if __name__ == "__main__":
    main()
