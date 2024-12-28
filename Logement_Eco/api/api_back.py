from fastapi import FastAPI
from .routers.bdd import ville, adresse, logement, piece, type_capteur, capteur, mesure, type_facture, facture
# from routers import autentication

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    # {"name": "Auth", "description": "Routes pour l'authentification et l'autorisation"},
    {"name": "Racine", "description": "Routes de base"},
    {"name": "Ville", "description": "Routes pour gérer les villes"},
    {"name": "Adresse", "description": "Routes pour gérer les adresses"},
    {"name": "Logement", "description": "Routes pour gérer les logements"},
    {"name": "Piece", "description": "Routes pour gérer les pièces des logements"},
    {"name": "Type_Capteur", "description": "Routes pour gérer les types de capteurs"},
    {"name": "Capteur", "description": "Routes pour gérer les capteurs"},
    {"name": "Mesure", "description": "Routes pour gérer les mesures des capteurs"},
    {"name": "Type_Facture", "description": "Routes pour gérer les types de factures"},
    {"name": "Facture", "description": "Routes pour gérer les factures"},
]

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
    title="Logement Éco-Responsable Backend",
    description="Application pour la gestion éco-responsable des logements",
    version="0.1.0",
    openapi_tags=tags_metadata
)

# Route principale pour tester l'api
@app.get("/", tags=["Racine"])
def health_check():
    return {"status": "OK"}

# Inclusion des routeurs avec des préfixes et des tags spécifiques
app.include_router(ville.router, tags=["Ville"], prefix="/ville")
app.include_router(adresse.router, tags=["Adresse"], prefix="/adresse")
app.include_router(logement.router, tags=["Logement"], prefix="/logement")
app.include_router(piece.router, tags=["Piece"], prefix="/piece")
app.include_router(type_capteur.router, tags=["Type_Capteur"], prefix="/type_capteur")
app.include_router(capteur.router, tags=["Capteur"], prefix="/capteur")
app.include_router(mesure.router, tags=["Mesure"], prefix="/mesure")
app.include_router(type_facture.router, tags=["Type_Facture"], prefix="/type_facture")
app.include_router(facture.router, tags=["Facture"], prefix="/facture")
# app.include_router(autentication.router, tags=["Auth"], prefix="/auth")
