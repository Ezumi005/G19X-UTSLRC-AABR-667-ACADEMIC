@echo off
REM ============================================================
REM  Motor Inteligente de Segmentacion - primera configuracion
REM  Ejecutar SOLO UNA VEZ (o cuando cambies de computadora)
REM  Tambien sirve para verificar la instalacion.
REM ============================================================
title Instalacion inicial del Motor de Segmentacion

if not exist ".venv\Scripts\python.exe" (
    echo [1/5] Creando entorno Python (.venv)...
    python -m venv .venv
) else (
    echo [1/5] Entorno Python ya existe, ok.
)

echo [2/5] Instalando dependencias Python...
call .venv\Scripts\python.exe -m pip install --quiet --upgrade pip
call .venv\Scripts\python.exe -m pip install --quiet -r requirements.txt

if not exist ".env" (
    echo [3/5] Creando .env desde la plantilla...
    copy .env.example .env >nul
    echo   >>> EDITA el archivo .env con tu DATABASE_URL y credenciales de Azure antes de continuar <<<
    notepad .env
) else (
    echo [3/5] .env ya existe, ok.
)

echo [4/5] Creando esquema de base de datos...
call .venv\Scripts\python.exe -m src.persistence.init_db

echo [5/5] Instalando dependencias del frontend...
cd frontend && call npm install && cd ..

echo.
echo ============================================
echo  Instalacion terminada.
echo  Siguiente paso: doble clic en levantar_proyecto.bat
echo  (la primera ingesta y segmentacion se hacen desde
echo   los comandos del README seccion 22, paso 6).
echo ============================================
pause
