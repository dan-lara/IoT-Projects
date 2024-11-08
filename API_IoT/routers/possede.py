from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlite3 import Connection

from models import Document, Bibliotheque
from tools import get_db

router = APIRouter()

# Fonction pour obtenir tous les documents dans une bibliothèque spécifique
@router.get("/{idBibli}", response_model=List[Document], tags=["Bibliotheque"])
def get_documents_in_bibliotheque(idBibli: int, db: Connection = Depends(get_db)) -> List[Document]:
    query = """
    SELECT Document.id, Document.Titre 
    FROM Document
    INNER JOIN Possede ON Document.id = Possede.idDoc
    WHERE Possede.idBibli = ?
    """
    cursor = db.execute(query, (idBibli,))
    documents = cursor.fetchall()
    if not documents:
        raise HTTPException(status_code=404, detail="Aucun document trouvé pour cette bibliothèque")
    
    return [{"id": doc["id"], "Titre": doc["Titre"]} for doc in documents]

# Fonction pour obtenir toutes les bibliothèques qui possèdent un document spécifique
@router.get("/{idDoc}", response_model=List[Bibliotheque], tags=["Document"])
def get_bibliotheques_with_document(idDoc: int, db: Connection = Depends(get_db)) -> List[Bibliotheque]:
    query = """
    SELECT Bibliotheque.id, Bibliotheque.Nom, Bibliotheque.Localisation
    FROM Bibliotheque
    INNER JOIN Possede ON Bibliotheque.id = Possede.idBibli
    WHERE Possede.idDoc = ?
    """
    cursor = db.execute(query, (idDoc,))
    bibliotheques = cursor.fetchall()
    if not bibliotheques:
        raise HTTPException(status_code=404, detail="Aucune bibliothèque trouvée pour ce document")
    
    return [{"id": bibli["id"], "Nom": bibli["Nom"], "Localisation": bibli["Localisation"]} for bibli in bibliotheques]
