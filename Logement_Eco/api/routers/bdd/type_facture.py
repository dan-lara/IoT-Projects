from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from ...models.database import Type_Facture
from ...tools import get_db

router = APIRouter()

# Route pour créer un nouveau type de facture
@router.post("/", response_model=Type_Facture, tags=["Type_Facture"])
def create_type_facture(type_facture: Type_Facture, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Type_Facture (nom, description)
    VALUES (?, ?)
    """
    cursor = db.execute(query, (type_facture.nom, type_facture.description))
    db.commit()
    type_facture_id = cursor.lastrowid
    cursor.close()
    return {**type_facture, "id": type_facture_id}

# Route pour obtenir tous les types de factures, avec des filtres optionnels
@router.get("/", response_model=List[Type_Facture], tags=["Type_Facture"])
def read_type_factures(
    db: Connection = Depends(get_db),
    nom: Optional[str] = Query(None, description="Filtrer par nom du type de facture"),
):
    query = "SELECT * FROM Type_Facture"
    params = []
    if nom:
        query += " WHERE nom = ?"
        params.append(nom)

    cursor = db.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return [
        {"id": row["id"], "nom": row["nom"], "description": row["description"]}
        for row in rows
    ]

# Route pour obtenir un type de facture spécifique par ID
@router.get("/{id}", response_model=Type_Facture, tags=["Type_Facture"])
def read_type_facture(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Type_Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de facture non trouvé")
    return {"id": row["id"], "nom": row["nom"], "description": row["description"]}

# Route pour mettre à jour un type de facture spécifique par ID
@router.put("/{id}", response_model=Type_Facture, tags=["Type_Facture"])
def update_type_facture(id: int, type_facture: Type_Facture, db: Connection = Depends(get_db)):
    query = """
    UPDATE Type_Facture
    SET nom = ?, description = ?
    WHERE id = ?
    """
    db.execute(query, (type_facture.nom, type_facture.description, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Type_Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de facture non trouvé")
    return {"id": row["id"], "nom": row["nom"], "description": row["description"]}

# Route pour supprimer un type de facture spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Type_Facture"])
def delete_type_facture(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Type_Facture WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de facture non trouvé")

    db.execute("DELETE FROM Type_Facture WHERE id = ?", (id,))
    db.commit()
    cursor.close()
    return {
        "message": "Type de facture supprimé avec succès",
        "deleted_type_facture": {"id": row["id"], "nom": row["nom"], "description": row["description"]}
    }
