"""Proceso de ingesta: fuente externa -> adaptador -> PostgreSQL.

Registra una ejecucion en ingestion_runs (trazabilidad), persiste el
dataset normalizado y guarda las incidencias del adaptador.

Uso (desde la raiz, con la API CRM simulada encendida en 8001):
    .venv/Scripts/python.exe -m src.persistence.ingest
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.adapters import SimulatedCRMAdapter
from src.adapters.base import AdapterResult
from src.persistence.db import connect
from src.persistence.repository import save_dataset


def _start_run(conn, source: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO ingestion_runs (source, started_at) VALUES (%s, %s) RETURNING run_id",
            (source, datetime.now(timezone.utc)),
        )
        return cur.fetchone()[0]


def _finish_ok(conn, run_id: int, result: AdapterResult, saved: dict[str, int]) -> None:
    r = result.report
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE ingestion_runs SET
                finished_at = %s, status = 'ok',
                customers_read = %s, customers_saved = %s,
                transactions_read = %s, transactions_saved = %s,
                interactions_read = %s, interactions_saved = %s,
                campaign_events_read = %s, campaign_events_saved = %s
            WHERE run_id = %s
            """,
            (
                datetime.now(timezone.utc),
                r.read.get("customers", 0), saved["customers"],
                r.read.get("transactions", 0), saved["transactions"],
                r.read.get("interactions", 0), saved["interactions"],
                r.read.get("campaign_events", 0), saved["campaign_events"],
                run_id,
            ),
        )
        for inc in r.incidents:
            cur.execute(
                "INSERT INTO ingestion_incidents (run_id, entity, external_id, field, error) VALUES (%s, %s, %s, %s, %s)",
                (run_id, inc.entity, inc.external_id, inc.field, inc.error),
            )


def _finish_error(conn, run_id: int, error: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE ingestion_runs SET finished_at = %s, status = 'error', error = %s WHERE run_id = %s",
            (datetime.now(timezone.utc), error[:1000], run_id),
        )


def run_ingestion(base_url: str = "http://127.0.0.1:8001") -> int:
    """Ejecuta una sincronizacion completa. Devuelve el run_id registrado."""
    adapter = SimulatedCRMAdapter(base_url)
    with connect() as conn:
        run_id = _start_run(conn, "crm_simulado")
        conn.commit()
        try:
            result = adapter.fetch_normalized()
            saved = save_dataset(conn, result.dataset)
            _finish_ok(conn, run_id, result, saved)
            conn.commit()
        except Exception as exc:
            conn.rollback()
            _finish_error(conn, run_id, str(exc))
            conn.commit()
            raise
    r = result.report
    print(f"Ingestion #{run_id} OK [{r.source}]")
    for entity in r.read:
        print(f"  {entity}: leidos={r.read[entity]} guardados={saved[entity]} rechazados={r.rejected[entity]}")
    print(f"  incidencias registradas: {len(r.incidents)}")
    return run_id


if __name__ == "__main__":
    run_ingestion()
