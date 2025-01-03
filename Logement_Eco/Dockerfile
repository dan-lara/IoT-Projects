FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /

# Copier les fichiers nécessaires
COPY ./requirements.txt ./
COPY ./.env ./
COPY ./api /api
COPY ./data /data
COPY ./front /front

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN cd data/ && python commands.py && python insert_users.py && cd ..

# Exposer le port pour FastAPI
EXPOSE 3000
EXPOSE 8000
EXPOSE 8001

# Commande par défaut pour exécuter l'application
CMD ["sh", "-c", "\
    uvicorn front.api:app --host 0.0.0.0 --port 3000 & \
    uvicorn api.api_back:app --host 0.0.0.0 --port 8000 & \
    uvicorn api.api_front:app --host 0.0.0.0 --port 8001 \
    "]
