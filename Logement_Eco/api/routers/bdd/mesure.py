from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection
from datetime import datetime

from ...models.database import Mesure, requestMesure
from ...tools import get_db

router = APIRouter()

# Route pour créer une nouvelle mesure
@router.post("/", response_model=Mesure, tags=["Mesure"])
def create_mesure(mesure: requestMesure, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Mesure (id_c, valeur, created_at)
    VALUES (?, ?, ?)
    """
    # if mesure.created_at is None:
    #     mesure.created_at = datetime.now()
    mesure = Mesure(id_c=mesure.id_c, valeur=mesure.valeur)
    mesure.created_at = datetime.now().isoformat() + "Z"
    cursor = db.execute(query, (mesure.id_c, mesure.valeur, mesure.created_at))
    db.commit()
    mesure_id = cursor.lastrowid
    cursor.close()
    return {**mesure.__dict__, "id": mesure_id}

# Route pour obtenir toutes les mesures, avec des filtres optionnels
@router.get("/", response_model=List[Mesure], tags=["Mesure"])
def read_mesures(
    db: Connection = Depends(get_db),
    id_c: Optional[int] = Query(None, description="Filtrer par ID du capteur"),
):
    query = "SELECT * FROM Mesure"
    params = []
    if id_c:
        query += " WHERE id_c = ?"
        params.append(id_c)

    cursor = db.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return [
        {
            "id": row["id"], "id_c": row["id_c"], 
            "valeur": row["valeur"], "created_at": row["created_at"]
        } for row in rows
    ]

# Route pour obtenir une mesure spécifique par ID
@router.get("/{id}", response_model=Mesure, tags=["Mesure"])
def read_mesure(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Mesure WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Mesure non trouvée")
    return {
        "id": row["id"], "id_c": row["id_c"], 
        "valeur": row["valeur"], "created_at": row["created_at"]
    }

# Route pour mettre à jour une mesure spécifique par ID
@router.put("/{id}", response_model=Mesure, tags=["Mesure"])
def update_mesure(id: int, mesure: Mesure, db: Connection = Depends(get_db)):
    query = """
    UPDATE Mesure 
    SET id_c = ?, valeur = ?, created_at = ?
    WHERE id = ?
    """
    db.execute(query, (mesure.id_c, mesure.valeur, mesure.created_at, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Mesure WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Mesure non trouvée")
    return {
        "id": row["id"], "id_c": row["id_c"], 
        "valeur": row["valeur"], "created_at": row["created_at"]
    }

# Route pour supprimer une mesure spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Mesure"])
def delete_mesure(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Mesure WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Mesure non trouvée")

    db.execute("DELETE FROM Mesure WHERE id = ?", (id,))
    db.commit()
    return {
        "message": "Mesure supprimée avec succès",
        "deleted_mesure": {
            "id": row["id"], "id_c": row["id_c"], 
            "valeur": row["valeur"], "created_at": row["created_at"]
        }
    }
