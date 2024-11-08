from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Emprunt
from tools import get_db

router = APIRouter()

# Route pour créer un nouvel emprunt
@router.post("/", response_model=Emprunt, tags=["Emprunt"])
def create_emprunt(emprunt: Emprunt, db: Connection = Depends(get_db)):
    query = "INSERT INTO Emprunt (idEtu, idDoc, Date) VALUES (?, ?, ?)"
    cursor = db.execute(query, (emprunt.idEtu, emprunt.idDoc, emprunt.Date))
    db.commit()
    return emprunt

# Route pour obtenir tous les emprunts, avec des filtres optionnels par idEtu et idDoc
@router.get("/", response_model=List[Emprunt], tags=["Emprunt"])
def read_emprunts(
    db: Connection = Depends(get_db),
    idEtu: Optional[int] = Query(None, description="Filtrer par ID de l'étudiant"),
    idDoc: Optional[int] = Query(None, description="Filtrer par ID du document")
):
    query = "SELECT * FROM Emprunt"
    params = []

    # Appliquer les filtres si spécifiés
    if idEtu:
        query += " WHERE idEtu = ?"
        params.append(idEtu)
    if idDoc:
        query += " AND idDoc = ?" if idEtu else " WHERE idDoc = ?"
        params.append(idDoc)

    cursor = db.execute(query, params)
    return [{"idEtu": row["idEtu"], "idDoc": row["idDoc"], "Date": row["Date"]} for row in cursor.fetchall()]

# Route pour obtenir un emprunt spécifique par ID étudiant et ID document
@router.get("/{idEtu}/{idDoc}", response_model=Emprunt, tags=["Emprunt"])
def read_emprunt(idEtu: int, idDoc: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Emprunt WHERE idEtu = ? AND idDoc = ?", (idEtu, idDoc))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")
    return {"idEtu": row["idEtu"], "idDoc": row["idDoc"], "Date": row["Date"]}

# Route pour supprimer un emprunt spécifique par ID étudiant et ID document, retournant l'emprunt supprimé
@router.delete("/{idEtu}/{idDoc}", response_model=dict, tags=["Emprunt"])
def delete_emprunt(idEtu: int, idDoc: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Emprunt WHERE idEtu = ? AND idDoc = ?", (idEtu, idDoc))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")

    db.execute("DELETE FROM Emprunt WHERE idEtu = ? AND idDoc = ?", (idEtu, idDoc))
    db.commit()
    return {
        "message": "Emprunt supprimé avec succès",
        "deleted_emprunt": {"idEtu": row["idEtu"], "idDoc": row["idDoc"], "Date": row["Date"]}
    }
