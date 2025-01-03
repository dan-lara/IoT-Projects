from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from ...models.database import Type_Capteur, requestType_Capteur
from ...tools import get_db

router = APIRouter()

# Route pour créer un nouveau type de capteur
@router.post("/", response_model=Type_Capteur, tags=["Type_Capteur"])
def create_type_capteur(type_capteur: requestType_Capteur, db: Connection = Depends(get_db)):
    query = """
    INSERT INTO Type_Capteur (nom, unite_mesure, description)
    VALUES (?, ?, ?)
    """
    cursor = db.execute(query, (type_capteur.nom, type_capteur.unite_mesure, type_capteur.description))
    db.commit()
    type_capteur_id = cursor.lastrowid
    cursor.close()
    return {**type_capteur, "id": type_capteur_id}

# Route pour obtenir tous les types de capteurs, avec un filtre optionnel par nom
@router.get("/", response_model=List[Type_Capteur], tags=["Type_Capteur"])
def read_types_capteurs(
    db: Connection = Depends(get_db),
    nom: Optional[str] = Query(None, description="Filtrer par nom du type de capteur")
):
    query = "SELECT * FROM Type_Capteur"
    params = []

    if nom:
        query += " WHERE nom LIKE ?"
        params.append(f"%{nom}%")

    cursor = db.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return [{"id": row["id"], "nom": row["nom"], "unite_mesure": row["unite_mesure"], 
             "description": row["description"]} for row in rows]

# Route pour obtenir un type de capteur spécifique par ID
@router.get("/{id}", response_model=Type_Capteur, tags=["Type_Capteur"])
def read_type_capteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Type_Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de capteur non trouvé")
    return {"id": row["id"], "nom": row["nom"], "unite_mesure": row["unite_mesure"], 
            "description": row["description"]}

# Route pour mettre à jour un type de capteur spécifique par ID
@router.put("/{id}", response_model=Type_Capteur, tags=["Type_Capteur"])
def update_type_capteur(id: int, type_capteur: requestType_Capteur, db: Connection = Depends(get_db)):
    query = """
    UPDATE Type_Capteur SET nom = ?, unite_mesure = ?, description = ?
    WHERE id = ?
    """
    db.execute(query, (type_capteur.nom, type_capteur.unite_mesure, type_capteur.description, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Type_Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de capteur non trouvé")
    return {"id": row["id"], "nom": row["nom"], "unite_mesure": row["unite_mesure"], 
            "description": row["description"]}

# Route pour supprimer un type de capteur spécifique par ID
@router.delete("/{id}", response_model=dict, tags=["Type_Capteur"])
def delete_type_capteur(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Type_Capteur WHERE id = ?", (id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Type de capteur non trouvé")

    db.execute("DELETE FROM Type_Capteur WHERE id = ?", (id,))
    db.commit()
    return {"message": "Type de capteur supprimé avec succès",
            "deleted_type_capteur": {"id": row["id"], "nom": row["nom"], 
                                     "unite_mesure": row["unite_mesure"], 
                                     "description": row["description"]}}
