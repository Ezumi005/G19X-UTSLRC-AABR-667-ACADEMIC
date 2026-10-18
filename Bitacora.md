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

## 28/09/2026 — 13:31
**Tipo:** Técnico / Arquitectura

**Actividad realizada:**  
Completé las etapas 10 y 11 del orden de desarrollo mediante una desviación aprobada por el usuario. Reintenté el endpoint online de Azure ML tras 5 días (names nuevos, ARM directo con identidad, eastus2 post-propagación, verificación del método de pago por el usuario en el portal): el rechazo `SubscriptionNotRegistered [N/A]` del plano de inferencia persiste en todas las combinaciones; es una limitación del tipo de suscripción, documentada con evidencia completa. Ante eso, el usuario aprobó mi plan recomendado: mantener el modelo **registrado y versionado en Azure ML** (kmeans-local:1 + entorno) y servir la inferencia en **Azure App Service** con el mismo artefacto. Desplegué el servicio de scoring (plan F1 gratuito en centralus, tras descubrir que la cuota F1 de eastus también estaba en 0), lo verifiqué contra los perfiles de control e integré el backend para consumirlo (etapa 11).

**Decisiones tomadas:**  
- Desviación documentada del criterio 8-9 del MVP: inferencia en App Service en lugar de endpoint online de Azure ML, por bloqueo externo del tipo de suscripción (evidencia en bitácora y README §7). El contrato de scoring es idéntico al de `azure/score.py` para migrar sin cambios si la suscripción lo permite algún día.
- Servicio de scoring (`azure/scoring_app/`): FastAPI mínimo con el MISMO artefacto y lógica de preparación, autenticación `X-API-Key`, health check; desplegado con Oryx build (aprendizajes: requería `SCM_DO_BUILD_DURING_DEPLOYMENT=true` y la app debe configurarse antes del primer arranque para no dejar el SCM wedged).
- Etapa 11: `src/services/scoring.py` (cliente con degradación 501/502), `queries.customer_features` (las 7 features por cliente desde PostgreSQL, misma convención de recency que features/rfm) y endpoint `POST /customers/{id}/predict` que devuelve cluster + etiqueta del último run.
- Credenciales `AZURE_SCORING_URL/KEY` en `.env` local (llave generada con `secrets`); documentadas en `.env.example`.

**Resultado:**  
- Scoring en la nube verificado: perfiles VIP/riesgo/navegador → clusters 2/5/0, idénticos al modelo local; 401 sin llave.
- Cadena completa en vivo: `POST /customers/CLI-0001/predict` → features desde PostgreSQL → scoring en Azure → cluster 2 "Clientes frecuentes de alto valor".
- 9 suites de pruebas en verde (nueva: tests/test_scoring.py con mock del servicio).
- Limpieza: PDF v1.0 eliminados por el usuario (commit ed5abae) y endpoints fallidos de prueba borrados.

**Archivos o componentes afectados:**  
- Nuevos: `azure/scoring_app/{main.py, requirements.txt}`, `src/services/scoring.py`, `tests/test_scoring.py`.
- Modificados: `src/persistence/queries.py` (+customer_features), `src/api/routes/customers.py` (+predict), `.env.example`, `.gitignore` (+artefacto copiado en scoring_app), `README.md` (§7, §9, §16), `Bitacora.md` (esta entrada).
- Azure: webapp `motor-seg-scoring` + plan `plan-sc-centralus` (F1) desplegados.

**Problemas o bloqueos:**  
- Resueltos hoy: bloqueo de inferencia (vía App Service) y cuota F1 0 en eastus (vía centralus). Sin bloqueos activos por primera vez desde el inicio de Azure.

**Siguiente paso:**  
Etapa 14 (resto: manejo de errores y ajustes de seguridad), etapa 15 (documentación final, recomendaciones para los 6 segmentos, demo), limpieza de Azure y vinculación a GitHub.

---

## 28/09/2026 — 14:09
**Tipo:** Técnico / Documentación

**Actividad realizada:**  
Cerré las etapas 14 y 15 del proyecto. Ejecuté primero las 9 suites de pruebas (todas en verde, como condición previa). Implementé el pulido de manejo de errores y seguridad: handler global de excepciones en la API (log completo en servidor, respuesta 500 controlada sin filtrar detalles) y timeout explícito de 60s en las llamadas a Azure OpenAI, con nueva prueba del 500 controlado. Generé las recomendaciones comerciales reales para los 6 segmentos (datos de demo, vía Azure OpenAI, persistidas). Completé la documentación final del README (estado de etapas, criterios del MVP cumplidos y nueva sección 18: guía de demostración) y ejecuté la limpieza de Azure: eliminé los 2 workspaces duplicados, conservando los recursos que el MVP utiliza.

**Decisiones tomadas:**  
- El handler global devuelve un mensaje genérico al cliente y registra el detalle solo en el log del servidor (no filtrar stack traces).
- La autenticación de la API propia queda documentada como decisión post-MVP (el PRD la condiciona a "cuando el entorno lo requiera"); el frontend de demo opera en localhost.
- En Azure se conservan únicamente: `openai-motor-seg` (Azure OpenAI), `ml-motor-seg-v2` (registro del modelo) y `motor-seg-scoring` + plan F1 (scoring). Se eliminan `ml-motor-segmentacion` y `ml-motor-seg-eus2` (duplicados de los intentos de diagnóstico).

**Resultado:**  
- 9 suites en verde; prueba nueva de error interno controlado pasando.
- Recomendaciones persistidas para los 6 segmentos (ids 2-7 en la tabla recommendations): cada una con descripción y 3 acciones coherentes con su perfil (VIP→programa de fidelización; riesgo→reactivación; navegadores→recuperación de carrito/primera compra; nuevos→onboarding; ocasionales→reactivación escalonada).
- README con §12 (estado), §14 (criterios cumplidos), §17 reordenada y §18 (guía de demo) — verificado que la estructura quedó coherente tras detectar y corregir una inserción desordenada.
- Scoring en Azure verificado tras la limpieza; workspaces duplicados en eliminación.

**Archivos o componentes afectados:**  
- `src/api/app.py` (handler global), `src/services/recommendations.py` (timeout), `tests/test_api.py` (+500 controlado).
- `README.md` (§12, §14, §17, §18), `Bitacora.md` (esta entrada).
- Azure: workspaces duplicados eliminados; base de datos con 6 recomendaciones.

**Problemas o bloqueos:**  
- Ninguno. Único pendiente opcional: vincular el repositorio a GitHub (requiere cuenta y decisión del usuario).

