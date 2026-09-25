# Bitácora del Proyecto

## Proyecto
**Motor Inteligente de Segmentación de Clientes**

## Objetivo de esta bitácora
Este archivo registra cronológicamente el trabajo realizado durante el proyecto, tanto en la parte **técnica** como en la **documentación**.

Debe servir para que cualquier modelo de IA o desarrollador pueda revisar rápidamente:
- qué se hizo;
- cuándo se hizo;
- qué decisiones se tomaron;
- por qué se tomaron;
- qué archivos o componentes se modificaron;
- qué problemas aparecieron;
- cuál es el siguiente paso.

---

# Reglas de uso para modelos de IA

1. Antes de trabajar en el proyecto, revisar en este orden:
   - `README.md`
   - `PRD`
   - `MVP`
   - `Bitacora.md`

2. Agregar una entrada cuando exista un avance real:
   - desarrollo;
   - investigación técnica;
   - documentación;
   - pruebas;
   - correcciones;
   - decisiones de arquitectura;
   - cambios de alcance;
   - problemas encontrados;
   - integración de tecnologías.

3. Escribir siempre en **primera persona**.

4. Cada entrada debe incluir:
   - fecha;
   - hora;
   - tipo de actividad;
   - actividad realizada;
   - decisiones tomadas;
   - resultado;
   - archivos o componentes afectados;
   - siguiente paso.

5. Formato obligatorio de fecha y hora:
   - Fecha: `DD/MM/AAAA`
   - Hora: `HH:MM` en formato de 24 horas.

6. No inventar actividades, resultados, decisiones ni horas.

7. Si una actividad pasada no tiene una hora confirmada, escribir:
   - `Hora: no registrada`

8. No borrar decisiones anteriores aunque después cambien.  
   Si una decisión cambia, crear una nueva entrada explicando el cambio.

9. Mantener las entradas concretas y útiles.  
   Esta bitácora no sustituye al PRD, MVP, README ni a la documentación técnica.

10. Diferenciar claramente entre:
   - **Técnico**
   - **Documentación**
   - **Investigación**
   - **Pruebas**
   - **Arquitectura**
   - **Gestión**

---

# Historial

## 02/09/2026 — Hora: no registrada
**Tipo:** Investigación / Análisis inicial

**Actividad realizada:**  
Comencé a estudiar el proyecto **Motor Inteligente de Segmentación de Clientes** para entender qué debía construirse y qué función tendría cada tecnología mencionada.

Investigué conceptos como CRM, segmentación de clientes, Machine Learning, FastAPI, React, PostgreSQL y servicios de Azure.

**Decisiones tomadas:**  
Concluí que antes de desarrollar debía entender:
- de dónde vendrían los datos;
- qué datos estarían disponibles;
- cómo se accedería a ellos;
- qué esperaba obtener el sistema.

**Resultado:**  
Obtuve una primera visión general del proyecto y de sus componentes principales.

**Componentes afectados:**  
Ninguno. Etapa de análisis.

**Siguiente paso:**  
Preparar el levantamiento de requerimientos.

---

## 07/09/2026 — 12:50
**Tipo:** Documentación / Levantamiento de requerimientos

**Actividad realizada:**  
Preparé un cuestionario para recopilar información necesaria sobre el sistema, los datos de clientes, CRM, APIs, fuentes de datos, usuarios, segmentación e integración.

También preparé una versión para Google Forms y redacté un mensaje para que el profesor, quien funciona como intermediario, pudiera hacerlo llegar a la empresa.

**Decisiones tomadas:**  
El cuestionario debía enfocarse principalmente en:
- problema a resolver;
- datos disponibles;
- fuentes de información;
- mecanismos de acceso;
- CRM actual;
- APIs;
- usuarios;
- funcionalidades;
- alcance.

**Resultado:**  
Se obtuvo una estructura inicial para realizar el levantamiento de requerimientos.

**Componentes afectados:**  
Documentación de requerimientos.

**Siguiente paso:**  
Esperar definición sobre el acceso real a la empresa y a sus datos.

---

## 07/09/2026 — 14:01
**Tipo:** Investigación técnica

**Actividad realizada:**  
Continué estudiando las tecnologías y conceptos del proyecto para comprender cómo se relacionan.

Revisé:
- CRM;
- ERP;
- CSV;
- API;
- endpoint;
- FastAPI;
- Python;
- React;
- PostgreSQL;
- Machine Learning;
- Azure Machine Learning;
- deployment;
- scoring code.

**Decisiones tomadas:**  
Separé conceptualmente las responsabilidades:
- React: frontend.
- FastAPI + Python: backend y lógica.
- PostgreSQL: almacenamiento.
- Python + Scikit-learn: creación del modelo de Machine Learning.
- Azure Machine Learning: registro, despliegue y gestión del modelo.
- Azure OpenAI Service: recomendaciones comerciales posteriores a la segmentación.

**Resultado:**  
La arquitectura comenzó a quedar conceptualmente clara.

**Componentes afectados:**  
Diseño conceptual de arquitectura.

**Siguiente paso:**  
Definir cómo entrarían los datos al sistema.

---

## 08/09/2026 — 11:16
**Tipo:** Documentación / Alcance

**Actividad realizada:**  
Separé formalmente el **PRD** del **MVP**.

Definí que:
- el PRD representa la visión completa del producto;
- el MVP representa únicamente la primera versión funcional que será desarrollada.

**Decisiones tomadas:**  
No mezclar PRD y MVP en el mismo documento ni tratar ambos como si tuvieran el mismo alcance.

**Resultado:**  
Se crearon dos líneas de documentación independientes para el proyecto.

**Componentes afectados:**  
PRD y MVP.

**Siguiente paso:**  
Ajustar ambos documentos cuando se definiera el origen real o simulado de los datos.

---

## 08/09/2026 — Hora: no registrada
**Tipo:** Arquitectura / Alcance

**Actividad realizada:**  
Recibí la indicación de que no tendría contacto directo con la empresa y que debía **simular los datos de entrada del CRM**.

**Decisiones tomadas:**  
El desarrollo no dependerá de acceso real al CRM de la empresa.

Los datos utilizados durante el desarrollo serán simulados, pero deberán representar un escenario empresarial realista.

**Resultado:**  
El proyecto obtuvo mayor libertad para diseñar una arquitectura adaptable sin depender de un proveedor específico.

**Componentes afectados:**  
PRD, MVP, arquitectura y estrategia de datos.

**Siguiente paso:**  
Definir cómo desacoplar la fuente simulada del motor de segmentación.

---

## 09/09/2026 — 12:59
**Tipo:** Arquitectura

**Actividad realizada:**  
Definí una decisión arquitectónica central: **el sistema no se construirá alrededor del CRM simulado**.

El CRM simulado será tratado únicamente como una fuente externa de datos.

**Decisiones tomadas:**  
Se utilizará una capa de adaptación entre las fuentes externas y el núcleo del sistema.

La arquitectura conceptual queda basada en:
- fuente externa;
- adaptador;
- contrato interno de datos;
- procesamiento;
- Machine Learning;
- servicios;
- frontend.

**Resultado:**  
El motor de segmentación podrá mantenerse independiente de la fuente de datos.

**Componentes afectados:**  
Arquitectura general.

**Siguiente paso:**  
Definir un contrato interno estable y diseñar la API simulada del CRM.

---

## 10/09/2026 — 18:28
**Tipo:** Arquitectura / Documentación

**Actividad realizada:**  
Refiné la estrategia de entrada de datos.

Definí que el proyecto utilizará:
- una **API CRM simulada** como fuente externa;
- un **adaptador específico** para transformar la respuesta de esa API;
- un **formato interno estándar** utilizado por el resto del sistema.

**Decisiones tomadas:**  
La API simulada no será el núcleo del sistema.

Los adaptadores pertenecerán a nuestra aplicación y serán responsables de traducir diferentes estructuras externas al contrato interno.

En el futuro podrán existir adaptadores como:
- `SimulatedCRMAdapter`;
- `HubSpotAdapter`;
- `SalesforceAdapter`;
- `CSVAdapter`;
- adaptadores para bases de datos u otras APIs.

**Resultado:**  
Se definió una arquitectura desacoplada y extensible que permitirá cambiar la fuente de datos sin modificar el motor de segmentación.

**Componentes afectados:**  
Arquitectura, capa de integración y diseño de datos.

**Siguiente paso:**  
Actualizar formalmente PRD, MVP y README.

