@echo off
REM ============================================================
REM  Motor Inteligente de Segmentacion - primera configuracion
REM  Ejecutar SOLO UNA VEZ (o cuando cambies de computadora)
REM  Tambien sirve para verificar la instalacion.
REM  Si algun paso falla, el script se DETIENE con mensaje claro
REM  (mismo patron que cargar_datos.bat): no continua con una
REM  instalacion a medias.
REM ============================================================
title Instalacion inicial del Motor de Segmentacion

if not exist ".venv\Scripts\python.exe" (
    echo [1/6] Creando entorno Python .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: no se pudo crear el entorno virtual. Revisa que Python este instalado y en el PATH.
        pause
        exit /b 1
    )
) else (
    echo [1/6] Entorno Python ya existe, ok.
)

echo [2/6] Instalando dependencias Python...
call .venv\Scripts\python.exe -m pip install --quiet --upgrade pip
call .venv\Scripts\python.exe -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ERROR: fallo la instalacion de dependencias Python. Revisa conexion a internet y el requirements.txt.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [3/6] Creando .env desde la plantilla...
    copy .env.example .env >nul
    echo   ** EDITA el archivo .env con tu DATABASE_URL y credenciales de Azure antes de continuar **
    notepad .env
) else (
    echo [3/6] .env ya existe, ok.
)

echo [4/6] Generando dataset del CRM simulado (data/*.json, reproducible)...
call .venv\Scripts\python.exe -m crm_simulator.generate_data
if errorlevel 1 (
    echo ERROR: no se pudo generar el dataset del simulador.
    pause
    exit /b 1
)

echo [5/6] Creando esquema de base de datos...
call .venv\Scripts\python.exe -m src.persistence.init_db
if errorlevel 1 (
    echo ERROR: fallo la creacion del esquema. Revisa que PostgreSQL este corriendo
    echo        y que .env tenga una DATABASE_URL correcta.
    pause
    exit /b 1
)

echo [6/6] Instalando dependencias del frontend...
cd frontend && call npm install && cd ..
if errorlevel 1 (
    echo ERROR: fallo npm install en frontend. Revisa que Node.js este instalado y en el PATH.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Instalacion terminada.
echo  Siguiente paso: doble clic en levantar_proyecto.bat
echo  y despues cargar_datos.bat (ingesta + segmentacion).
echo ============================================
pause
