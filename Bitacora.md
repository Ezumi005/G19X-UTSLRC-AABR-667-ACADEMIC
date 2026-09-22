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