---

## 10/09/2026 — Hora: no registrada
**Tipo:** Documentación

**Actividad realizada:**  
Actualicé el **PRD** y el **MVP** para incorporar la arquitectura basada en:
- API CRM simulada;
- adaptador de entrada;
- contrato interno estable;
- independencia del motor respecto a la fuente.

También creé `README.md` como mapa principal del proyecto para desarrolladores y modelos de IA.

**Decisiones tomadas:**  
El README debe funcionar como referencia constante durante el desarrollo y explicar de manera clara:
- qué es el proyecto;
- qué se está construyendo;
- qué decisiones arquitectónicas deben respetarse;
- qué responsabilidad tiene cada tecnología;
- qué componentes forman parte del MVP;
- qué orden de desarrollo seguir.

**Resultado:**  
La documentación principal quedó alineada con la arquitectura desacoplada.

**Archivos afectados:**
- `PRD_Motor_Inteligente_Segmentacion_Clientes_v1.1.pdf`
- `MVP_Motor_Inteligente_Segmentacion_Clientes_v1.1.pdf`
- `README.md`

**Siguiente paso:**  
Definir el contrato interno v1 y comenzar el diseño técnico de la API CRM simulada.

---

## 10/09/2026 — Hora: no registrada
**Tipo:** Documentación / Gestión

**Actividad realizada:**  
Creé `Bitacora.md` para registrar cronológicamente el desarrollo técnico y documental del proyecto.

**Decisiones tomadas:**  
Cada nueva actividad deberá registrarse con fecha, hora, tipo de actividad, decisiones, resultado, componentes afectados y siguiente paso.

Los modelos de IA deberán consultar esta bitácora antes de continuar el trabajo y actualizarla después de avances relevantes.

**Resultado:**  
El proyecto cuenta ahora con un historial persistente de decisiones y avances.

**Archivo afectado:**  
`Bitacora.md`

**Siguiente paso:**  
Comenzar la definición formal del contrato interno de datos.

---

## 10/09/2026 — 19:11
**Tipo:** Técnico / Pruebas

**Actividad realizada:**  
Realicé la auditoría del entorno de desarrollo antes de escribir cualquier código. Comprobé la presencia, versión y ubicación de Git, Python, py, pip, venv, Node.js, npm, PostgreSQL, Azure CLI, Docker y winget, además de los paquetes de Python que necesitará el proyecto (FastAPI, Uvicorn, Pandas, NumPy, Scikit-learn, azure-ai-ml y openai). También verifiqué si existía algún servicio o instalación de PostgreSQL en el sistema.

**Decisiones tomadas:**  
Clasifiqué las herramientas del entorno en cuatro grupos: instaladas, faltantes para el MVP, necesarias más adelante y no necesarias todavía. Definí que los paquetes de Python se instalarán dentro de un entorno virtual del proyecto y no de forma global. Azure CLI, Docker, el SDK de Azure Machine Learning y el SDK de Azure OpenAI quedan aplazados hasta sus etapas correspondientes.

**Resultado:**  
Entorno verificado:
- Instalados: Git 2.55.0, Python 3.14.2, pip 25.3, venv (librería estándar), Node.js v24.13.0, npm y winget 1.29.290.
- Faltan para el MVP: PostgreSQL (sin instalación ni servicio) y los paquetes de Python (FastAPI, Uvicorn, Pandas, NumPy, Scikit-learn), que se instalarán en el venv del proyecto.
- Se necesitarán después: Azure CLI, azure-ai-ml, openai y Docker.
- No necesarios todavía: Power BI, Azure AI Search, Microsoft Entra ID y GitHub Actions.

**Archivos o componentes afectados:**  
Ninguno; la auditoría fue de solo lectura.

**Problemas o bloqueos:**  
- La política de ejecución de PowerShell bloquea `npm.ps1`, por lo que npm no puede ejecutarse desde PowerShell hasta corregirlo.
- Python 3.14 es una versión muy reciente: falta verificar la compatibilidad de Pandas, NumPy y Scikit-learn al crear el entorno virtual.
- Los PDF del PRD y del MVP no pueden leerse directamente con las herramientas actuales; se evaluará extraer su texto a archivos de referencia en formato Markdown.

**Siguiente paso:**  
Corregir la política de ejecución de PowerShell, decidir cuándo instalar PostgreSQL y después comenzar la definición del contrato interno de datos V1.

---

## 10/09/2026 — 19:32
**Tipo:** Técnico

**Actividad realizada:**  
Completé la preparación del entorno de desarrollo. Corregí la política de ejecución de PowerShell (RemoteSigned para CurrentUser) para habilitar npm, verifiqué su funcionamiento e instalé PostgreSQL 18.6 mediante winget con el asistente interactivo.

**Decisiones tomadas:**  
- Aplicar RemoteSigned en el ámbito CurrentUser como solución al bloqueo de `npm.ps1` (reversible y limitado a mi usuario).
- Instalar PostgreSQL 18 (última versión estable) en lugar de 17, al no existir restricciones de compatibilidad para un proyecto nuevo.
- Ejecutar el instalador en modo interactivo para que yo mismo defina la contraseña del superusuario `postgres` (la guardaré para el backend en un `.env` local, nunca en el repositorio).
- Aplazar la creación del entorno virtual de Python y la instalación de librerías (FastAPI, Uvicorn, Pandas, NumPy, Scikit-learn) hasta el scaffolding del proyecto.
- Aplazar Azure CLI, Docker y los SDKs de Azure hasta sus etapas correspondientes.

**Resultado:**  
- npm funcional (v11.6.2).
- PostgreSQL 18.6 instalado, con servicio `postgresql-x64-18` en estado Running y `psql` verificado en `C:\Program Files\PostgreSQL\18\bin\psql.exe`.
- Entorno base del MVP listo: Git 2.55.0, Python 3.14.2, pip 25.3, venv, Node.js v24.13.0, npm 11.6.2, PostgreSQL 18.6 y winget.

**Archivos o componentes afectados:**  
- `Bitacora.md` (registro de la sesión).
- Sistema: política de ejecución de PowerShell (CurrentUser) e instalación de PostgreSQL 18.

**Problemas o bloqueos:**  
- `psql` no aparece en el PATH de la sesión actual de PowerShell; se usará la ruta completa o una terminal nueva.
- Pendiente verificar la compatibilidad de Pandas/NumPy/Scikit-learn con Python 3.14 al crear el venv.

**Siguiente paso:**  
Definir el contrato interno de datos V1 y crear la estructura inicial del proyecto (scaffolding) con su entorno virtual.

---

## 10/09/2026 — 19:44
**Tipo:** Arquitectura / Técnico

**Actividad realizada:**  
Creé la estructura inicial del proyecto (scaffolding), inicialicé el repositorio Git, generé el entorno virtual e instalé las librerías base (pydantic, fastapi, uvicorn, requests, pandas, numpy, scikit-learn). Extraje el texto de los PDF del PRD v1.1 y del MVP v1.1 a archivos Markdown de referencia en `docs/` usando pypdf en un entorno temporal aparte. Leí ambos documentos completos y, con base en ellos y en el README, definí formalmente el **Contrato Interno de Datos V1**, codificado en Pydantic y verificado con una prueba automática.

**Decisiones tomadas:**  
- Definí el contrato V1 con las entidades Customer, Transaction, Interaction y CampaignEvent, más un contenedor NormalizedDataset como salida estándar de los adaptadores.
- Montos como `float` (moneda única en el MVP, destino analítico/ML), no `Decimal`.
- Enums canónicos: ProductCategory (8 valores, con `otros` como escape de mapeo), InteractionType (web_visit, product_view, abandoned_cart) y CampaignEventType (sent, delivered, opened, clicked). Los tipos de interacción o evento desconocidos se descartan con reporte, no se fuerzan a un valor "otros".
- Ubiqué correos abiertos y clics de campañas en CampaignEvent (opened/clicked), e Interaction reservada para comportamiento digital fuera de campañas.
- Agregué `product_name` opcional en Transaction e Interaction, justificado por la sección 10 del PRD (información transaccional incluye producto) y por las features de preferencias.
- CampaignEvent sin ID propio: identidad compuesta por campaña, cliente, tipo y fecha.
- Estructura monorepo con un único venv para el MVP, con carpetas separadas para simulador, núcleo (`src`), tests y frontend futuro.