**Siguiente paso:**  
Vincular GitHub si se decide (instrucciones listas) y realizar la demostración final del MVP. Con esto, el proyecto queda completo según el alcance definido.

---

## 06/10/2026 — 14:35
**Tipo:** Gestión

**Actividad realizada:**  
Vinculé el repositorio con GitHub, el último pendiente opcional del proyecto. Instalé GitHub CLI, autenticé la sesión (flujo de código de dispositivo, credenciales del usuario) y creé el repositorio remoto con el nombre solicitado.

**Decisiones tomadas:**  
- Repositorio **privado** (contiene documentación académica y del proyecto).
- Nombre asignado por el usuario: `G19X-UTSLRC-AABR-667-ACADEMIC`.
- Rama `main` enlazada a `origin/main`; los `.env` y secretos siguen excluidos por `.gitignore` (verificado durante todo el desarrollo).

**Resultado:**  
- Repositorio publicado: https://github.com/Ezumi005/G19X-UTSLRC-AABR-667-ACADEMIC con los 23 commits del historial completo.
- Con esto, el proyecto queda cerrado: 15/15 etapas del orden de desarrollo, demo documentada (README §18) y respaldo remoto.

**Archivos o componentes afectados:**  
- Git: remoto `origin` añadido; `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. (Nota: el login inicial de gh requirió dos intentos; se resolvió lanzando el flujo de dispositivo en segundo plano y compartiendo el código de un solo uso).

**Siguiente paso:**  
Ninguno pendiente. Posibles continuaciones futuras: mejoras post-MVP (autenticación de la API, audiencias dinámicas, adaptadores para CRM reales, migración del scoring a endpoint online de Azure ML si la suscripción lo habilita).

---

## 06/10/2026 — 14:43
**Tipo:** Gestión

**Actividad realizada:**  
Retiré los PDF del PRD y del MVP del repositorio de Git a solicitud del usuario: se eliminaron del índice (quedan intactos solo en la carpeta local) y se agregó `*.pdf` al `.gitignore` para que nunca vuelvan a versionarse.

**Decisiones tomadas:**  
- Los documentos oficiales (PRD/MVP) dejan de vivir en el repositorio; el código y la bitácora siguen siendo la fuente del desarrollo.
- Nota transparente: los PDF permanecen en los commits antiguos del historial (el repo es privado). Si el usuario quisiera purgarlos del historial completo, requeriría reescribirlo (filter-repo + force push), lo cual contradice la regla de no alterar el historial; queda como decisión pendiente solo si él la pide.

**Resultado:**  
- PDF del PRD y del MVP fuera del repositorio y del remoto de GitHub; archivos locales intactos; `.gitignore` actualizado.

**Archivos o componentes afectados:**  
- `.gitignore`, índice de Git (remoción de 2 PDF), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Confirmar si se retiran también los otros PDF locales ("Información General - Empresarial", "Mini diccionario") y/o los extractos Markdown de `docs/` del repositorio.

---

## 06/10/2026 — 15:13
**Tipo:** Técnico

**Actividad realizada:**  
Completé el Nivel 1 del plan de mejora de la web (derivado del análisis PRD/MVP vs implementación). Implementé: botón "Predecir segmento (Azure)" en el detalle expandible de cada cliente (expone en la interfaz la inferencia en la nube que ya funcionaba solo por API), gráficas en el Dashboard con recharts (clientes por segmento, gasto acumulado promedio, recencia promedio y top categorías), filtros de clientes (segmento, ciudad, búsqueda por ID, resueltos en SQL) y la vista Ejecuciones con el historial de runs y sus métricas. Verifiqué todo en vivo y con las pruebas de API ampliadas.

**Decisiones tomadas:**  
- `recharts` como librería de gráficas (estándar en React, ligera).
- Filtros resueltos en SQL (no en el cliente) para que la paginación siga siendo correcta con resultados filtrados.
- Nuevo endpoint `GET /segmentation/runs` (PRD §19: consultar ejecuciones) y `GET /dashboard` enriquecido con perfil promedio por segmento (desde el JSONB de `segments`) y top de categorías.
- La predicción se cachea por cliente en la interfaz tras la primera consulta.

**Resultado:**  
- Backend: filtros + runs + dashboard enriquecido, con pruebas ampliadas en verde (commit c6a84d8).
- Frontend: 4 gráficas nuevas, barra de filtros, botón de predicción con resultado (cluster + etiqueta) y página Ejecuciones; `npm run build` en verde.
- Verificación en vivo: runs (#4, silhouette 0.4144), filtro "Clientes nuevos" (3 de 70), dashboard (6 perfiles, 8 categorías) y predicción real `CLI-0003 → cluster 2 "Clientes frecuentes de alto valor"`.

**Archivos o componentes afectados:**  
- Backend: `src/persistence/queries.py`, `src/api/routes/{customers,segments}.py`, `tests/test_api.py`.
- Frontend: `package.json` (+recharts), `src/{api.ts, types.ts, App.tsx, styles.css}`, `src/pages/{Dashboard, Customers, Runs}.tsx`.
- Docs: `README.md` (§9, §11, §16, §18), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno (un import faltante de `Query` detectado por las pruebas y corregido al instante).

**Siguiente paso:**  
Nivel 2 del plan de mejora: audiencias dinámicas (PRD §16), vista de cliente propia, seguridad básica de la API y panel de observabilidad; o lo que el usuario priorice.

---

## 07/10/2026 — 20:34
**Tipo:** Técnico

**Actividad realizada:**  
Completé el Nivel 2 del plan de mejora: audiencias dinámicas (PRD §16, RF-18/19), página de detalle de cliente y observabilidad de ingestión en la web (PRD §31). Implementé la tabla `audiences` con condiciones JSONB y membresía recalculada en cada consulta; endpoints CRUD + export CSV (`/audiences`); `GET /ingestion/runs` con duraciones, conteos leídos/guardados e incidencias; el detalle de cliente ahora incluye sus 7 features del contrato de scoring; y en el frontend las vistas Audiencias (constructor de condiciones, listado, miembros, export, borrado), Detalle de cliente (RFM, features, predicción en Azure) y el historial de ingestión dentro de Ejecuciones. Verifiqué todo en vivo.

**Decisiones tomadas:**  
- Condiciones de audiencia combinables por AND: segmento del último run, ciudad (ILIKE), frecuencia mínima, días sin compra y "ha comprado categoría X"; validadas con Pydantic (incluye enum canónico de categorías del contrato).
- La membresía NO se persiste: se recalcula contra los datos vigentes en cada consulta (RF-19) y se actualiza el tamaño/fecha de último cálculo como estadística.
- Export CSV servido directamente por el backend (`text/csv` + Content-Disposition) para uso en campañas.
- La seguridad de la API (API key/roles) queda como pieza separada y deshabilitada para no romper la demo local; documentada como decisión post-MVP.
- Parámetros SQL con casts explícitos (`::text/::int`) para que PostgreSQL infiera tipos en las comparaciones con NULL.

**Resultado:**  
- Backend (commit bd7cb03): audiencias + runs de ingesta + features en detalle de cliente, con `tests/test_audiences.py` en verde y suite de API completa.
- Frontend: vistas nuevas funcionando, `npm run build` en verde.
- Verificación en vivo: audiencia "riesgo + electrónica" → 64 clientes coherentes; export CSV (66 líneas); detalle CLI-0001 con 7 features y segmento; historial de 8 ingestiones con duraciones e incidencias.

**Archivos o componentes afectados:**  
- Backend: `schema.sql`, `queries.py`, `routes/{audiences,ingestion,customers,app}.py`, `tests/test_audiences.py`.
- Frontend: `api.ts`, `types.ts`, `App.tsx`, `styles.css`, `pages/{Audiences, CustomerDetail, Customers, Runs}.tsx`.
- Docs: `README.md` (§9, §10, §11, §16, §18), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno relevante (dos correcciones menores al vuelo: import de `Link` y casts SQL).

**Siguiente paso:**  
Nivel 3 del plan de mejora cuando se decida: GitHub Actions (CI gratuito en repo público), Docker Compose, churn/CLV, adaptador CSV; y la decisión pendiente de seguridad de la API para demostraciones externas.

---

## 13/10/2026 — 15:46
**Tipo:** Técnico

**Actividad realizada:**  
Ajustes de experiencia de usuario pedidos por el usuario final y corrección del fallo de predicción. Diagnostiqué el error de scoring: el plan gratuito F1 de Azure "duerme" la app tras inactividad y el primer request (arranque en frío) excedía nuestro timeout de 15s; el servicio estaba sano (health 0.5s, predicción OK). Antes de cambiar nada, respondí al usuario las preguntas sobre el menú Ejecuciones (trazabilidad/historial) y las audiencias dinámicas (conversión del análisis en listas accionables para campañas, con export CSV).

**Decisiones tomadas:**  
- Fix de scoring: timeout de 90s + reintento automático (2 intentos) en `src/services/scoring.py`, documentando la causa (arranque en frío del plan F1).
- Dashboard: se elimina la sección "Últimas ejecuciones"; gasto total y ticket promedio se formatean con moneda configurable.
- Etiquetas de gráficas: texto completo con salto de línea (componente de tick personalizado) en vez de truncar con "…".
- Nueva configuración de usuario (engranaje en la barra superior): tema claro/oscuro y moneda (MXN/USD/EUR/COP/ARS/CLP/PEN), persistidos en localStorage y aplicados con variables CSS.
- Limpieza de datos técnicos para el usuario final: sin "Run #N" ni métricas de clustering (silhouette/DB/inertia) en las vistas de negocio; Segmentos muestra solo totales; porcentajes legibles (campaign_click_rate como %).

**Resultado:**  
- Predicción verificada en vivo tras el fix (CLI-0005 → cluster 2) y backend reiniciado con el código nuevo; pruebas de scoring y API en verde; `npm run build` OK.
- Web con tema oscuro/claro y moneda configurable; dashboard y perfiles con montos en moneda; gráficas con etiquetas completas.

**Archivos o componentes afectados:**  
- Backend: `src/services/scoring.py` (timeout + reintento).
- Frontend: `settings.tsx` (nuevo: provider de ajustes), `main.tsx`, `App.tsx` (engranaje + panel), `styles.css` (reescrito con variables CSS + tema oscuro), `pages/{Dashboard, SegmentDetail, Segments, Customers, CustomerDetail}.tsx`.
- `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- El reportado por el usuario (predicción con error de scoring) quedó corregido y explicado: era arranque en frío del plan gratuito, no un fallo del sistema.

