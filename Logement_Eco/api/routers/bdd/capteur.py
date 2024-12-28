from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection
from datetime import datetime
from ...models.database import Capteur
from ...tools import get_db

router = APIRouter()

# Route pour créer un nouveau capteur
@router.post("/", response_model=Capteur, tags=["Capteur"])
def create_capteur(capteur: Capteur, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Capteur (id_tc, id_p, ref_commerciale, precision_min, precision_max, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    if capteur.created_at is None:
        capteur.created_at = datetime.now()
    cursor = db.execute(
        query, 
        (capteur.id_tc, capteur.id_p, capteur.ref_commerciale, capteur.precision_min, 
         capteur.precision_max, capteur.created_at)
    )
    db.commit()
    capteur_id = cursor.lastrowid
    cursor.close()
    return {**capteur, "id": capteur_id}

# Route pour obtenir tous les capteurs, avec des filtres optionnels
@router.get("/", response_model=List[Capteur], tags=["Capteur"])
def read_capteurs(
    db: Connection = Depends(get_db),
    id_tc: Optional[int] = Query(None, description="Filtrer par ID du type de capteur"),
    id_p: Optional[int] = Query(None, description="Filtrer par ID de la pièce"),
):
    query = "SELECT * FROM Capteur"
    params = []
    filters = []

    if id_tc:
        filters.append("id_tc = ?")
        params.append(id_tc)
    if id_p:
        filters.append("id_p = ?")
        params.append(id_p)
    
    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor = db.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return [
        {
            "id": row["id"], "id_tc": row["id_tc"], "id_p": row["id_p"],
            "ref_commerciale": row["ref_commerciale"], 
            "precision_min": row["precision_min"], "precision_max": row["precision_max"],
            "actif": row["actif"], "created_at": row["created_at"]
        } for row in rows
    ]

# Route pour obtenir un capteur spécifique par ID
@router.get("/{id}", response_model=Capteur, tags=["Capteur"])
def read_capteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return {
        "id": row["id"], "id_tc": row["id_tc"], "id_p": row["id_p"],
        "ref_commerciale": row["ref_commerciale"], 
        "precision_min": row["precision_min"], "precision_max": row["precision_max"],
        "actif": row["actif"], "created_at": row["created_at"]
    }

# Route pour mettre à jour un capteur spécifique par ID
@router.put("/{id}", response_model=Capteur, tags=["Capteur"])
def update_capteur(id: int, capteur: Capteur, db: Connection = Depends(get_db)):
    query = """
    UPDATE Capteur 
    SET id_tc = ?, id_p = ?, ref_commerciale = ?, precision_min = ?, precision_max = ?, port_comm = ?, created_at = ?
    WHERE id = ?
    """
    db.execute(
        query, 
        (capteur.id_tc, capteur.id_p, capteur.ref_commerciale, capteur.precision_min, 
         capteur.precision_max, capteur.created_at, id)
    )
    db.commit()
    cursor = db.execute("SELECT * FROM Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return {
        "id": row["id"], "id_tc": row["id_tc"], "id_p": row["id_p"],
        "ref_commerciale": row["ref_commerciale"], 
        "precision_min": row["precision_min"], "precision_max": row["precision_max"],
        "actif": row["actif"], "created_at": row["created_at"]
    }

# Route pour supprimer un capteur spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Capteur"])
def delete_capteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")

    db.execute("DELETE FROM Capteur WHERE id = ?", (id,))
    db.commit()
    return {
        "message": "Capteur supprimé avec succès",
        "deleted_capteur": {
            "id": row["id"], "id_tc": row["id_tc"], "id_p": row["id_p"],
            "ref_commerciale": row["ref_commerciale"], 
            "precision_min": row["precision_min"], "precision_max": row["precision_max"],
            "actif": row["actif"], "created_at": row["created_at"]
        }
    }
