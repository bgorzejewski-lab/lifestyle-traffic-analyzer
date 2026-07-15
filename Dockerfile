FROM python:3.12-slim

WORKDIR /app

# Instalacja zależności systemowych (jeśli potrzebne)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt-get/lists/*

# Kopiowanie listy zależności i instalacja
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pobranie polskiego modelu językowego spaCy
RUN python -m spacy download pl_core_news_sm

# Kopiowanie pozostałych plików projektu
COPY . .

# Ekspozycja portu Streamlit
EXPOSE 8501

# Konfiguracja uruchomieniowa (headless, na interfejsie 0.0.0.0)
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
