# 🚀 GitHub Setup - Szybka Instrukcja

## Krok 1: Zaloguj się do GitHub CLI

Otwórz **NOWY TERMINAL** i uruchom:

```bash
gh auth login
```

### Wybierz opcje:
1. **What account do you want to log into?**
   → `GitHub.com`

2. **What is your preferred protocol for Git operations?**
   → `HTTPS`

3. **Authenticate Git with your GitHub credentials?**
   → `Yes`

4. **How would you like to authenticate GitHub CLI?**
   → `Login with a web browser`

5. Skopiuj **8-cyfrowy kod** który się pojawi
6. Naciśnij Enter
7. Przeglądarka otworzy się automatycznie
8. Wklej kod i zatwierdź

---

## Krok 2: Wróć tutaj

Po zalogowaniu, wróć tutaj i powiedz **"gotowe"** lub **"zalogowany"**.

Wtedy automatycznie:
- Stworzę repozytorium `twitter-analyzer` na GitHubie
- Dodam remote origin
- Zrobię push

---

## Sprawdzenie czy jesteś zalogowany

Możesz sprawdzić w nowym terminalu:
```bash
gh auth status
```

Powinno pokazać:
```
✓ Logged in to github.com as batman-haker
```

---

## Co się stanie po zalogowaniu?

Komenda która zostanie uruchomiona:
```bash
gh repo create twitter-analyzer \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description="🐦 Full-stack Twitter/X analyzer"
```

To automatycznie:
1. Stworzy repo `batman-haker/twitter-analyzer` na GitHub
2. Doda remote `origin`
3. Wypushuje commit
4. Wyświetli link do repozytorium

---

**Gotowy? Uruchom `gh auth login` w nowym terminalu!** 🚀