**Resultado:**  
- Contrato Interno de Datos V1 vigente: documento en `docs/contrato_interno_datos_v1.md`, código en `src/contracts/` (enums.py, models.py) y prueba `tests/test_contrato.py` en verde (entidades válidas, rechazos y opcionales).
- Entorno virtual verificado sobre Python 3.14: pydantic 2.13.5, numpy 2.5.3, pandas 3.0.5, scikit-learn 1.9.1, fastapi 0.141.1. Se cerró el riesgo de compatibilidad registrado en la auditoría.
- PRD y MVP disponibles como Markdown de consulta en `docs/`.
- Repositorio Git inicializado (rama main, sin commits aún).

**Archivos o componentes afectados:**  
- Nuevos: `.gitignore`, `requirements.txt`, `src/__init__.py`, `src/contracts/{__init__.py, enums.py, models.py}`, `tests/{__init__.py, test_contrato.py}`, `docs/contrato_interno_datos_v1.md`, `docs/PRD_Motor_Inteligente_Segmentacion_Clientes_v1.1.md`, `docs/MVP_Motor_Inteligente_Segmentacion_Clientes_v1.1.md`, `.venv/` (local).
- Modificados: `README.md` (sección 4 actualizada y nuevas secciones 16 y 17: estructura y entorno), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. La compatibilidad de las librerías con Python 3.14 quedó confirmada.

**Siguiente paso:**  
Diseñar el dataset CRM simulado (perfiles de comportamiento diferenciables) y construir la API CRM simulada con su propio formato externo.

---

## 10/09/2026 — 20:05
**Tipo:** Técnico

**Actividad realizada:**  
Diseñé y construí la fuente de datos externa del MVP. Definí un dataset CRM simulado con 6 perfiles de comportamiento (VIP, frecuente, ocasional, en riesgo, nuevo y navegador sin compra), cada uno con distribuciones propias de frecuencia de compra, ticket, recencia, preferencias de categoría, actividad web y respuesta a campañas. Implementé el generador `crm_simulator/generate_data.py` y la API `crm_simulator/app.py` (FastAPI). Generé el dataset, levanté la API en el puerto 8001 y verifiqué todos los endpoints, incluida la paginación.

**Decisiones tomadas:**  
- Semilla fija (SEED=42) y fecha de corte fija (2026-09-10): el dataset es reproducible y el RFM estable entre regeneraciones.
- El formato externo es deliberadamente distinto del contrato interno: campos renombrados (`clientId`, `opId`, `ts`, `totalAmount`, `productLine`), estructura anidada (`demographics.age`), montos como texto con 2 decimales, `memberSince` solo fecha, enums en inglés mayúsculas (`WEB_SESSION`, `OPEN`, etc.).
- Incluí categorías externas fuera del canon (`BOOKS`, `GARDEN_TOOLS`) y 5 registros corruptos (3 transacciones y 2 clientes inválidos) para probar en el adaptador las reglas de mapeo a `otros` y de reporte de inválidos.
- La asignación real de perfil por cliente se guarda como ground truth únicamente en `data/meta.json`; nunca se expone por la API, para no contaminar el futuro clustering y poder validar los grupos contra la verdad conocida.
- La API sirve listas completas con paginación opcional (`limit`/`offset`) bajo un sobre `{total, count, data}`; el dataset vive en archivos JSON que la API carga al inicio.

**Resultado:**  
- Dataset generado: 500 clientes (50 VIP, 100 frecuentes, 125 ocasionales, 75 en riesgo, 75 nuevos, 75 navegadores), 6,512 transacciones en 18 meses, 18,004 interacciones y 9,131 eventos de campaña.
- API CRM simulada operativa y verificada: `/health`, `/crm/customers`, `/crm/transactions`, `/crm/interactions`, `/crm/campaign-events`, con documentación interactiva en `http://127.0.0.1:8001/docs`.

**Archivos o componentes afectados:**  
- Nuevos: `crm_simulator/__init__.py`, `crm_simulator/generate_data.py`, `crm_simulator/app.py`, `data/*.json` (generados, no versionados).
- Modificados: `README.md` (secciones 3, 16 y 17: implementación actual de la fuente, estructura y comandos de ejecución), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno relevante. Los volúmenes quedaron algo mayores a lo estimado (18k interacciones), pero son manejables en memoria para el MVP.

**Siguiente paso:**  
Implementar el `SimulatedCRMAdapter`: consumir la API simulada, transformar su formato externo al contrato interno V1 y reportar los registros inválidos.

---

## 14/09/2026 — 12:08
**Tipo:** Gestión / Documentación

**Actividad realizada:**  
Adopté formalmente las reglas de **control de versiones con Git** como parte de las reglas de trabajo del proyecto: registrar todo el desarrollo progresivamente en Git, realizar commits después de avances significativos con mensajes claros, no esperar al final para crear el historial, no eliminar ni alterar commits existentes, mantener el repositorio listo para vincularse a GitHub y reflejar cada avance importante tanto en Git como en `Bitacora.md`.

Apliqué la regla de inmediato: verifiqué el estado del repositorio y la identidad de Git configurada, y creé el historial inicial con el trabajo acumulado hasta hoy.

**Decisiones tomadas:**  
- Las reglas de Git quedaron documentadas en la sección 13 del README ("Reglas que NO se deben romper") para que cualquier desarrollador o modelo de IA las respete.
- Creé un primer commit consolidado con el estado actual del proyecto (commit `f019c32`: documentación, contrato interno V1, dataset y API CRM simulada) en lugar de intentos de dividir retroactivamente hitos ya pasados; a partir de ahora cada avance significativo tendrá su propio commit junto con su entrada en esta bitácora.
- El remoto de GitHub queda pendiente hasta que se decida crear el repositorio remoto.

**Resultado:**  
- Historial Git iniciado en la rama `main` con 22 archivos versionados (los PDF oficiales incluidos; `.venv/` y `data/` quedan fuera por `.gitignore`).
- Reglas de versionado vigentes y documentadas en el README.

**Archivos o componentes afectados:**  
- `README.md` (sección 13: nuevas reglas de control de versiones).
- `Bitacora.md` (esta entrada).
- Repositorio Git (commit inicial `f019c32` y commit de esta regla).

**Problemas o bloqueos:**  
- Ninguno. Git ya tenía identidad configurada (user: Ezumi005).

**Siguiente paso:**  
Implementar el `SimulatedCRMAdapter`: consumir la API simulada, transformar su formato externo al contrato interno V1 y reportar los registros inválidos.

---

## 14/09/2026 — 12:13
**Tipo:** Documentación / Gestión

**Actividad realizada:**  
Incorporé formalmente el control de versiones con Git en la documentación del proyecto. Antes de modificar nada, revisé el contenido y la estructura del README, el PRD, el MVP y esta bitácora para conservar terminología y no alterar decisiones existentes.

**Decisiones tomadas:**  
- El README no requirió cambios: la sección 13 ya contiene las reglas de control de versiones (agregadas hoy a las 12:08) y cubre todos los puntos requeridos; decidí no duplicarla.
- Como los PDF del PRD y del MVP no pueden editarse directamente desde el entorno, agregué una adenda al final de sus extractos Markdown en `docs/`, marcada explícitamente como fuera del PDF v1.1 y pendiente de incorporarse al documento fuente cuando se genere la versión 1.2.
- En el PRD, Git quedó como consideración de gestión técnica (nueva sección 39), dejando claro que es herramienta de desarrollo y trazabilidad, no funcionalidad del producto; complementa la sección 27 existente.
- En el MVP, Git quedó como requisito de desarrollo/versionado breve y enfocado en trazabilidad y control de cambios (nueva sección 25).
- Por instrucción explícita de esta tarea, no realicé commits ni acciones de Git; los cambios quedan pendientes de confirmar en el repositorio.

**Resultado:**  
- PRD: adenda "Gestión técnica: control de versiones del desarrollo" (sección 39) + nota en el encabezado del extracto.
- MVP: adenda "Control de versiones y trazabilidad del MVP" (sección 25) + nota en el encabezado del extracto.
- README: verificado sin cambios necesarios.
- Coherencia verificada entre los cuatro documentos: mismas reglas, mismo alcance, sin contradicciones con secciones previas (PRD §27 y MVP §19 ya mencionaban Git como tecnología).

