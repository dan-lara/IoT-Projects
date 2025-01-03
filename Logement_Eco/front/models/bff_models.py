from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Ville(BaseModel):
    Code: int
    Nom: str

class Adresse(BaseModel):
    id: int
    Numero: int
    Voie: str
    Nom_voie: str
    Code: int
    Ville: Ville
    ligne: Optional[str] = None   
        
class Mesure(BaseModel):
    id: int
    valeur: float
    created_at: datetime
   
class Capteur(BaseModel):
    id: int
    ref_commerciale: str
    type_capteur: str
    unite_mesure: str
    precision_min: float
    precision_max: float
    actif: bool
    created_at: datetime
    mesures: List[Mesure] = []

class Piece(BaseModel):
    id: int
    nom: str
    loc_x: Optional[float]
    loc_y: Optional[float]
    loc_z: Optional[float]
    created_at: datetime
    capteurs: List[Capteur] = []

class Logement(BaseModel):
    id: int
    numero_telephone: Optional[str] = None
    adresse_ip: Optional[str] = None
    created_at: datetime
    adresse: Adresse
    pieces: List[Piece] = []
    photo_url: Optional[str] = None
    
class Facture(BaseModel):
    id: int
    logement_id: int
    type_facture: str
    date_facture: datetime
    montant: float
    valeur_consommee: Optional[float]
    unite_consommation: Optional[str]
    created_at: datetime