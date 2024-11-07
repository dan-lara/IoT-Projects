from pydantic import BaseModel

# Modèles de données avec Pydantic

class Document(BaseModel):
    Titre: str

class Auteur(BaseModel):
    Nom: str
    Prenom: str

class Bibliotheque(BaseModel):
    Nom: str
    Localisation: str

class Etudiant(BaseModel):
    Nom: str
    Prenom: str
    idAd: int

class Adresse(BaseModel):
    Numero: int
    Voie: str
    Nom_voie: str
    Code: int

class Ville(BaseModel):
    Code: int
    Nom: str