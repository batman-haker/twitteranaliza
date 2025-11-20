@echo off
echo ================================
echo   TWITTER ANALYZER - START
echo ================================
echo.

REM Sprawdz czy node_modules istnieje
if not exist "frontend\node_modules\" (
    echo [INFO] Instalowanie zaleznosci frontendu...
    cd frontend
    call npm install
    cd ..
)

REM Uruchom backend w nowym oknie
echo [1/2] Uruchamianie backendu (FastAPI)...
start "Backend - FastAPI" cmd /k "cd backend && py -m uvicorn main:app --reload --port 8000"
timeout /t 3 /nobreak > nul

REM Uruchom frontend w nowym oknie
echo [2/2] Uruchamianie frontendu (Next.js)...
start "Frontend - Next.js" cmd /k "cd frontend && npm run dev"

echo.
echo ================================
echo   APLIKACJA URUCHOMIONA!
echo ================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Otworz w przegladarce: http://localhost:3000
echo.
echo Aby zatrzymac aplikacje, zamknij oba okna terminala.
echo.
pause
