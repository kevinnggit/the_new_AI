# services.py: Kapselt die Logik für die Kommunikation mit dem Google Gemini API.

import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Lädt die Umgebungsvariablen aus der .env-Datei
# Hier wird der API-Schlüssel sicher geladen, ohne ihn im Code zu speichern.
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Konfiguriert das Generative AI SDK mit dem API-Schlüssel
genai.configure(api_key=API_KEY)

# Initialisiert das text- und bildfähige (multimodale) Modell
model = genai.GenerativeModel('gemini-1.5-flash')


def _ensure_api_key():
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY ist nicht gesetzt. Bitte in backend/.env eintragen oder als Umgebungsvariable setzen.")


def generate_chat_response(history):
    """
    Generiert eine Antwort im Chat basierend auf dem bisherigen Verlauf.
    Die `history` sorgt dafür, dass die KI Kontext hat.
    """
    _ensure_api_key()
    # Formatiert die Historie für die API
    messages = []
    for item in history:
        role = 'user' if item['isUser'] else 'model'
        messages.append({'role': role, 'parts': [item['text']]})

    # Sendet die Anfrage an die Gemini API
    response = model.generate_content(messages)
    return response.text


def describe_image(prompt, image_bytes, mime_type):
    """
    Analysiert ein Bild und gibt eine textuelle Beschreibung zurück.
    """
    _ensure_api_key()
    # Öffnet das Bild aus den Bytes, um es für die API vorzubereiten
    image_pil = Image.open(io.BytesIO(image_bytes))

    # Sendet das Bild und den Prompt an das multimodale Modell
    response = model.generate_content([prompt, image_pil])
    return response.text
