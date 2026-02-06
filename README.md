# PII Anonymizer

Automatische Anonymisierung personenbezogener Daten (PII) aus Texten mit Microsoft Presidio.

## Features

- **Automatische PII-Erkennung**: Erkennt Namen, E-Mails, Telefonnummern, Adressen, Daten, IBANs und mehr
- **Mehrsprachig**: Unterstützt Deutsch und Englisch
- **Einfache UI**: Split-View Interface zum einfachen Vergleich
- **Copy-to-Clipboard**: Schnelles Kopieren der anonymisierten Texte
- **Docker-ready**: Einfaches Deployment auf Railway oder anderen Plattformen

## Erkannte Entity-Typen

- **PERSON**: Namen von Personen
- **EMAIL_ADDRESS**: E-Mail-Adressen
- **PHONE_NUMBER**: Telefonnummern
- **LOCATION**: Adressen, Städte, Länder
- **DATE_TIME**: Datums- und Zeitangaben
- **IBAN_CODE**: Bankverbindungen
- **CREDIT_CARD**: Kreditkartennummern
- **IP_ADDRESS**: IP-Adressen
- **URL**: Web-Adressen

## Technologie-Stack

- **Backend**: FastAPI (Python)
- **PII Detection**: Microsoft Presidio
- **NLP**: spaCy (de_core_news_lg, en_core_web_lg)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Deployment**: Docker

## Lokale Entwicklung

### Voraussetzungen

- Python 3.11+
- Docker (optional)

### Installation

1. Repository klonen oder Dateien kopieren

2. Virtuelle Umgebung erstellen (optional, aber empfohlen):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Dependencies installieren:
```bash
pip install -r requirements.txt
```

4. spaCy Modelle herunterladen:
```bash
python -m spacy download de_core_news_lg
python -m spacy download en_core_web_lg
```

5. App starten:
```bash
uvicorn app.main:app --reload
```

6. Browser öffnen: [http://localhost:8000](http://localhost:8000)

## Docker Deployment

### Lokal mit Docker

1. Image bauen:
```bash
docker build -t pii-anonymizer .
```

2. Container starten:
```bash
docker run -p 8000:8000 pii-anonymizer
```

3. Browser öffnen: [http://localhost:8000](http://localhost:8000)

### Deployment auf Railway

1. GitHub Repository erstellen und Code pushen

2. Auf [Railway](https://railway.app) anmelden

3. Neues Projekt erstellen:
   - "Deploy from GitHub repo" wählen
   - Repository auswählen
   - Railway erkennt automatisch das Dockerfile

4. Deploy abwarten (ca. 5-10 Minuten beim ersten Mal wegen spaCy Models)

5. App über die generierte Railway-URL nutzen

**Hinweis**: Der erste Build kann länger dauern, da die spaCy Modelle (ca. 500 MB) heruntergeladen werden.

## API Endpoints

### GET /
Zeigt die Web-UI an.

### POST /anonymize
Anonymisiert den übergebenen Text.

**Request Body**:
```json
{
  "text": "Max Mustermann wohnt in Berlin. Seine Email ist max@example.com",
  "language": "de"
}
```

**Response**:
```json
{
  "original": "Max Mustermann wohnt in Berlin. Seine Email ist max@example.com",
  "anonymized": "[PERSON] wohnt in [LOCATION]. Seine Email ist [EMAIL_ADDRESS]",
  "entities": [
    {
      "type": "PERSON",
      "text": "Max Mustermann",
      "start": 0,
      "end": 14,
      "score": 0.85
    },
    ...
  ]
}
```

### GET /health
Health check endpoint für Monitoring.

## Beispiele

### Deutscher Text
**Input**:
```
Max Mustermann wohnt in Berlin, Hauptstraße 123.
Seine Email ist max@example.com und seine Telefonnummer ist +49 123 456789.
Geburtsdatum: 15.03.1985
```

**Output**:
```
[PERSON] wohnt in [LOCATION], [LOCATION].
Seine Email ist [EMAIL_ADDRESS] und seine Telefonnummer ist [PHONE_NUMBER].
Geburtsdatum: [DATE_TIME]
```

### English Text
**Input**:
```
John Doe lives in New York, 123 Main Street.
Call him at +1-555-0123 or email john@example.com
```

**Output**:
```
[PERSON] lives in [LOCATION], [LOCATION].
Call him at [PHONE_NUMBER] or email [EMAIL_ADDRESS]
```

## Tastenkürzel

- **Strg/Cmd + Enter**: Text anonymisieren
- **Strg/Cmd + C** (im Output-Feld): Text kopieren

## Sicherheitshinweise

- Die App verarbeitet Daten **lokal** - keine Daten werden extern gespeichert
- Für Produktivumgebungen empfohlen:
  - HTTPS aktivieren
  - Rate Limiting implementieren
  - Authentifizierung hinzufügen
  - Logging von sensiblen Daten vermeiden

## Lizenz

MIT License - Siehe LICENSE Datei

## Credits

Powered by [Microsoft Presidio](https://github.com/microsoft/presidio)
