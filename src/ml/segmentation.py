"""Ejecuta y persiste una segmentacion completa (etapa 8 del orden de desarrollo).

Flujo: PostgreSQL -> features -> K-Means (k=FINAL_K) -> etiquetas comerciales
-> tablas segmentation_runs / segments / customer_segments.

Las etiquetas se asignan con reglas sobre el PERFIL de cada cluster (medias en
unidades originales), no sobre su numero: asi un reordenamiento de clusters no
rompe la interpretacion. Las reglas fueron definidas tras analizar los
resultados reales (Bitacora 22/09/2026), cumpliendo la regla del README de no
nombrar clusters antes de conocer sus caracteristicas.

Uso (desde la raiz, requiere .env y base con datos):
    .venv/Scripts/python.exe -m src.ml.segmentation
"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
from psycopg.types.json import Jsonb
from sklearn.metrics import davies_bouldin_score, silhouette_score

from src.features.rfm import build_features, load_from_postgres
from src.ml.clustering import FINAL_K, SEED, cluster_profiles, prepare_matrix, train_kmeans
from src.persistence.db import connect

CLUSTER_DESCRIPTIONS = {
    "Clientes frecuentes de alto valor": (
        "Compran seguido, gastan mucho y mantienen actividad reciente. "
        "Prioridad de fidelizacion y programas preferenciales."
    ),
    "Navegadores sin compra": (
        "Actividad web intensa con carritos abandonados y ninguna compra registrada. "
        "Objetivo claro de conversion con incentivos de primera compra."
    ),
    "Clientes nuevos": (
        "Registrados hace menos de tres meses con pocas compras. "
        "Prioridad de onboarding y segunda compra."
    ),
    "Navegadores con compra esporádica": (
        "Alta actividad digital y carritos abandonados con compras aisladas. "
        "Oportunidad de conversion y cross-selling."
    ),
    "Clientes en riesgo de inactividad": (
        "Compraban con regularidad pero llevan mas de siete meses sin actividad. "
        "Objetivo de campanas de reactivacion."
    ),
    "Compradores ocasionales": (
        "Compran de forma esporadica y con baja interaccion. "
        "Potencial de aumento de frecuencia y ticket."
    ),
}


def label_clusters(profiles: pd.DataFrame) -> dict[int, dict]:
    """Asigna etiqueta comercial y descripcion a cada cluster segun su perfil.

    Reglas por prioridad (medias en unidades originales):
    1. frequency >= 15 y monetary >= 30000  -> frecuentes de alto valor
    2. frequency <= 0.5                     -> navegadores sin compra
    3. tenure_days <= 90                    -> nuevos
    4. web_visits >= 30                     -> navegadores con compra esporadica
    5. recency_days >= 150                  -> en riesgo de inactividad
    6. resto                                -> compradores ocasionales
    Falla si dos clusters reciben la misma etiqueta (exige revision humana).
    """
    asignaciones: dict[int, dict] = {}
    vistos: dict[str, int] = {}
    for cluster_id, row in profiles.iterrows():
        if row["frequency"] >= 15 and row["monetary"] >= 30000:
            label = "Clientes frecuentes de alto valor"
        elif row["frequency"] <= 0.5:
            label = "Navegadores sin compra"
        elif row["tenure_days"] <= 90:
            label = "Clientes nuevos"
        elif row["web_visits"] >= 30:
            label = "Navegadores con compra esporádica"
        elif row["recency_days"] >= 150:
            label = "Clientes en riesgo de inactividad"
        else:
            label = "Compradores ocasionales"
        if label in vistos:
            raise ValueError(
                f"Etiqueta duplicada '{label}' en clusters {vistos[label]} y {cluster_id}: "
                "revisar reglas de interpretacion antes de persistir."
            )
        vistos[label] = cluster_id
        asignaciones[cluster_id] = {"label": label, "description": CLUSTER_DESCRIPTIONS[label]}
    return asignaciones


def _row_to_json(row: pd.Series) -> dict:
    """Serie -> dict serializable (NaN -> None, numericos redondeados a 2 decimales)."""
    out: dict = {}
    for key, value in row.items():
        if pd.isna(value):
            out[key] = None
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            out[key] = round(float(value), 2)
        else:
            out[key] = value
    return out


def run_segmentation() -> int:
    """Ejecuta la segmentacion completa y la persiste. Devuelve el run_id."""
    frames = load_from_postgres()
    features = build_features(**frames)
    xs, scaler, prep = prepare_matrix(features)

    model = train_kmeans(xs, FINAL_K)
    labels = model.labels_
    metrics = {
        "silhouette": round(float(silhouette_score(xs, labels)), 4),
        "inertia": round(float(model.inertia_), 1),
        "davies_bouldin": round(float(davies_bouldin_score(xs, labels)), 4),
    }
    profiles = cluster_profiles(features, labels)
    asignaciones = label_clusters(profiles)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO segmentation_runs (model_name, k, seed, started_at) VALUES (%s, %s, %s, %s) RETURNING run_id",
                ("kmeans_local", FINAL_K, SEED, datetime.now(timezone.utc)),
            )
            run_id = cur.fetchone()[0]
        conn.commit()
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        """UPDATE segmentation_runs SET finished_at = %s, status = 'ok',
                           metrics = %s, params = %s, n_customers = %s WHERE run_id = %s""",
                        (
                            datetime.now(timezone.utc),
                            Jsonb(metrics),
                            Jsonb({k: v for k, v in prep.items()}),
                            len(features),
                            run_id,
                        ),
                    )
                    segment_ids: dict[int, int] = {}
                    for cluster_id, info in asignaciones.items():
                        row = profiles.loc[cluster_id]
                        cur.execute(
                            """INSERT INTO segments (run_id, cluster_id, label, description, n_customers, profile)
                               VALUES (%s, %s, %s, %s, %s, %s) RETURNING segment_id""",
                            (
                                run_id,
                                int(cluster_id),
                                info["label"],
                                info["description"],
                                int(row["clientes"]),
                                Jsonb(_row_to_json(row.drop("clientes"))),
                            ),
                        )
                        segment_ids[cluster_id] = cur.fetchone()[0]
                    asignaciones_df = pd.DataFrame(
                        {"customer_id": features["customer_id"], "cluster_id": labels}
                    )
                    asignaciones_df["segment_id"] = asignaciones_df["cluster_id"].map(segment_ids)
                    asignaciones_df.insert(0, "run_id", run_id)
                    cur.executemany(
                        "INSERT INTO customer_segments (run_id, customer_id, cluster_id, segment_id) VALUES (%(run_id)s, %(customer_id)s, %(cluster_id)s, %(segment_id)s)",
                        asignaciones_df.to_dict("records"),
                    )
            conn.commit()
        except Exception as exc:
            conn.rollback()
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE segmentation_runs SET finished_at = %s, status = 'error', error = %s WHERE run_id = %s",
                    (datetime.now(timezone.utc), str(exc)[:1000], run_id),
                )
            conn.commit()
            raise

    print(f"Segmentation #{run_id} OK [kmeans_local k={FINAL_K}]")
    print(f"  clientes asignados: {len(features)} | metricas: {metrics}")
    for cluster_id in sorted(asignaciones):
        row = profiles.loc[cluster_id]
        info = asignaciones[cluster_id]
        print(f"  Cluster {cluster_id} ({int(row['clientes'])} clientes): {info['label']}")
    return run_id


if __name__ == "__main__":
    run_segmentation()
