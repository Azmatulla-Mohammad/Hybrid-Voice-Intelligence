@echo off
setlocal

echo Starting EDITH AI...

set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"

if not exist "%BACKEND_DIR%\app\main.py" (
  echo [ERROR] Backend entrypoint not found at "%BACKEND_DIR%\app\main.py".
  exit /b 1
)

if not exist "%FRONTEND_DIR%\package.json" (
  echo [ERROR] Frontend package.json not found at "%FRONTEND_DIR%\package.json".
  exit /b 1
)

start "EDITH Backend" /D "%BACKEND_DIR%" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 5 >nul

start "EDITH Frontend" /D "%FRONTEND_DIR%" cmd /k "npm run dev"

echo EDITH Systems Online.
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
pause
