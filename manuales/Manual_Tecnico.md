# Manual Técnico — Motor Inteligente de Segmentación de Clientes

**Versión:** 2.0 · **Fecha:** 16/10/2026 · **Audiencia:** desarrolladores/operadores del sistema
**Propósito:** operación técnica del sistema: componentes en ejecución, procesos, endpoints, base de datos, pruebas, mantenimiento y solución de problemas. Para el diseño conceptual ver `Documento_Tecnico.md`; para instalar ver `Guia_de_Instalacion.md`.

---

## 1. Componentes en ejecución

| Componente | Comando | Puerto | Notas |
|---|---|---|---|
| CRM simulado (fuente externa) | `.venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001` | 8001 | Sistema externo independiente con formato propio (`clientId`, `totalAmount` como texto…) |
| API principal | `.venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000` | 8000 | **Arranque ~20 s** (carga de pandas/sklearn): no es un cuelgue |
| Frontend dev | `cd frontend && npm run dev` | 5173 | Vite + HMR; llama a `127.0.0.1:8000` (CORS ya configurado) |
| PostgreSQL | servicio `postgresql-x64-18` | 5432 | Base `motor_segmentacion` creada por `src.persistence.init_db` |

Servicios de nube (opcionales; el sistema degrada sin ellos):
- **Azure App Service `motor-seg-scoring`** (plan F1, centralus): sirve el modelo. Arranque en frío 10–30 s después de inactividad → el backend usa timeout 90 s + 1 reintento.
- **Azure OpenAI `openai-motor-seg`** (gpt-5.4-mini): recomendaciones y sugerencia de mapeo.

## 2. Procesos del pipeline

| Proceso | Comando/endpoint | Qué hace |
|---|---|---|
| Ingesta | `python -m src.persistence.ingest` o `POST /ingestion/sync` | Simulador → adaptador → PostgreSQL; registra run de ingesta con duraciones, conteos e incidencias |
| Segmentación | `python -m src.ml.segmentation` o `POST /segmentation/run` | Features → K-Means k=6 → etiquetas → `segmentation_runs`/`segments`/`customer_segments` |
| Predicción | `POST /customers/{id}/predict` | Features del cliente → scoring Azure → cluster + etiqueta del último run |
| Recomendación | `POST /segments/{id}/recommendation` | Perfil del segmento → Azure OpenAI → JSON comercial persistido |
| Fuente CSV | `POST /sources/csv/upload → /suggest → /validate → POST /sources/csv → POST /sources/{id}/sync` | Subida → sugerencia IA → dry-run → creación → sincronización |

## 3. API — referencia operativa

Base `http://127.0.0.1:8000` · Swagger: `/docs`.

**Infra/ingesta:** `GET /health` (estado por dependencia), `GET /ingestion/runs`, `POST /ingestion/sync`
**Clientes:** `GET /customers` (filtros `segment`, `city`, `q`; paginación `limit`/`offset`), `GET /customers/{id}`, `POST /customers/{id}/predict`
**Segmentación:** `POST /segmentation/run`, `GET /segmentation/runs`, `GET /segments`, `GET /segments/{id}`, `GET|POST /segments/{id}/recommendation`
**Dashboard:** `GET /dashboard` (KPIs, distribución, perfiles, top categorías)
**Audiencias:** `POST /audiences`, `GET /audiences`, `GET /audiences/{id}` (membresía recalculada en vivo), `DELETE /audiences/{id}`, `GET /audiences/{id}/export` (CSV)
**Fuentes:** `GET /sources`, `GET /sources/schema/{entidad}`, `POST /sources/csv/upload`, `POST /sources/csv/suggest`, `POST /sources/csv/validate`, `POST /sources/csv`, `POST /sources/{id}/sync`, `DELETE /sources/{id}`

