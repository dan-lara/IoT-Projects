from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Etudiant
from tools import get_db

router = APIRouter()

# Route pour créer un nouvel étudiant
@router.post("/", response_model=Etudiant, tags=["Etudiant"])
def create_etudiant(etudiant: Etudiant, db: Connection = Depends(get_db)):
    query = "INSERT INTO Etudiant (Nom, Prenom, idAd) VALUES (?, ?, ?)"
    cursor = db.execute(query, (etudiant.Nom, etudiant.Prenom, etudiant.idAd))
    db.commit()
    etudiant_id = cursor.lastrowid
    return {**etudiant.dict(), "id": etudiant_id}

# Route pour obtenir tous les étudiants, avec des filtres optionnels pour Nom et Prenom
@router.get("/", response_model=List[Etudiant], tags=["Etudiant"])
def read_etudiants(
    db: Connection = Depends(get_db),
    nom: Optional[str] = Query(None, description="Filtrer par nom"),
    prenom: Optional[str] = Query(None, description="Filtrer par prénom")
):
    query = "SELECT * FROM Etudiant"
    params = []

    # Application des filtres si spécifiés
    if nom:
        query += " WHERE Nom = ?"
        params.append(nom)
    if prenom:
        query += " AND Prenom = ?" if nom else " WHERE Prenom = ?"
        params.append(prenom)

    cursor = db.execute(query, params)
    return [{"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]} for row in cursor.fetchall()]

# Route pour obtenir un étudiant spécifique par ID
@router.get("/{id}", response_model=Etudiant, tags=["Etudiant"])
def read_etudiant(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Etudiant WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Etudiant non trouvé")
    return {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]}

# Route pour mettre à jour un étudiant spécifique par ID
@router.put("/{id}", response_model=Etudiant, tags=["Etudiant"])
def update_etudiant(id: int, etudiant: Etudiant, db: Connection = Depends(get_db)):
    query = "UPDATE Etudiant SET Nom = ?, Prenom = ?, idAd = ? WHERE id = ?"
    db.execute(query, (etudiant.Nom, etudiant.Prenom, etudiant.idAd, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Etudiant WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Etudiant non trouvé")
    return {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]}

# Route pour supprimer un étudiant spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Etudiant"])
def delete_etudiant(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Etudiant WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Etudiant non trouvé")

    db.execute("DELETE FROM Etudiant WHERE id = ?", (id,))
    db.commit()
    return {"message": "Etudiant supprimé avec succès",
            "deleted_etudiant": {"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]}}