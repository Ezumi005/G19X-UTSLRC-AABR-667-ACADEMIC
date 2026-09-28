# Motor Inteligente de Segmentación de Clientes

## 1. Propósito del proyecto

Construir una aplicación web que reciba datos de clientes, los normalice, calcule variables útiles, segmente clientes mediante Machine Learning y genere recomendaciones comerciales por segmento mediante Azure OpenAI.

El proyecto se desarrolla para **PluriOne S.A. de C.V. (Develop Talent & Technology)** y se implementará inicialmente con **datos simulados**, porque no se contará con acceso a los sistemas reales de la empresa.

## 2. Decisión de arquitectura principal

**El sistema NO se construye alrededor del CRM simulado.**

El CRM simulado es únicamente una fuente externa de entrada. El núcleo del sistema trabaja con un **modelo interno de datos estable**. Cada fuente externa debe tener un **adaptador** que traduzca su formato al formato interno.

Esto permite reemplazar en el futuro la fuente simulada por HubSpot, Salesforce, Dynamics, una base de datos, archivos CSV/JSON u otra fuente sin modificar el motor de segmentación.

```text
Fuente externa
    |
    v
Adaptador de la fuente
    |
    v
Contrato interno de datos
    |
    v
PostgreSQL / procesamiento / ML / aplicación
```

## 3. Fuente de datos del MVP

Se creará una **API que simule la fuente de datos de un CRM**. Esta API debe comportarse como un sistema externo y entregar datos en un formato propio.

Endpoints propuestos del simulador:

- `GET /crm/customers`
- `GET /crm/transactions`
- `GET /crm/interactions`
- `GET /crm/campaign-events`

La API simulada NO debe devolver directamente las features finales del modelo. Debe entregar datos suficientemente cercanos a una fuente empresarial para que el sistema tenga que integrarlos y transformarlos.

Implementación actual: `crm_simulator/` — generador de dataset con semilla fija (6 perfiles de comportamiento, ~500 clientes, 18 meses de historia) + API FastAPI en el puerto 8001. Su formato externo (`clientId`, `totalAmount` como texto, `productLine`, etc.) es deliberadamente distinto del contrato interno. El perfil real de cada cliente se guarda como ground truth en `data/meta.json` y NO se sirve por la API.

## 4. Contrato interno de datos

Los adaptadores deben convertir cualquier fuente al siguiente modelo conceptual.

### Customer

- `customer_id`
- `age`
- `city`
- `registered_at`

### Transaction

- `transaction_id`
- `customer_id`
- `purchased_at`
- `amount`
- `category`

### Interaction

- `interaction_id`
- `customer_id`
- `interaction_type`
- `occurred_at`

### CampaignEvent

- `campaign_id`
- `customer_id`
- `event_type`
- `occurred_at`

Los tipos y la obligatoriedad de cada campo están definidos en el **Contrato Interno de Datos V1**, formalizado en `docs/contrato_interno_datos_v1.md` y codificado con Pydantic en `src/contracts/` (prueba: `tests/test_contrato.py`). Los campos opcionales pueden ser nulos. Los cambios al contrato deben versionarse y registrarse en `Bitacora.md`.

## 5. Features para segmentación

A partir del contrato interno se construye una tabla de features por cliente. Como mínimo:

- `recency_days`: días desde la última compra.
- `frequency`: cantidad de compras.
- `monetary`: gasto acumulado.

Features adicionales permitidas:

- `avg_ticket`
- `campaign_click_rate`
- `emails_opened`
- `web_visits`
- `abandoned_carts`
- `favorite_category`
- métricas de engagement derivadas.

**RFM es la base mínima.** No agregar features sin justificar su utilidad y calidad.

Implementación actual: `src/features/rfm.py` — construye desde PostgreSQL la tabla por cliente (498 filas): RFM con fecha de referencia determinista (`max(purchased_at)` del dataset) más features justificadas: `avg_ticket`, `tenure_days`, `web_visits`, `product_views`, `abandoned_carts`, `emails_opened`, `campaign_click_rate` y `favorite_category` (metadato, no entra directo al clustering). `recency_days` es nulo para clientes sin compras; la imputación se decidirá en la etapa de ML. Las features no se persisten: se computan a demanda (CSV de inspección en `data/features_rfm.csv`).

