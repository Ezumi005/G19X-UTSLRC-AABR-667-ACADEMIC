"""Pruebas unitarias de build_features (sin base de datos: frames sinteticos)."""

import pandas as pd

from src.features.rfm import build_features, quality_report

REF = pd.Timestamp("2026-09-10T12:00:00Z")


def frames_sinteticos():
    customers = pd.DataFrame(
        {
            "customer_id": ["A", "B", "C"],
            "registered_at": pd.to_datetime(
                ["2024-09-10", "2026-08-01", "2025-01-01"], utc=True
            ),
        }
    )
    transactions = pd.DataFrame(
        {
            "transaction_id": ["T1", "T2", "T3", "T9"],
            "customer_id": ["A", "A", "C", "Z"],
            "purchased_at": pd.to_datetime(
                ["2026-09-05", "2026-08-31", "2026-01-15", "2026-09-01"], utc=True
            ),
            "amount": [100.0, 50.0, 200.0, 999.0],
            "category": ["electronica", "moda", "hogar", "juguetes"],
        }
    )
    interactions = pd.DataFrame(
        {
            "interaction_id": ["I1", "I2", "I3"],
            "customer_id": ["B", "B", "A"],
            "interaction_type": ["web_visit", "abandoned_cart", "product_view"],
        }
    )
    campaign_events = pd.DataFrame(
        {
            "campaign_id": ["C1", "C1", "C1", "C1", "C2"],
            "customer_id": ["B", "B", "A", "A", "C"],
            "event_type": ["sent", "clicked", "sent", "opened", "sent"],
        }
    )
    return customers, transactions, interactions, campaign_events


def prueba_rfm_basico():
    c, t, i, e = frames_sinteticos()
    f = build_features(c, t, i, e, reference_date=REF).set_index("customer_id")

    assert f.loc["A", "frequency"] == 2
    assert f.loc["A", "monetary"] == 150.0
    assert f.loc["A", "avg_ticket"] == 75.0
    assert f.loc["A", "recency_days"] == 5.5  # 2026-09-05T00:00Z -> 2026-09-10T12:00Z
    assert f.loc["A", "favorite_category"] == "electronica"  # empate 1-1 -> alfabetico
    assert f.loc["A", "emails_opened"] == 1
    assert f.loc["A", "campaign_click_rate"] == 0.0  # 0 clics / 1 envio

    assert f.loc["C", "frequency"] == 1
    assert f.loc["C", "tenure_days"] == 617  # 2025-01-01 -> 2026-09-10


def prueba_cliente_sin_compras():
    c, t, i, e = frames_sinteticos()
    f = build_features(c, t, i, e, reference_date=REF).set_index("customer_id")
    b = f.loc["B"]
    assert b["frequency"] == 0
    assert b["monetary"] == 0.0
    assert b["avg_ticket"] == 0.0
    assert pd.isna(b["recency_days"])
    assert pd.isna(b["favorite_category"])
    assert b["abandoned_carts"] == 1
    assert b["web_visits"] == 1
    assert b["product_views"] == 0
    assert b["campaign_click_rate"] == 1.0  # 1 clic / 1 envio


def prueba_huerfanos_excluidos():
    c, t, i, e = frames_sinteticos()
    f = build_features(c, t, i, e, reference_date=REF)
    ids = set(f["customer_id"])
    assert ids == {"A", "B", "C"}
    assert 999.0 not in set(f["monetary"])  # la transaccion huerfana no suma


def prueba_sin_interacciones_ni_campanas():
    c, t, i, e = frames_sinteticos()
    f = build_features(c, t.head(0), i.head(0), e.head(0), reference_date=REF).set_index("customer_id")
    assert f.loc["A", "frequency"] == 0
    assert f.loc["A", "web_visits"] == 0
    assert f.loc["A", "campaign_click_rate"] == 0.0
    assert pd.isna(f.loc["A", "recency_days"])


def prueba_fecha_referencia_por_defecto():
    c, t, i, e = frames_sinteticos()
    f = build_features(c, t, i, e)  # sin reference_date -> max(purchased_at)
    assert f.set_index("customer_id").loc["A", "recency_days"] == 0.0  # A tiene la compra mas reciente


def prueba_quality_report():
    c, t, i, e = frames_sinteticos()
    q = quality_report(c, t, i, e)
    assert q["customers"] == 3
    assert q["registros_huerfanos"]["transactions"] == 1
    assert q["ids_duplicados"]["transactions"] == 0
    assert q["montos_negativos"] == 0


if __name__ == "__main__":
    prueba_rfm_basico()
    prueba_cliente_sin_compras()
    prueba_huerfanos_excluidos()
    prueba_sin_interacciones_ni_campanas()
    prueba_fecha_referencia_por_defecto()
    prueba_quality_report()
    print("OK: build_features verificado (RFM, sin compras, huerfanos, vacios, fecha por defecto, calidad)")
