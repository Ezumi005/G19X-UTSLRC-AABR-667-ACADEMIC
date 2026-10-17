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


def prueba_duplicado_se_resuelve_por_calidad():
    df = perfiles_prueba()
    # cluster 2 tambien sin compras (empate con cluster 1 en la regla 2)
    df.loc[2, "frequency"] = 0.0
    df.loc[2, "monetary"] = 0.0
    a = label_clusters(df)
    etiquetas = [info["label"] for info in a.values()]
    assert len(set(etiquetas)) == 6
    # el cluster con mas carritos abandonados encierra mejor "navegador" (cluster 1: 40.8 vs 0.9)
    assert a[1]["label"] == "Navegadores sin compra"
    # el perdedor cae a la regla general, como ya lo hacia
    assert a[2]["label"] == "Compradores ocasionales"


def prueba_duplicado_mejor_calificado_gana():
    # dos clusters que cumplen la regla 1; gana el de mayor monetary (cluster 0)
    df = pd.DataFrame(
        {
            "clientes": [10, 10],
            "recency_days": [10.0, 100.0],
            "frequency": [20.0, 16.0],
            "monetary": [90000.0, 35000.0],
            "web_visits": [20.0, 5.0],
            "abandoned_carts": [2.0, 1.0],
            "campaign_click_rate": [0.3, 0.05],
            "tenure_days": [700.0, 701.0],
            "avg_ticket": [2000.0, 600.0],
            "product_views": [8.0, 2.0],
            "emails_opened": [5.0, 2.0],
        }
    )
    a = label_clusters(df)
    assert a[0]["label"] == "Clientes frecuentes de alto valor"
    assert a[1]["label"] == "Compradores ocasionales"


def prueba_variante_general_determinista():
    # cuatro clusters: dispute en la regla 4; el perdedor cae a la general ya
    # tomada -> recibe la variante determinista de menor actividad
    df = pd.DataFrame(
        {
            "clientes": [10, 10, 10, 10],
            "recency_days": [10.0, 20.0, 20.0, 100.0],
            "frequency": [30.0, 3.0, 3.0, 3.0],
            "monetary": [50000.0, 3000.0, 3000.0, 2000.0],
            "web_visits": [20.0, 60.0, 70.0, 5.0],
            "abandoned_carts": [2.0, 3.0, 3.0, 1.0],
            "campaign_click_rate": [0.3, 0.3, 0.3, 0.3],
            "tenure_days": [700.0, 400.0, 401.0, 500.0],
            "avg_ticket": [2000.0, 800.0, 900.0, 700.0],
            "product_views": [8.0, 2.0, 2.0, 2.0],
            "emails_opened": [5.0, 2.0, 2.0, 2.0],
        }
    )
    a = label_clusters(df)
    assert a[0]["label"] == "Clientes frecuentes de alto valor"
    assert a[2]["label"] == "Navegadores con compra esporádica"
    assert a[3]["label"] == "Compradores ocasionales"
    assert a[1]["label"] == "Compradores ocasionales de baja actividad"
    assert len({info["label"] for info in a.values()}) == 4


def prueba_exceso_general_falla():
    # cuatro clusters sin ninguna regla: se agotan las variantes generales
    base = {
        "clientes": [10, 10, 10, 10],
        "recency_days": [100.0, 101.0, 102.0, 103.0],
        "frequency": [3.0, 4.0, 5.0, 6.0],
        "monetary": [2000.0, 2100.0, 2200.0, 2300.0],
        "web_visits": [5.0, 6.0, 7.0, 8.0],
        "abandoned_carts": [1.0, 1.1, 1.2, 1.3],
        "campaign_click_rate": [0.3, 0.3, 0.3, 0.3],
        "tenure_days": [500.0, 501.0, 502.0, 503.0],
        "avg_ticket": [700.0, 710.0, 720.0, 730.0],
        "product_views": [2.0, 2.1, 2.2, 2.3],
        "emails_opened": [2.0, 2.1, 2.2, 2.3],
    }
    try:
        label_clusters(pd.DataFrame(base))
        raise AssertionError("Se esperaba error al agotarse las variantes generales")
    except ValueError as exc:
        assert "variantes" in str(exc)


def prueba_row_to_json():
    serie = pd.Series({"recency_days": float("nan"), "monetary": 123.456, "label": "x"})
    resultado = _row_to_json(serie)
    assert resultado["recency_days"] is None
    assert resultado["monetary"] == 123.46
    assert resultado["label"] == "x"


if __name__ == "__main__":
    prueba_etiquetas_reales()
    prueba_reglas_por_prioridad()
    prueba_duplicado_se_resuelve_por_calidad()
    prueba_duplicado_mejor_calificado_gana()
    prueba_variante_general_determinista()
    prueba_exceso_general_falla()
    prueba_row_to_json()
    print("OK: interpretacion verificada (etiquetas, prioridad, desempate, variantes, guardas, serializacion)")