## 6. Machine Learning

- Lenguaje: Python.
- Librerías iniciales: Pandas, NumPy y Scikit-learn.
- Enfoque inicial: clustering.
- Algoritmo inicial: K-Means.
- El modelo se desarrolla y valida primero de forma local.
- Se deben comparar distintas cantidades de clusters y evaluar al menos Silhouette Score e interpretación comercial.
- Los clusters no reciben nombres comerciales hasta analizar sus características reales.

Ejemplo correcto:

`Cluster 2` -> se analiza -> "Clientes frecuentes de alto valor".

No asignar etiquetas comerciales antes de conocer los resultados del modelo.

Implementación actual: `src/ml/clustering.py` — prepara la matriz (imputación de `recency_days` nulo al máximo observado, `log1p` en variables sesgadas, StandardScaler), evalúa k=2..10 con Silhouette/Inertia/Davies-Bouldin bajo una regla pre-declarada (mejor Silhouette, empate ≤0.01 → menor k), entrena K-Means (semilla 42, n_init=10), verifica estabilidad (ARI entre semillas), perfila clusters en unidades originales y valida contra los perfiles reales (`data/meta.json`, solo validación). Features del modelo: `recency_days, frequency, monetary, web_visits, abandoned_carts, campaign_click_rate, tenure_days` (se excluyen `avg_ticket`, `product_views` y `emails_opened` por correlación alta). Artefacto: `models/kmeans_local.pkl` (no versionado). Estado: **k=6, decisión de negocio** (Bitacora.md, 22/09/2026, amparada en PRD §30): Silhouette 0.414 casi idéntico al mejor estadístico 0.430 (k=4), estabilidad 0.993, ARI vs perfiles reales 0.794 (vs 0.659 de k=4); aísla el segmento de riesgo con pureza 100%. La regla estadística se sigue calculando e imprimiendo en cada ejecución para trazabilidad.

Interpretación y persistencia: `src/ml/segmentation.py` asigna **etiquetas comerciales** mediante reglas sobre el perfil de cada cluster (independientes del número de cluster; falla si dos clusters reciben la misma etiqueta) y guarda cada ejecución en `segmentation_runs`, `segments` (con perfil JSONB) y `customer_segments`. Etiquetas vigentes: Clientes frecuentes de alto valor · Navegadores sin compra · Compradores ocasionales · Clientes nuevos · Navegadores con compra esporádica · Clientes en riesgo de inactividad.

## 7. Azure Machine Learning

Azure Machine Learning se usa DESPUÉS de validar el modelo localmente.

Responsabilidades cumplidas:
- registrar el modelo: **hecho** (`kmeans-local:1` en el workspace `ml-motor-seg-v2`);
- versionarlo y definir su ambiente: **hecho** (`motor-segmentacion-env:1`, mismas versiones del entrenamiento);
- desplegarlo y exponer un endpoint de inferencia: **los endpoints online de Azure ML no están disponibles para este tipo de suscripción** (bloqueo documentado con evidencia en `Bitacora.md`, 23-28/09/2026: 4 regiones, 4 workspaces, proveedores completos, ARM directo con identidad — el plano de inferencia rechaza la suscripción).

**Desviación aprobada (documentada):** la inferencia se sirve en **Azure App Service** (`motor-seg-scoring`, plan F1 gratuito en centralus) con el MISMO artefacto y lógica (`azure/scoring_app/`, autenticación `X-API-Key`). El backend lo consume mediante `src/services/scoring.py` (`POST /customers/{id}/predict`); React nunca lo toca. El contrato de scoring es idéntico al de `azure/score.py` (Azure ML) para poder migrar a un endpoint online si la suscripción lo permite en el futuro.

## 8. Azure OpenAI

Azure OpenAI NO realiza la segmentación.

Su función en este proyecto es recibir un resumen de las características de un segmento y producir:

- descripción comercial;
- recomendaciones de marketing/ventas;
- acciones sugeridas por segmento.

Las recomendaciones son apoyo para decisión humana, no acciones automáticas obligatorias.

## 9. Backend

Tecnología principal: **Python + FastAPI**.

Responsabilidades:

- consumir fuentes externas;
- ejecutar adaptadores;
- validar datos;
- comunicarse con PostgreSQL;
- preparar procesos de segmentación;
- consumir Azure Machine Learning;
- consumir Azure OpenAI;
- exponer la API principal del producto;
- proteger credenciales y secretos.

Endpoints iniciales de la aplicación:

- `POST /ingestion/sync`
- `GET /customers`
- `GET /customers/{id}`
- `POST /customers/{id}/predict` (inferencia en Azure)
- `POST /segmentation/run`
- `GET /segments`
- `GET /segments/{id}`
- `GET /segments/{id}/recommendation`
- `POST /segments/{id}/recommendation`

Los nombres pueden cambiar, pero las responsabilidades deben mantenerse separadas.

Implementación actual: `src/api/` (puerto 8000: `.venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000`). Routers por dominio (`ingestion`, `customers`, `segments`, `dashboard`) más `/health`. `GET /segments` devuelve el último run exitoso; `POST /segments/{id}/recommendation` está reservado (501) hasta la etapa de Azure OpenAI. Lecturas centralizadas en `src/persistence/queries.py`. CORS habilitado solo para desarrollo React (localhost:5173/3000). Verificado en vivo: los 8 endpoints responden, incluidos 404 y 501.

## 10. PostgreSQL

PostgreSQL almacena la representación interna del sistema y sus resultados.

Entidades mínimas esperadas:

- customers
- transactions
- interactions
- campaign_events
- segmentation_runs
- segments
- customer_segments
- recommendations

No guardar el payload externo como si fuera el modelo interno definitivo. Primero debe pasar por su adaptador y validación.

Implementación actual: `src/persistence/schema.sql` — tablas `customers`, `transactions`, `interactions`, `campaign_events` (espejo del contrato V1, con CHECKs de enums), `ingestion_runs`/`ingestion_incidents` (trazabilidad de ingestiones) y `segmentation_runs`/`segments`/`customer_segments` (trazabilidad de segmentaciones: cada ejecución conserva sus segmentos con perfil JSONB y sus asignaciones). Sin FKs en las tablas de datos: la integridad referencial corresponde al procesamiento (contrato, sección 2); las tablas de segmentación sí llevan FKs estructurales. Falta `recommendations` (llegará con Azure OpenAI).

## 11. Frontend

Tecnología: **React** (preferentemente TypeScript/TSX).

Vistas mínimas:

- Dashboard.
- Clientes.
- Segmentos.
- Detalle de segmento.
- Recomendaciones.

React consume únicamente la API del backend. Las claves de Azure y demás secretos nunca deben estar en el frontend.

Implementación actual: `frontend/` — Vite + React 19 + TypeScript + react-router. Vistas: Dashboard (indicadores y distribución de segmentos), Clientes (tabla paginada con expansión de detalle y segmento asignado), Segmentos (tarjetas) y Detalle de segmento (perfil medio, métricas del run y botón de recomendación que informa del estado pendiente de Azure OpenAI). Cliente HTTP centralizado en `src/api.ts` (URL base configurable con `VITE_API_BASE`); sin credenciales ni llamadas a servicios externos.

## 12. Orden de desarrollo

1. Definir contrato interno de datos.
2. Generar dataset simulado realista.
3. Crear API simulada del CRM.
4. Crear adaptador del CRM simulado.
5. Validar y guardar datos normalizados en PostgreSQL.
6. Crear pipeline de preparación y features RFM.
7. Crear y validar K-Means localmente.
8. Interpretar clusters.
9. Crear backend principal con FastAPI.
10. Registrar y desplegar modelo en Azure ML.
11. Conectar backend con endpoint de Azure ML.
12. Integrar Azure OpenAI para recomendaciones.
13. Crear React y consumir la API del backend.
14. Agregar seguridad, manejo de errores y pruebas.
15. Documentar y preparar demostración.