**Archivos o componentes afectados:**  
- `docs/PRD_Motor_Inteligente_Segmentacion_Clientes_v1.1.md` (encabezado + adenda sección 39).
- `docs/MVP_Motor_Inteligente_Segmentacion_Clientes_v1.1.md` (encabezado + adenda sección 25).
- `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Los PDF oficiales del PRD y del MVP no pueden modificarse desde este entorno; la regla vive en Markdown hasta que se genere el PDF v1.2 con la adenda incorporada al fuente.

**Siguiente paso:**  
Confirmar en Git los cambios de documentación cuando se solicite, incorporar la adenda al fuente del PDF al generar la v1.2 y continuar con la implementación del `SimulatedCRMAdapter`.

---

## 22/09/2026 — 15:42
**Tipo:** Técnico

**Actividad realizada:**  
Implementé el `SimulatedCRMAdapter`, la capa que traduce el formato externo del CRM simulado al Contrato Interno de Datos V1. Antes de codificar presenté el diseño (componentes a reutilizar, responsabilidad exacta, tablas de mapeo y ubicación) y esperé confirmación. Creé el paquete `src/adapters/` con la interfaz común `BaseAdapter`, las estructuras de reporte (`AdapterResult`, `AdapterReport`, `Incident`) y el adaptador concreto. Escribí pruebas unitarias y realicé una verificación end-to-end con la API CRM simulada encendida.

**Decisiones tomadas:**  
- Ubicación: `src/adapters/`, al nivel de `src/contracts/`; el resto del sistema solo conocerá `BaseAdapter` y el contrato interno.
- `BaseAdapter` como ABC mínimo con un único método `fetch_normalized()` para formalizar el punto de extensión de futuros adaptadores (HubSpot, CSV, etc.).
- Funciones de transformación puras, separadas del cliente HTTP: permiten probar el mapeo sin levantar la API.
- Reglas aplicadas según el contrato: categorías externas sin equivalente (`BOOKS`, `GARDEN_TOOLS`) → `otros`; tipos de interacción/evento desconocidos → descarte con reporte; registros que no validan → excluidos e incluidos en el reporte de incidencias con entidad, ID externo, campo y error.
- Los errores de red/HTTP de la fuente interrumpen la ejecución (fallan de forma audible); los errores de registro individual no detienen la sincronización (cumple RF-05 del PRD).

**Resultado:**  
- Pruebas unitarias en verde (`tests/test_adapter.py`): mapeos, conversión de tipos, enums, escape a `otros` y reporte de inválidos.
- Verificación end-to-end exitosa contra el simulador: 500 clientes leídos → 498 aceptados; 6,512 transacciones → 6,509 aceptadas; 18,004 interacciones y 9,131 eventos aceptados completos; exactamente los 5 registros corruptos inyectados quedaron en el reporte de incidencias y fuera del dataset.
- La salida del adaptador es un `NormalizedDataset` válido según el contrato (verificado con entidades reales del simulador).

**Archivos o componentes afectados:**  
- Nuevos: `src/adapters/__init__.py`, `src/adapters/base.py`, `src/adapters/simulated_crm_adapter.py`, `tests/test_adapter.py`.
- Modificados: `README.md` (árbol de estructura de la sección 16 y comando de prueba en la sección 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno relevante. Nota menor: al ejecutar scripts desde una carpeta externa hay que exportar `PYTHONPATH` hacia la raíz del proyecto para poder importar `src`.

**Siguiente paso:**  
Diseñar el esquema de PostgreSQL y la persistencia de los datos normalizados (etapa 5 del orden de desarrollo).

---

## 22/09/2026 — 16:12
**Tipo:** Técnico

**Actividad realizada:**  
Implementé la persistencia en PostgreSQL del contrato interno (etapa 5 del orden de desarrollo). Diseñé el esquema, construí la capa `src/persistence/` (conexión, inicializador de base, repositorio con upserts y proceso de ingesta) y verifiqué todo en vivo: creación de la base `motor_segmentacion`, aplicación del esquema, dos ingestas completas contra el simulador encendido y consulta de los resultados directamente en la base.

**Decisiones tomadas:**  
- Driver `psycopg` 3 (SQL directo) en lugar de SQLAlchemy ORM: el contrato ya vive en Pydantic y no conviene una capa paralela de modelos.
- Esquema versionado en un `schema.sql` idempotente con un inicializador propio (`init_db.py`), en lugar de Alembic, que se evaluará si el esquema evoluciona mucho.
- Tablas creadas ahora: las 4 del contrato más `ingestion_runs` e `ingestion_incidents` para trazabilidad (RF-25, RNF-MVP-08). Las tablas de segmentación se dejarán para su etapa.
- Upserts idempotentes (`ON CONFLICT DO UPDATE` / `DO NOTHING`) para poder re-sincronizar sin duplicar (RF-MVP-18).
- Sin claves foráneas por ahora: la integridad referencial es responsabilidad del procesamiento según el contrato (sección 2), y sin esa capa los registros huérfanos de clientes rechazados romperían la ingesta. Documentado en el propio esquema.
- Credenciales en `.env` local (excluido de Git, verificado con `git check-ignore`); agregué `python-dotenv` y `psycopg[binary]` a requirements.

**Resultado:**  
- Base `motor_segmentacion` creada y esquema aplicado (6 tablas con CHECKs de enums del contrato).
- Ingesta end-to-end verificada dos veces: 498 clientes, 6,509 transacciones, 18,004 interacciones y 9,131 eventos persistidos; conteos idénticos tras la segunda ingesta (idempotencia comprobada).
- `ingestion_runs` registra ambas ejecuciones con estado `ok` y conteos leídos/guardados; `ingestion_incidents` conserva las 5 incidencias por ejecución.
- Categorías en base: los 8 valores canónicos, incluido `otros` (128 registros de BOOKS/GARDEN_TOOLS traducidos por el adaptador).

**Archivos o componentes afectados:**  
- Nuevos: `.env.example`, `src/persistence/{__init__.py, db.py, schema.sql, repository.py, init_db.py, ingest.py}`, `.env` (local, no versionado).
- Modificados: `requirements.txt` (+psycopg[binary], +python-dotenv), `README.md` (secciones 10, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno técnico. Nota: la contraseña de PostgreSQL quedó en el `.env` local tras indicarla el usuario en el chat; para un entorno real convendría rotarla, pero para el MVP local con datos simulados se mantiene.

**Siguiente paso:**  
Construir el pipeline de preparación de datos y features RFM sobre los datos ya persistidos (etapa 6 del orden de desarrollo).

---

## 22/09/2026 — 16:29
**Tipo:** Técnico

**Actividad realizada:**  
Implementé el pipeline de features (etapa 6 del orden de desarrollo). Creé `src/features/rfm.py`, que carga las tablas del contrato desde PostgreSQL, ejecuta chequeos de calidad y construye la tabla de features por cliente. Escribí pruebas unitarias con frames sintéticos (`tests/test_features.py`) y ejecuté el pipeline completo sobre la base real, incluyendo una validación de las features contra los perfiles reales del simulador (ground truth de `data/meta.json`, usado únicamente para validar, nunca para calcular).

**Decisiones tomadas:**  
- Fecha de referencia de recency = `max(purchased_at)` del dataset (determinista, alineada al ancla fija del simulador); se descartó `now()` porque degradaría el RFM con el paso del tiempo.
- Features v1: RFM base (`recency_days`, `frequency`, `monetary`) + features justificadas: `avg_ticket`, `tenure_days`, `web_visits`, `product_views`, `abandoned_carts`, `emails_opened`, `campaign_click_rate` y `favorite_category` (metadato). La justificación clave: sin features de engagement, el perfil "navegador sin compra" sería indistinguible de un cliente inactivo.
- `recency_days` queda nulo para clientes sin compras (19 casos); la imputación se decidirá y documentará en la etapa de ML.
- Núcleo puro en pandas (`build_features` recibe DataFrames) separado de la carga desde PostgreSQL: permite pruebas unitarias sin base de datos.
- Los registros huérfanos (clientes rechazados por inválidos) se excluyen del cálculo y se reportan en el chequeo de calidad; las features no se persisten (se computan a demanda, CSV de inspección en `data/`).

**Resultado:**  
- Pruebas unitarias en verde (RFM, clientes sin compras, huérfanos, frames vacíos, fecha por defecto, calidad).
- Pipeline ejecutado sobre la base: 498 clientes × 12 columnas; 0 IDs duplicados; 275 registros huérfanos excluidos (1 transacción, 227 interacciones, 47 eventos); 0 montos negativos.
- Validación contra perfiles reales: las medias por perfil confirman separación clara (VIP: recency 6.4 / monetary 148k / click_rate 0.50; riesgo: recency 231.8 / sin engagement; navegador: 58 visitas / 43 carritos abandonados / frequency 1.0; nuevo: tenure 36.6 días).

**Archivos o componentes afectados:**  
- Nuevos: `src/features/__init__.py`, `src/features/rfm.py`, `tests/test_features.py`, `data/features_rfm.csv` (generado, no versionado).
- Modificados: `README.md` (secciones 5, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. Durante las pruebas corregí dos expectativas mal calculadas a mano (recency con hora del ancla y click_rate de un caso) y un matiz de pandas (`None` se convierte en `NaN`); el código final quedó con `NaN` consistente.

**Siguiente paso:**  
Implementar y validar el clustering K-Means local sobre estas features (etapa 7): selección e imputación de variables, escalado, búsqueda de k (Silhouette, Inertia, Davies-Bouldin) e interpretación inicial de clusters.

---

## 22/09/2026 — 16:42
**Tipo:** Técnico / Pruebas

**Actividad realizada:**  
Implementé el modelo de clustering K-Means local (etapa 7). Creé `src/ml/clustering.py` con: preparación de la matriz, evaluación de k=2..10, entrenamiento, verificación de estabilidad, perfilado de clusters en unidades originales y validación contra los perfiles reales del simulador. Escribí pruebas unitarias (`tests/test_clustering.py`) con datos sintéticos y ejecuté el pipeline completo sobre los 498 clientes reales. Además, comparé explícitamente k=4 contra k=6 para informar la decisión de negocio con datos.

**Decisiones tomadas:**  
- Imputación de `recency_days` nulo (19 clientes) con tope al máximo observado (316.55 días): quienes nunca compraron son al menos tan inactivos como el registro más inactivo; excluirlos habría eliminado un segmento real (navegadores sin compra).
- Features del modelo (7): RFM + `web_visits`, `abandoned_carts`, `campaign_click_rate`, `tenure_days`. Se excluyeron `avg_ticket` (redundante por construcción: M/F), `product_views` y `emails_opened` (correlación ≥ 0.63 con las incluidas). La matriz de correlación se imprime en la ejecución como justificación.
- Transformación `log1p` en variables de conteo/gasto sesgadas + `StandardScaler`.
- Regla pre-declarada de selección de k: mejor Silhouette con empate (≤0.01) resuelto al menor k. Métricas de soporte: Inertia (codo) y Davies-Bouldin. Estabilidad medida con ARI promedio entre 5 semillas.
- Artefacto guardado en `models/kmeans_local.pkl` (joblib: modelo + scaler + configuración y métricas); carpeta `models/` excluida de Git (regenerable con semilla fija).

**Resultado:**  
- Pruebas unitarias en verde (preparación, imputación, elección de k, estabilidad y perfiles).
- Métricas: k=4 elegido por la regla pre-declarada (Silhouette 0.4297; DB 0.9079; estabilidad ARI 1.000). k=8 obtuvo 0.4320 (diferencia 0.0023 → empate → menor k).
- k=4 produce 4 grupos coherentes: activos de alto consumo (150: frecuentes+VIP), ocasionales/inactivos (192), navegadores (73, pureza 100%) y nuevos (83, tenure 66 días). ARI contra perfiles reales: 0.659.
- k=6 evaluado como alternativa: ARI 0.794; separa limpiamente riesgo (75/75), ocasionales (122/122) y divide navegadores entre quienes alguna vez compraron y quienes no; frecuentes y VIP siguen fusionados por la fuerte correlación de sus features. Silhouette 0.4136 (coste mínimo frente a 0.4297).
- **Decisión pendiente (próxima etapa, interpretación):** mantener k=4 (regla pre-declarada) o adoptar k=6 justificado por interpretación comercial (el PRD §30 permite combinar métricas con interpretación). El artefacto actual guarda k=4.

**Archivos o componentes afectados:**  
- Nuevos: `src/ml/__init__.py`, `src/ml/clustering.py`, `tests/test_clustering.py`, `models/kmeans_local.pkl` (generado, no versionado).
- Modificados: `.gitignore` (+`models/`), `README.md` (secciones 6, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno relevante. Durante la sesión corregí: un desliz de diseño (el scaler debía devolverse desde `prepare_matrix`) y la falta del guard `__main__` que hacía correr el módulo sin salida.

**Siguiente paso:**  
Interpretar los clusters y decidir k (4 vs 6) combinando métricas e interpretación comercial; después asignar etiquetas comerciales a los clusters elegidos y persistir la segmentación (segments, customer_segments).

---

## 22/09/2026 — 16:44
**Tipo:** Gestión / Técnico

**Actividad realizada:**  
Decidí el k definitivo del MVP: **k=6**, combinando métricas e interpretación comercial como permite la sección 30 del PRD. Actualicé `FINAL_K=6` en `src/ml/clustering.py` (la regla estadística se sigue calculando e imprimiendo para trazabilidad), reentrené el modelo y regeneré el artefacto `models/kmeans_local.pkl`.

**Decisiones tomadas:**  
- Adopté k=6 frente al k=4 de la regla puramente estadística porque: eleva el ARI contra perfiles reales de 0.659 a 0.794, aísla el segmento de riesgo con pureza 100% (objetivo accionable de retención, caso de uso central del producto) y su Silhouette (0.4136) es casi idéntico al mejor (0.4297, k=4).
- Esta entrada **cambia** la decisión provisional de la entrada de las 16:42 sin modificarla: aquella dejó la elección explícitamente pendiente de esta etapa.
- La estructura de la comparación k=4 vs k=6 quedó documentada en la bitácora y en el README (sección 6).

**Resultado:**  
- Modelo definitivo k=6: estabilidad entre semillas 0.993, ARI 0.794.
- Clusters resultantes (medias originales): activos de alto consumo (150), ocasionales (122), en riesgo (75, recency 231.8), nuevos (66, tenure 48), navegadores con compra esporádica (66) y navegadores sin compra (19).
- Frecuentes y VIP permanecen fusionados en un solo cluster (correlación 0.92 de sus features): limitación conocida, documentada, a revisar si el negocio exige separarlos.

**Archivos o componentes afectados:**  
- `src/ml/clustering.py` (constante FINAL_K=6 con justificación), `models/kmeans_local.pkl` (regenerado, no versionado).
- `README.md` (sección 6: estado del modelo), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Interpretar los 6 clusters, asignar etiquetas comerciales justificadas y persistir la segmentación en PostgreSQL (segmentation_runs, segments, customer_segments).

---

## 22/09/2026 — 16:48
**Tipo:** Técnico

**Actividad realizada:**  
Completé la etapa 8: interpreté los clusters y persistí la segmentación. Definí etiquetas comerciales para los 6 clusters con base en sus perfiles reales (medias en unidades originales), amplié el esquema de PostgreSQL con las tablas `segmentation_runs`, `segments` y `customer_segments`, implementé `src/ml/segmentation.py` (ejecución completa: features → modelo → etiquetas → persistencia trazable) y verifiqué todo en vivo contra la base. Reejecuté las 5 suites de pruebas del proyecto: todas en verde.

**Decisiones tomadas:**  
- Etiquetas asignadas por **reglas sobre el perfil del cluster** (prioridad: alto valor → sin compra → nuevo → navegador con compra → riesgo → ocasional), no por número de cluster: un reordenamiento del modelo no rompe la interpretación. Si dos clusters recibieran la misma etiqueta, el proceso falla y exige revisión humana.
- Etiquetas vigentes y su evidencia: Clientes frecuentes de alto valor (freq 31.5, monetary 68.5k), Navegadores sin compra (0 compras, 61 visitas, 41 carritos), Compradores ocasionales (freq 5.9, sin engagement), Clientes nuevos (tenure 48 días), Navegadores con compra esporádica (50 visitas, 37 carritos, freq 1.6), Clientes en riesgo de inactividad (recency 232 días, engagement 0).
- Cada ejecución conserva sus propios segmentos y asignaciones (historial completo); `segments` guarda etiqueta, descripción comercial, tamaño y perfil JSONB; `customer_segments` lleva FK a customers y a su segment/run.
- La ejecución reentrena el modelo con semilla fija en lugar de cargar el artefacto: cada run queda autónomo y reproducible.

**Resultado:**  
- Segmentación #1 persistida: estado ok, k=6, 498 clientes asignados, métricas en JSONB (Silhouette 0.4136, Inertia 783.0, DB 0.8533).
- 6 segmentos en base con etiquetas y tamaños: 150 / 19 / 122 / 66 / 66 / 75 — coherentes con el crosstab contra perfiles reales de la etapa anterior.
- Pruebas en verde: contrato, adaptador, features, clustering e interpretación.

**Archivos o componentes afectados:**  
- Nuevos: `src/ml/segmentation.py`, `tests/test_segmentation.py`.
- Modificados: `src/persistence/schema.sql` (+3 tablas de segmentación), `README.md` (secciones 6, 10, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno relevante. Corregí un borde de serialización detectado por las pruebas (floats en Series de dtype objeto no se redondeaban) y dos escenarios de prueba mal planteados por mí; el guard de etiquetas duplicadas demostró funcionar correctamente.

**Siguiente paso:**  
Construir el backend principal con FastAPI (etapa 9): endpoints de ingestión, clientes, segmentos y ejecución de segmentación sobre lo ya persistido.

---

## 22/09/2026 — 16:53
**Tipo:** Técnico

**Actividad realizada:**  
Construí el backend principal con FastAPI (etapa 9, inicio de la semana 2). Creé `src/api/` con `create_app()` y routers por dominio (ingestion, customers, segments, dashboard), centralicé las lecturas en `src/persistence/queries.py` y expuse los endpoints definidos en el README §9. Verifiqué los 8 endpoints en vivo con simulador y backend encendidos, incluyendo los casos de error (404 cliente inexistente, 502 si el simulador no está disponible, 501 del endpoint de recomendaciones reservado para Azure OpenAI).

**Decisiones tomadas:**  
- Estructura con routers por dominio y consultas de lectura en la capa de persistencia: la API no contiene SQL disperso ni lógica de ML; solo orquesta procesos existentes (ingesta y segmentación).
- `GET /segments` devuelve el último run exitoso; cada run conserva su historial completo en las tablas de segmentación.
- `POST /segments/{id}/recommendation` reservado con 501: el contrato de la API queda definido desde ahora, pero la implementación pertenece a la etapa de Azure OpenAI.
- CORS habilitado únicamente para los orígenes de desarrollo de React (localhost:5173/3000).
- Respuestas como diccionarios consistentes (snake_case); los response models tipados se evaluarán al integrar el frontend.
- Las pruebas automatizadas de API (TestClient/httpx) quedan para la etapa de pruebas (14); hoy se verificó en vivo.
- Corrección de determinismo detectada durante la verificación: agregué `ORDER BY` a la carga de tablas en `load_from_postgres` porque el orden de filas variaba entre ejecuciones y con él las métricas del modelo (0.4136 vs 0.4139). Tras el cambio, dos ejecuciones consecutivas producen métricas idénticas (Silhouette 0.4144, Inertia 784.1).

**Resultado:**  
- API operativa en puerto 8000 con documentación interactiva en `/docs`.
- Verificación en vivo: health, customers (498, con etiqueta de segmento), detalle de cliente con estadísticas, segments (6 con etiquetas y perfil JSONB), detalle de segmento, dashboard (totales, gasto, distribución, última ingesta/segmentación), POST /ingestion/sync (run #3) y POST /segmentation/run (run #2) ejecutados desde la propia API.
- Determinismo del pipeline confirmado con dos runs consecutivos idénticos; además, el reordenamiento de cluster IDs entre ejecuciones demostró que las etiquetas por reglas siguen a los perfiles y no al número de cluster.

**Archivos o componentes afectados:**  
- Nuevos: `src/api/{__init__.py, app.py}`, `src/api/routes/{__init__.py, ingestion.py, customers.py, segments.py, dashboard.py}`, `src/persistence/queries.py`.
- Modificados: `src/features/rfm.py` (ORDER BY para determinismo), `.env.example` (SIMULATOR_URL opcional), `README.md` (secciones 9, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. El único hallazgo (no determinismo por orden de filas) fue corregido y verificado en el momento.

**Siguiente paso:**  
Registrar y desplegar el modelo en Azure Machine Learning (etapa 10): instalar Azure CLI y SDK, registrar el artefacto kmeans_local, definir el ambiente y exponer el endpoint de inferencia; después conectar el backend con ese endpoint.

---

## 22/09/2026 — 19:42
**Tipo:** Técnico / Gestión

**Actividad realizada:**  
Adelanté la etapa 13 (frontend React) porque las etapas 10-12 (Azure ML y Azure OpenAI) quedaron bloqueadas a la espera de la suscripción de Azure; le indiqué al usuario dónde crearla (azure.microsoft.com/free con crédito de $200 USD, o el plan para estudiantes) y qué recursos necesitaremos. Construí la aplicación frontend completa: scaffolding con Vite, React 19 + TypeScript, react-router-dom y las cuatro vistas mínimas del MVP. Verifiqué la compilación (tsc + build), el arranque del dev server y la integración con el backend encendido.

**Decisiones tomadas:**  
- Reorden del plan registrado: React (etapa 13) antes de Azure ML/OpenAI (etapas 10-12) por dependencia externa; el propio MVP (sección 23) permite ajustar el orden por prioridades y las reglas de trabajo exigen documentar el cambio.
- Vite + React + TypeScript con react-router-dom; sin librerías de UI ni estado global: el MVP se cubre con fetch, hooks y CSS propio.
- Cliente HTTP centralizado (`src/api.ts`) con URL base configurable (`VITE_API_BASE`), por defecto `http://127.0.0.1:8000`; el frontend no contiene credenciales ni consume ningún servicio externo distinto del backend.
- La vista de detalle de segmento incluye el botón de recomendación que consume `POST /segments/{id}/recommendation` y muestra el estado 501 ("pendiente de Azure OpenAI") de forma informativa, dejando la vista lista para cuando exista la integración.
- Durante el scaffolding, el generador de Vite produjo una plantilla vanilla-ts en lugar de react-ts (el flag no atravesó PowerShell); en lugar de regenerar, instalé React/react-dom manualmente, ajusté tsconfig (jsx react-jsx, strict) y escribí la estructura a mano.

