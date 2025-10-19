# Stage 1: Offizielles Python-Image als Basis
FROM python:3.11-slim

# Setzt das Arbeitsverzeichnis im Container
WORKDIR /code

# Umgebungsvariablen für Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Kopiert die Abhängigkeiten und installiert sie
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Kopiert den gesamten Anwendungs-Code in das Arbeitsverzeichnis
COPY ./app /code/app

# Startet den Server, wenn der Container läuft
# Der Server ist auf 0.0.0.0 verfügbar, um von außerhalb des Containers erreichbar zu sein
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
