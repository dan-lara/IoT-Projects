from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Auteur
from tools import get_db

router = APIRouter()

# Route pour créer un nouvel auteur
@router.post("/", response_model=Auteur, tags=["Auteur"])
def create_auteur(auteur: Auteur, db: Connection = Depends(get_db)):
    query = "INSERT INTO Auteur (Nom, Prenom) VALUES (?, ?)"
    cursor = db.execute(query, (auteur.Nom, auteur.Prenom))
    db.commit()
    auteur_id = cursor.lastrowid
    return {**auteur.dict(), "id": auteur_id}

# Route pour obtenir tous les auteurs, avec des filtres optionnels pour Nom et Prenom
@router.get("/", response_model=List[Auteur], tags=["Auteur"])
def read_auteurs(
    db: Connection = Depends(get_db),
    nom: Optional[str] = Query(None, description="Filtrer par nom"),
    prenom: Optional[str] = Query(None, description="Filtrer par prénom")
):
    query = "SELECT * FROM Auteur"
    params = []

    # Application des filtres si spécifiés
    if nom:
        query += " WHERE Nom = ?"
        params.append(nom)
    if prenom:
        query += " AND Prenom = ?" if nom else " WHERE Prenom = ?"
        params.append(prenom)

    cursor = db.execute(query, params)
    return [{"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"]} for row in cursor.fetchall()]

# Route pour obtenir un auteur spécifique par ID
@router.get("/{id}", response_model=Auteur, tags=["Auteur"])
def read_auteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Auteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    return {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"]}

# Route pour mettre à jour un auteur spécifique par ID
@router.put("/{id}", response_model=Auteur, tags=["Auteur"])
def update_auteur(id: int, auteur: Auteur, db: Connection = Depends(get_db)):
    query = "UPDATE Auteur SET Nom = ?, Prenom = ? WHERE id = ?"
    db.execute(query, (auteur.Nom, auteur.Prenom, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Auteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    return {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"]}

# Route pour supprimer un auteur spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Auteur"])
def delete_auteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Auteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    db.execute("DELETE FROM Auteur WHERE id = ?", (id,))
    db.commit()
    return {"message": "Auteur supprimé avec succès",
            "deleted_auteur": {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"]}}
