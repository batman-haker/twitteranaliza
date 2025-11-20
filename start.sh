#!/bin/bash

echo "================================"
echo "  TWITTER ANALYZER - START"
echo "================================"
echo ""

# Sprawdź czy node_modules istnieje
if [ ! -d "frontend/node_modules" ]; then
    echo "[INFO] Instalowanie zależności frontendu..."
    cd frontend
    npm install
    cd ..
fi

# Uruchom backend w tle
echo "[1/2] Uruchamianie backendu (FastAPI)..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Poczekaj 3 sekundy
sleep 3

# Uruchom frontend w tle
echo "[2/2] Uruchamianie frontendu (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "================================"
echo "  APLIKACJA URUCHOMIONA!"
echo "================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Otwórz w przeglądarce: http://localhost:3000"
echo ""
echo "Aby zatrzymać aplikację, naciśnij Ctrl+C"
echo ""

# Funkcja czyszczenia
cleanup() {
    echo ""
    echo "Zatrzymywanie aplikacji..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Przechwytuj Ctrl+C
trap cleanup SIGINT SIGTERM

# Czekaj w nieskończoność
wait
