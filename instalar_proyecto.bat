@echo off
REM ============================================================
REM  Motor Inteligente de Segmentacion - primera configuracion
REM  Ejecutar SOLO UNA VEZ (o cuando cambies de computadora)
REM  Tambien sirve para verificar la instalacion.
REM ============================================================
title Instalacion inicial del Motor de Segmentacion

if not exist ".venv\Scripts\python.exe" (
    echo [1/6] Creando entorno Python (.venv)...
    python -m venv .venv
) else (
    echo [1/6] Entorno Python ya existe, ok.
)

echo [2/6] Instalando dependencias Python...
call .venv\Scripts\python.exe -m pip install --quiet --upgrade pip
call .venv\Scripts\python.exe -m pip install --quiet -r requirements.txt

if not exist ".env" (
    echo [3/6] Creando .env desde la plantilla...
    copy .env.example .env >nul
    echo   >>> EDITA el archivo .env con tu DATABASE_URL y credenciales de Azure antes de continuar <<<
    notepad .env
) else (
    echo [3/6] .env ya existe, ok.
)

echo [4/6] Generando dataset del CRM simulado (data/*.json, reproducible)...
call .venv\Scripts\python.exe -m crm_simulator.generate_data

echo [5/6] Creando esquema de base de datos...
call .venv\Scripts\python.exe -m src.persistence.init_db

echo [6/6] Instalando dependencias del frontend...
cd frontend && call npm install && cd ..

echo.
echo ============================================
echo  Instalacion terminada.
echo  Siguiente paso: doble clic en levantar_proyecto.bat
echo  y despues cargar_datos.bat (ingesta + segmentacion).
echo ============================================
pause
