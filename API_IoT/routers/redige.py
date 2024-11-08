from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlite3 import Connection

from models import Document, Auteur
from tools import get_db

router = APIRouter()

# Fonction pour obtenir tous les auteurs d'un document spécifique
@router.get("/{idDoc}", response_model=List[Auteur], tags=["Document"])
def get_authors_of_document(idDoc: int, db: Connection = Depends(get_db)) -> List[Auteur]:
    query = """
    SELECT Auteur.id, Auteur.Nom, Auteur.Prenom
    FROM Auteur
    INNER JOIN Redige ON Auteur.id = Redige.idAut
    WHERE Redige.idDoc = ?
    """
    cursor = db.execute(query, (idDoc,))
    authors = cursor.fetchall()
    if not authors:
        raise HTTPException(status_code=404, detail="Aucun auteur trouvé pour ce document")
    
    return [{"id": author["id"], "Nom": author["Nom"], "Prenom": author["Prenom"]} for author in authors]

# Fonction pour obtenir tous les documents rédigés par un auteur spécifique

@router.get("/{idAut}", response_model=List[Document], tags=["Auteur"])
def get_documents_by_author(idAut: int, db: Connection = Depends(get_db)) -> List[Document]:
    query = """
    SELECT Document.id, Document.Titre
    FROM Document
    INNER JOIN Redige ON Document.id = Redige.idDoc
    WHERE Redige.idAut = ?
    """
    cursor = db.execute(query, (idAut,))
    documents = cursor.fetchall()
    if not documents:
        raise HTTPException(status_code=404, detail="Aucun document trouvé pour cet auteur")
    
    return [{"id": doc["id"], "Titre": doc["Titre"]} for doc in documents]
