from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.partial import meteo, facture
from routers.front import capteur, index

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Ancien", "description": "Routes anciennes les factures et obtenir les données météorologiques"},
    {"name": "Frontend", "description": "Routes pour le frontend de l'application"}
]

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
    title="Logement Éco-Responsable Frontend",
    description="Application pour la gestion éco-responsable des logements",
    version="0.1.0",
    openapi_tags=tags_metadata
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(facture.router, tags=["Ancien"], prefix="/facture")
app.include_router(meteo.router, tags=["Ancien"], prefix="/meteo")

app.include_router(capteur.router, tags=["Capteur"], prefix="/capteur")
app.include_router(index.router, tags=["Frontend"], prefix="")