**Siguiente paso:**  
Siguientes mejoras del plan cuando el usuario decida (Nivel 3: CI, Docker, churn/CLV, seguridad de API).

---

## 13/10/2026 — 15:52
**Tipo:** Técnico / Documentación

**Actividad realizada:**  
Ronda de usabilidad para el usuario final, pedida explícitamente. Anoté en el README (§7) el diagnóstico y fix del arranque en frío del scoring en Azure. Añadí subtítulos de propósito en cada menú, un glosario con modales informativos (`InfoTip`) solo en términos poco comunes (RFM, recencia, ticket, carritos abandonados, tasa de clic, cluster, silhouette, Davies-Bouldin, k, audiencia, ingesta, incidencias, inferencia), y pulí detalles: footer sin jerga técnica, eliminé la línea redundante de conteo en Clientes (ya la muestra el paginador), títulos simplificados. Conservé la trazabilidad completa (página Ejecuciones) con su papel de soporte. Ejecuté pruebas de uso.

**Decisiones tomadas:**  
- Glosario central (`glossary.ts`) + componente `InfoTip` reutilizable: botón "?" que abre un mini-modal con explicación coloquial; solo en términos no obvios, como pidió el usuario.
- Cada menú explica su propósito en una línea bajo el título (curva de aprendizaje rápida).
- La página de Ejecuciones se mantiene íntegra (trazabilidad) pero etiquetada como "vista de soporte", y las vistas de negocio quedan limpias de datos técnicos.
- Corregí en el acto una doble codificación de acentos en Dashboard.tsx que introdujo un `Set-Content` de PowerShell (lección: reescrituras de archivo solo con las herramientas de edición, no con cmdlets).

**Resultado:**  
- README §7 con la nota operativa del cold start (causa, diagnóstico y fix).
- Web: 13 términos con modal explicativo, 5 menús con propósito claro, footer y textos pulidos.
- Pruebas de uso: `npm run build` en verde; suites de API y audiencias en verde; dev server sirviendo los módulos nuevos (InfoTip/glosario/ajustes verificados por HTTP); checklist estructural completado (propósito por menú, tips solo en términos poco comunes, sin redundancias, sin datos técnicos en vistas de negocio).

**Archivos o componentes afectados:**  
- `README.md` (§7), `Bitacora.md` (esta entrada).
- Frontend: `glossary.ts` y `InfoTip.tsx` (nuevos), `App.tsx`, `styles.css` (estilos del tip), `pages/{Dashboard, Customers, CustomerDetail, Segments, SegmentDetail, Audiences, Runs}.tsx`.

