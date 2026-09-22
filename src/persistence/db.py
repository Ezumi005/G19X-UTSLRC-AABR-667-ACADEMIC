"""Conexion a PostgreSQL del motor de segmentacion.

La URL de conexion se lee de la variable de entorno DATABASE_URL, con
fallback al archivo .env de la raiz del proyecto (ver .env.example).
"""

from __future__ import annotations

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg import conninfo

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL no definida. Copia .env.example como .env en la raiz del proyecto y ajusta la contrasena."
        )
    return url


def connect():
    """Conexion a la base del motor (motor_segmentacion)."""
    return psycopg.connect(database_url())


def admin_connect():
    """Conexion administrativa a la base 'postgres' (para crear la base si no existe)."""
    params = conninfo.conninfo_to_dict(database_url())
    params["dbname"] = "postgres"
    return psycopg.connect(conninfo.make_conninfo(**params))
