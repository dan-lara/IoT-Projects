from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from .routers.bdd import ville, adresse, logement, piece, type_capteur, capteur, mesure, type_facture, facture, generic
from .routers import autentication

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Racine", "description": "Routes de base"},    
    {"name": "Auth", "description": "Routes pour l'authentification et l'autorisation"},
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
app.include_router(ville.router, tags=["Ville"], prefix="/ville")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(adresse.router, tags=["Adresse"], prefix="/adresse")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(logement.router, tags=["Logement"], prefix="/logement")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(piece.router, tags=["Piece"], prefix="/piece")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(type_capteur.router, tags=["Type_Capteur"], prefix="/type_capteur")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(capteur.router, tags=["Capteur"], prefix="/capteur")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(mesure.router, tags=["Mesure"], prefix="/mesure")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(type_facture.router, tags=["Type_Facture"], prefix="/type_facture")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(facture.router, tags=["Facture"], prefix="/facture")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(generic.router, tags=["Generic"], prefix="/generic")#, dependencies=[Depends(autentication.get_api_key)])
app.include_router(autentication.router, tags=["Auth"], prefix="/auth")
