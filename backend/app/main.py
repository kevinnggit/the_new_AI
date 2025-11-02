
# main.py - Hier sind alle API-Endpunkte definiert, die unser Backend anbietet.

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from . import services
import logging

# Hier erstellen wir unsere FastAPI-Anwendung
app = FastAPI(
    title="NSPACE AI API",
    description="Das Backend für meine kleine Chat- und Bilderkennungs-App",
    version="1.0.0"
)

# CORS einrichten, damit das Frontend mit dem Backend reden kann
# (Die laufen ja auf verschiedenen Ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für die Entwicklung erstmal alle Origins erlauben
    allow_credentials=False,  # Credentials gehen nicht mit Wildcard
    allow_methods=["*"],  # Alle Methoden erlauben (GET, POST, usw.)
    allow_headers=["*"],  # Alle Header durchlassen
)


@app.get("/")
def read_root():
    """Simpler Health-Check - damit man sehen kann, ob das Backend überhaupt läuft"""
    return {"status": "Backend is running"}


@app.get("/health/details")
def health_details():
    """Gibt ein paar Diagnosedaten zurück, aber ohne Secrets preiszugeben"""
    try:
        # Checken, ob der API-Key geladen wurde
        has_api_key = bool(getattr(services, "API_KEY", None))
        return {"ok": True, "has_api_key": has_api_key}
    except Exception as e:
        logging.exception("Fehler im /health/details Endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat_endpoint(history: List[Dict[str, Any]]):
    """
    Der Chat-Endpunkt - bekommt den bisherigen Verlauf und gibt die Antwort zurück.
    """
    try:
        # Service aufrufen, der mit der KI kommuniziert
        response_text = services.generate_chat_response(history)
        return {"reply": response_text}
    except Exception as e:
        # Bei Fehler den kompletten Stacktrace loggen, damit man weiß, was schiefging
        logging.exception("Fehler im /api/chat Endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recognize-image")
async def recognize_image_endpoint(
        prompt: str = Form("Was siehst du auf diesem Bild? Beschreibe es detailliert."),
        image: UploadFile = File(...)
):
    """
    Bilderkennung - bekommt ein Bild und einen Prompt, gibt Beschreibung zurück.
    """
    try:
        # Bild aus dem Upload auslesen
        image_bytes = await image.read()

        # Ab zur Bilderkennung in den Service
        description = services.describe_image(prompt, image_bytes, image.content_type)
        return {"description": description}
    except Exception as e:
        # Fehler loggen mit Stacktrace
        logging.exception("Fehler im /api/recognize-image Endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
