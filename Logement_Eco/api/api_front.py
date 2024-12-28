import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import meteo, facture

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Ancien", "description": "Routes anciennes les factures et obtenir les données météorologiques"},
]

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
    title="Ancien Frontend",
    description="Application pour la frontend initial",
    version="0.1.0",
    openapi_tags=tags_metadata
)

folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static/"))
app.mount("/static", StaticFiles(directory=folder_path), name="static")

app.include_router(facture.router, tags=["Facture"], prefix="/facture")
app.include_router(meteo.router, tags=["Meteo"], prefix="/meteo")