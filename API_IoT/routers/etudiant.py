from fastapi import APIRouter, Depends
from typing import List
import sqlite3
from models import Etudiant

def get_db():
    conn = sqlite3.connect('biblio.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

router = APIRouter()

@router.post("/insere_etudiant", response_model=Etudiant)
def create_etudiant(etudiant: Etudiant, db: sqlite3.Connection = Depends(get_db)):
    query = "INSERT INTO Etudiant (Nom, Prenom, idAd) VALUES (?, ?, ?)"
    cursor = db.execute(query, (etudiant.Nom, etudiant.Prenom, etudiant.idAd))
    db.commit()
    etudiant_id = cursor.lastrowid
    return {**etudiant.dict(), "id": etudiant_id}

@router.get("/get_all", response_model=List[Etudiant])
def read_etudiants(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT * FROM Etudiant")
    return [{"id": row["id"], "Nom": row["Nom"], "Prenom": row["Prenom"], "idAd": row["idAd"]} for row in cursor.fetchall()]