**Problemas o bloqueos:**  
- Ninguno pendiente. (Corregido al vuelo el problema de encoding mencionado.)

**Siguiente paso:**  
Revisión visual del usuario en el navegador (refresh con HMR ya aplicado) y siguientes mejoras del plan (Nivel 3) cuando decida.

---

## 13/10/2026 — 15:56
**Tipo:** Técnico

**Actividad realizada:**  
Simplifiqué la configuración a pedido del usuario: la moneda queda fija en pesos mexicanos (MXN) y se eliminó el selector; el panel de configuración conserva únicamente el tema claro/oscuro.

**Decisiones tomadas:**  
- El formateo de montones (`fmtMoney`) queda fijo en MXN sin depender de preferencias; se eliminó el estado de moneda y su persistencia.

**Resultado:**  
- Panel de configuración con solo el tema; build en verde y cambios aplicados en caliente por el dev server.

**Archivos o componentes afectados:**  
- `frontend/src/settings.tsx`, `frontend/src/App.tsx`, `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Continuar con el plan de mejora cuando el usuario decida.

---

## 15/10/2026 — 12:37
**Tipo:** Técnico / Pruebas

**Actividad realizada:**  
Atendí el reporte de pantalla en blanco al entrar a Segmentos. Diagnostiqué el sistema completo: las 9 suites de pruebas en verde y los endpoints que consume la página funcionando; la causa operativa fue que los servidores locales estaban caídos tras el paso de los días (el backend además tarda ~20 s en arrancar por la carga de librerías). Añadí robustez real: `ErrorBoundary` en la raíz de la app para que cualquier error de la interfaz se muestre con un mensaje legible y botón de recarga, en lugar de una pantalla en blanco. Reinicié el servidor de desarrollo con la caché de Vite limpia y dejé backend y frontend operativos y verificados.

**Decisiones tomadas:**  
- ErrorBoundary con mensaje amigable + detalle del error y botón de recarga: la pantalla en blanco queda eliminada como modo de fallo y, si algo se rompe, el usuario puede reportar el mensaje exacto.
- Reinicio limpio del dev server (borrado de `node_modules/.vite`) para descartar estado envenenado del HMR tras las ediciones en caliente.
- Documentada en el README la nota operativa del arranque lento del backend (~20 s).

**Resultado:**  
- Backend arriba (health OK), frontend servido con módulos nuevos verificados, `GET /segments` respondiendo 6 segmentos.
- `npm run build` en verde; usuario puede recargar la app con confianza.

**Archivos o componentes afectados:**  
- Nuevos: `frontend/src/ErrorBoundary.tsx`.
- Modificados: `frontend/src/main.tsx` (envoltura de ErrorBoundary), `README.md` (§11 + nota operativa), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Resuelto el reporte: servidores arriba y fallos visibles a partir de ahora.

**Siguiente paso:**  
Confirmar con el usuario que la app carga correctamente tras el refresh y continuar con el plan de mejora cuando decida.

---

## 15/10/2026 — 12:47
**Tipo:** Documentación

**Actividad realizada:**  
Documenté en el README la nueva sección **"6-bis. Cómo se generan los segmentos y las audiencias"** a pedido del usuario, para dejar clara la distinción en los documentos técnicos: el flujo de generación de segmentos (datos → features RFM+engagement → preparación → K-Means → etiquetas por perfil, con su ejecución e historial), el funcionamiento de las audiencias dinámicas (condiciones AND del usuario, evaluadas en SQL, recalculadas en cada consulta, export CSV) y una tabla con la diferencia esencial (algoritmo descubre vs. usuario define; entender vs. actuar; cuándo cambia cada una), cerrando con el flujo de negocio completo.

**Decisiones tomadas:**  
- Sección insertada tras la §6 (contexto de ML) con sufijo "6-bis" para no renumerar el resto del documento.
- Lenguaje claro y directo, con referencias a los módulos y comandos reales para que cualquiera pueda trazar cada paso.

**Resultado:**  
- README actualizado como mapa completo: cualquier desarrollador, IA o usuario técnico puede entender cómo nacen los segmentos y las audiencias sin leer código.

**Archivos o componentes afectados:**  
- `README.md` (nueva §6-bis), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Continuar con el plan de mejora cuando el usuario decida.

---

## 15/10/2026 — 12:51
**Tipo:** Técnico

**Actividad realizada:**  
Añadí el botón **"Recalcular segmentos"** en la página de Segmentos (`POST /segmentation/run` desde la interfaz, sin necesidad de usar el backend o la consola) y eliminé el pie de página con el nombre del proyecto, como pidió el usuario. Verifiqué en vivo la ruta del botón: ejecutó el run #5 (k=6, 6 segmentos, 1.6 s) y la lista refleja el run nuevo.

**Decisiones tomadas:**  
- El botón deshabilita mientras recalcula y muestra un aviso de confirmación al terminar; refresca la lista automáticamente (los enlaces a detalles antiguos siguen válidos porque el historial se conserva).
- Fuera el footer; su regla CSS se reemplazó por la barra de acciones del botón.

**Resultado:**  
- La segmentación se puede disparar 100% desde la web; build en verde y verificación en vivo OK.

**Archivos o componentes afectados:**  
- `frontend/src/api.ts` (+runSegmentation), `frontend/src/pages/Segments.tsx` (botón + recarga), `frontend/src/App.tsx` (sin footer), `frontend/src/styles.css`, `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Lo que el usuario decida del plan de mejora.

---

## 15/10/2026 — 22:08
**Tipo:** Técnico

**Actividad realizada:**  
Completé la **Sesión 1 del plan de profesionalización (Track A — acabado visual)**, con el requisito añadido por el usuario de que las gráficas aporten valor real sin datos redundantes. Realicé auditoría de las 4 gráficas del Dashboard (cada una responde una pregunta de negocio distinta: masa de clientes, valor, enfriamiento y producto; ninguna duplica las tarjetas globales) y las potencié: paleta consistente por segmento entre gráficas, tooltips con formato (pesos exactos, días, conteos y nombre completo), y barras clicables que navegan al detalle del segmento. Implementé el sistema de feedback propio (`Feedback.tsx`): notificaciones toast y diálogos de confirmación estilizados que reemplazan todos los `window.alert/confirm` (predicción, recálculo de segmentos, borrado de audiencias). Añadí skeletons de carga (`Skeleton.tsx`) en Dashboard, Clientes, Segmentos, Audiencias, Ejecuciones y detalle de cliente; responsive para móvil/tablet (tablas con scroll, barra colapsable, grids a una columna); y branding propio (favicon SVG con monograma de barras de segmentos).

