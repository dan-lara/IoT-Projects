from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Bibliotheque
from tools import get_db

router = APIRouter()

# Route pour créer une nouvelle bibliothèque
@router.post("/", response_model=Bibliotheque, tags=["Bibliotheque"])
def create_bibliotheque(bibliotheque: Bibliotheque, db: Connection = Depends(get_db)):
    query = "INSERT INTO Bibliotheque (Nom, Localisation) VALUES (?, ?)"
    cursor = db.execute(query, (bibliotheque.Nom, bibliotheque.Localisation))
    db.commit()
    bibliotheque_id = cursor.lastrowid
    return {**bibliotheque.dict(), "id": bibliotheque_id}

# Route pour obtenir toutes les bibliothèques, avec un filtre optionnel par nom
@router.get("/", response_model=List[Bibliotheque], tags=["Bibliotheque"])
def read_bibliotheques(
    db: Connection = Depends(get_db),
    Nom: Optional[str] = Query(None, description="Filtrer par nom de la bibliothèque")
):
    query = "SELECT * FROM Bibliotheque"
    params = []

    # Appliquer le filtre si spécifié
    if Nom:
        query += " WHERE Nom LIKE ?"
        params.append(f"%{Nom}%")

    cursor = db.execute(query, params)
    return [{"id": row["id"], "Nom": row["Nom"], "Localisation": row["Localisation"]} for row in cursor.fetchall()]

# Route pour obtenir une bibliothèque spécifique par ID
@router.get("/{id}", response_model=Bibliotheque, tags=["Bibliotheque"])
def read_bibliotheque(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Bibliotheque WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Bibliothèque non trouvée")
    return {"id": row["id"], "Nom": row["Nom"], "Localisation": row["Localisation"]}

# Route pour mettre à jour une bibliothèque par ID
@router.put("/{id}", response_model=Bibliotheque, tags=["Bibliotheque"])
def update_bibliotheque(id: int, bibliotheque: Bibliotheque, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Bibliotheque WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Bibliothèque non trouvée")

    query = "UPDATE Bibliotheque SET Nom = ?, Localisation = ? WHERE id = ?"
    db.execute(query, (bibliotheque.Nom, bibliotheque.Localisation, id))
    db.commit()
    return {**bibliotheque.dict(), "id": id}

# Route pour supprimer une bibliothèque par ID, retournant la bibliothèque supprimée
@router.delete("/{id}", response_model=dict, tags=["Bibliotheque"])
def delete_bibliotheque(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Bibliotheque WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Bibliothèque non trouvée")

    db.execute("DELETE FROM Bibliotheque WHERE id = ?", (id,))
    db.commit()
    return {
        "message": "Bibliothèque supprimée avec succès",
        "deleted_bibliotheque": {"id": row["id"], "Nom": row["Nom"], "Localisation": row["Localisation"]}
    }
