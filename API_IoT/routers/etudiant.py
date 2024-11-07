from fastapi import APIRouter, Depends
from typing import List
from sqlite3 import Connection

from models import Etudiant
from tools import get_db

router = APIRouter()

@router.post("/insere_etudiant", response_model=Etudiant)
def create_etudiant(etudiant: Etudiant, db: Connection = Depends(get_db)):
    query = "INSERT INTO Etudiant (Nom, Prenom, idAd) VALUES (?, ?, ?)"
    cursor = db.execute(query, (etudiant.Nom, etudiant.Prenom, etudiant.idAd))
    db.commit()
    etudiant_id = cursor.lastrowid
    return {**etudiant.dict(), "id": etudiant_id}

@router.get("/get_all", response_model=List[Etudiant])
def read_etudiants(db: Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Etudiant")
    return [{"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]} for row in cursor.fetchall()]
