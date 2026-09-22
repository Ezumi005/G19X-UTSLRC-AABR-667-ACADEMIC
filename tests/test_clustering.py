"""Pruebas unitarias del clustering (datos sinteticos, sin base de datos)."""

import numpy as np
import pandas as pd

from src.ml.clustering import (
    FEATURE_COLUMNS,
    choose_k,
    cluster_profiles,
    evaluate_ks,
    prepare_matrix,
    stability,
    train_kmeans,
)

RNG = np.random.default_rng(42)


def features_minimas(n: int = 60) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [f"C{i:03d}" for i in range(n)],
            "tenure_days": RNG.integers(10, 1000, n),
            "recency_days": RNG.uniform(0, 300, n),
            "frequency": RNG.integers(0, 50, n),
            "monetary": RNG.uniform(0, 50000, n),
            "avg_ticket": RNG.uniform(0, 3000, n),
            "web_visits": RNG.integers(0, 80, n),
            "product_views": RNG.integers(0, 40, n),
            "abandoned_carts": RNG.integers(0, 70, n),
            "emails_opened": RNG.integers(0, 20, n),
            "campaign_click_rate": RNG.uniform(0, 1, n),
            "favorite_category": "electronica",
        }
    )


def prueba_prepare_matrix():
    df = features_minimas()
    df.loc[0, "recency_days"] = np.nan
    df.loc[1, "recency_days"] = np.nan
    xs, scaler, info = prepare_matrix(df)
    assert xs.shape == (60, len(FEATURE_COLUMNS))
    assert info["recency_imputados"] == 2
    assert np.isclose(xs.mean(axis=0), 0, atol=1e-9).all()
    assert np.isclose(xs.std(axis=0), 1, atol=1e-3).all()
    assert np.isfinite(xs).all()
    assert hasattr(scaler, "transform")


def prueba_imputacion_cap():
    df = features_minimas(10)
    df.loc[5, "recency_days"] = np.nan
    maximo = df["recency_days"].max()
    xs, _, info = prepare_matrix(df)
    assert info["recency_cap_dias"] == round(float(maximo), 2)
    assert info["recency_imputados"] == 1


def blobs_separados() -> np.ndarray:
    arriba = RNG.normal([0, 0], 0.4, size=(40, 2))
    abajo = RNG.normal([6, 6], 0.4, size=(40, 2))
    return np.vstack([arriba, abajo])


def prueba_evaluate_y_choose_k():
    xs = blobs_separados()
    metrics = evaluate_ks(xs, k_range=range(2, 6))
    assert list(metrics.columns) == ["k", "silhouette", "inertia", "davies_bouldin"]
    k = choose_k(metrics)
    fila = metrics[metrics["k"] == k].iloc[0]
    assert fila["silhouette"] >= metrics["silhouette"].max() - 0.01
    assert k <= 4


def prueba_entrenamiento_y_estabilidad():
    xs = blobs_separados()
    model = train_kmeans(xs, k=2)
    assert set(model.labels_) == {0, 1}
    assert (model.labels_[:40] == model.labels_[0]).all()
    assert (model.labels_[40:] == model.labels_[41]).all()
    assert model.labels_[0] != model.labels_[41]
    assert stability(xs, 2) > 0.99


def prueba_cluster_profiles():
    df = pd.DataFrame(
        {
            "customer_id": ["A", "B", "C", "D"],
            "tenure_days": [100, 110, 900, 910],
            "recency_days": [1.0, 2.0, 200.0, 210.0],
            "frequency": [10, 20, 1, 2],
            "monetary": [1000.0, 2000.0, 100.0, 200.0],
            "avg_ticket": [100.0, 100.0, 100.0, 100.0],
            "web_visits": [5, 6, 50, 51],
            "product_views": [1, 2, 3, 4],
            "abandoned_carts": [0, 1, 30, 31],
            "emails_opened": [2, 2, 2, 2],
            "campaign_click_rate": [0.5, 0.5, 0.1, 0.1],
            "favorite_category": ["moda", "moda", "hogar", "hogar"],
        }
    )
    labels = np.array([0, 0, 1, 1])
    prof = cluster_profiles(df, labels)
    assert prof.loc[0, "clientes"] == 2 and prof.loc[1, "clientes"] == 2
    assert prof.loc[0, "frequency"] == 15.0
    assert prof.loc[1, "monetary"] == 150.0
    assert prof.loc[1, "abandoned_carts"] == 30.5


if __name__ == "__main__":
    prueba_prepare_matrix()
    prueba_imputacion_cap()
    prueba_evaluate_y_choose_k()
    prueba_entrenamiento_y_estabilidad()
    prueba_cluster_profiles()
    print("OK: clustering verificado (preparacion, imputacion, eleccion de k, estabilidad, perfiles)")
