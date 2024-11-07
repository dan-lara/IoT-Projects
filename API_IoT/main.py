from fastapi import FastAPI
from routers import etudiant

tags_metadata = [
    {"name": "Racine", "description": "Routes de base"},
    {"name": "Etudiant", "description": "Routes pour gérer les étudiants"},
    {"name": "Auteur", "description": "Routes pour gérer les auteurs"},
    {"name": "Document", "description": "Routes pour gérer les documents"},
    {"name": "Emprunt", "description": "Routes pour gérer les emprunts"},
    {"name": "Bibliotheque", "description": "Routes pour gérer les bibliothèques"},
    {"name": "Adresse", "description": "Routes pour gérer les adresses et les villes"},
]

app = FastAPI(
        title = "Biblio Gestion",
        description = "Gestion des étudiants et des livres",
        version = "0.1.0", 
        openapi_tags=tags_metadata
    )

app.include_router(etudiant.router,tags=["Etudiant"],prefix="/etudiant")

@app.get("/", tags=["Racine"])
def home():
    return {"Message": "Hello World"}

@app.get("/health", tags=["Racine"])
def health():
    return {"Message": "En bonne santé"}