Nota: las etapas 10-12 (Azure ML / Azure OpenAI) requieren suscripción de Azure; la etapa 13 (React) se adelantó mientras se obtiene la suscripción (registro en `Bitacora.md`, 22/09/2026).

## 13. Reglas que NO se deben romper

- No acoplar el modelo de ML al formato del CRM simulado.
- No modificar el motor de segmentación para integrar una nueva fuente; crear un nuevo adaptador.
- No usar Azure OpenAI para decidir los clusters.
- No llamar directamente a Azure ML u OpenAI desde React.
- No exponer claves o secretos en el frontend.
- No empezar por Azure ML antes de tener un modelo local funcional.
- No agregar tecnologías secundarias si el camino principal todavía no funciona.
- No asumir datos reales de PluriOne; el proyecto trabaja con datos simulados.

### Control de versiones con Git

Todo el desarrollo debe registrarse progresivamente en Git para generar un historial completo del proyecto:

- Git se inicializa desde el comienzo del desarrollo.
- Se realizan commits después de avances significativos, con mensajes claros y descriptivos.
- No se espera hasta el final para crear el historial.
- No se elimina ni altera el historial de commits existente.
- El repositorio debe quedar preparado para vincularse posteriormente con GitHub (remoto pendiente de configurar).
- Cada avance importante queda reflejado tanto en Git como en `Bitacora.md`.

## 14. Qué debe demostrar el MVP

El MVP debe probar de extremo a extremo que:

1. una fuente CRM simulada puede entregar datos;
2. un adaptador puede traducirlos al contrato interno;
3. los datos pueden validarse y persistirse;
4. Python puede generar features de segmentación;
5. el modelo puede crear clusters útiles;
6. Azure ML puede servir el modelo desplegado;
7. Azure OpenAI puede generar recomendaciones por segmento;
8. FastAPI puede exponer el resultado;
9. React puede visualizarlo.

## 15. Adaptación futura a un CRM real

Para integrar un CRM real:

1. estudiar su API o mecanismo de acceso;
2. crear un conector/adaptador para esa fuente;
3. mapear sus campos al contrato interno;
4. validar la salida del adaptador;
5. mantener sin cambios el resto del sistema siempre que el contrato interno no cambie.

**Principio rector:** las fuentes externas cambian; el núcleo del sistema debe permanecer estable.

## 16. Estructura del repositorio

