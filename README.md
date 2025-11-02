

# NSPACE AI - Mein persönliches KI-Projekt

Hey! Schön, dass du hier bist. 

Das ist mein kleines Side-Project, an dem ich in meiner Freizeit arbeite. Die Idee war, mal was mit der Gemini API von Google zu bauen – einfach um zu sehen, was damit so möglich ist. Herausgekommen ist eine Web-App, mit der man chatten oder Bilder analysieren lassen kann.

## Was kann die App?

Eigentlich zwei Dinge:

1. **Chat**: Du kannst mit der KI plaudern, Fragen stellen, diskutieren – was dir gerade einfällt
2. **Bilderkennung**: Lade ein Bild hoch und lass die KI beschreiben, was sie sieht

## Technischer Aufbau

Das Backend läuft mit **FastAPI** (Python) und kommuniziert mit der Google Gemini API. Das Frontend ist in **Vue.js** geschrieben und sieht hoffentlich ganz ansprechend aus.

Alles läuft in Docker-Containern, damit man es überall starten kann, ohne groß was installieren zu müssen.

### Was du brauchst

- Docker und Docker Compose auf deinem Rechner
- Einen Google Gemini API-Key (gibt's kostenlos bei Google)

### So läuft's

1. Projekt klonen:
   ```bash
   git clone https://github.com/kevinnggit/the_new_AI.git
   cd the_new_AI
   ```

2. Im Backend-Ordner eine `.env` Datei erstellen und deinen API-Key reinschreiben:
   ```
   GOOGLE_API_KEY=dein-api-key-hier
   ```

3. Container starten:
   ```bash
   docker-compose up --build
   ```

4. Browser öffnen und zu `http://localhost:5173` gehen – schon läuft's!

Das Backend ist dann unter `http://localhost:8000` erreichbar.

## Projektstruktur

```
.
├── backend/          # FastAPI Backend
│   ├── app/         # Hauptcode
│   ├── tests/       # Tests
│   └── Dockerfile
├── frontend/         # Vue.js Frontend
│   ├── src/
│   └── Dockerfile
└── docker-compose.yml
```

## Tests laufen lassen

Falls du das Backend testen willst:

```bash
cd backend
pip install -r requirements.txt
pip install pytest
pytest
```

## Was ich noch vorhabe

Auf meiner mentalen To-Do-Liste steht noch einiges – ist halt ein Work in Progress. Schau mal in die `mangel.txt`, da hab ich aufgeschrieben, was mir noch fehlt und was ich noch verbessern will.

## Lizenz

Ist frei nutzbar für alle, die Lust haben, damit rumzuspielen oder es weiterzuentwickeln.

---

Falls du Fragen hast oder Verbesserungsvorschläge – immer her damit!
