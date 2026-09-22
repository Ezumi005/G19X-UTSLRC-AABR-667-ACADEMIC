"""Pruebas unitarias de la interpretacion de clusters (label_clusters)."""

import pandas as pd

from src.ml.segmentation import _row_to_json, label_clusters


def perfiles_prueba() -> pd.DataFrame:
    base = {
        "clientes": [150, 19, 122, 66, 66, 75],
        "recency_days": [16.5, float("nan"), 87.9, 13.1, 111.8, 231.8],
        "frequency": [31.5, 0.0, 5.9, 2.0, 1.6, 10.9],
        "monetary": [68543.0, 0.0, 3454.0, 1810.0, 957.0, 10349.0],
        "web_visits": [27.7, 61.4, 5.6, 16.2, 50.5, 1.3],
        "abandoned_carts": [2.5, 40.8, 0.9, 3.0, 36.8, 0.1],
        "campaign_click_rate": [0.27, 0.31, 0.03, 0.05, 0.42, 0.0],
        "tenure_days": [762.6, 459.5, 716.4, 48.3, 332.7, 849.9],
        "avg_ticket": [1859.3, 0.0, 577.9, 923.6, 523.1, 947.8],
        "product_views": [10.7, 12.7, 2.7, 6.2, 11.6, 0.7],
        "emails_opened": [5.3, 5.5, 2.7, 0.9, 4.9, 0.8],
    }
    return pd.DataFrame(base)


def prueba_etiquetas_reales():
    asignaciones = label_clusters(perfiles_prueba())
    assert len(asignaciones) == 6
    assert asignaciones[0]["label"] == "Clientes frecuentes de alto valor"
    assert asignaciones[1]["label"] == "Navegadores sin compra"
    assert asignaciones[2]["label"] == "Compradores ocasionales"
    assert asignaciones[3]["label"] == "Clientes nuevos"
    assert asignaciones[4]["label"] == "Navegadores con compra esporádica"
    assert asignaciones[5]["label"] == "Clientes en riesgo de inactividad"
    for info in asignaciones.values():
        assert info["description"]


def prueba_reglas_por_prioridad():
    # caso minimo: tenure bajo PERO frecuencia/monetary altos -> alto valor tiene prioridad sobre nuevo
    df = pd.DataFrame(
        {
            "clientes": [10, 10],
            "recency_days": [10.0, 100.0],
            "frequency": [20.0, 5.0],
            "monetary": [40000.0, 3000.0],
            "web_visits": [20.0, 5.0],
            "abandoned_carts": [2.0, 1.0],
            "campaign_click_rate": [0.3, 0.05],
            "tenure_days": [50.0, 700.0],
            "avg_ticket": [2000.0, 600.0],
            "product_views": [8.0, 2.0],
            "emails_opened": [5.0, 2.0],
        }
    )
    a = label_clusters(df)
    assert a[0]["label"] == "Clientes frecuentes de alto valor"
    assert a[1]["label"] == "Compradores ocasionales"


def prueba_etiqueta_duplicada_falla():
    df = perfiles_prueba()
    # cluster 2 tambien sin compras -> misma etiqueta que cluster 1
    df.loc[2, "frequency"] = 0.0
    df.loc[2, "monetary"] = 0.0
    try:
        label_clusters(df)
        raise AssertionError("Se esperaba error por etiqueta duplicada")
    except ValueError as exc:
        assert "duplicada" in str(exc)


def prueba_row_to_json():
    serie = pd.Series({"recency_days": float("nan"), "monetary": 123.456, "label": "x"})
    resultado = _row_to_json(serie)
    assert resultado["recency_days"] is None
    assert resultado["monetary"] == 123.46
    assert resultado["label"] == "x"


if __name__ == "__main__":
    prueba_etiquetas_reales()
    prueba_reglas_por_prioridad()
    prueba_etiqueta_duplicada_falla()
    prueba_row_to_json()
    print("OK: interpretacion verificada (etiquetas, prioridad, duplicados, serializacion)")