**Resultado:**  
- Frontend operativo: Dashboard (tarjetas de indicadores, distribución de segmentos con barras, últimas ejecuciones), Clientes (tabla paginada de 50, expansión de detalle con estadísticas, etiqueta de segmento), Segmentos (tarjetas con descripción y enlace) y Detalle de segmento (métricas del run, perfil medio, vista previa de clientes, panel de recomendación).
- `npm run build` en verde (tipos y bundle); dev server verificado en `http://localhost:5173` (nota: Vite escucha en IPv6/localhost) junto al backend en 8000.

**Archivos o componentes afectados:**  
- Nuevos: `frontend/` completo (index.html, tsconfig, package.json, `src/{main.tsx, App.tsx, api.ts, types.ts, styles.css}`, `src/pages/{Dashboard, Customers, Segments, SegmentDetail}.tsx`).
- Modificados: `README.md` (secciones 11, 12-nota, 16 y 17), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Etapas 10-12 bloqueadas hasta obtener la suscripción de Azure (acción del usuario en curso).
- Menores y corregidos en el momento: plantilla equivocada del scaffolding, una línea CSS corrupta y el diagnóstico del puerto IPv6 de Vite.

**Siguiente paso:**  
Etapa 14 disponible sin nube: suite de pruebas de API (httpx/TestClient), manejo de errores y ajustes de seguridad; en paralelo, al conseguir la suscripción de Azure, retomar las etapas 10-12 (registro y despliegue en Azure ML, luego Azure OpenAI).

