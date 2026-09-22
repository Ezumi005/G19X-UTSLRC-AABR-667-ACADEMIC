"""Construccion de features RFM por cliente.

Origen: datos normalizados en PostgreSQL (espejo del Contrato Interno V1).
Salida: DataFrame de una fila por cliente con RFM como base minima y features
de engagement justificadas (PRD seccion 12, MVP seccion 10).

Features producidas:
- tenure_days: dias desde el registro del cliente (antiguedad).
- recency_days: dias desde la ultima compra (NULL si nunca compro; la
  imputacion se decide en la etapa de ML).
- frequency: numero de compras.
- monetary: gasto acumulado.
- avg_ticket: ticket promedio (0 si no hay compras).
- web_visits / product_views / abandoned_carts: conteos de interacciones.
- emails_opened: aperturas de campanas.
- campaign_click_rate: clics / envios recibidos (0 si no recibio envios).
- favorite_category: categoria dominante por compras (metadato; no entra
  directa al clustering). Desempate determinista: alfabetico.

Decisiones:
- Fecha de referencia de recency/tenure = max(purchased_at) del dataset
  (determinista y alineada al ancla fija del simulador).
- Las transacciones de clientes inexistentes (huerfanas) se excluyen del
  calculo; el conteo se reporta en quality_report.

Uso (desde la raiz, requiere .env y base inicializada):
    .venv/Scripts/python.exe -m src.features.rfm
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.persistence.db import connect

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

TABLE_COLUMNS: dict[str, list[str]] = {
    "customers": ["customer_id", "registered_at"],
    "transactions": ["transaction_id", "customer_id", "purchased_at", "amount", "category"],
    "interactions": ["interaction_id", "customer_id", "interaction_type"],
    "campaign_events": ["campaign_id", "customer_id", "event_type"],
}

INTERACTION_COLS = ["web_visit", "product_view", "abandoned_cart"]


def load_from_postgres() -> dict[str, pd.DataFrame]:
    """Carga las 4 tablas del contrato desde PostgreSQL como DataFrames."""
    frames: dict[str, pd.DataFrame] = {}
    with connect() as conn:
        with conn.cursor() as cur:
            for table, columns in TABLE_COLUMNS.items():
                cur.execute(f"SELECT {', '.join(columns)} FROM {table}")
                frames[table] = pd.DataFrame(cur.fetchall(), columns=columns)
    return frames


def quality_report(
    customers: pd.DataFrame,
    transactions: pd.DataFrame,
    interactions: pd.DataFrame,
    campaign_events: pd.DataFrame,
) -> dict[str, object]:
    """Chequeos de calidad previos al calculo (MVP seccion 9)."""
    known = set(customers["customer_id"])
    return {
        "customers": len(customers),
        "transactions": len(transactions),
        "interactions": len(interactions),
        "campaign_events": len(campaign_events),
        "ids_duplicados": {
            "transactions": int(transactions["transaction_id"].duplicated().sum()),
            "interactions": int(interactions["interaction_id"].duplicated().sum()),
        },
        "registros_huerfanos": {
            "transactions": int((~transactions["customer_id"].isin(known)).sum()),
            "interactions": int((~interactions["customer_id"].isin(known)).sum()),
            "campaign_events": int((~campaign_events["customer_id"].isin(known)).sum()),
        },
        "montos_negativos": int((transactions["amount"].astype(float) < 0).sum()),
    }


def build_features(
    customers: pd.DataFrame,
    transactions: pd.DataFrame,
    interactions: pd.DataFrame,
    campaign_events: pd.DataFrame,
    reference_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Core puro: DataFrames del contrato -> tabla de features por cliente."""
    customers = customers[["customer_id", "registered_at"]].copy()
    customers["registered_at"] = pd.to_datetime(customers["registered_at"], utc=True)

    tx = transactions.copy()
    tx["purchased_at"] = pd.to_datetime(tx["purchased_at"], utc=True)
    tx["amount"] = tx["amount"].astype(float)
    known = set(customers["customer_id"])
    tx = tx[tx["customer_id"].isin(known)]

    if reference_date is None:
        reference_date = tx["purchased_at"].max()
    reference_date = pd.Timestamp(reference_date)

    base = customers.set_index("customer_id")

    grouped = tx.groupby("customer_id")
    agg = pd.DataFrame(
        {
            "frequency": grouped.size(),
            "monetary": grouped["amount"].sum(),
            "last_purchase": grouped["purchased_at"].max(),
        }
    )
    favorite = (
        tx.groupby(["customer_id", "category"])
        .size()
        .rename("n")
        .reset_index()
        .sort_values(["n", "category"], ascending=[False, True])
        .drop_duplicates("customer_id")
        .set_index("customer_id")["category"]
    )

    inter = interactions[interactions["customer_id"].isin(known)]
    inter_counts = (
        inter.groupby(["customer_id", "interaction_type"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=INTERACTION_COLS, fill_value=0)
    )

    ce = campaign_events[campaign_events["customer_id"].isin(known)]

    def _count(event: str) -> pd.Series:
        return ce[ce["event_type"] == event].groupby("customer_id").size()

    sent, opened, clicked = _count("sent"), _count("opened"), _count("clicked")

    df = (
        base.join(agg)
        .join(favorite.rename("favorite_category"))
        .join(inter_counts)
        .join(opened.rename("emails_opened"))
        .join(sent.rename("_sent"))
        .join(clicked.rename("_clicked"))
    )

    df["tenure_days"] = (reference_date - df["registered_at"]).dt.days
    df["recency_days"] = (reference_date - df["last_purchase"]).dt.total_seconds() / 86400.0
    frequency = df["frequency"].fillna(0)
    df["avg_ticket"] = np.where(frequency > 0, df["monetary"].fillna(0.0) / frequency.replace(0, 1), 0.0)
    sent_n = df["_sent"].fillna(0)
    df["campaign_click_rate"] = np.where(sent_n > 0, df["_clicked"].fillna(0) / sent_n.replace(0, 1), 0.0)

    for column in ["frequency", "web_visit", "product_view", "abandoned_cart", "emails_opened"]:
        df[column] = df[column].fillna(0).astype(int)
    df["monetary"] = df["monetary"].fillna(0.0)

    out = pd.DataFrame(
        {
            "customer_id": df.index,
            "tenure_days": df["tenure_days"].astype(int),
            "recency_days": df["recency_days"],
            "frequency": df["frequency"],
            "monetary": df["monetary"],
            "avg_ticket": df["avg_ticket"],
            "web_visits": df["web_visit"],
            "product_views": df["product_view"],
            "abandoned_carts": df["abandoned_cart"],
            "emails_opened": df["emails_opened"],
            "campaign_click_rate": df["campaign_click_rate"],
            "favorite_category": df["favorite_category"],
        }
    ).reset_index(drop=True)
    return out


def _validate_against_ground_truth(features: pd.DataFrame) -> None:
    """Muestra medias por perfil real (solo validacion analitica; el ground truth
    del simulador nunca participa en el calculo de features)."""
    meta_path = DATA_DIR / "meta.json"
    if not meta_path.exists():
        print("(sin meta.json: se omite la validacion contra perfiles)")
        return
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    truth = pd.Series(meta["ground_truth"], name="profile")
    merged = features.merge(truth, left_on="customer_id", right_index=True)
    cols = [
        "recency_days", "frequency", "monetary", "avg_ticket",
        "web_visits", "abandoned_carts", "campaign_click_rate", "tenure_days",
    ]
    summary = merged.groupby("profile")[cols].mean().round(2)
    print("\n--- Validacion contra perfiles reales (medias) ---")
    print(summary.to_string())


def main() -> None:
    frames = load_from_postgres()
    report = quality_report(**frames)
    print("--- Calidad de datos ---")
    for key, value in report.items():
        print(f"  {key}: {value}")

    features = build_features(**frames)
    print(f"\nFeatures calculadas: {features.shape[0]} clientes x {features.shape[1]} columnas")
    print(features.head(5).to_string(index=False))

    stats_cols = [
        "tenure_days", "recency_days", "frequency", "monetary",
        "avg_ticket", "web_visits", "abandoned_carts", "campaign_click_rate",
    ]
    print("\n--- Estadisticas generales ---")
    print(features[stats_cols].describe().round(2).to_string())

    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "features_rfm.csv"
    features.to_csv(out_path, index=False)
    print(f"\nFeatures guardadas en: {out_path}")

    _validate_against_ground_truth(features)


if __name__ == "__main__":
    main()