Códigos: `404` inexistente · `409` nombre duplicado (audiencia/fuente) · `422` validación (con detalle del campo) · `500` error interno controlado · `501` dependencia IA/scoring no configurada · `502` dependencia nube caída · `503` IA no disponible (sugerencias).

## 4. Base de datos (tablas)

- **Contrato V1 (espejo con CHECKs):** `customers`, `transactions`, `interactions`, `campaign_events`
- **Trazabilidad:** `ingestion_runs`, `ingestion_incidents`, `segmentation_runs`, `segments`, `customer_segments`
- **Producto:** `recommendations`, `audiences` (condiciones JSONB), `data_sources` (entidad, mapeo, fichero, última sincronización)
- **Fuente de valores:** `src/persistence/schema.sql`; acceso a datos centralizado en `queries.py`; upserts idempotentes en `repository.py`

## 5. Pruebas y CI

```powershell
.\.venv\Scripts\python.exe -m tests.test_contrato      # patrón por suite (10 módulos):
# contrato, adapter, features, clustering, segmentation, recommendations,
# scoring, api, audiences, sources
.\.venv\Scripts\python.exe -m ruff check src tests crm_simulator azure
cd frontend; npm run build
```
CI (`.github/workflows/ci.yml`): en cada push levanta PostgreSQL 18 como servicio, aplica esquema, simula ingesta, segmenta, corre las **10 suites** + ruff + build del frontend. Estado: badge al inicio del README.

## 6. Mantenimiento — dónde tocar

| Quiero… | Archivo |
|---|---|
| Añadir/quitar un campo del contrato | `src/contracts/` (+ actualiza sin tocar más: la web y el prompt de IA se generan por introspección) |
| Añadir una fuente nueva (API real) | Nuevo archivo en `src/adapters/` implementando `BaseAdapter` |
| Cambiar la k o el modelo | `src/ml/clustering.py` (`FINAL_K`, `SEED`) + regenérese el artefacto servido en Azure |
| Cambiar etiquetas comerciales | `src/ml/segmentation.py` (`REGLAS`, `METRICAS_DESEMPATE`, `CLUSTER_DESCRIPTIONS`) |
| Cambiar reglas de audiencias | `queries.audience_members` |
| Ajustar proveedor de recomendaciones/mapeo | `src/services/recommendations.py`, `src/services/mapping_suggest.py` |

Reglas inviolables (README §13): no acoplar el motor al formato del CRM, no usar IA generativa para decidir clusters, no llamar a Azure desde el frontend, no subir secretos al repo.

## 7. Solución de problemas frecuentes

| Síntoma | Causa | Acción |
|---|---|---|
| El backend no responde los primeros ~20 s | Carga inicial de pandas/sklearn | Esperar; es normal |
| `predict` tarda 10–30 s | Arranque en frío del plan F1 | Reintentar; el backend ya reintenta solo una vez |
| `501` en recomendación/predicción | `.env` sin `AZURE_OPENAI_*` / `AZURE_SCORING_*` | Configurar `.env` y reiniciar backend |
| `502` en predict | Scoring en Azure caído/durmiendo | Verificar App Service en portal; reintentar |
| `503` en sugerencia de mapeo | IA no configurada o con fallo | Continuar con el asistente manual (el dry-run sigue validando) |
| La web sale en blanco | Servidores caídos tras días | Levantar simulador/backend; usar el botón de recarga del ErrorBoundary |
| `Error interno del servidor` en cualquier endpoint | Ver el traceback en la consola del backend | Capturar y revisar; el run de segmentación queda marcado `error` en Ejecuciones |
| Puerto en uso (8000/8001/5173) | Proceso previo vivo | `Get-NetTCPConnection -LocalPort <puerto> -State Listen` → parar proceso |

## 8. Historial y trazabilidad

Toda decisión, verificación y bloqueo del desarrollo está registrado cronológicamente en `Bitacora.md`. El historial de Git no se reescribe; releases etiquetados: `v1.0.0` (MVP original) y `v2.0.0` (cierre final).
