FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (includes spaCy models from GitHub)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Railway sets PORT dynamically
EXPOSE 8000

# Run the application (use PORT env var or default to 8000)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
