@echo off
echo Starting EDITH AI...

start "EDITH Backend" /D "c:\Users\Azmat\OneDrive\Desktop\final projects\mark\backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to initialize...
timeout /t 5

start "EDITH Frontend" /D "c:\Users\Azmat\OneDrive\Desktop\final projects\mark\frontend" cmd /k "npm run dev"

echo EDITH Systems Online.
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
pause
