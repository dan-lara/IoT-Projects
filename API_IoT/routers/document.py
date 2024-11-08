from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlite3 import Connection

from models import Document
from tools import get_db

router = APIRouter()

# Route pour créer un nouveau document
@router.post("/", response_model=Document, tags=["Document"])
def create_document(document: Document, db: Connection = Depends(get_db)):
    query = "INSERT INTO Document (Titre) VALUES (?)"
    cursor = db.execute(query, (document.Titre,))
    db.commit()
    document_id = cursor.lastrowid
    return {**document.dict(), "id": document_id}

# Route pour obtenir tous les documents, avec un filtre optionnel pour le Titre
@router.get("/", response_model=List[Document], tags=["Document"])
def read_documents(
    db: Connection = Depends(get_db),
    titre: Optional[str] = Query(None, description="Filtrer par titre")
):
    query = "SELECT * FROM Document"
    params = []

    # Appliquer le filtre si spécifié
    if titre:
        query += " WHERE Titre = ?"
        params.append(titre)

    cursor = db.execute(query, params)
    return [{"id": row["id"], "Titre": row["Titre"]} for row in cursor.fetchall()]

# Route pour obtenir un document spécifique par ID
@router.get("/{id}", response_model=Document, tags=["Document"])
def read_document(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Document WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return {"id": row["id"], "Titre": row["Titre"]}

# Route pour mettre à jour un document spécifique par ID
@router.put("/{id}", response_model=Document, tags=["Document"])
def update_document(id: int, document: Document, db: Connection = Depends(get_db)):
    query = "UPDATE Document SET Titre = ? WHERE id = ?"
    db.execute(query, (document.Titre, id))
    db.commit()

    cursor = db.execute("SELECT * FROM Document WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return {"id": row["id"], "Titre": row["Titre"]}

# Route pour supprimer un document spécifique par ID, retournant le document supprimé
@router.delete("/{id}", response_model=dict, tags=["Document"])
def delete_document(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Document WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    db.execute("DELETE FROM Document WHERE id = ?", (id,))
    db.commit()
    return {"message": "Document supprimé avec succès", "deleted_document": {"id": row["id"], "Titre": row["Titre"]}}