---

## 23/09/2026 — 13:34
**Tipo:** Técnico / Gestión

**Actividad realizada:**  
Comencé la etapa 10 (registrar y desplegar el modelo en Azure ML) con la suscripción que obtuvo el usuario. Instalé los SDK (`azure-ai-ml`, `azure-identity`, `openai`) en el venv, verifiqué el Azure CLI (ya lo tenía el usuario con la extensión ml), preparé los artefactos de despliegue en `azure/` (score.py que replica exactamente la preparación del modelo, entorno conda con las mismas versiones de sklearn/numpy, yamls de endpoint y deployment, y script de despliegue por SDK), creé el resource group `rg-motor-segmentacion` (eastus) y el workspace `ml-motor-segmentacion`, registré el modelo `kmeans-local:1` (artefacto regenerado y alineado con los runs deterministas) y el entorno `motor-segmentacion-env:1`. La creación del endpoint online falló de forma repetida; diagnostiqué la causa hasta la raíz.

**Decisiones tomadas:**  
- Regeneré el artefacto `kmeans_local.pkl` antes de registrarlo para que quedara alineado con la carga determinista (ORDER BY) y coincidiera con los cluster IDs de los runs persistidos.
- score.py recibe las 7 features en unidades originales por cliente y replica imputación de recency, log1p y escalado usando la configuración guardada en el propio artefacto (sin duplicar lógica).
- Entorno conda con versiones idénticas a las de entrenamiento (scikit-learn 1.9.1, numpy 2.5.3) para garantizar compatibilidad del pickle.
- Ante el fallo persistente del CLI (`az ml`), migre el despliegue a un script por SDK (`azure/deploy_endpoint.py`), idempotente y parametrizable.
- Diagnóstico progresivo del error `SubscriptionNotRegistered [N/A]`: registre manualmente Microsoft.Network, Microsoft.Compute y Microsoft.InferenceService (no estaban), probé nombres nuevos y una segunda región (workspace `ml-motor-seg-eus2` en eastus2); el fallo persistió porque la causa real es la **oferta FreeTrial con límite de gasto activado**, que no permite endpoints online.

