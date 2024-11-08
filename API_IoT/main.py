from fastapi import FastAPI
from routers import etudiant, auteur, document, emprunt, bibliotheque, adresse, possede, redige

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Racine", "description": "Routes de base"},
    {"name": "Etudiant", "description": "Routes pour gérer les étudiants"},
    {"name": "Auteur", "description": "Routes pour gérer les auteurs"},
    {"name": "Document", "description": "Routes pour gérer les documents"},
    {"name": "Emprunt", "description": "Routes pour gérer les emprunts"},
    {"name": "Bibliotheque", "description": "Routes pour gérer les bibliothèques"},
    {"name": "Adresse", "description": "Routes pour gérer les adresses et les villes"},
]

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
        title = "Biblio Gestion",
        description = "Gestion des étudiants et des livres",
        version = "0.1.0", 
        openapi_tags=tags_metadata
    )

# Inclusion des routeurs avec des préfixes et des tags spécifiques
app.include_router(etudiant.router, tags=["Etudiant"], prefix="/etudiant")
app.include_router(auteur.router, tags=["Auteur"], prefix="/auteur")
app.include_router(document.router, tags=["Document"], prefix="/document")
app.include_router(emprunt.router, tags=["Emprunt"], prefix="/emprunt")
app.include_router(bibliotheque.router, tags=["Bibliotheque"], prefix="/bibliotheque")
app.include_router(adresse.router, tags=["Adresse"], prefix="/adresse")
app.include_router(possede.router, prefix="/possede")
app.include_router(redige.router, prefix="/redige")

# Route de base pour la page d'accueil
@app.get("/", tags=["Racine"])
def home():
    return {"Message": "Hello World"}

# Route pour vérifier la santé de l'application
@app.get("/health", tags=["Racine"])
def health():
    return {"Message": "En bonne santé"}