# PRD FINAL — Motor Inteligente de Segmentación de Clientes

**Versión:** v2.0 (estado final de desarrollo)
**Fecha:** 16/10/2026
**Base:** `PRD_Motor_Inteligente_Segmentacion_Clientes_v1.1.pdf` (documento fuente original, que permanece inalterado)
**Complementos anteriores:** extracto Markdown del v1.1 + adenda Git del 14/09/2026 + README del repositorio (fuente operativa)

> Este documento **no sustituye** al PRD v1.1: registra el **estado final verificado** del producto, indica qué requisitos quedaron implementados (y cómo se probó cada uno), las desviaciones aprobadas y el mapa de dónde usa Inteligencia Artificial el sistema. Ante cualquier duda normativa, el PDF v1.1 manda.

---

## 1. Resumen del producto final

Motor de segmentación de clientes para PluriOne S.A. de C.V. que:

1. Recibe datos de **fuentes externas desacopladas** (CRM simulado vía API y CSVs arbitrarios subidos desde la web con sugerencia de mapeo por IA).
2. Los normaliza al **Contrato Interno de Datos V1** mediante adaptadores intercambiables.
3. Persiste en PostgreSQL con trazabilidad completa de ingestas e incidencias.
4. Construye features RFM + engagement, entrena **K-Means (k=6)** y asigna **etiquetas comerciales** por perfil de cluster con desempate determinista.
5. Expone todo por **API FastAPI** y lo hace operable desde una **web React** (dashboard, clientes, segmentos con recomendaciones de IA, audiencias dinámicas, fuentes y ejecuciones).
6. Ejecuta **predicción de cluster por cliente** mediante un modelo servido en la nube de Azure.

Estado: **MVP completo y verificado** — 10 suites de pruebas en verde, CI en GitHub Actions, build de frontend limpio, E2E en vivo de todos los apartados (registro en `Bitacora.md`, entrada del 16/10).

---

## 2. Estado final de los requisitos funcionales (PRD v1.1, sección 28)

| Req. | Descripción (síntesis) | Estado | Evidencia |
|------|------------------------|--------|-----------|
| RF-01 | Recibir datos estructurados de clientes desde fuentes externas | ✔ Cumple | Fuente simulada (`crm_simulator`, puerto 8001) + fuentes CSV (asistente web, vista Fuentes) |
| RF-02 | Cada fuente integrada mediante adaptador equivalente | ✔ Cumple | `SimulatedCRMAdapter` y `DynamicCSVAdapter` (misma interfaz `BaseAdapter`) |
| RF-03 | Convertir datos externos al contrato interno vigente | ✔ Cumple | Contrato V1 codificado con Pydantic en `src/contracts/`; suite `test_contrato` + `test_adapter` |
| RF-04 | Validar datos normalizados antes de incorporarlos | ✔ Cumple | Validación Pydantic por fila en ambos adaptadores |
| RF-05 | Registrar incidencias sin detener la ingesta | ✔ Cumple | `Incident` por fila inválida; tablas `ingestion_runs`/`ingestion_incidents` |
| RF-06 | Almacenar datos normalizados en PostgreSQL | ✔ Cumple | Espejo del contrato para 4 entidades + upserts idempotentes |
| RF-07 | Limpiar y transformar antes del análisis | ✔ Cumple | `src/features/rfm.py` con chequeos de calidad y reglas de inválidos |
| RF-08 | Generar features para segmentación | ✔ Cumple | 7 features por cliente (recency, frequency, monetary, web_visits, abandoned_carts, campaign_click_rate, tenure_days) |
| RF-09 | Ejecutar modelos de clustering | ✔ Cumple | K-Means con evaluación k=2..10, k=6 elegido por criterio comercial justificado |
| RF-10 | Generar segmentos automáticamente | ✔ Cumple | `segmentation_runs` + 6 segmentos por ejecución |
| RF-11 | Asignar clientes a los segmentos resultantes | ✔ Cumple | `customer_segments` por ejecución |
| RF-12 | Almacenar resultados y metadatos de ejecución | ✔ Cumple | Métricas (silhouette, inercia, Davies-Bouldin), semilla, duración y estado del run |
| RF-13 | Consultar segmentos y clientes asociados | ✔ Cumple | Endpoints `/segments`, `/customers` (con filtros y paginación) |
| RF-14 | Mostrar características de cada segmento | ✔ Cumple | Perfil JSONB por segmento + visualización en web |
| RF-15 | Repetir segmentación con datos actualizados | ✔ Cumple (mejorado) | `POST /segmentation/run` con desempate determinista de etiquetas (16/10) |
| RF-16 | Manejar versiones del modelo | ✔ Cumple | Modelo sembrado/registrado; `model_name`, semilla y métricas por run |
| RF-17 | Recomendaciones por segmento mediante IA generativa | ✔ Cumple | Azure OpenAI (gpt-5.4-mini) — ver mapa de IA §5 |
| RF-18 | Crear audiencias basadas en condiciones | ✔ Cumple (ampliado al MVP) | Audiencias dinámicas JSONB + export CSV |
| RF-19 | Actualizar audiencias cuando cambien los datos | ✔ Cumple | Membresía recalculada en cada consulta (persona no persistida) |

**Requisito extra entregado (fuera del alcance v1.1, sugerido en evolución):** conexión de fuentes CSV **sin código** mediante sugerencia de mapeo con IA (RF-01/02/03 amplificados).

## 3. Estado final de los requisitos no funcionales (sección 29)

