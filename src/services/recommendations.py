"""Recomendaciones comerciales por segmento mediante Azure OpenAI.

Responsabilidad (PRD seccion 17 / MVP seccion 15): recibir el resumen
estadistico de un segmento y generar una descripcion comercial y recomendaciones
de marketing/retencion. Azure OpenAI NO decide clusters ni recibe datos de
clientes individuales: solo agregados por segmento.

Degrada de forma controlada: si no hay credenciales configuradas, el endpoint
del backend responde 501 informativo.
"""

from __future__ import annotations

import json
import os
import re

from openai import AzureOpenAI

PROFILE_LABELS = {
    "recency_days": "dias desde la ultima compra",
    "frequency": "compras en 18 meses",
    "monetary": "gasto acumulado",
    "avg_ticket": "ticket promedio",
    "web_visits": "visitas web (90 dias)",
    "product_views": "productos vistos",
    "abandoned_carts": "carritos abandonados",
    "emails_opened": "correos abiertos",
    "campaign_click_rate": "tasa de clic en campanas",
    "tenure_days": "antiguedad en dias",
}

SYSTEM_PROMPT = (
    "Eres un consultor comercial senior de retail. Recibes el resumen estadistico "
    "de un segmento de clientes (medias por cliente). Responde SIEMPRE en espanol "
    "y EXCLUSIVAMENTE con un objeto JSON valido con esta forma exacta: "
    '{"descripcion": "2 o 3 frases que perfilen al segmento en lenguaje comercial", '
    '"recomendaciones": ["accion concreta 1", "accion concreta 2", "accion concreta 3"]} '
    "Las recomendaciones deben ser accionables (marketing, retencion, fidelizacion, "
    "cross-selling o up-selling) y coherentes con los numeros del segmento. "
    "No incluyas texto fuera del JSON."
)


def azure_openai_available() -> bool:
    return bool(os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"))


def build_messages(label: str, description: str | None, n_customers: int, profile: dict) -> list[dict]:
    metricas = "\n".join(
        f"- {PROFILE_LABELS.get(key, key)}: {value}"
        for key, value in profile.items()
        if value is not None
    )
    user = (
        f"Segmento: {label}\n"
        f"Tamaño: {n_customers} clientes\n"
        f"Contexto del negocio: {description or 'sin descripcion interna'}\n\n"
        f"Medias por cliente del segmento:\n{metricas}"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def parse_json_loose(texto: str) -> dict:
    """Parsea la respuesta del modelo tolerando texto alrededor del JSON."""
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        coincidencia = re.search(r"\{.*\}", texto, re.DOTALL)
        if coincidencia:
            return json.loads(coincidencia.group(0))
        raise ValueError(f"respuesta sin JSON parseable: {texto[:200]}")


def generate_recommendation(
    label: str, description: str | None, n_customers: int, profile: dict
) -> dict:
    """Llama a Azure OpenAI y devuelve {'descripcion': str, 'recomendaciones': [str]}."""
    if not azure_openai_available():
        raise RuntimeError("Azure OpenAI no configurado: faltan AZURE_OPENAI_* en el entorno.")
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version="2024-10-21",
    )
    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5-4-mini"),
        messages=build_messages(label, description, n_customers, profile),
        temperature=0.4,
        max_completion_tokens=700,
    )
    contenido = response.choices[0].message.content or ""
    resultado = parse_json_loose(contenido)
    if not isinstance(resultado.get("recomendaciones"), list) or not resultado.get("descripcion"):
        raise ValueError(f"respuesta con estructura inesperada: {str(resultado)[:200]}")
    return resultado
