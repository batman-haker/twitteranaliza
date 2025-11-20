# 🐦 Twitter Analyzer - Jak Uruchomić

## 🚀 Szybki Start

### Windows
1. Kliknij dwukrotnie: **`start.bat`**
2. Otwórz przeglądarkę: **http://localhost:3000**

### Linux / Mac
```bash
./start.sh
```
Lub:
```bash
bash start.sh
```

---

## 📋 Jak Używać Aplikacji

### 1. Uruchom aplikację
- Windows: `start.bat`
- Linux/Mac: `./start.sh`

### 2. Otwórz w przeglądarce
```
http://localhost:3000
```

### 3. Użyj interfejsu
1. **Wpisz nick** użytkownika z Twittera (np. `elonmusk`, `naval`, `stocktavia`)
2. **Ustaw slider** - ile tweetów chcesz pobrać (5-100)
3. **Zaznacz opcje:**
   - ☑️ **Analizuj linki** - Claude AI przeanalizuje artykuły (wolniejsze)
   - ☑️ **Zapisz do JSON** - zapisze wyniki do pliku
4. Kliknij **"Analizuj profil"**

### 4. Zobacz wyniki
- **Tweety wyświetlą się na stronie**
- Możesz kliknąć linki do tweetów
- Jeśli zaznaczyłeś "Zapisz do JSON", plik zostanie zapisany w `exports/`

---

## 📁 Struktura Plików

```
twitter-analyzer/
├── backend/           # FastAPI backend
├── frontend/          # Next.js frontend
├── exports/           # Zapisane JSON-y
│   └── batch/        # Batch exports (po 50 tweetów)
├── start.bat         # Uruchomienie na Windows
├── start.sh          # Uruchomienie na Linux/Mac
└── .env              # Klucze API
```

---

## ⚙️ Konfiguracja

### Wymagane API Keys w `.env`:
```env
# TwitterAPI.io (WYMAGANE)
TWITTERAPI_IO_KEY=twój_klucz_tutaj

# Claude API (opcjonalne - tylko do analizy linków)
CLAUDE_API_KEY=twój_klucz_tutaj
```

---

## 🔧 Zaawansowane Użycie

### Batch Fetch (masowe pobieranie)
Pobiera 50 tweetów z wielu kont jednocześnie:

```bash
cd backend
py batch_fetch.py
```

Edytuj listę kont w `batch_fetch.py`:
```python
accounts = [
    "elonmusk",
    "naval",
    "stocktavia",
    # ... więcej
]
```

### Ręczne uruchomienie

**Backend:**
```bash
cd backend
py -m uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🛑 Jak Zatrzymać

### Windows
- Zamknij oba okna terminala (Backend i Frontend)

### Linux/Mac
- Naciśnij `Ctrl+C` w terminalu

---

## 📊 Przykłady Użycia

### Pobierz 50 tweetów od Elona Muska
1. Wpisz: `elonmusk`
2. Ustaw slider: **50**
3. Zaznacz: ☑️ Zapisz do JSON
4. Kliknij: **Analizuj profil**

### Pobierz 100 tweetów z analizą linków
1. Wpisz: `naval`
2. Ustaw slider: **100**
3. Zaznacz: ☑️ Analizuj linki + ☑️ Zapisz do JSON
4. Kliknij: **Analizuj profil**
5. ⚠️ **UWAGA:** Analiza 100 tweetów z linkami może zająć kilka minut!

---

## ❓ Częste Problemy

### "Błąd połączenia z API"
- Sprawdź czy backend działa na porcie 8000
- Uruchom: `http://localhost:8000/api/health`

### "User not found"
- Sprawdź czy nick jest poprawny (bez @)
- Sprawdź czy konto istnieje na Twitter/X

### "Rate limit exceeded"
- API ma limit requestów
- Poczekaj kilka minut i spróbuj ponownie

### Frontend nie startuje
```bash
cd frontend
npm install
npm run dev
```

### Backend nie startuje
```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload --port 8000
```

---

## 📝 Notatki

- **Paginacja naprawiona** ✅ (4 listopada 2025)
- **Batch fetch działa** ✅ (32 konta pobrane)
- **Frontend gotowy** ✅ (Next.js 15 + TypeScript)
- **Backend gotowy** ✅ (FastAPI + TwitterAPI.io)

---

## 🔗 Porty

- **Backend (FastAPI):** http://localhost:8000
- **Frontend (Next.js):** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

---

**Data:** 2025-11-06
**Wersja:** 1.0
**Status:** ✅ Gotowe do użycia