```text
MSIA/                          # raíz del proyecto (repositorio Git)
├── README.md                  # este documento: mapa del proyecto
├── Bitacora.md                # historial cronológico del desarrollo
├── PRD_*.pdf / MVP_*.pdf      # fuentes de verdad oficiales (documentos originales)
├── .gitignore
├── requirements.txt           # dependencias Python del proyecto
├── docs/                      # documentación técnica
│   ├── contrato_interno_datos_v1.md                  # contrato interno V1 (documento)
│   ├── PRD_Motor_..._v1.1.md                         # texto extraído del PRD (referencia)
│   └── MVP_Motor_..._v1.1.md                         # texto extraído del MVP (referencia)
├── src/                       # núcleo de la aplicación
│   ├── contracts/             # contrato interno codificado (Pydantic)
│   ├── adapters/              # adaptadores: fuente externa → contrato interno
│   │   ├── base.py            # BaseAdapter (ABC) + AdapterResult/AdapterReport
│   │   └── simulated_crm_adapter.py   # SimulatedCRMAdapter (API en puerto 8001)
│   ├── persistence/           # PostgreSQL: esquema, repositorio, ingesta y consultas
│   │   ├── schema.sql         # esquema interno (espejo del contrato V1 + segmentación)
│   │   ├── db.py              # conexión vía DATABASE_URL (.env)
│   │   ├── repository.py      # upserts idempotentes
│   │   ├── queries.py         # consultas de lectura para la API
│   │   ├── init_db.py         # crea la base y aplica el esquema
│   │   └── ingest.py          # sincronización: simulador → adaptador → PostgreSQL
│   ├── features/              # ingeniería de características
│   │   └── rfm.py             # tabla RFM + engagement por cliente (desde PostgreSQL)
│   ├── ml/                    # motor de segmentación
│   │   ├── clustering.py      # preparación, evaluación de k, entrenamiento y validación
│   │   └── segmentation.py    # etiquetas comerciales + persistencia de ejecuciones
│   ├── services/              # servicios que consumen plataformas Azure
│   │   ├── recommendations.py # Azure OpenAI (gpt-5.4-mini DataZone)
│   │   └── scoring.py         # cliente del scoring en Azure App Service
│   └── api/                   # API principal FastAPI (puerto 8000)
│       ├── app.py             # create_app + /health + CORS de desarrollo
│       └── routes/            # routers: ingestion, customers, segments, dashboard
├── tests/                     # pruebas (contrato y adaptador)
├── crm_simulator/             # API CRM simulada: fuente externa independiente
│   ├── generate_data.py       # generador del dataset (semilla fija → reproducible)
│   └── app.py                 # API FastAPI con formato externo propio (puerto 8001)
├── azure/                     # despliegue en Azure
│   ├── scoring_app/           # servicio de inferencia (App Service, F1, centralus)
│   ├── score.py               # scoring equivalente para endpoint online de Azure ML
│   ├── conda_env.yml / environment.yml  # entorno registrado en Azure ML
│   └── deploy_endpoint.py     # despliegue por SDK (endpoint online)
├── data/                      # dataset generado *.json + meta.json/ground truth (no versionado)
├── models/                    # artefactos de modelos, p.ej. kmeans_local.pkl (no versionado)
├── frontend/                  # React 19 + TypeScript + Vite (puerto 5173)
│   └── src/
│       ├── api.ts             # cliente HTTP de la API del backend
│       ├── types.ts           # tipos de las respuestas
│       └── pages/             # Dashboard, Customers, Segments, SegmentDetail
└── .venv/                     # entorno virtual local (no versionado)
```

Los extractos en `docs/` son solo para consulta rápida; ante cualquier duda, el PDF original manda.

## 17. Preparación del entorno de desarrollo

Verificado (10/09/2026): Git 2.55, Python 3.14.2, Node.js 24 + npm 11, PostgreSQL 18.6 (servicio `postgresql-x64-18`), winget.

```powershell
# desde la raíz del proyecto
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m tests.test_contrato     # prueba del contrato interno
.venv\Scripts\python.exe -m tests.test_adapter      # prueba del adaptador (unitaria, sin API encendida)
```

**API CRM simulada** (fuente externa, puerto 8001):

```powershell
.venv\Scripts\python.exe -m crm_simulator.generate_data          # genera data/*.json (semilla fija, reproducible)
.venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001
# Documentación interactiva: http://127.0.0.1:8001/docs
# Backend principal (puerto 8000)
.venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000
# Docs interactivas: http://127.0.0.1:8000/docs  (POST /ingestion/sync requiere el simulador en 8001)
```

El backend principal usa el puerto 8000. Las credenciales de PostgreSQL y de Azure viven en un `.env` local, nunca en el repositorio.

**Frontend React** (puerto 5173; requiere el backend en 8000):

```powershell
cd frontend
npm install        # solo la primera vez
npm run dev        # abre http://localhost:5173
```

**PostgreSQL** (requiere `.env` con `DATABASE_URL`; ver `.env.example`):

```powershell
.venv\Scripts\python.exe -m src.persistence.init_db    # crea la base motor_segmentacion y aplica el esquema (idempotente)
.venv\Scripts\python.exe -m src.persistence.ingest     # ingesta completa: simulador → adaptador → PostgreSQL (requiere simulador en 8001)
.venv\Scripts\python.exe -m src.features.rfm          # features RFM desde PostgreSQL (escribe data/features_rfm.csv)
.venv\Scripts\python.exe -m src.ml.clustering         # evaluación de k + entrenamiento + validación (escribe models/kmeans_local.pkl)
.venv\Scripts\python.exe -m src.ml.segmentation       # ejecuta y persiste la segmentación (k=6, con etiquetas comerciales)
```
