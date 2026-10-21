@echo off
REM ============================================================
REM  Motor Inteligente de Segmentacion de Clientes - ARRANQUE
REM  Levanta el proyecto completo: simulador + API + frontend
REM  Uso: doble clic sobre este archivo (o ejecutarlo desde la
REM  raiz del proyecto). Cierra el proyecto cerrando las 3
REM  ventanas negras que se abren.
REM ============================================================
title Arranque del Motor de Segmentacion

REM Verificar que se ejecuta desde la raiz del proyecto
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: este script debe ejecutarse desde la RAIZ del proyecto.
    echo Carpeta esperada: la que contiene .venv\ y README.md
    echo Movete a esa carpeta y vuelve a lanzarlo.
    pause
    exit /b 1
)

if not exist "data\customers.json" (
    echo Generando dataset del CRM simulado - primera vez...
    call .venv\Scripts\python.exe -m crm_simulator.generate_data
)

echo [1/3] Levantando CRM simulado (puerto 8001)...
start "Simulador CRM (8001) - CIERRA ESTA VENTANA PARA DETENER" cmd /k ".venv\Scripts\python.exe -m uvicorn crm_simulator.app:app --port 8001"
timeout /t 3 /nobreak >nul

echo [2/3] Levantando API backend (puerto 8000, arranca en ~20 s)...
start "API Backend (8000) - CIERRA ESTA VENTANA PARA DETENER" cmd /k ".venv\Scripts\python.exe -m uvicorn src.api.app:app --port 8000 --log-level warning"
timeout /t 5 /nobreak >nul

echo [3/3] Levantando frontend web (puerto 5173)...
start "Frontend (5173) - CIERRA ESTA VENTANA PARA DETENER" cmd /k "cd frontend && npm run dev"

echo Esperando el primer arranque del backend (~25 s)...
timeout /t 25 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================
echo  TODO LISTO:
echo   - Aplicacion web : http://localhost:5173
echo   - API/Swagger    : http://127.0.0.1:8000/docs
echo  Para detener TODO: cierra las 3 ventanas
echo  negras que se abrieron.
echo ============================================
pause