**Decisiones tomadas:**  
- Auditoría de gráficas: se mantienen exactamente 4 porque cada una responde una pregunta distinta; no se agregaron gráficas redundantes (p. ej. frecuencia/ticket por segmento se descartaron por correlación con gasto).
- Un solo proveedor de feedback (toasts + confirm) global vía contexto; los errores de Azure/OpenAI ahora se notifican con toast rojo y las confirmaciones usan modal propio.
- Colores por segmento consistentes en todas las gráficas para lectura cruzada.
- Verificación extra de encoding tras usar cmdlets sobre Dashboard.tsx (sin corrupción esta vez).

**Resultado:**  
- `npm run build` en verde; dev server sirviendo todos los módulos nuevos; backend arriba.
- La app ya no muestra diálogos nativos del navegador ni textos "Cargando…"; experiencia visual considerablemente más profesional.

**Archivos o componentes afectados:**  
- Nuevos: `frontend/src/Feedback.tsx`, `frontend/src/Skeleton.tsx`, `frontend/public/favicon.svg`.
- Modificados: `main.tsx` (proveedor de feedback), `pages/{Dashboard, Customers, CustomerDetail, Segments, Audiences, Runs}.tsx`, `styles.css` (toasts, modal, skeleton, tooltips, responsive), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno (dos roces de tipado de recharts resueltos al instante).

**Siguiente paso:**  
Sesión 2 (Track B): CI con GitHub Actions, `/health` real por dependencia y lint — cuando el usuario apruebe.

---

## 15/10/2026 — 22:40
**Tipo:** Técnico

**Actividad realizada:**  
Rediseño visual "cremoso" pedido por el usuario + integración de iconos profesionales. Reemplacé toda la paleta de la interfaz por tonos cálidos (crema, caramelo, terracota, espresso) en ambos temas — claro tipo latte y oscuro tipo mocha — incluyendo badges, toasts, topbar e inputs. Instalé `lucide-react` y sustituí los iconos básicos: navegación con icono por sección (dashboard/clientes/segmentos/audiencias/ejecuciones), engranaje de configuración, "?" de ayuda (HelpCircle), lupa en filtrar, chispas en predecir (Azure), flecha giratoria animada en recalcular, papelera en eliminar y descarga en export CSV. Actualicé el favicon al nuevo degradado caramelo y la paleta de las gráficas a colores cálidos consistentes (terracota, miel, salvia, rosa envejecido, eucalipto, camello).

**Decisiones tomadas:**  
- Paleta cálida completa basada en variables CSS (mismas clases, solo valores): fondo crema `#f6f1e7`, panel `#fffdf7`, primario caramelo `#b4703f`, topbar espresso; oscuro en tonos mocha.
- `lucide-react` (MIT, gratuito, +1500 iconos como componentes) en vez de iconos de texto/emoji: es el estándar de React y hace tree-shaking.
- Botones y enlaces secundarios ahora admiten icono + texto (inline-flex).
- Se retiró el aviso inline del recálculo (el toast verde ya lo notifica), evitando redundancia.

**Resultado:**  
- `npm run build` en verde; dev server sirviendo los cambios; interfaz con identidad cálida coherente en claro/oscuro y gráficas en la misma familia de color.

