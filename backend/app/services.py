
# services.py - Hier ist die ganze Logik für die Kommunikation mit der Gemini API.

import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Umgebungsvariablen laden - da liegt auch der API-Key, den ich nicht im Code haben will
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# SDK mit dem API-Key konfigurieren
genai.configure(api_key=API_KEY)

# Das Modell initialisieren - Flash ist gut für Text und Bilder
model = genai.GenerativeModel('gemini-1.5-flash')


def _ensure_api_key():
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY fehlt! Bitte in die backend/.env eintragen.")


def generate_chat_response(history):
    """
    Erzeugt eine Chat-Antwort basierend auf dem bisherigen Verlauf.
    Die History ist wichtig, damit die KI weiß, worüber wir vorher geredet haben.
    """
    _ensure_api_key()
    # Geschichte in das Format bringen, das die API versteht
    messages = []
    for item in history:
        role = 'user' if item['isUser'] else 'model'
        messages.append({'role': role, 'parts': [item['text']]})

    # Anfrage an Gemini schicken
    response = model.generate_content(messages)
    return response.text


def describe_image(prompt, image_bytes, mime_type):
    """
    Analysiert ein Bild und gibt zurück, was die KI darin sieht.
    """
    _ensure_api_key()
    # Bild aus den Bytes laden
    image_pil = Image.open(io.BytesIO(image_bytes))

    # Bild + Prompt an das Modell schicken
    response = model.generate_content([prompt, image_pil])
    return response.text
