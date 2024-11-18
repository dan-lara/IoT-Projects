from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlite3 import Connection
from datetime import datetime

from models.database import Piece
from tools import get_db

router = APIRouter()

# Route pour créer une nouvelle pièce
@router.post("/", response_model=Piece, tags=["Piece"])
def create_piece(piece: Piece, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Piece (id_l, nom, loc_x, loc_y, loc_z, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    if piece.created_at is None:
        piece.created_at = datetime.now()
    cursor = db.execute(query, (piece.id_l, piece.nom, piece.loc_x, piece.loc_y, piece.loc_z, piece.created_at))
    db.commit()
    piece_id = cursor.lastrowid
    return {**piece, "id": piece_id, "created_at": created_at}

# Route pour obtenir toutes les pièces, avec des filtres optionnels par id_l ou nom
@router.get("/", response_model=List[Piece], tags=["Piece"])
def read_pieces(
    db: Connection = Depends(get_db),
    id_l: Optional[int] = Query(None, description="Filtrer par ID du logement"),
    nom: Optional[str] = Query(None, description="Filtrer par nom de la pièce")
):
    query = "SELECT * FROM Piece"
    params = []

    if id_l is not None:
        query += " WHERE id_l = ?"
        params.append(id_l)
    if nom:
        query += " AND nom LIKE ?" if id_l is not None else " WHERE nom LIKE ?"
        params.append(f"%{nom}%")

    cursor = db.execute(query, params)
    return [{"id": row["id"], "id_l": row["id_l"], "nom": row["nom"], 
             "loc_x": row["loc_x"], "loc_y": row["loc_y"], "loc_z": row["loc_z"],
             "created_at": row["created_at"]} for row in cursor.fetchall()]

# Route pour obtenir une pièce spécifique par ID
@router.get("/{id}", response_model=Piece, tags=["Piece"])
def read_piece(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Piece WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")
    return {"id": row["id"], "id_l": row["id_l"], "nom": row["nom"], 
            "loc_x": row["loc_x"], "loc_y": row["loc_y"], "loc_z": row["loc_z"],
            "created_at": row["created_at"]}

# Route pour mettre à jour une pièce spécifique par ID
@router.put("/{id}", response_model=Piece, tags=["Piece"])
def update_piece(id: int, piece: Piece, db: Connection = Depends(get_db)):
    query = """
    UPDATE Piece SET id_l = ?, nom = ?, loc_x = ?, loc_y = ?, loc_z = ?
    WHERE id = ?
    """
    db.execute(query, (piece.id_l, piece.nom, piece.loc_x, piece.loc_y, piece.loc_z, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Piece WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")
    return {"id": row["id"], "id_l": row["id_l"], "nom": row["nom"], 
            "loc_x": row["loc_x"], "loc_y": row["loc_y"], "loc_z": row["loc_z"],
            "created_at": row["created_at"]}

# Route pour supprimer une pièce spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Piece"])
def delete_piece(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Piece WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Pièce non trouvée")

    db.execute("DELETE FROM Piece WHERE id = ?", (id,))
    db.commit()
    return {"message": "Pièce supprimée avec succès",
            "deleted_piece": {"id": row["id"], "id_l": row["id_l"], "nom": row["nom"], 
                              "loc_x": row["loc_x"], "loc_y": row["loc_y"], "loc_z": row["loc_z"],
                              "created_at": row["created_at"]}}