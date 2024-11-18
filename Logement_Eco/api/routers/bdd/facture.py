from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection
from datetime import datetime
from models.database import Facture
from tools import get_db

router = APIRouter()

# Route pour créer une nouvelle facture
@router.post("/", response_model=Facture, tags=["Facture"])
def create_facture(facture: Facture, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Facture (id_l, id_tc, date_facture, montant, valeur_consommee, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = db.execute(query, (
        facture.id_l,
        facture.id_tc,
        facture.date_facture,
        facture.montant,
        facture.valeur_consommee,
        facture.created_at or datetime.now()
    ))
    db.commit()
    facture_id = cursor.lastrowid
    return {**facture.dict(), "id": facture_id}

# Route pour obtenir toutes les factures, avec filtres optionnels
@router.get("/", response_model=List[Facture], tags=["Facture"])
def read_factures(
    db: Connection = Depends(get_db),
    id_l: Optional[int] = Query(None, description="Filtrer par logement"),
    id_tc: Optional[int] = Query(None, description="Filtrer par type de facture")
):
    query = "SELECT * FROM Facture"
    params = []
    if id_l:
        query += " WHERE id_l = ?"
        params.append(id_l)
    if id_tc:
        query += " AND id_tc = ?" if id_l else " WHERE id_tc = ?"
        params.append(id_tc)

    cursor = db.execute(query, params)
    return [
        {
            "id": row["id"],
            "id_l": row["id_l"],
            "id_tc": row["id_tc"],
            "date_facture": row["date_facture"],
            "montant": row["montant"],
            "valeur_consommee": row["valeur_consommee"],
            "created_at": row["created_at"]
        }
        for row in cursor.fetchall()
    ]

# Route pour obtenir une facture spécifique par ID
@router.get("/{id}", response_model=Facture, tags=["Facture"])
def read_facture(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    return {
        "id": row["id"],
        "id_l": row["id_l"],
        "id_tc": row["id_tc"],
        "date_facture": row["date_facture"],
        "montant": row["montant"],
        "valeur_consommee": row["valeur_consommee"],
        "created_at": row["created_at"]
    }

# Route pour mettre à jour une facture spécifique par ID
@router.put("/{id}", response_model=Facture, tags=["Facture"])
def update_facture(id: int, facture: Facture, db: Connection = Depends(get_db)):
    query = """
    UPDATE Facture
    SET id_l = ?, id_tc = ?, date_facture = ?, montant = ?, valeur_consommee = ?, created_at = ?
    WHERE id = ?
    """
    db.execute(query, (
        facture.id_l,
        facture.id_tc,
        facture.date_facture,
        facture.montant,
        facture.valeur_consommee,
        facture.created_at or datetime.now(),
        id
    ))
    db.commit()

    cursor = db.execute("SELECT * FROM Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    return {
        "id": row["id"],
        "id_l": row["id_l"],
        "id_tc": row["id_tc"],
        "date_facture": row["date_facture"],
        "montant": row["montant"],
        "valeur_consommee": row["valeur_consommee"],
        "created_at": row["created_at"]
    }

# Route pour supprimer une facture spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Facture"])
def delete_facture(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    db.execute("DELETE FROM Facture WHERE id = ?", (id,))
    db.commit()
    return {
        "message": "Facture supprimée avec succès",
        "deleted_facture": {
            "id": row["id"],
            "id_l": row["id_l"],
            "id_tc": row["id_tc"],
            "date_facture": row["date_facture"],
            "montant": row["montant"],
            "valeur_consommee": row["valeur_consommee"],
            "created_at": row["created_at"]
        }
    }
