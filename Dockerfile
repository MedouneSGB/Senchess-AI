# Utiliser une image Python officielle
FROM python:3.9-slim

# Installer les dépendances système pour OpenCV et autres
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY api/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'API
COPY api/ .

# Variables d'environnement
ENV HUGGINGFACE_REPO_ID=MedouneSGB/senchess-models
ENV MODEL_TYPE=ensemble
ENV USE_HUGGINGFACE=true
ENV PORT=8080

# Exposer le port
EXPOSE 8080

# Lancer l'application avec gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 index:app
