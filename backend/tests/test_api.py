from fastapi.testclient import TestClient

# FastAPI App importieren
from app.main import app

# Test-Client erstellen
client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json().get("status") == "Backend is running"


def test_chat_endpoint_monkeypatch(monkeypatch):
    # Service mocken, damit keine echten API-Calls gemacht werden
    def fake_generate_chat_response(history):
        assert isinstance(history, list)
        return "Hallo! Dies ist eine Testantwort."

    import app.services as services
    monkeypatch.setattr(services, "generate_chat_response", fake_generate_chat_response)

    payload = [
        {"isUser": True, "text": "Hallo"},
        {"isUser": False, "text": "Wie kann ich helfen?"},
    ]

    # Request abfeuern
    resp = client.post("/api/chat", json=payload)

    # Prüfen, ob alles passt
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert data["reply"] == "Hallo! Dies ist eine Testantwort."


def test_recognize_image_endpoint_monkeypatch(monkeypatch, tmp_path):
    # Bilderkennungs-Service mocken
    def fake_describe_image(prompt, image_bytes, mime_type):
        assert isinstance(image_bytes, (bytes, bytearray))
        assert mime_type in ("image/png", "image/jpeg")
        return f"Beschreibung für Prompt: {prompt[:10]}... (Test)"

    import app.services as services
    monkeypatch.setattr(services, "describe_image", fake_describe_image)

    # Kleines Dummy-PNG erstellen
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0bIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    files = {
        "image": ("test.png", png_bytes, "image/png"),
    }
    data = {
        "prompt": "Beschreibe das Bild",
    }

    # Request abschicken
    resp = client.post("/api/recognize-image", files=files, data=data)

    # Checken, ob's funktioniert hat
    assert resp.status_code == 200
    data = resp.json()
    assert "description" in data
    assert "(Test)" in data["description"]