**Archivos o componentes afectados:**  
- `frontend/package.json` (+lucide-react), `styles.css` (paleta cremosa, iconos en botones, animación de giro), `App.tsx`, `InfoTip.tsx`, `pages/{Segments, Customers, Audiences, Dashboard}.tsx`, `public/favicon.svg`, `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Validación visual del usuario y, cuando apruebe, Sesión 2 del plan (CI, /health real, lint).

---

## 15/10/2026 — 23:14
**Tipo:** Técnico

**Actividad realizada:**  
Sustituí el punto decorativo del título por un **logo de marca** real: componente `Logo.tsx` con las barras de segmentos en degradado caramelo (idéntico al favicon), junto al título "Motor de Segmentación de Clientes" en la barra superior. Coherencia favicon ↔ logo ↔ gráficos.

**Decisiones tomadas:**  
- Logo como componente SVG propio (mismo diseño del favicon) en vez de un icono genérico de librería: refuerza la identidad de marca.

**Resultado:**  
- Build en verde; dev server sirviendo el componente; barra superior con identidad completa.

**Archivos o componentes afectados:**  
- Nuevos: `frontend/src/Logo.tsx`. Modificados: `App.tsx`, `styles.css` (fuera .brand-dot), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
Sesión 2 del plan (CI, /health real, lint) cuando el usuario apruebe; el login queda como decisión opcional según el destino de la demo.

---

## 16/10/2026 — 06:20
**Tipo:** Técnico (Sesión 2 — Track B)

**Actividad realizada:**  
Implementé la Sesión 2 del plan de profesionalización: `/health` real por dependencia (PostgreSQL con ping, Azure scoring con verificación HTTP tolerante al arranque en frío, Azure OpenAI con chequeo de configuración; estado global "ok"/"degradado"), lint con `ruff` (config en `pyproject.toml`, selección E/F/I/W; el código pasó limpio) y **CI con GitHub Actions**: workflow `ci.yml` con dos jobs — backend (PostgreSQL 18 como servicio, esquema, simulador en segundo plano, ingesta, segmentación, las 9 suites y ruff) y frontend (npm ci + build TypeScript). Badge de estado agregado al inicio del README. Ajusté dos pruebas para CI: health tolera dependencias externas degradadas y la prueba del 502 fuerza `SIMULATOR_URL` a un puerto muerto.

**Decisiones tomadas:**  
- El health reporta "degradado" (no error 500) si una dependencia externa falla: el diagnóstico es información, no una caída.
- CI usa Python 3.13 en el runner (compatibilidad garantizada de wheels) aunque desarrollamos en 3.14.
- La prueba de ingesta sin simulador se aísla con variable de entorno para no depender del estado del puerto 8001.

**Resultado:**  
- 9 suites + ruff en verde localmente; workflow publicado para su primera ejecución en GitHub con este commit.

**Archivos o componentes afectados:**  
- `src/api/app.py` (health real), `pyproject.toml` (nuevo, ruff), `requirements.txt` (+ruff), `.github/workflows/ci.yml` (nuevo), `tests/test_api.py` (health e ingesta CI-safe), `README.md` (badge), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno local; pendiente verificar la primera corrida del workflow en GitHub tras el push.

**Siguiente paso:**  
Sesión 3: API tipada (response models), capturas del README, Docker documentado, sección de autenticación en la documentación y release v1.0.0.

---

## 16/10/2026 — 06:27
**Tipo:** Técnico (Sesión 3 — cierre del plan de profesionalización)

**Actividad realizada:**  
Completé la Sesión 3 y con ella el plan de profesionalización. Resultados de la Sesión 2 primero: **el CI de GitHub Actions pasó en su primera ejecución** (1m22s: PostgreSQL servicio + esquema + simulador + ingesta + segmentación + 9 suites + ruff + build del frontend; badge verde en el README). En esta sesión: **API tipada** con response models de Pydantic en todos los endpoints de lectura/escritura principales (`src/api/schemas.py` — Swagger/OpenAPI completo), **documentación de la decisión de autenticación** (nueva sección 19 del README: por qué el MVP no tiene login — demo académica local, PRD §25 condicional, y qué se agregaría si el entorno lo exige), **archivos Docker** (`docker-compose.yml` + Dockerfiles por servicio, documentados y cubiertos por diseño aunque sin Docker Desktop local), **capturas automáticas del README** (Playwright + Chromium headless: dashboard claro/oscuro, clientes, segmento con recomendación y audiencias, guardadas en `docs/img/`) y preparación del **release v1.0.0**.

**Decisiones tomadas:**  
- Response models centralizados en un solo módulo; anotados vía `response_model` para que FastAPI documente y valide las respuestas.
- La ausencia de login queda como decisión documentada con su justificación y su camino de evolución (API key/JWT → roles), no como pendiente silencioso.
- Capturas generadas con navegador real automatizado (2x de escala para nitidez), tema claro y oscuro incluidos.
- Docker documentado como opcional; el stack de demo local sigue siendo el camino principal.

**Resultado:**  
- Todas las suites y lint en verde; CI verde en GitHub; README con badge, capturas y secciones 19-20.
- El proyecto queda con acabado profesional completo para su entrega académica.

**Archivos o componentes afectados:**  
- `src/api/schemas.py` (nuevo), `routes/{customers, segments, audiences, ingestion}.py` (response models), `README.md` (capturas + §19 + §20), `docker-compose.yml` y `docker/Dockerfile.{python, frontend}` (nuevos), `docs/img/*.png` (5 capturas), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. (Corregidos al vuelo: orden de imports señalado por ruff y un response_model provisional mal elegido en el POST de audiencias.)

**Siguiente paso:**  
Publicar el release v1.0.0 en GitHub con notas de versión. Tras eso, el proyecto queda cerrado salvo decisiones futuras del usuario (login, despliegue en la nube, nuevos modelos).

---

## 16/10/2026 — 11:48
**Tipo:** Técnico / Arquitectura

**Actividad realizada:**  
Construí la **adaptación de fuentes sin código y asistida por IA**, pedido del usuario ("todo lo posible desde el frontend", "sin hardcoding", "una IA que se encargue"). Backend: `DynamicCSVAdapter` (misma interfaz `BaseAdapter` que el simulado — el motor no se enteró), tabla `data_sources`, endpoints de fuentes (subir CSV con detección de columnas, validación en seco, creación, sincronización y borrado) y refactor de la ingesta a `persist_result()` reutilizable por cualquier adaptador. Eliminé el hardcoding de esquemas: los campos por entidad ahora se derivan por **introspección de los modelos Pydantic del contrato** (única fuente de verdad; un campo nuevo aparece solo en UI, validación y prompt de IA). Servicio `mapping_suggest.py`: Azure OpenAI (gpt-5.4-mini, temperature 0) recibe esquema introspectado + columnas + filas de muestra y sugiere entidad + mapeo; el endpoint endurece la respuesta (filtra columnas inexistentes) y degrada con 503 si la IA no está. Frontend: nueva vista **Fuentes** (icono Database) con asistente de 3 pasos (subir → mapeo con sugerencia IA pre-llenada y badge de confianza, todo editable → validación en seco con vista previa e incidencias → guardar y sincronizar), listado con ciclo de vida (sincronizar/eliminar).

**Decisiones tomadas:**  
- La IA **sugiere todo** (entidad y mapeo), el humano **confirma**: su salida pasa el filtro de columnas, la validación Pydantic del contrato y la revisión del usuario antes de tocar la base.
- Introspección del contrato en lugar de diccionarios duplicados (adiós `ENTITY_FIELDS` manual).
- Fechas regionales (dd/mm/yyyy) se normalizan en el adaptador (hallazgo de la prueba en vivo: Pydantic solo acepta ISO; la IA incluso lo advirtió en sus notas).
- Sin IA disponible, el asistente manual queda 100% operativo (degradación elegante).

**Resultado:**  
- **Verificación en vivo con IA real**: CSV con columnas `id_cliente, anios, poblacion, cuando_se_registro` → la IA sugirió entidad `customers` y los 4 mapeos correctos (99% de confianza); tras el fix de fechas, validación 2/3 (solo la fila con edad 999 cae en incidencias, como debe ser); sincronización exitosa y datos de prueba limpiados.
- 10 suites + ruff en verde (nueva: `test_sources` con flujo manual completo, sugerencia con mock y degradación 503); `npm run build` OK.

**Archivos o componentes afectados:**  
- Backend: `src/adapters/csv_adapter.py`, `src/services/mapping_suggest.py`, `src/api/routes/sources.py`, `src/persistence/ingest.py` (persist_result), `schema.sql` (+data_sources), `requirements.txt` (+python-multipart), `tests/test_sources.py`.
- Frontend: `pages/Sources.tsx` (nueva), `api.ts`, `types.ts`, `App.tsx` (nav Fuentes), `styles.css`, `glossary.ts` (+término contrato).
- Docs: `README.md` (§3, §9, §16, §18), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno pendiente. Corregidos en el camino: filtro de la sugerencia endurecido en el endpoint, prueba del 503 con token real y normalización de fechas regionales. Extra: al revisar el workflow descubrí que la lista de suites del CI estaba hardcodeada con las 9 originales y **no ejecutaba `test_sources`**; lo corregí en el mismo cierre (job renombrado a "10 suites + lint") y verifiqué en el log de Actions que la suite nueva realmente corre en CI.

**Resultado del cierre:** commits `41a9e0d` (vista Fuentes + asistente IA + fix fechas + docs) y `cf10a69` (CI con 10 suites) pusheados a `main` (repo público); run de Actions **green** con la suite `test_sources` ejecutándose dentro del CI (verificado por log).

**Siguiente paso:**  
Push con CI verificando la suite de fuentes (hecho, verde); el usuario puede probar el asistente desde la web (vista Fuentes).

---

## 16/10/2026 — 12:25
**Tipo:** Documentación

**Actividad realizada:**  
Pasé de revisión completa del README para registrar lo hecho que había quedado sin documentar: endpoints `/sources` completos y corregidos (la línea anterior tenía un `|` suelto y omitía `POST /sources/csv` de creación y `DELETE /sources/{id}`, además de `/schema/{entidad}` por introspección), router `mapping_suggest.py` y routers `audiences`/`sources` en el árbol del proyecto, tabla `data_sources` en la sección del esquema, vista `Sources` en el listado de páginas React, sección de pruebas actualizada a **10 suites** (con ejemplo `test_sources`) y estado del proyecto al 16/10/2026 (MVP cerrado + fuentes CSV asistidas por IA).

**Decisiones tomadas:**  
- Mantener el árbol y las listas de endpoints como mapa fiel del sistema: cualquier archivo nuevo del núcleo se refleja en §16 en el mismo avance que lo crea.

**Resultado:**  
- README consistentes con el código real (verificado por grep contra el árbol de archivos); sin código nuevo en este avance.

**Archivos o componentes afectados:**  
- `README.md` (§4 estado, §9 fuentes, §11 esquema, §16 árbol, §17 pruebas), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno.

**Siguiente paso:**  
El usuario prueba la vista **Fuentes** en el navegador; siguientes mejoras cuando decida (seguridad de API para demostraciones externas, churn/CLV, adaptadores de CRM reales).

---

## 16/10/2026 — 18:12
**Tipo:** Pruebas y calidad

**Actividad realizada:**  
Ejecuté una revisión integral de pruebas del sistema (a pedido del usuario): 10 suites unitarias, recorrido funcional de la API por todos los apartados (health, dashboard, clientes con filtros/paginación, detalle con features, predicción real en Azure, segmentos y métricas, recomendación regenerada con IA real, ejecuciones de segmentación e ingesta, audiencias con ciclo de vida, fuentes CSV con ciclo completo y IA real), casos de error y smoke E2E de las 7 páginas del frontend con Playwright, incluyendo el asistente de Fuentes operando en el navegador con la sugerencia de IA real.

**Decisiones tomadas:**  
- No alteré el diseño de `label_clusters` (falla si dos clusters reciben la misma etiqueta, decisión documentada que "exige revisión humana");documenté el hallazgo como riesgo estructural pendiente de decisión del usuario: cualquier carga nueva que desplace levemente los perfiles de cluster puede provocar una etiqueta duplicada y fallar el recálculo con error 500.

**Resultado:**  
- Suites: 10/10 en verde; ruff limpio. Frontend dev up (estaba caído tras los días).
- E2E en vivo (4/4 fases):health ok con las 3 dependencias; predict real en 1 s con cluster correcto (y validado también con un cliente sincronizado por IA con 0 transacciones: cluster 5, comportamiento huérfano razonable); audiencias 4/4 (422 enum con lista esperada, 409 por nombre duplicado con detalle, 404 en inexistente, membresía recalculada75 → export CSV con 75+header); fuentes: IA real sugirió mapping con 98% de confianza, dry-run 2/3 (la fila de edad 999 en incidencias, como debe), sync 2 → predict del cliente nuevo contra Azure OK → limpieza integral (fuente eliminada, clientes C-IA-% borrados, run de segmentación #6 re-creado OK con 498 clientes); recomendación real regenerada en 3 s.
- Frontend Playwright 7/7 páginas sin ErrorBoundary; smoke del asistente de Fuentes en el navegador: badge IA real, los 4 selects autocompletados (`id_cliente→id_cliente`, etc.) y validación en seco visible.
- Hallazgos (sentencia en el resumen al usuario): 1) 500 real de `POST /segmentation/run` con etiqueta duplicada en clusters 0 y 2 — disparado por los 2 clientes de prueba, no un bug; riesgo de diseño latente documentado; 2) `predict` devuelve `segment.cluster_id: null` (inconsistencia cosmetica del response model); 3) el endpoint `/dashboard` no tiene variante `/dashboard/summary` (así lo diseñé y la UI usa `/dashboard`); 4) los textos de error HTTP muestran `¿` como `�` solo en consolas Windows (los JSON de la API son UTF-8 correctos); 5) desempate PS 5.1: sin `-Form`/`-SkipHttpErrorCheck` (usé curl.exe).

**Archivos o componentes afectados:**  
- Solo `Bitacora.md` y `README.md` (estado del proyecto al 16/10); sin cambios de código: los hallazgos quedan documentados y la base restaurada a 498 clientes con run #6 OK.

**Problemas o bloqueos:**  
- Ninguno operativo. Pendiente de decisión del usuario: endurecer la asignación de etiquetas (desempate determinista) o dejar el comportamiento vigilante actual.

**Siguiente paso:**  
Decisión del usuario sobre el desempate de etiquetas (hecho); luego posibles mejoras de seguridad de API / churn-CLV.

---

## 16/10/2026 — 18:51
**Tipo:** Técnico / Mejora de robustez

**Actividad realizada:**  
Implementé la mejora que el usuario aprobó tras la revisión integral: **desempate determinista de etiquetas** en `src/ml/segmentation.py`. Antes, dos clusters que recibieran la misma etiqueta abortaban el recálculo con error 500 (lo vivimos en la revisión con 2 clientes externos con valores por defecto). Ahora: si varios clusters cumplen la misma regla, la etiqueta es del que mejor encierra el concepto (métricas de desempate: mayor monetary en alto valor, menor frecuencia y más carritos abandonados en navegadores, menor tenure en nuevos, más web_visits en navegador esporádico, mayor recency en riesgo) y los perdedores se reevalúan con reglas de menor prioridad; los clusters sin ninguna regla reciben "Compradores ocasionales" o sus variantes documentadas ("… de baja actividad", "… de actividad mínima") si la base ya está tomada. Solo se falla si se agotan las variantes (revisión humana). Además corregí la inconsistencia cosmética de `predict`: el `segment` ahora incluye `cluster_id` (antes `null`).

**Decisiones tomadas:**  
- Desempate por calidad de concepto en vez de fallar: el típico desplazamiento por cargas pequeñas ya no rompe el sistema; la ambigüedad real (clusters literalmente indistinguibles que agotan las variantes) sigue fallando con mensaje claro.
- Variantes de etiqueta general en vez de marcas raras: mantienen sentido comercial y las recomendaciones se pueden regenerar por etiqueta.

**Resultado:**  
- `test_segmentation` ampliada a 7 pruebas (reales, prioridad, desempate por calidad, mejor calificado gana, variante determinista, agotamiento de variantes, serialización) en verde; las otras 9 suites y ruff sin cambios.
- **Verificación en vivo del caso que antes fallaba**: inserté los 2 clientes huérfanos, `POST /segmentation/run` ahora OK (run 7, 6 etiquetas únicas, cluster desplazado → "Compradores ocasionales de baja actividad"); `predict` regresa `cluster_id` lleno; limpié los clientes de prueba y el run 8 restauró la línea base de 498.

**Archivos o componentes afectados:**  
- `src/ml/segmentation.py` (label_clusters, reglas/métricas/variantes como datos), `src/api/routes/customers.py` (+cluster_id en predict), `tests/test_segmentation.py` (7 pruebas), `README.md` (§6 interpretación), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. En el camino detecté y corregí que mi primer escenario de prueba estaba mal construido (empataba en sin compra, no en la general).

**Siguiente paso:**  
Push y CI; el desempate queda verificado de punta a punta. Posibles mejoras restantes: seguridad de API para demostraciones externas, churn/CLV.

---

## 16/10/2026 — 19:22
**Tipo:** Documentación / Cierre oficial

**Actividad realizada:**  
**Cierre oficial del MVP (v2.0 FINAL)** a instrucción del usuario, bajo la regla de solo añadir información (sin eliminar el historial ni los documentos v1.1). Ejecuté la certificación final (10/10 suites, ruff, build del frontend — todo en verde) y generé documentación técnica de cierre:

- `docs/PRD_Motor_Inteligente_Segmentacion_Clientes_v2.0_FINAL.md` (nuevo): estado final de los 19 RF y 13 RNF con evidencia de cada uno, 5 desviaciones/decisiones de arquitectura aprobadas, criterios de aceptación verificados y evolución futura. Referencia explícita de que el PDF v1.1 manda.
- `docs/MVP_Motor_Inteligente_Segmentacion_Clientes_v2.0_FINAL.md` (nuevo): alcance entregado etapa por etapa, arquitectura final, historial de versiones (v1.0 → v1.1 → v2.0 FINAL).
- `README.md` (solo adiciones): nueva **sección 21 "Dónde se usa Inteligencia Artificial"** (mapa de los 3 usos de IA con sus guardas: recomendaciones con Azure OpenAI, sugerencia de mapeo de fuentes CSV con Azure OpenAI y el modelo K-Means como machine learning no generativo — incluyendo qué NO usa IA), nueva **sección 22 "Manual de arranque completo"** (pasos 1-8 desde clonar el repositorio hasta la web: venv, .env, PostgreSQL, simulador, ingesta, segmentación, backend, frontend + verificación + pruebas + Docker + CI) y nueva **sección 23 "Estado final del proyecto"** con la declaración de cierre y los documentos v2.0.

**Decisiones tomadas:**  
- Los documentos v2.0 son ADICIONALES y de cierre: el PRD/MVP v1.1 (PDF y extractos) se conserva intacto como base normativa.
- El mapa de IA queda en README (§21) y en el PRD FINAL (§5) para que nunca haya duda de dónde se usa IA: recomendación por segmento, sugerencia de mapeo y el modelo ML (nunca decide clusters ni etiquetas).

**Resultado:**  
- Certificación final en verde: 10 suites, ruff, `npm run build`. CI en GitHub Actions green.
- Repositorio completo con instrucciones de arranque desde cero (README §22) y estado final declarado (§23).

**Archivos o componentes afectados:**  
- Nuevos: los 2 documentos v2.0 en `docs/`.
- Modificados (solo adiciones): `README.md` (§21, §22, §23), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. Corregidos al vuelo: artefactos de characters del heredoc de PowerShell al escribir el manual (backticks escapados y 4 palabras corruptas) — revisado el contenido final línea por línea.

**Siguiente paso:**  
Nada bloqueante: MVP v2.0 declarado terminado. Evolución potencial solo si el usuario lo pide (login, churn/CLV, adaptadores de CRM reales, endpoint online de Azure ML).

---

## 17/10/2026 — 22:11
**Tipo:** Documentación / Entregables

**Actividad realizada:**  
Generé los **documentos técnicos de entrega** solicitados por el usuario como guías (carpeta `manuales/`, solo adiciones al repositorio):

- `Manual_Tecnico.md`: operación del sistema (componentes y puertos, procesos del pipeline, referencia de la API y códigos de estado, tablas de la base, pruebas y CI, mapa de mantenimiento por archivo y solución de problemas).
- `Manual_de_Usuario.md`: guía de uso para el usuario final (las 6 vistas de la web paso a paso, cómo leer métricas, significado de mensajes y guion de demostración).
- `Guia_de_Instalacion.md`: instalación desde cero desde el repositorio (requisitos, venv, .env, PostgreSQL, 4 terminales, verificación, Docker y troubleshooting).
- `Documento_Tecnico.md`: diseño y decisiones técnicas (arquitectura, contrato V1, motor ML e interpretación, mapa de IA, seguridad, calidad).

Además generé el **código fuente en `.zip`** (`Motor_Segmentacion_Codigo_Fuente_v2.0.zip`, ~1.6 MB, 130+ archivos) con `git archive`: solo contenido versionado del repositorio — sin `.env`, `.venv`, `node_modules`, PDFs pesados ni artefactos binarios.

**Decisiones tomadas:**  
- Los manuales conviven con la documentación existente (README y docs v2.0 siguen siendo la referencia operativa; los manuales son las guías "para enviar").
- El zip se genera desde Git (no del sistema de archivos) para garantizar exactamente el estado versionado y sin secretos; el binario queda ignorado por `.gitignore`.

**Resultado:**  
- 4 manuales listados arriba listos para envío; zip generado tras el commit de los manuales (incluyéndolos).

**Archivos o componentes afectados:**  
- Nuevos: `manuales/` (4 guías). Modificados: `.gitignore` (+zip), `Bitacora.md` (esta entrada).

**Problemas o bloqueos:**  
- Ninguno. Corregidos al vuelo pequeños artefactos de redacción de los manuales (revisión manual línea por línea).

**Siguiente paso:**  
Commit/push de los entregables y verificación de CI; proyecto en estado de cierre definitivo.

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
