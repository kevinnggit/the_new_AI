# main.py: Definiert die API-Endpunkte unserer Anwendung.

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from . import services
import logging

# Initialisiert die FastAPI-Anwendung
app = FastAPI(
    title="KI-Anwendung API",
    description="Backend für die KI-gestützte Chat- und Bilderkennungs-App",
    version="1.0.0"
)

# Konfiguriert CORS (Cross-Origin Resource Sharing)
# Dies ist wichtig, damit unser Frontend (das auf einem anderen Port/einer anderen Domain läuft)
# mit dem Backend kommunizieren kann.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt Anfragen von allen Origins (für die Entwicklung)
    allow_credentials=False,  # Keine Credentials mit Wildcard-Origin
    allow_methods=["*"],  # Erlaubt alle HTTP-Methoden (GET, POST, etc.)
    allow_headers=["*"],  # Erlaubt alle Header
)


@app.get("/")
def read_root():
    """ Ein einfacher Endpunkt, um zu testen, ob das Backend läuft. """
    return {"status": "Backend is running"}


@app.get("/health/details")
def health_details():
    """ Liefert einfache Diagnoseinformationen ohne Geheimnisse preiszugeben. """
    try:
        # Prüfen, ob der API-Key im Service geladen ist
        has_api_key = bool(getattr(services, "API_KEY", None))
        return {"ok": True, "has_api_key": has_api_key}
    except Exception as e:
        logging.exception("Fehler im /health/details Endpoint: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat_endpoint(history: List[Dict[str, Any]]):
    """
    Endpunkt für die Chat-Funktion.
    Nimmt den bisherigen Gesprächsverlauf entgegen und gibt die KI-Antwort zurück.
    """
    try:
        # Ruft die Chat-Logik aus dem Service-Modul auf
        response_text = services.generate_chat_response(history)
        return {"reply": response_text}
    except Exception as e:
        # Loggt die vollständige Ausnahme inkl. Stacktrace, um die Ursache klar zu sehen
        logging.exception("Fehler im /api/chat Endpoint: %s", e)
        # Gibt eine Fehlermeldung zurück, falls etwas schiefgeht
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recognize-image")
async def recognize_image_endpoint(
        prompt: str = Form("Was siehst du auf diesem Bild? Beschreibe es detailliert."),
        image: UploadFile = File(...)
):
    """
    Endpunkt für die Bilderkennung.
    Nimmt ein Bild und einen Text-Prompt entgegen und gibt die Bildbeschreibung zurück.
    """
    try:
        # Liest die Bilddaten aus dem UploadFile
        image_bytes = await image.read()

        # Ruft die Bilderkennungs-Logik aus dem Service-Modul auf
        description = services.describe_image(prompt, image_bytes, image.content_type)
        return {"description": description}
    except Exception as e:
        # Loggt die vollständige Ausnahme inkl. Stacktrace
        logging.exception("Fehler im /api/recognize-image Endpoint: %s", e)
        # Gibt eine Fehlermeldung zurück, falls etwas schiefgeht
        raise HTTPException(status_code=500, detail=str(e))
