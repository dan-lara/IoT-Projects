from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Adresse
from tools import get_db

router = APIRouter()

# Route pour créer une nouvelle adresse
@router.post("/", response_model=Adresse, tags=["Adresse"])
def create_adresse(adresse: Adresse, db: Connection = Depends(get_db)):
    query = "INSERT INTO Adresse (Numero, Voie, Nom_voie, Code) VALUES (?, ?, ?, ?)"
    cursor = db.execute(query, (adresse.Numero, adresse.Voie, adresse.Nom_voie, adresse.Code))
    db.commit()
    adresse_id = cursor.lastrowid
    return {**adresse.dict(), "id": adresse_id}

# Route pour obtenir toutes les adresses, avec un filtre optionnel par nom de voie
@router.get("/", response_model=List[Adresse], tags=["Adresse"])
def read_adresses(
    db: Connection = Depends(get_db),
    Nom_voie: Optional[str] = Query(None, description="Filtrer par nom de la voie")
):
    query = "SELECT * FROM Adresse"
    params = []

    # Appliquer le filtre si spécifié
    if Nom_voie:
        query += " WHERE Nom_voie LIKE ?"
        params.append(f"%{Nom_voie}%")

    cursor = db.execute(query, params)
    return [
        {"id": row["id"], "Numero": row["Numero"], "Voie": row["Voie"], "Nom_voie": row["Nom_voie"], "Code": row["Code"]}
        for row in cursor.fetchall()
    ]

# Route pour obtenir une adresse spécifique par ID
@router.get("/{id}", response_model=Adresse, tags=["Adresse"])
def read_adresse(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Adresse WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")
    return {"id": row["id"], "Numero": row["Numero"], "Voie": row["Voie"], "Nom_voie": row["Nom_voie"], "Code": row["Code"]}

# Route pour mettre à jour une adresse par ID
@router.put("/{id}", response_model=Adresse, tags=["Adresse"])
def update_adresse(id: int, adresse: Adresse, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Adresse WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")

    query = "UPDATE Adresse SET Numero = ?, Voie = ?, Nom_voie = ?, Code = ? WHERE id = ?"
    db.execute(query, (adresse.Numero, adresse.Voie, adresse.Nom_voie, adresse.Code, id))
    db.commit()
    return {**adresse.dict(), "id": id}

# Route pour supprimer une adresse par ID, retournant l'adresse supprimée
@router.delete("/{id}", response_model=dict, tags=["Adresse"])
def delete_adresse(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Adresse WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")

    db.execute("DELETE FROM Adresse WHERE id = ?", (id,))
    db.commit()
    return {
        "message": "Adresse supprimée avec succès",
        "deleted_adresse": {
            "id": row["id"],
            "Numero": row["Numero"],
            "Voie": row["Voie"],
            "Nom_voie": row["Nom_voie"],
            "Code": row["Code"]
        }
    }
