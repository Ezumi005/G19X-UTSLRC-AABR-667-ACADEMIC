# Guía de Instalación — Motor Inteligente de Segmentación de Clientes

**Versión:** 2.0 · **Fecha:** 16/10/2026 · **Plataforma de desarrollo:** Windows (instrucciones para Linux/macOS incluidas al final)

Esta guía deja el sistema completo corriendo desde cero, partiendo **solo de este repositorio**:
https://github.com/Ezumi005/G19X-UTSLRC-AABR-667-ACADEMIC

---

## 1. Prerequisitos

| Software | Versión mínima | Para qué |
|---|---|---|
| Git | 2.x | Clonar el repositorio |
| Python | 3.12 (proyecto probado en 3.14) | Backend, motor ML, simulador, pruebas |
| Node.js + npm | 20 / 11 | Frontend React |
| PostgreSQL | 16 (proyecto probado en 18.6) | Base de datos |

**Opcionales (credenciales de nube, para las 3 funciones de IA):** cuenta de Azure con un recurso de App Service (scoring) y uno de Azure OpenAI. Sin ellas el sistema corre en **modo degradado**: todo el motor y la web funcionan; solo faltan predicciones, recomendaciones y sugerencia de mapeo.

## 2. Obtener el código

```powershell
git clone https://github.com/Ezumi005/G19X-UTSLRC-AABR-667-ACADEMIC.git MotorSeg
cd MotorSeg
```

## 3. Entorno Python y dependencias

```powershell
python -m venv .venv
.\.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Variables de entorno

```powershell
copy .env.example .env            # macOS/Linux: cp .env.example .env
```
Editar `.env` (todas las claves con su explicación aparecen comentadas el el propio archivo):

```
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/motor_segmentacion
# Opcionales (IA):
SIMULATOR_URL=http://127.0.0.1:8001
AZURE_SCORING_URL=https://motor-seg-scoring.../score     + AZURE_SCORING_API_KEY
AZURE_OPENAI_ENDPOINT=https://openai-motor-seg.../openai + AZURE_OPENAI_API_KEY + AZURE_OPENAI_DEPLOYMENT
```
⚠️ Nunca subir el `.env` al repositorio (el `.gitignore` ya lo excluye).

**Modo sin Azure (100% local):** las claves de Azure son opcionales; con solo `DATABASE_URL` el proyecto funciona completo (ingesta, segmentación, web, audiencias) y las tres asistencias de IA degradan de forma controlada (501/503). Detalle en README §25.

## 5. Dataset del CRM simulado

```powershell
.\.venv\Scripts\python.exe -m crm_simulator.generate_data
```
Genera `data/*.json` (dataset reproducible con semilla fija: ~500 clientes, transacciones, interacciones y campañas). **Sin este paso el simulador no tiene datos que servir** (la carpeta `data/` no se versiona). `instalar_proyecto.bat` y `levantar_proyecto.bat` lo ejecutan automáticamente si falta.

## 6. Esquema de base de datos

```powershell
.\.venv\Scripts\python.exe -m src.persistence.init_db
```
Crea la base `motor_segmentacion` (si no existe) y todas las tablas (contrato V1 + trazabilidad + producto).

## 7. Ejecutar el sistema (4 terminales)

**Terminal 1 — CRM simulado (fuente externa, déjalo corriendo):**
```powershell
.\.venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001
```

**Terminal 2 — primera ingesta + segmentación:**
```powershell
.\.venv\Scripts\python.exe -m src.persistence.ingest      # ~498 clientes → PostgreSQL
.\.venv\Scripts\python.exe -m src.ml.segmentation         # K-Means k=6 + etiquetas
```

**Terminal 3 — API backend:**
```powershell
.\.venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000
# El arranque tarda ~20 segundos (carga de pandas/sklearn): es normal
```

**Terminal 4 — frontend:**
```powershell
cd frontend
npm install
npm run dev        # http://localhost:5173
```

## 8. Verificación de la instalación

1. `http://127.0.0.1:8000/health` → JSON con `"status": "ok"` (o `"degradado"` solo si faltan credenciales de Azure).
2. `http://localhost:5173` → Dashboard con **498 clientes, 6 segmentos** y KPIs.
3. `http://127.0.0.1:8000/docs` → Swagger con todos los endpoints.
4. Pruebas opcionales de confianza: `.venv\Scripts\python.exe -m tests.test_api` (módulo a módulo, 10 en total).

## 9. Arranque diario (datos ya cargados)

Más tarde (datos ya cargados): solo terminales 1 (simulador), 3 (backend) y 4 (frontend). Repetir ingesta/segmentación es idempotente y solo se hace cuando se deseen datos nuevos.


## 10. Alternativa todo-en-uno: Docker

```powershell
docker compose up --build
# frontend 5173 · backend 8000 · simulador 8001 · postgres 5432
```
Requiere Docker Desktop. Postgres corriendo local es innecesario en este modo.

## 11. Solución de problemas de instalación

| Problema | Solución |
|---|---|
| `venv no reconoce el comando` y `python -m venv` falla | Confirmar Python ≥3.12 con `python --version`; crear venv con `python -3.12 -m venv .venv` |
| Error de compilación al instalar *x* con pip | Actualizar pip: `python -m pip install --upgrade pip` y repetir `pip install -r requirements.txt` |
| Error de conexión al usar `DATABASE_URL` | Confirmar servicio `postgresql-x64-18` activo (`services.msc`) y usuario/contraseña correctos |
| `database "motor_segmentacion" does not exist` al init_db | Ejecutar `init_db` una vez — ya lo crea — y verificar que `DATABASE_URL` apunte a la instancia local |
| Puertos ocupado (8000/8001/5173/5432) | `Get-NetTCPConnection -LocalPort <puerto> -State Listen` y parar el proceso previo |
| npm install falla | Confirmar Node ≥20 (`node -v`); borrar `node_modules` + `package-lock.json` y repetir |
| La web abre pero sale en blanco | El backend siguió arrancado; esperar ~20 s y recargar; en caso extremo usar el botón del ErrorBoundary |
| Frontend no conecta con el backend | Confirmar que el backend vive en el puerto 8000 (`/health` arriba) y que se ejecutó `npm run dev` desde la carpeta `frontend/` |
| PowerShell se queja de ejecución de scripts | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

## 12. Despliegue (opcional)

CI (GitHub Actions) automatiza pruebas; para producción se recomienda contenedorizar cada servicio (Dockerfiles ya incluidos) y provisionar PostgreSQL administrado. Las credenciales de Azure vía variables de entorno del servicio de hosting, jamás en el código. Autenticación de la API: ver README §19 (API key/JWT como primer paso).
