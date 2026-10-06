"""Consultas de lectura para la API (unico punto de acceso a datos de la API)."""

from __future__ import annotations

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from src.persistence.db import connect


def latest_ok_run_id(conn: psycopg.Connection) -> int | None:
    with conn.cursor() as cur:
        cur.execute("SELECT run_id FROM segmentation_runs WHERE status = 'ok' ORDER BY run_id DESC LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else None


def list_customers(
    limit: int,
    offset: int,
    segment: str | None = None,
    city: str | None = None,
    q: str | None = None,
) -> tuple[list[dict], int]:
    """Clientes con paginacion, filtros opcionales (segmento/ciudad/texto) y
    etiqueta de segmento del ultimo run exitoso."""
    conditions = ["1 = 1"]
    params: dict = {"limit": limit, "offset": offset}
    if segment:
        conditions.append("s.label = %(segment)s")
        params["segment"] = segment
    if city:
        conditions.append("c.city ILIKE %(city)s")
        params["city"] = f"%{city}%"
    if q:
        conditions.append("c.customer_id ILIKE %(q)s")
        params["q"] = f"%{q}%"
    where = " AND ".join(conditions)
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        run_id = latest_ok_run_id(conn)
        cur.execute(
            f"""
            SELECT c.customer_id, c.age, c.city, c.registered_at,
                   cs.cluster_id, s.label AS segment_label
            FROM customers c
            LEFT JOIN customer_segments cs ON cs.customer_id = c.customer_id AND cs.run_id = %(run)s
            LEFT JOIN segments s ON s.segment_id = cs.segment_id
            WHERE {where}
            ORDER BY c.customer_id
            LIMIT %(limit)s OFFSET %(offset)s
            """,
            {**params, "run": run_id},
        )
        items = [dict(r) for r in cur.fetchall()]
        cur.execute(
            f"""
            SELECT count(*) AS n FROM customers c
            LEFT JOIN customer_segments cs ON cs.customer_id = c.customer_id AND cs.run_id = %(run)s
            LEFT JOIN segments s ON s.segment_id = cs.segment_id
            WHERE {where}
            """,
            {**params, "run": run_id},
        )
        total = cur.fetchone()["n"]
    return items, total


def get_customer(customer_id: str) -> dict | None:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT customer_id, age, city, registered_at FROM customers WHERE customer_id = %s", (customer_id,))
        customer = cur.fetchone()
        if customer is None:
            return None
        cur.execute(
            """
            SELECT count(*) AS frequency,
                   coalesce(sum(amount), 0)::float AS monetary,
                   max(purchased_at) AS last_purchase,
                   count(DISTINCT category) AS categories_count
            FROM transactions WHERE customer_id = %s
            """,
            (customer_id,),
        )
        stats = dict(cur.fetchone())
        cur.execute(
            """
            SELECT s.segment_id, s.label, s.cluster_id
            FROM customer_segments cs
            JOIN segments s ON s.segment_id = cs.segment_id
            WHERE cs.customer_id = %s AND cs.run_id = %s
            """,
            (customer_id, latest_ok_run_id(conn)),
        )
        segment = cur.fetchone()
    out = dict(customer)
    out["stats"] = stats
    out["segment"] = dict(segment) if segment else None
    return out


def latest_segments() -> tuple[int | None, list[dict]]:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        run_id = latest_ok_run_id(conn)
        if run_id is None:
            return None, []
        cur.execute(
            "SELECT segment_id, cluster_id, label, description, n_customers, profile "
            "FROM segments WHERE run_id = %s ORDER BY cluster_id",
            (run_id,),
        )
        segments = [dict(r) for r in cur.fetchall()]
    return run_id, segments


def get_segment(segment_id: int) -> dict | None:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT s.segment_id, s.cluster_id, s.label, s.description, s.n_customers, s.profile,
                   r.run_id, r.k, r.metrics, r.started_at, r.status AS run_status
            FROM segments s JOIN segmentation_runs r ON r.run_id = s.run_id
            WHERE s.segment_id = %s
            """,
            (segment_id,),
        )
        segment = cur.fetchone()
        if segment is None:
            return None
        cur.execute(
            """
            SELECT cs.customer_id, c.city, c.registered_at
            FROM customer_segments cs JOIN customers c ON c.customer_id = cs.customer_id
            WHERE cs.segment_id = %s
            ORDER BY cs.customer_id
            LIMIT %s OFFSET %s
            """,
            (segment_id, 20, 0),
        )
        customers = [dict(r) for r in cur.fetchall()]
    out = dict(segment)
    out["customers_preview"] = customers
    return out


def ingestion_run_summary(run_id: int) -> dict:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT run_id, source, status, started_at, finished_at, customers_read, customers_saved, "
            "transactions_read, transactions_saved, interactions_read, interactions_saved, "
            "campaign_events_read, campaign_events_saved FROM ingestion_runs WHERE run_id = %s",
            (run_id,),
        )
        out = dict(cur.fetchone())
        cur.execute("SELECT count(*) AS n FROM ingestion_incidents WHERE run_id = %s", (run_id,))
        out["incidents"] = cur.fetchone()["n"]
    return out


def segmentation_run_summary(run_id: int) -> dict:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT run_id, model_name, k, status, n_customers, metrics, started_at, finished_at "
            "FROM segmentation_runs WHERE run_id = %s",
            (run_id,),
        )
        out = dict(cur.fetchone())
        cur.execute(
            "SELECT segment_id, cluster_id, label, n_customers FROM segments WHERE run_id = %s ORDER BY cluster_id",
            (run_id,),
        )
        out["segments"] = [dict(r) for r in cur.fetchall()]
    return out


def save_recommendation(segment_id: int, model: str, resultado: dict) -> int:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO recommendations (segment_id, model, descripcion, recomendaciones) "
                "VALUES (%s, %s, %s, %s) RETURNING recommendation_id",
                (segment_id, model, resultado["descripcion"], Jsonb(resultado["recomendaciones"])),
            )
            return cur.fetchone()[0]


def customer_features(customer_id: str) -> dict | None:
    """Las 7 features del contrato de scoring para un cliente (unidades originales).

    Recency usa como referencia max(purchased_at) global (misma convencion que
    src/features/rfm.py); sin compras -> recency_days None (el scoring la imputa).
    """
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT registered_at FROM customers WHERE customer_id = %s", (customer_id,))
        cliente = cur.fetchone()
        if cliente is None:
            return None
        cur.execute("SELECT max(purchased_at) AS ref FROM transactions")
        ref = cur.fetchone()["ref"]
        cur.execute(
            """SELECT count(*) AS frequency, coalesce(sum(amount), 0)::float AS monetary,
                      max(purchased_at) AS last_purchase
               FROM transactions WHERE customer_id = %s""",
            (customer_id,),
        )
        tx = cur.fetchone()
        cur.execute(
            """SELECT count(*) FILTER (WHERE interaction_type = 'web_visit') AS web_visits,
                      count(*) FILTER (WHERE interaction_type = 'abandoned_cart') AS abandoned_carts
               FROM interactions WHERE customer_id = %s""",
            (customer_id,),
        )
        inter = cur.fetchone()
        cur.execute(
            """SELECT count(*) FILTER (WHERE event_type = 'sent') AS sent,
                      count(*) FILTER (WHERE event_type = 'clicked') AS clicked
               FROM campaign_events WHERE customer_id = %s""",
            (customer_id,),
        )
        ce = cur.fetchone()

    recency = None
    if tx["last_purchase"] is not None and ref is not None:
        recency = round((ref - tx["last_purchase"]).total_seconds() / 86400.0, 2)
    tenure = round((ref - cliente["registered_at"]).total_seconds() / 86400.0) if ref else 0
    click_rate = (ce["clicked"] / ce["sent"]) if ce["sent"] else 0.0
    return {
        "recency_days": recency,
        "frequency": tx["frequency"],
        "monetary": round(tx["monetary"], 2),
        "web_visits": inter["web_visits"],
        "abandoned_carts": inter["abandoned_carts"],
        "campaign_click_rate": round(click_rate, 4),
        "tenure_days": tenure,
    }


def list_segmentation_runs(limit: int = 20) -> list[dict]:
    """Historial de ejecuciones de segmentacion (trazabilidad, PRD seccion 19)."""
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT run_id, model_name, k, status, n_customers, metrics, started_at, finished_at "
            "FROM segmentation_runs ORDER BY run_id DESC LIMIT %s",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]


def latest_recommendation(segment_id: int) -> dict | None:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT recommendation_id, segment_id, model, descripcion, recomendaciones, created_at "
            "FROM recommendations WHERE segment_id = %s ORDER BY recommendation_id DESC LIMIT 1",
            (segment_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def dashboard_summary() -> dict:
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT count(*) AS n FROM customers")
        total_customers = cur.fetchone()["n"]
        cur.execute(
            "SELECT count(*) AS n, coalesce(sum(amount), 0)::float AS total, coalesce(avg(amount), 0)::float AS avg_ticket FROM transactions"
        )
        tx = dict(cur.fetchone())
        cur.execute(
            "SELECT run_id, status, finished_at FROM ingestion_runs ORDER BY run_id DESC LIMIT 1"
        )
        last_ingestion = cur.fetchone()
        run_id = latest_ok_run_id(conn)
        distribution: list[dict] = []
        last_seg: dict | None = None
        segments_profile: list[dict] = []
        if run_id is not None:
            cur.execute(
                "SELECT run_id, k, n_customers, started_at FROM segmentation_runs WHERE run_id = %s",
                (run_id,),
            )
            last_seg = dict(cur.fetchone())
            cur.execute(
                "SELECT segment_id, label, n_customers FROM segments WHERE run_id = %s ORDER BY cluster_id",
                (run_id,),
            )
            distribution = [dict(r) for r in cur.fetchall()]
            cur.execute(
                """SELECT label,
                          (profile->>'recency_days')::float AS recency_days,
                          (profile->>'frequency')::float AS frequency,
                          (profile->>'monetary')::float AS monetary,
                          (profile->>'avg_ticket')::float AS avg_ticket
                   FROM segments WHERE run_id = %s ORDER BY cluster_id""",
                (run_id,),
            )
            segments_profile = [dict(r) for r in cur.fetchall()]
        cur.execute(
            "SELECT category, count(*) AS n FROM transactions GROUP BY category ORDER BY n DESC LIMIT 8"
        )
        top_categories = [dict(r) for r in cur.fetchall()]
    return {
        "total_customers": total_customers,
        "total_transactions": tx["n"],
        "total_spend": tx["total"],
        "avg_ticket": tx["avg_ticket"],
        "last_ingestion": dict(last_ingestion) if last_ingestion else None,
        "last_segmentation": last_seg,
        "segments_distribution": distribution,
        "segments_profile": segments_profile,
        "top_categories": top_categories,
    }
