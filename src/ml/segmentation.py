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
    "Compradores ocasionales de baja actividad": (
        "Compran poco y casi no navegan: clientes dormidos con historial valido. "
        "Reactivacion con recordatorios y descuentos suaves."
    ),
    "Compradores ocasionales de actividad mínima": (
        "Comportamiento de compra minimo con interaccion web casi nula. "
        "Objetivo de campanas baratas de reacuerdo antes de darlos por perdidos."
    ),
}

ETIQUETAS_GENERALES = (
    "Compradores ocasionales",
    "Compradores ocasionales de baja actividad",
    "Compradores ocasionales de actividad mínima",
)


def label_clusters(profiles: pd.DataFrame) -> dict[int, dict]:
    """Asigna etiqueta comercial y descripcion a cada cluster segun su perfil.

    Reglas por prioridad (medias en unidades originales):
    1. frequency >= 15 y monetary >= 30000  -> frecuentes de alto valor
    2. frequency <= 0.5                     -> navegadores sin compra
    3. tenure_days <= 90                    -> nuevos
    4. web_visits >= 30                     -> navegadores con compra esporadica
    5. recency_days >= 150                  -> en riesgo de inactividad
    6. resto                                -> compradores ocasionales

    Si dos clusters coinciden en una regla, se queda con la etiqueta el que
    mejor encierra el concepto (metrica por etiqueta: mas monetary en alto
    valor, menos frecuencia y mas carritos abandonados en navegadores, etc.);
    el resto se reevalua con reglas de menor prioridad. Los clusters que no
    cumplen ninguna regla reciben la etiqueta general "Compradores ocasionales"
    (o su siguiente variante de menor actividad si ya esta tomada). Solo se
    falla si hay mas clusters sin reglas que variantes disponibles, caso que
    si exige revision humana.
    """
    tomadas: dict[str, int] = {}
    por_resolver = {cluster_id: 0 for cluster_id in profiles.index}
    asignaciones: dict[int, dict] = {}
    usos_general = 0
    max_pasos = len(REGLAS) * len(profiles) + 2

    for _ in range(max_pasos):
        coincidencias: dict[int, list[int]] = {}
        for cluster_id, desde in por_resolver.items():
            fila = profiles.loc[cluster_id]
            indice = len(REGLAS)
            for i in range(desde, len(REGLAS)):
                if REGLAS[i][1](fila):
                    indice = i
                    break
            coincidencias.setdefault(indice, []).append(cluster_id)

        ids_general = sorted(
            coincidencias.pop(len(REGLAS), []),
            key=lambda c: METRICAS_DESEMPATE["Compradores ocasionales"](profiles.loc[c]),
            reverse=True,
        )
        for cluster_id in ids_general:
            if usos_general >= len(ETIQUETAS_GENERALES):
                raise ValueError(
                    "Mas clusters sin reglas que variantes de 'Compradores ocasionales': "
                    "revisar reglas de interpretacion antes de persistir."
                )
            label = ETIQUETAS_GENERALES[usos_general]
            usos_general += 1
            tomadas[label] = cluster_id
            asignaciones[cluster_id] = {"label": label, "description": CLUSTER_DESCRIPTIONS[label]}
            del por_resolver[cluster_id]

        hubo_escalado = False
        for idx, ids in coincidencias.items():
            label = REGLAS[idx][0]
            ganador = ids[0] if len(ids) == 1 else max(ids, key=lambda c: METRICAS_DESEMPATE[label](profiles.loc[c]))
            for cluster_id in ids:
                if cluster_id == ganador and tomadas.get(label) is None:
                    tomadas[label] = cluster_id
                    asignaciones[cluster_id] = {
                        "label": label,
                        "description": CLUSTER_DESCRIPTIONS[label],
                    }
                    del por_resolver[cluster_id]
                else:
                    por_resolver[cluster_id] = idx + 1
                    hubo_escalado = True
        if not por_resolver:
            break
        if not hubo_escalado:
            raise RuntimeError("Resolucion de etiquetas sin progreso: revisar reglas de interpretacion.")

    if por_resolver:
        raise RuntimeError("Resolucion de etiquetas incompleta: revisar reglas de interpretacion.")
    return asignaciones


REGLAS = (
    (
        "Clientes frecuentes de alto valor",
        lambda fila: fila["frequency"] >= 15 and fila["monetary"] >= 30000,
    ),
    ("Navegadores sin compra", lambda fila: fila["frequency"] <= 0.5),
    ("Clientes nuevos", lambda fila: fila["tenure_days"] <= 90),
    ("Navegadores con compra esporádica", lambda fila: fila["web_visits"] >= 30),
    ("Clientes en riesgo de inactividad", lambda fila: fila["recency_days"] >= 150),
)

# Metrica de desempate por etiqueta (mayor valor = mejor candidato al concepto).
METRICAS_DESEMPATE = {
    "Clientes frecuentes de alto valor": lambda fila: (fila["monetary"], fila["frequency"]),
    "Navegadores sin compra": lambda fila: (-fila["frequency"], fila["abandoned_carts"]),
    "Clientes nuevos": lambda fila: -fila["tenure_days"],
    "Navegadores con compra esporádica": lambda fila: fila["web_visits"],
    "Clientes en riesgo de inactividad": lambda fila: fila["recency_days"],
    "Compradores ocasionales": lambda fila: fila["frequency"],
}


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
