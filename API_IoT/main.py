from fastapi import FastAPI
from routers import etudiants
import sqlite3


def get_db():
    conn = sqlite3.connect('biblio.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

tags_metadata = [
    {"name": "Racine", "description": "Routes de base"},
    {"name": "Etudiant", "description": "Routes pour gérer les étudiants"},
    {"name": "Document", "description": "Routes pour gérer les documents"},
    {"name": "Auteur", "description": "Routes pour gérer les auteurs"},
    {"name": "Bibliotheque", "description": "Routes pour gérer les bibliothèques"},
    {"name": "Adresse", "description": "Routes pour gérer les adresses"},
    {"name": "Ville", "description": "Routes pour gérer les villes"},
]

app = FastAPI(
        title = "Biblio Gestion",
        description = "Gestion des étudiants et des livres",
        version = "0.1.0", 
        openapi_tags=tags_metadata
    )

app.include_router(etudiants.router,tags=["Etudiant"],prefix="/etudiant")

@app.get("/", tags=["Racine"])
def home():
    return {"Message": "Hello World"}

@app.get("/health", tags=["Racine"])
def health():
    return {"Message": "En bonne santé"}