# Documento Técnico — Motor Inteligente de Segmentación de Clientes

**Versión:** 2.0 · **Fecha de cierre:** 16/10/2026 · **Estado:** MVP FINAL verificado (CI green, tag `v2.0.0`)
**Propósito:** describir el diseño y las decisiones técnicas del sistema (el "por qué" y el "qué"). El "cómo se opera" está en el Manual Técnico y el "cómo se instala" en la Guía de Instalación.

---

## 1. Objetivo y alcance

Producto para PluriOne S.A. de C.V.: transformar datos de clientes provenientes de cualquier fuente en **segmentos accionables**, con evidencia estadística, recomendaciones comerciales de IA y audiencias listas para campañas.

Alcance entregado:
- Cadena completa: fuente externa → contrato interno → PostgreSQL → features → K-Means → etiquetas → API → web.
- Tres capacidades de IA: recomendaciones por segmento, sugerencia de mapeo de fuentes CSV y scoring en la nube.
- Trazabilidad total (ingestiones, ejecuciones, modelo, predicciones).

Fuera de alcance (documentado como evolución): autenticación multiusuario, churn/CLV predictivo, adaptadores de CRMs reales.

## 2. Arquitectura por capas

```
FUENTES EXTERNAS            NÚCLEO (independiente de la fuente)          CONSUMO
┌────────────────┐     ┌──────────────────────────────────────┐     ┌──────────────┐
│ CRM simulado   │────▶│ Adaptadores  ──▶ Contrato V1 (Pydantic)    │────▶│ API FastAPI  │
│ (API 8001)     │     │ DynamicCSV   ──▶ Validación por fila       │     │ (8000)       │
│ CSV (web)      │     │                                  │     │      │        │
└────────────────┘     └──────────┬───────────────────────────┘     └──────┬───────┘
                                  ▼                                        ▼
                      ┌─────────────────────────┐              ┌────────────────────┐
                      │ PostgreSQL (espejo V1 + │              │ React web (5173)   │
                      │ trazabilidad de runs)   │              │ 7 páginas + temas  │
                      └─────────────┬───────────┘              └────────────────────┘
                                    │
                     features RFM ──▶ K-Means k=6 (local, semilla fija)
                                    │
                     etiquetas por perfil (reglas + desempate determinista)
```

**Principio rector:** el motor nunca sabe de dónde vienen los datos. Una fuente nueva = un adaptador nuevo (o un CSV con ayuda de la IA), cero cambios en el núcleo.

## 3. Contrato Interno de Datos V1

Fuente única de verdad: `src/contracts/` (Pydantic) + `docs/contrato_interno_datos_v1.md`.

| Entidad | Campos clave |
|---|---|
| `Customer` | `customer_id`*, `age`, `city`, `registered_at` |
| `Transaction` | `transaction_id`*, `customer_id`*, `purchased_at`, `total_amount`*, `product_category`*, `channel` |
| `Interaction` | `interaction_id`*, `customer_id`*, `occurred_at`, `type`, `detail` (product_views, emails_opened, carts) |
| `CampaignEvent` | `event_id`*, `customer_id`*, `campaign_id`, `event_type`, `click` |
| `NormalizedDataset` | 4 más `report` (leídos, válidos, incidencias) |

`*` obligatorio. Los enums evitan valores abiertos. El contrato se **introspecta**: las vistas de la API/web y el prompt de la IA se generan desde los modelos (un campo nuevo se propaga solo).

## 4. Modelo de datos y motor

**Features (7):** `recency_days`, `frequency`, `monetary`, `web_visits`, `abandoned_carts`, `campaign_click_rate`, `tenure_days` — RFM clásico + señal digital, construidas desde PostgreSQL.

**Clustering:** K-Means con semilla fija; evaluación de k=2..10 (silhouette/inercia/Davies-Bouldin) **más análisis comercial de perfiles** ⇒ **k=6** (decisión informada y documentada). Registrado como `kmeans_local:1` en Azure ML; el artefacto se sirve desde Azure App Service.

**Interpretación (etiquetas):** reglas por prioridad sobre el perfil medio del cluster (alto valor → sin compra → nuevos → navegadores esporádicos → riesgo → general). Desde v2.0 el choque de etiquetas se resuelve **por mejor calificado del concepto** y variantes de la etiqueta general; solo la ambigüedad real exige revisión humana.

## 5. Donde se usa IA (fronteras definidas)

| Uso | Proveedor | Entrada → salida | Guardas |
|---|---|---|---|
| Recomendaciones comerciales | Azure OpenAI `gpt-5.4-mini` | agregados del segmento → JSON comercial | temperature 0, timeout, parseo tolerante, degradación 501/503 |
| Sugerencia de mapeo CSV | Azure OpenAI `gpt-5.4-mini` | esquema introspectado + columnas + muestra → entidad + mapping + confianza | filtro de columnas, validación Pydantic, **confirmación humana**, dry-run |
| Scoring (predicción por cliente) | Azure App Service (=F1) | 7 features → cluster + etiqueta | API key `X-API-Key`, timeout 90 s + 1 reintento (arranque en frío) |

Reglas inviolables: la IA generativa **nunca decide clusters ni etiquetas**; la web nunca llama a Azure ni ve llaves; las llamadas a Azure salen solo del backend.

## 6. Seguridad y privacidad

- Secretos en `.env` local (no versionado); `.env.example` como plantilla.
- Sin login por decisión documentada (demo académica local); camino definido API key/JWT → roles.
- Datos sintéticos (simulador determinista): ninguna forma de datos personales reales.
- CORS restringido a orígenes de desarrollo (5173/3000).

## 7. Calidad del software

- **10 suites unitarias/integración** (`tests/test_*.py`): contrato, adaptador, features, clustering, interpretación, recomendaciones, scoring, API, audiencias, fuentes.
- **Lint ruff** (E/F/I/W) limpio; **CI GitHub Actions** (PostgreSQL como servicio: esquema → simulador → ingesta → segmentación → 10 suites → ruff → build de frontend).
- **E2E en vivo:** API completa, IA real y las 7 páginas con Playwright (Bitácora 16/10).

## 8. Referencias

- README del repositorio: fuente operativa (arquitectura §2, endpoints §9, estructura §16, mapa de IA §21, arranque §22).
- `docs/PRD_..._v2.0_FINAL.md`: estado de RF/RNF. · `docs/MVP_..._v2.0_FINAL.md`: alcance.
- `Bitacora.md`: historial cronológico completo de decisiones y verificaciones.
