from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection
from datetime import datetime

from models.database import Logement
from tools import get_db

router = APIRouter()

# Route pour créer un nouveau logement
@router.post("/", response_model=Logement, tags=["Logement"])
def create_logement(logement: Logement, db: Connection = Depends(get_db)):
    query = "INSERT INTO Logement (id_adresse, numero_telephone, adresse_ip, created_at) VALUES (?, ?, ?, ?)"
    if logement.created_at is None:
        logement.created_at = datetime.now()
    cursor = db.execute(query, (logement.id_adresse, logement.numero_telephone, logement.adresse_ip, logement.created_at))
    db.commit()
    logement_id = cursor.lastrowid
    return {**logement, "id": logement_id}

# Route pour obtenir tous les logements, avec des filtres optionnels
@router.get("/", response_model=List[Logement], tags=["Logement"])
def read_logements(
    db: Connection = Depends(get_db),
    id_adresse: Optional[int] = Query(None, description="Filtrer par ID d'adresse"),
    numero_telephone: Optional[str] = Query(None, description="Filtrer par numéro de téléphone")
):
    query = "SELECT * FROM Logement"
    params = []

    # Application des filtres si spécifiés
    if id_adresse:
        query += " WHERE id_adresse = ?"
        params.append(id_adresse)
    if numero_telephone:
        query += " AND numero_telephone = ?" if id_adresse else " WHERE numero_telephone = ?"
        params.append(numero_telephone)

    cursor = db.execute(query, params)
    return [{"id": row["id"], "id_adresse": row["id_adresse"], "numero_telephone": row["numero_telephone"],
             "adresse_ip": row["adresse_ip"], "created_at": row["created_at"]} for row in cursor.fetchall()]

# Route pour obtenir un logement spécifique par ID
@router.get("/{id}", response_model=Logement, tags=["Logement"])
def read_logement(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Logement WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    return {"id": row["id"], "id_adresse": row["id_adresse"], "numero_telephone": row["numero_telephone"],
            "adresse_ip": row["adresse_ip"], "created_at": row["created_at"]}

# Route pour mettre à jour un logement spécifique par ID
@router.put("/{id}", response_model=Logement, tags=["Logement"])
def update_logement(id: int, logement: Logement, db: Connection = Depends(get_db)):
    query = "UPDATE Logement SET id_adresse = ?, numero_telephone = ?, adresse_ip = ?, created_at = ? WHERE id = ?"
    db.execute(query, (logement.id_adresse, logement.numero_telephone, logement.adresse_ip, logement.created_at, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Logement WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Logement non trouvé")
    return {"id": row["id"], "id_adresse": row["id_adresse"], "numero_telephone": row["numero_telephone"],
            "adresse_ip": row["adresse_ip"], "created_at": row["created_at"]}

# Route pour supprimer un logement spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Logement"])
def delete_logement(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Logement WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Logement non trouvé")

    db.execute("DELETE FROM Logement WHERE id = ?", (id,))
    db.commit()
    return {"message": "Logement supprimé avec succès",
            "deleted_logement": {"id": row["id"], "id_adresse": row["id_adresse"], "numero_telephone": row["numero_telephone"],
                                 "adresse_ip": row["adresse_ip"], "created_at": row["created_at"]}}