| Req. | Estado | Notas |
|------|--------|-------|
| RNF-01 Seguridad | ✔ Parcial documentado | Secretos en `.env` (no versionado), API-key en el scoring de Azure, CORS restringido a desarrollo; sin login por decisión documentada (README §19) |
| RNF-02 Privacidad | ✔ | Datos sintéticos del simulador (sin datos reales de PluriOne) |
| RNF-03 Rendimiento | ✔ | Backend arranca ~20 s (carga de pandas/sklearn); predict 1-3 s (con posible arranque en frío de F1 documentado) |
| RNF-04 Escalabilidad | ✔ | Upserts idempotentes + recalculo por ejecución; sin reconstrucción completa |
| RNF-05 Modularidad | ✔ | contracts/adapters/persistence/features/ml/api/web separados |
| RNF-06 Bajo acoplamiento | ✔ | Fuente externa nunca define estructura interna (regla §13 del README) |
| RNF-07 Adaptabilidad | ✔ | Nuevas fuentes = nuevo adaptador; CSV sin código |
| RNF-08 Mantenibilidad | ✔ | 10 suites, lint ruff, CI, árbol por responsabilidad |
| RNF-09 Trazabilidad | ✔ | Runs de ingesta (duraciones, conteos, incidencias) y de segmentación (métricas) visibles en la web |
| RNF-10 Compatibilidad | ✔ | Navegadores modernos (React 19 + Vite) |
| RNF-11 Manejo de errores | ✔ | 404/409/422/500/501/502/503 controlados; degradación elegante si la IA no está; ErrorBoundary en la web |
| RNF-12 Observabilidad | ✔ | `/health` por dependencia, logs, historial de ejecuciones |
| RNF-13 Evolución del contrato | ✔ | Contrato versionado V1; cambios futuros se versionarían |

## 4. Desviaciones aprobadas y decisiones de arquitectura final

1. **Azure ML endpoint online → Azure App Service.** La suscripción bloqueaba los endpoints online (`SubscriptionNotRegistered`); la inferencia se sirve en `motor-seg-scoring` (F1, centralus) con el mismo artefacto y contrato. Migration path documentado (`azure/score.py` + `azure/deploy_endpoint.py` listos).
2. **k=6 sobre k=4:** decisión informada por análisis comercial de perfiles (PRD §30 permite combinar métricas con interpretación).
3. **Sin login en el MVP:** decisión documentada (README §19) con camino de evolución (API key/JWT → roles).
4. **Desempate determinista de etiquetas (16/10/2026):** los choques entre clusters ya no abortan la segmentación; se resuelven por "mejor calificado del concepto" + variantes de la etiqueta general. Solo la ambigüedad real exige revisión humana.
5. **Fuentes CSV asistidas por IA:** la IA sugiere entidad y mapeo; el humano siempre confirma y pasa validación del contrato antes de tocar la base.

## 5. Mapa de uso de Inteligencia Artificial

> Los tres usos de IA del sistema, con sus fronteras de seguridad:

1. **Recomendaciones comerciales por segmento (IA generativa).**
   - Proveedor: Azure OpenAI (`gpt-5.4-mini`, deployment de DataZone), recurso `openai-motor-seg`.
   - Entrada: agregados reales del segmento (perfil JSONB). Salida: JSON comercial (estrategia, tácticas, canales) persistido.
   - Guardas: temperature 0.4 (redacción comercial acotada; el mapeo CSV usa 0 determinista), parseo tolerante, timeout, degradación informativa si no está configurada. La información fluye backend→OpenAI; la web nunca llama a Azure directamente (hilo claro).

2. **Sugerencia de mapeo para fuentes CSV (IA generativa).**
   - Mismo deployment: recibe esquema introspectado del contrato + columnas del CSV + filas de muestra y propone entidad + mapping columnas→campos (sinónimos EN/ES, formatos de fecha, confianza estimada).
   - Guardas: filtro de columnas inexistentes, validación Pydantic, confirmación humana; el dry-run validado en seco ocurre contra el contrato antes de sincronizar. Degrada con 503 cuando no hay configuración, y el asistente manual sigue funcionando.

3. **Modelo de aprendizaje automático (no generativo).**
   - K-Means k=6 (scikit-learn, semilla fija) calculado **localmente** y su artefacto registrado en Azure ML; scoring servido en Azure App Service para la predicción por cliente.
   - Regla inviolable: **la IA nunca decide los clusters** (README §13); las etiquetas comerciales provienen de reglas humanas sobre el perfil.

No hay ningún otro uso de IA: las etiquetas, audiencias, dashboard o validaciones no dependen de modelos de lenguaje.

## 6. Criterios generales de aceptación (sección 36 del v1.1) — verificación

- Arquitectura por capas con contrato interno estable → ✔ (suite `test_contrato`, README §4)
- Adaptador por fuente y datos en PostgreSQL → ✔ (suite `test_sources`, E2E en vivo)
- Motor reproducible con segmentos etiquetados → ✔ (semilla fija, métricas por run)
- Interpretación comercial explicable → ✔ (reglas por perfil y desempate documentado)
- API + web funcionales y trazables → ✔ (10 suites + smoke E2E de 7 páginas con Playwright)
- Seguridad y privacidad controladas → ✔ (secretos fuera del repo; decisión de login documentada)

## 7. Evolución futura (más allá del MVP final)

- Autenticación real de la API (API key/JWT + roles) si el entorno de demostración lo exige.
- Migración del scoring a endpoint online de Azure ML cuando la suscripción lo permita.
- Adaptadores de CRM reales (HubSpot, Salesforce) vía el mismo `BaseAdapter`.
- Predicción de churn / CLV reutilizando la infraestructura de features.
- Contrato interno v2 si aparecen entidades nuevas (versionado por RNF-13).