**Resultado:**  
- Resource group, 2 workspaces, modelo y entorno registrados y listos en Azure.
- Endpoint bloqueado por el límite de gasto de la suscripción (pendiente de acción del usuario: quitar el spending limit en el portal manteniendo el crédito).
- Causa raíz documentada con evidencia (quotaId FreeTrial_2014-09-01, spendingLimit On).

**Archivos o componentes afectados:**  
- Nuevos: `azure/{score.py, conda_env.yml, environment.yml, endpoint.yml, deployment.yml, deploy_endpoint.py}`.
- `models/kmeans_local.pkl` regenerado; SDKs instalados en `.venv`.
- `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Bloqueo externo: la suscripción FreeTrial con spending limit no permite crear endpoints online de Azure ML. Acción requerida del usuario: quitar el límite de gasto en el portal (requiere método de pago; el crédito de $200 se conserva). Como limpieza pendiente: eliminar el workspace duplicado (eastus o eastus2) cuando el endpoint funcione.

**Siguiente paso:**  
Cuando el usuario quite el límite de gasto: ejecutar `azure/deploy_endpoint.py` (todo queda ya preparado), probar el endpoint con clientes reales, guardar URL y llave en `.env` y continuar con la etapa 11 (backend consume el endpoint).

---

## 23/09/2026 — 19:22
**Tipo:** Técnico / Gestión

**Actividad realizada:**  
Continué la etapa 10 y adelanté parte de la 12 en Azure. El usuario quitó el límite de gasto de la suscripción ( pasó de FreeTrial a PayAsYouGo, conservando el crédito) y lo verifiqué por API. Reintenté el despliegue del endpoint online con nombres nuevos, un workspace nuevo creado ya con la suscripción sana y también la región eastus2: el error evolucionó de `SubscriptionNotRegistered` a `InferencingClientCallFailed`, consistente con el retraso de propagación de elegibilidad documentado para cuentas recién actualizadas (puede tardar horas). En paralelo registré el proveedor `Microsoft.CognitiveServices`, creé el recurso de Azure OpenAI `openai-motor-seg` (S0, eastus), consulté su catálogo de modelos (solo familia GPT-5.x disponible) e intenté desplegar `gpt-5.4-mini` con SKU GlobalStandard.

**Decisiones tomadas:**  
- Workspace definitivo previsto: `ml-motor-seg-v2` (creado post-upgrade); los dos anteriores (`ml-motor-segmentacion` y `ml-motor-seg-eus2`) quedan como candidatas a limpieza.
- Modelo de recomendaciones elegido: `gpt-5.4-mini` con SKU `GlobalStandard` (las versiones/SKU antiguas ya no existen en el catálogo 2026; el SKU `Standard` fue rechazado).
- Se definieron las variables de entorno de Azure (`AZURE_OPENAI_*`, `AZURE_ML_*`) en `.env.example` para documentar el contrato de configuración del backend.

**Resultado:**  
- Suscripción verificada como PayAsYouGo con spendingLimit Off.
- Recurso Azure OpenAI creado (`openai-motor-seg`); endpoint y llave ya guardados en `.env` local tras el flujo de despliegue (pendiente de confirmar funcionamiento).
- **Bloqueos externos activos:** (1) el endpoint online de Azure ML sigue rechazándose por propagación de elegibilidad; (2) el despliegue del modelo OpenAI falla con `InsufficientQuota` porque la cuenta nueva tiene cuota 0 para toda la familia GPT-5 — se requiere solicitud de cuota en el portal.

**Archivos o componentes afectados:**  
- Azure: resource `openai-motor-seg` creado; workspace `ml-motor-seg-v2` creado; intentos de endpoint documentados.
- Locales: `.env` (credenciales OpenAI, no versionado), `.env.example` (nuevas variables documentadas), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Pendiente del usuario: solicitar cuota para `gpt-5.4-mini` (GlobalStandard, East US) en el portal (recurso openai-motor-seg → Cuotas → Solicitar cuota; sugerido 50K TPM).
- Pendiente de Azure: propagación de la elegibilidad de endpoints online (reintentar en próximas horas).

**Siguiente paso:**  
Cuando haya cuota aprobada: desplegar `gpt-5-4-mini`, probar una llamada real y continuar la etapa 12 (servicio de recomendaciones + tabla recommendations + endpoint del backend). En paralelo reintentar el endpoint de Azure ML y, al funcionar, cerrar la etapa 10 y la 11 (consumo desde el backend).

---

## 23/09/2026 — 20:38
**Tipo:** Técnico

**Actividad realizada:**  
Implementé la etapa 12 (recomendaciones comerciales con Azure OpenAI) en su totalidad de código, lista para activarse en cuanto la cuota se apruebe. Creé el servicio `src/services/recommendations.py` (construcción del prompt con agregados del segmento, llamada al deployment de Azure OpenAI y parseo tolerante de la respuesta JSON), la tabla `recommendations` en el esquema, los endpoints reales `POST /segments/{id}/recommendation` (genera y persiste) y `GET /segments/{id}/recommendation` (devuelve la última generada), y actualicé el frontend para mostrar y regenerar la recomendación en el detalle de segmento. Verifiqué todo con pruebas unitarias, build del frontend y prueba en vivo del flujo degradado.

**Decisiones tomadas:**  
- El prompt recibe únicamente agregados por segmento (medias, tamaño, etiqueta): Azure OpenAI no decide clusters ni ve clientes individuales, como exige el PRD (sección 17).
- Respuesta en JSON estricto (descripcion + recomendaciones) con parseo tolerante por si el modelo agrega texto alrededor.
- Degrada de forma controlada: sin credenciales → 501 informativo; con credenciales pero servicio caído → 502. El frontend distingue ambos estados.
- Las recomendaciones se persisten por segmento con historial (append); el GET devuelve siempre la última.
- `openai>=1.50` agregado a requirements.txt (ya estaba instalado en el venv).

**Resultado:**  
- 7 suites de pruebas en verde (contrato, adaptador, features, clustering, interpretación y recomendaciones).
- Esquema aplicado con la tabla `recommendations`; build del frontend en verde.
- Verificación en vivo: GET devuelve `null` (sin recomendaciones aún) y POST responde 501 con mensaje claro mientras llega la cuota.
- Se detectaron y cerraron procesos viejos del backend/frontend que ocupaban los puertos desde el 22/09.
- Reintentos del endpoint de Azure ML (nombres nuevos y workspace post-upgrade): sigue bloqueado por propagación de elegibilidad; se reintentará más adelante.

**Archivos o componentes afectados:**  
- Nuevos: `src/services/{__init__.py, recommendations.py}`, `tests/test_recommendations.py`.
- Modificados: `src/persistence/schema.sql` (+tabla recommendations), `src/persistence/queries.py` (+save/latest recommendation), `src/api/routes/segments.py` (endpoints reales de recomendación), `requirements.txt` (+openai), `frontend/src/{types.ts, api.ts, pages/SegmentDetail.tsx, styles.css}`, `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Externos, sin cambio: cuota de gpt-5.4-mini pendiente de aprobación (formulario enviado; 1-2 días hábiles) y propagación de endpoints online de Azure ML pendiente.

