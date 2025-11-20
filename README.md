# 🐦 Twitter/X Analyzer

Aplikacja webowa do analizy profili Twitter/X. Pobiera ostatnie posty użytkownika i analizuje linki w treści.

## ✨ Funkcje

- ✅ **Pobieranie tweetów** - Do 100 ostatnich postów
- ✅ **Analiza linków** - Automatyczne wykrywanie URL w postach
- ✅ **AI Summary** - Claude API analizuje treść artykułów
- ✅ **Statystyki** - Likes, retweets, views, replies
- ✅ **User Info** - Followers, following, verification

## 🏗️ Architektura

```
twitter-analyzer/
├── backend/          # FastAPI + Python
│   ├── main.py              # API endpoints
│   ├── twitter_client.py    # TwitterAPI.io client
│   ├── link_analyzer.py     # Claude AI link analysis
│   └── requirements.txt
├── frontend/         # Next.js + React + TypeScript
│   ├── app/
│   │   ├── page.tsx         # Główna strona
│   │   ├── layout.tsx
│   │   └── globals.css
│   └── package.json
└── .env              # API keys
```

## 🚀 Szybki start

### 1. Backend (FastAPI)

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload --port 8000
```

Backend dostępny na: **http://localhost:8000**

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny na: **http://localhost:3000**

## 🔑 Konfiguracja API

Plik `.env` w głównym katalogu:

```env
# TwitterAPI.io
TWITTERAPI_IO_KEY=new1_fb3c3227406d409199569a59c755e13b
TWITTER_USER_ID=375958626547507200

# Claude API (opcjonalne - dla analizy linków)
CLAUDE_API_KEY=sk-ant-api03-...
```

## 📖 Jak używać

1. **Otwórz** http://localhost:3000
2. **Wpisz** username Twitter/X (np. `elonmusk`)
3. **Wybierz** liczbę tweetów (5-100)
4. **Zaznacz** czy analizować linki przez AI
5. **Kliknij** "Analizuj profil"

## 🎯 Przykłady użycia

### Test backend API (curl):

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"username":"elonmusk","max_tweets":10,"analyze_links":false}'
```

### Odpowiedź API:

```json
{
  "success": true,
  "username": "elonmusk",
  "user_info": {
    "name": "Elon Musk",
    "followers": 228660564,
    "following": 1224
  },
  "total_tweets": 10,
  "tweets": [
    {
      "id": "...",
      "text": "Tweet content...",
      "created_at": "2025-11-03...",
      "metrics": {
        "like_count": 45770,
        "retweet_count": 6272,
        "reply_count": 2075,
        "view_count": 4712530
      },
      "extracted_links": ["https://example.com/article"]
    }
  ]
}
```

## 🔧 Endpointy API

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Health check |
| `/api/health` | GET | Status API keys |
| `/api/analyze` | POST | Analizuj profil |
| `/api/test/{username}` | GET | Test user lookup |

## 📦 Technologie

### Backend:
- **FastAPI** - REST API framework
- **TwitterAPI.io** - Twitter data provider
- **Claude API** - AI content analysis
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client

### Frontend:
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management

## ⚡ Rate Limiting

- **TwitterAPI.io**: ~20 tweetów na request
- **Claude API**: Limit zależny od planu

## 🐛 Troubleshooting

### Backend nie startuje:
```bash
cd backend
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### Frontend błędy TypeScript:
```bash
cd frontend
rm -rf node_modules .next
npm install
```

### CORS errors:
Backend ma już skonfigurowane CORS dla `localhost:3000`

## 📝 To-Do / Przyszłe funkcje

- [ ] Export do JSON/CSV
- [ ] Filtrowanie tweetów po dacie
- [ ] Wyszukiwanie słów kluczowych
- [ ] Sentiment analysis (pozytywny/negatywny)
- [ ] Timeline visualization
- [ ] Database cache (PostgreSQL/MongoDB)
- [ ] Deploy na cloud (Vercel + Railway)

## 🤝 Wkład

Pull requests welcome! Dla większych zmian, otwórz issue najpierw.

## 📄 Licencja

MIT License - użyj jak chcesz!

---

**Autor:** Batman Haker 🦇
**Data:** Listopad 2025
**Wersja:** 1.0.0
