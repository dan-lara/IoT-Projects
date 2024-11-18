from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from sqlite3 import Connection

from models.database import Ville
from tools import get_db

router = APIRouter()
# Route pour créer une nouvelle ville
@router.post("/", response_model=Ville, tags=["Ville"])
def create_ville(ville: Ville, db: Connection = Depends(get_db)):
    query = "INSERT INTO Ville (Code, Nom) VALUES (?, ?)"
    try:
        db.execute(query, (ville.Code, ville.Nom))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création de la ville : {e}")
    return ville

#Route pour obtenir toutes les villes, avec un filtre optionnel par nom
@router.get("/", response_model=List[Ville], tags=["Ville"])
def read_villes(db: Connection = Depends(get_db), Nom: str = Query(None, description="Filtrer par nom de la ville")):
    query = "SELECT * FROM Ville"
    params = []

    # Appliquer le filtre si spécifié
    if Nom:
        query += " WHERE Nom LIKE ?"
        params.append(f"%{Nom}%")

    cursor = db.execute(query, params)
    return [
        {"Code": row["Code"], "Nom": row["Nom"]}
        for row in cursor.fetchall()
    ]

# Route pour obtenir une ville spécifique par Code
@router.get("/{code}", response_model=Ville, tags=["Ville"])
def read_ville(code: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Ville WHERE Code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Ville non trouvée")
    return {"Code": row["Code"], "Nom": row["Nom"]}

# Route pour mettre à jour une ville spécifique par Code
@router.put("/{code}", response_model=Ville, tags=["Ville"])
def update_ville(code: int, ville: Ville, db: Connection = Depends(get_db)):
    query = "UPDATE Ville SET Nom = ? WHERE Code = ?"
    db.execute(query, (ville.Nom, code))
    db.commit()

    cursor = db.execute("SELECT * FROM Ville WHERE Code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Ville non trouvée")
    return {"Code": row["Code"], "Nom": row["Nom"]}

# Route pour supprimer une ville spécifique par Code
@router.delete("/{code}", response_model=dict, tags=["Ville"])
def delete_ville(code: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Ville WHERE Code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Ville non trouvée")

    db.execute("DELETE FROM Ville WHERE Code = ?", (code,))
    db.commit()
    return {"message": "Ville supprimée avec succès", "deleted_ville": {"Code": row["Code"], "Nom": row["Nom"]}}