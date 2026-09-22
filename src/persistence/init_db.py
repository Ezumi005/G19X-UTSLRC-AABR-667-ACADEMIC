"""Inicializa la base de datos: crea la base si no existe y aplica el esquema.

Uso (desde la raiz del proyecto):
    .venv/Scripts/python.exe -m src.persistence.init_db
Requiere .env con DATABASE_URL (ver .env.example).
"""

from __future__ import annotations

from pathlib import Path

from psycopg import errors

from src.persistence.db import admin_connect, connect

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DB_NAME = "motor_segmentacion"


def ensure_database() -> None:
    try:
        with admin_connect() as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"Base de datos creada: {DB_NAME}")
    except errors.DuplicateDatabase:
        print(f"Base de datos ya existente: {DB_NAME}")
    except errors.InsufficientPrivilege:
        raise RuntimeError("El usuario de DATABASE_URL no tiene permiso para crear bases de datos.") from None


def apply_schema() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(schema)
    print(f"Esquema aplicado: {SCHEMA_PATH.name}")


def main() -> None:
    ensure_database()
    apply_schema()
    print("Inicializacion de PostgreSQL completada.")


if __name__ == "__main__":
    main()
