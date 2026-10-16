"""Sugerencia automatica de mapeo CSV -> contrato mediante Azure OpenAI.

La IA recibe el esquema del contrato (introspectado de src/contracts, no
hardcodeado) y las columnas con filas de muestra del CSV; propone la entidad
y el mapeo. El usuario confirma en la interfaz y todo pasa la validacion
Pydantic del contrato antes de tocar la base: la IA sugiere, no decide.
"""

from __future__ import annotations

import os

from openai import AzureOpenAI

from src.adapters.csv_adapter import campos_de_entidad, entidades_validas
from src.services.recommendations import azure_openai_available, parse_json_loose

SYSTEM_PROMPT = (
    "Eres un integrador de datos senior. Recibes el esquema de un contrato de datos "
    "(entidades con sus campos; los campos obligatorios estan marcados) y las columnas "
    "de un CSV con algunas filas de muestra. Tu tarea: (1) decidir cual entidad del "
    "contrato representa el CSV, (2) mapear las columnas del CSV a los campos del "
    "contrato que correspondan por significado. Considera sinonimos en espanol e "
    "ingles (monto/importe/total -> amount; fecha_compra/when -> purchased_at; "
    "id_cliente/ident -> customer_id, etc.), formatos de fecha diversos y montos como "
    "texto. Responde EXCLUSIVAMENTE con un objeto JSON valido con esta forma exacta: "
    '{"entity": "nombre_entidad", "mapping": {"campo_contrato": "columna_csv"}, '
    '"unused_columns": ["columnas que no mapean"], "confidence": numero_0_a_100, '
    '"notes": "observaciones breves en espanol"}. En mapping incluye solo campos del '
    "contrato de la entidad elegida y usa exclusivamente columnas existentes del CSV; "
    "si un campo obligatorio no tiene columna clara, omitelo y mencionarlo en notes."
)


def suggest_mapping(columns: list[str], sample_rows: list[dict]) -> dict:
    """Llama a Azure OpenAI y devuelve la sugerencia validada en forma."""
    if not azure_openai_available():
        raise RuntimeError("Azure OpenAI no configurado: faltan AZURE_OPENAI_* en el entorno.")
    esquema = {entidad: campos_de_entidad(entidad) for entidad in entidades_validas()}
    cliente = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version="2024-10-21",
    )
    respuesta = cliente.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5-4-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"ESQUEMA DEL CONTRATO (entidad -> campos; true = obligatorio):\n{esquema}\n\n"
                    f"COLUMNAS DEL CSV:\n{columns}\n\n"
                    f"PRIMERAS FILAS DE MUESTRA:\n{sample_rows}"
                ),
            },
        ],
        temperature=0,
        max_completion_tokens=800,
        timeout=60,
    )
    contenido = respuesta.choices[0].message.content or ""
    sugerencia = parse_json_loose(contenido)

    entidad = sugerencia.get("entity")
    if entidad not in entidades_validas():
        raise ValueError(f"La IA sugirio una entidad invalida: {entidad}")
    mapping_crudo = sugerencia.get("mapping") or {}
    mapping = {campo: columna for campo, columna in mapping_crudo.items() if columna in columns}
    return {
        "entity": entidad,
        "mapping": mapping,
        "unused_columns": [c for c in sugerencia.get("unused_columns", []) if c in columns],
        "confidence": sugerencia.get("confidence"),
        "notes": sugerencia.get("notes"),
    }
