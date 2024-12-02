from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import meteo, facture, capteur

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Facture", "description": "Routes pour gérer les factures"},
    {"name": "Meteo", "description": "Routes pour obtenir les données météorologiques"},
]

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
    title="Logement Éco-Responsable Frontend",
    description="Application pour la gestion éco-responsable des logements",
    version="0.1.0",
    openapi_tags=tags_metadata
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(facture.router, tags=["Facture"], prefix="/facture")
app.include_router(meteo.router, tags=["Meteo"], prefix="/meteo")
app.include_router(capteur.router, tags=["Capteur"], prefix="/capteur")