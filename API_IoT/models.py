from pydantic import BaseModel
from typing import Optional
# Modèles de données avec Pydantic

# Modèle pour la table Document
class Document(BaseModel):
    Titre: str
    id: Optional[int] = None  # Optionnel car l'ID est généré automatiquement

# Modèle pour la table Auteur
class Auteur(BaseModel):
    Nom: str
    Prenom: str
    id: Optional[int] = None  # Optionnel car l'ID est généré automatiquement

# Modèle pour la table Bibliotheque
class Bibliotheque(BaseModel):
    Nom: str
    Localisation: str
    id: Optional[int] = None  # Optionnel car l'ID est généré automatiquement

# Modèle pour la table Etudiant
class Etudiant(BaseModel):
    Nom: str
    Prenom: str
    idAd: int  # Référence vers l'ID de Adresse
    id: Optional[int] = None  # Optionnel car l'ID est généré automatiquement

# Modèle pour la table Adresse
class Adresse(BaseModel):
    Numero: int
    Voie: str
    Nom_voie: str
    Code: int  # Référence vers le Code de Ville
    id: Optional[int] = None  # Optionnel car l'ID est généré automatiquement

# Modèle pour la table Ville
class Ville(BaseModel):
    Code: int  # Code est la clé primaire
    Nom: str

# Modèle pour la table Emprunte (relation entre Etudiant et Document)
class Emprunt(BaseModel):
    idEtu: int  # Référence vers l'ID d'un étudiant
    idDoc: int  # Référence vers l'ID d'un document
    Date: str  # Date de l'emprunt

# Modèle pour la table Possede (relation entre Bibliotheque et Document)
class Possede(BaseModel):
    idBibli: int  # Référence vers l'ID d'une bibliothèque
    idDoc: int  # Référence vers l'ID d'un document
    Ref: str  # Référence unique pour le document dans la bibliothèque

# Modèle pour la table Redige (relation entre Auteur et Document)
class Redige(BaseModel):
    idAut: int  # Référence vers l'ID d'un auteur
    idDoc: int  # Référence vers l'ID d'un document
    Date: str  # Date de rédaction ou de publication