**Siguiente paso:**  
Cuando se apruebe la cuota: desplelar `gpt-5-4-mini`, guardar credenciales en `.env`, generar la primera recomendación real de extremo a extremo y registrar el resultado. En paralelo reintentar el endpoint de Azure ML para cerrar las etapas 10 y 11.

---

## 23/09/2026 — 20:48
**Tipo:** Técnico

**Actividad realizada:**  
Activé la etapa 12 de forma real: las recomendaciones comerciales con Azure OpenAI ya funcionan de extremo a extremo. La solicitud de cuota para gpt-5.4-mini en East US fue denegada por saturación regional (no por la cuenta), así que probé programáticamente 5 regiones adicionales y dos vías sin formulario: el model-router y el SKU **DataZoneStandard**. El despliegue con DataZoneStandard en el recurso East US funcionó de inmediato (pool de cuota con disponibilidad). Generé la primera recomendación real desde el servicio, verifiqué el flujo completo por la API (POST genera y persiste; GET consulta) y eliminé los 5 recursos de prueba de otras regiones.

**Decisiones tomadas:**  
- Deployment definitivo: **gpt-5-4-mini con SKU DataZoneStandard** (nombre `gpt-5-4-mini-dz`) en el recurso `openai-motor-seg` de East US; el SKU Global Standard quedó descartado por cuota 0 y denegación regional.
- Corrección de compatibilidad con la familia GPT-5: `max_tokens` → `max_completion_tokens` en el servicio de recomendaciones.
- Credenciales reales escritas en `.env` (endpoint con subdominio del recurso, llave y nombre del deployment); nunca versionadas.
- Los recursos OpenAI de prueba en otras regiones se eliminaron para dejar la suscripción limpia.

**Resultado:**  
- Primera recomendación real generada (segmento "Navegadores sin compra"): descripción precisa del perfil y 3 acciones concretas (campaña de primera compra, recuperación de carrito multicanal, nurturing).
- Flujo API verificado en vivo: POST `/segments/24/recommendation` generó y persistió (recommendation_id=1, modelo gpt-5-4-mini-dz) y GET devolvió la recomendación almacenada.
- Etapa 12 completada; el frontend ya muestra/regenera recomendaciones en el detalle de segmento.

**Archivos o componentes afectados:**  
- `src/services/recommendations.py` (fix max_completion_tokens), `.env` local (credenciales reales de Azure OpenAI).
- Azure: deployment `gpt-5-4-mini-dz` creado; 5 recursos de prueba eliminados.
- `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Resuelto el bloqueo de cuota vía DataZoneStandard. Único bloqueo restante del proyecto: la propagación de elegibilidad del endpoint online de Azure ML (etapas 10-11), que se reintenta más adelante.

**Siguiente paso:**  
Reintentar el despliegue del endpoint de Azure ML (workspace ml-motor-seg-v2) y, al funcionar, conectar el backend (etapa 11). Después: etapa 14 (pruebas y seguridad) y 15 (documentación final y demo).

---

## 23/09/2026 — 20:50
**Tipo:** Gestión

**Actividad realizada:**  
Cerré la sesión de trabajo del día. Resumí y dejé anotado todo lo pendiente del proyecto para retomarlo mañana con claridad.

**Decisiones tomadas:**  
Registrar de forma explícita el backlog restante en la bitácora, ordenado por etapa, para que cualquier sesión futura (yo u otro asistente) pueda continuar sin perder contexto.

**Resultado:**  
Estado del MVP al cierre del día: 12 de 15 etapas del orden de desarrollo completadas y verificadas (de contrato interno a recomendaciones con Azure OpenAI). Pendientes anotados:

1. **Etapa 10 — Endpoint de Azure ML:** reintentar el despliegue con `azure/deploy_endpoint.py` en el workspace `ml-motor-seg-v2` (bloqueado por propagación de elegibilidad de la suscripción tras el upgrade; todo lo demás ya está registrado y preparado).
2. **Etapa 11 — Backend ↔ Azure ML:** al funcionar el endpoint, guardar `AZURE_ML_ENDPOINT_URL` y `AZURE_ML_ENDPOINT_KEY` en `.env`, implementar el cliente en el backend y un endpoint de predicción por cliente.
3. **Etapa 14 — Pruebas y seguridad:** suite automatizada de la API (TestClient/httpx), endurecimiento de manejo de errores y validaciones.
4. **Etapa 15 — Documentación final y demo:** README de demostración, generación de recomendaciones para los 6 segmentos y preparación de la demostración final.
5. **Limpieza de Azure (al terminar la demo):** eliminar los workspaces duplicados (`ml-motor-segmentacion`, `ml-motor-seg-eus2`), borrar o detener el endpoint online para evitar consumo y, si procede, conservar solo el recurso Azure OpenAI necesario.
6. **GitHub:** el repositorio local está listo para vincularse a un remoto cuando se decida (regla de control de versiones, README sección 13).

**Archivos o componentes afectados:**  
- `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Solo el ya documentado: propagación de elegibilidad de endpoints online de Azure ML (externo, con tiempo).

**Siguiente paso:**  
Retomar mañana con el reintento del endpoint de Azure ML (etapa 10) y encadenar la 11.

---

## 25/09/2026 — 01:53
**Tipo:** Técnico / Investigación

**Actividad realizada:**  
Reintenté la etapa 10 (endpoint de Azure ML) con diagnóstico profundo, y avancé la etapa 14 con la suite de pruebas de la API. En Azure: probé nombre nuevo por SDK, llamada cruda directa a ARM (PUT del endpoint) y análisis del código fuente del SDK. El ARM reveló primero que el endpoint exige campo `identity` (con identidad SystemAssigned el registro del endpoint SÍ se crea y pasa la validación inicial), pero la operación interna de provisionamiento (`mfeOperationsStatus`) confirmó que el rechazo final sigue siendo `SubscriptionNotRegistered [N/A]` a nivel del servicio de inferencia: la propagación de elegibilidad de la suscripción (upgraded hace ~30 horas) aún no completa. Documenté la causa y dejé el flujo preparado. En local: implementé `tests/test_api.py`, la primera suite de integración de la API (TestClient + PostgreSQL real).

**Decisiones tomadas:**  
- Diagnóstico cerrado por capas: (1) no son los resource providers (todos registrados), (2) no es la región ni el workspace, (3) no es la identidad del endpoint (resuelta vía ARM), (4) es la propagación del plano de inferencia tras el upgrade de la suscripción — reintentar con calma en la ventana de 24-48h.
- `deploy_endpoint.py` mejorado: identidad explícita, modo `AZ_SKIP_ENDPOINT` (endpoint ya creado por ARM) y asignación de tráfico consultando el endpoint real para conservar su identidad.
- Suite de API con TestClient sobre la base real (integración), cubriendo los 8 endpoints y los casos 404/502; `httpx` agregado a requirements.

**Resultado:**  
- El registro del endpoint se crea correctamente vía ARM con identidad (avance real frente a intentos anteriores), pero el provisionamiento sigue bloqueado por Azure (externo, con tiempo).
- 8 suites de pruebas del proyecto en verde (contrato, adaptador, features, clustering, interpretación, recomendaciones y API).
- Endpoint fallido de prueba eliminado para dejar Azure limpio.

**Archivos o componentes afectados:**  
- Modificados: `azure/deploy_endpoint.py` (identidad + modo skip-endpoint + tráfico), `requirements.txt` (+httpx), `Bitacora.md` (esta entrada).
- Nuevos: `tests/test_api.py`.

**Problemas o bloqueos:**  
- Persiste el único bloqueo externo: propagación de elegibilidad de endpoints online (etapas 10-11). Todo lo demás del MVP funciona.

**Siguiente paso:**  
Reintentar el endpoint (crear por ARM con identidad + deployment por SDK con `AZ_SKIP_ENDPOINT=1`); al funcionar, guardar credenciales en `.env` e implementar el cliente del backend (etapa 11). Seguir etapa 14 (seguridad/manejo de errores) y 15 (documentación y demo).

---

# Plantilla para nuevas entradas

## DD/MM/AAAA — HH:MM
**Tipo:** Técnico / Documentación / Investigación / Arquitectura / Pruebas / Gestión

**Actividad realizada:**  
Hoy realicé...

**Decisiones tomadas:**  
Decidí...

**Resultado:**  
El resultado fue...

**Archivos o componentes afectados:**  
- ...

**Problemas o bloqueos:**  
- Ninguno / ...

**Siguiente paso:**  
...
