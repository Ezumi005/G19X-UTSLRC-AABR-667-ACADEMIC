@echo off
REM ============================================================
REM  Motor Inteligente de Segmentacion - cargar datos
REM  Ejecuta la ingesta (simulador -> PostgreSQL) y la
REM  segmentacion (K-Means + etiquetas).
REM  Requisito: el simulador debe estar corriendo (puerto 8001)
REM  (levantarlo con levantar_proyecto.bat, o cerrar esta ventana
REM   y no importa: este script avisa si no esta arriba).
REM ============================================================
title Cargar datos (ingesta + segmentacion)

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: ejecutalo desde la raiz del proyecto.
    pause
    exit /b 1
)

echo Conectividad del simulador (8001)...
curl -s -o nul http://127.0.0.1:8001/health
if errorlevel 1 (
    echo.
    echo AVISO: el simulador parece caido. Levanta primero levantar_proyecto.bat
    echo        o una terminal con: .venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001
    choice /c SN /m "Continuar de todas formas"
    if errorlevel 2 exit /b 1
)

if not exist "data\customers.json" (
    echo.
    echo Dataset del simulador no encontrado - generandolo, primera vez...
    call .venv\Scripts\python.exe -m crm_simulator.generate_data
    if errorlevel 1 (
        echo ERROR: no se pudo generar el dataset del simulador.
        pause
        exit /b 1
    )
)

echo.
echo [1/2] INGESTA (simulador - PostgreSQL)...
call .venv\Scripts\python.exe -m src.persistence.ingest
if errorlevel 1 (
    echo.
    echo ERROR: la ingesta fallo - NO se ejecuta la segmentacion.
    echo        Revisa que PostgreSQL este corriendo y el .env tenga DATABASE_URL correcta.
    pause
    exit /b 1
)

echo.
echo [2/2] SEGMENTACION (K-Means + etiquetas)...
call .venv\Scripts\python.exe -m src.ml.segmentation
if errorlevel 1 (
    echo.
    echo ERROR: la segmentacion fallo. Revisa el mensaje de arriba.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Datos cargados. Abre/actualiza http://localhost:5173
echo ============================================
pause
