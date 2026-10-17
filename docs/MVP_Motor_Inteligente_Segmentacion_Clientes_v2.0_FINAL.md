# MVP FINAL — Motor Inteligente de Segmentación de Clientes

**Versión:** v2.0 (MVP cerrado)
**Fecha:** 16/10/2026
**Base:** `MVP_Motor_Inteligente_Segmentacion_Clientes_v1.1.pdf` (permanece inalterado) y README del repositorio (fuente operativa)
**Estado de pruebas:** 10/10 suites en verde + lint ruff + build del frontend + CI de GitHub Actions en verde + revisión integral E2E en vivo (Bitácora 16/10)

> Documento de cierre: declara qué entrega el MVP final, cómo levantarlo desde el repositorio y cómo demostrarlo. No elimina ni altera el documento v1.1; lo actualiza a estado final.

---

## 1. Alcance entregado (etapas del README §12 + ampliaciones)

| # | Etapa | Entregable | Estado |
|---|-------|------------|--------|
| 1 | Entorno y base | Python 3.14, PostgreSQL 18, Git, Tickets; estructura por capas | ✔ |
| 2 | Contrato V1 | `src/contracts/` Pydantic + documento + suite | ✔ |
| 3 | Fuente simulada | `crm_simulator` (API 8001, formatos externos propios) | ✔ |
| 4 | Adaptador externo | `SimulatedCRMAdapter` + reporte de incidencias | ✔ |
| 5 | Persistencia | Esquema espejo del contrato + trazabilidad | ✔ |
| 6 | Features | RFM + engagement (7 features) | ✔ |
| 7 | Clustering | K-Means k=6, evaluación, estabilidad, validación | ✔ |
| 8 | Interpretación | Etiquetas comerciales + desempate determinista (16/10) | ✔ |
| 9 | Backend | FastAPI con routers por dominio + `/health` real | ✔ |
| 10-11 | Azure inferencia | Scoring en App Service (desviación aprobada §7 del README); artefacto/registro en Azure ML | ✔ |
| 12 | Recomendaciones | Azure OpenAI por segmento con persistencia | ✔ |
| 13 | Frontend | React 19 + TS: 7 páginas, gráficas, filtros, export, tema claro/oscuro | ✔ |
| 14 | Seguridad y pruebas | Handler global, timeouts, 10 suites, ruff, CI con badge | ✔ |
| 15 | Documentación | README completo, guía de demo §18, bitácora histórica, Docker §20 | ✔ |
| + | **Audiencias dinámicas** | PRD §16 hechas MVP: condiciones JSONB, recálculo vivo, export CSV | ✔ |
| + | **Fuentes CSV con IA** | Asistente web: subida → sugerencia de mapeo por IA → validación en seco → sincronización; introspección del contrato sin hardcodeo | ✔ |
| + | **Profesionalización** | CI en GitHub Actions, API tipada (OpenAPI), capturas automáticas, autodocumentación de decisión de login, Docker opcional | ✔ |

## 2. Arquitectura final (resumen)

```
Fuentes externas ──▶ Adaptadores (contrato V1) ──▶ PostgreSQL (trazabilidad)
                                                        │
                          features RFM ──▶ K-Means ──▶ segmentos + etiquetas + customer_segments
                                                        │
                          ┌─────────────────────────────┤
                     API FastAPI (8000)          Azure scoring (App Service)
                          │                                  ▲
                     React web (5173) ──── /customers/{id}/predict ┘

Notas: el clustering corre local y reproducible (semilla fija); su artefacto
se sirve desde Azure para la prediccion; todas las llamadas a Azure salen
unicamente desde el backend (la web nunca toca Azure ni sus llaves).
```

Detalle completo en README §2, §16 y PRD FINAL (docs/PRD_..._v2.0_FINAL.md).

## 3. Instrucciones de arranque desde el repositorio

**Requisitos:** Windows, Git, Python 3.12+ (proyecto en 3.14), Node.js 20+, PostgreSQL 16+ (proyecto en 18).

```powershell
# 1) Obtener el proyecto
git clone https://github.com/Ezumi005/G19X-UTSLRC-AABR-667-ACADEMIC.git MotorSeg
cd MotorSeg

# 2) Entorno Python y dependencias
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 3) Variables de entorno (sin ellas: modo degradado sin IA ni scoring)
copy .env.example .env         # editar DATABASE_URL, AZURE_SCORING_*, AZURE_OPENAI_*

# 4) Base de datos
.\.venv\Scripts\python.exe -m src.persistence.init_db

# 5) CRM simulado (source externa; terminal 1)
.\.venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001

# 6) Primera ingesta + segmentación (terminal 2, raíz del proyecto)
.\.venv\Scripts\python.exe -m src.persistence.ingest
.\.venv\Scripts\python.exe -m src.ml.segmentation

# 7) Backend principal (terminal 2)
.\.venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000   # ~20 s de arranque

# 8) Frontend (terminal 3)
cd frontend; npm install; npm run dev   # http://localhost:5173
```

Verificación rápida: `GET http://127.0.0.1:8000/health` debe devolver `ok` (o `degradado` solo si `.env` incompleta).
Alternativa todo-en-uno: `docker-compose up` (Docker Desktop, README §20).
Pruebas: 10 suite modules + frontend build + CI (detalle README §17).

## 4. Guía de demostración (resumen)

1. Iniciar sesión de demo en el README §18 del repo (5 minutos: dashboard → clientes → predict → segmento con recomendación → audiencias → fuentes CSV con IA → ejecuciones).
2. La vista **Fuentes** con un CSV en español crudo muestra la sugerencia de la IA con badge de confianza: demostración del diferenciador del cierre.

## 5. Historial de versiones

- **v1.0** (28/09/2026): MVP original (etapas 1-15, release/tag v1.0.0).
- **v1.1** (15-16/10/2026): profesionalización (CI, API tipada, capturas, login docs, Docker) y fuentes CSV asistidas por IA.
- **v2.0 FINAL** (16/10/2026): robustez de interpretación (desempate determinista y variantes), revisión integral E2E (API + IA real + Playwright), documentación final. **MVP declarado cerrado**; ver PRD FINAL para el estado de requisitos y el mapa de IA.
