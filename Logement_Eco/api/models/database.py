from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modèle pour la table Ville
class Ville(BaseModel):
    Code: int  # Code unique pour chaque ville
    Nom: str  # Nom de la ville

# Modèle pour la table Adresse
class Adresse(BaseModel):
    id: Optional[int] = None  # ID de l'adresse, généré automatiquement
    Numero: int  # Numéro de l'adresse
    Voie: str  # Nom de la rue
    Nom_voie: str  # Nom spécifique de la voie
    Code: int  # Code de la ville, correspondant à la table Ville

# Modèle pour la table Logement
class requestLogement(BaseModel):
    id_adresse: int  # Référence de l'adresse
    numero_telephone: Optional[str] = None  # Numéro de téléphone du logement
    adresse_ip: Optional[str] = None  # Adresse IP
class Logement(BaseModel):
    id: Optional[int] = None  # ID du logement, généré automatiquement
    id_adresse: int  # Référence de l'adresse
    numero_telephone: Optional[str] = None  # Numéro de téléphone du logement
    adresse_ip: Optional[str] = None  # Adresse IP
    created_at: Optional[datetime] = None  # Date de création

# Modèle pour la table Piece
class requestPiece(BaseModel):
    id_l: int  # Référence du logement
    nom: str  # Nom de la pièce
    loc_x: Optional[float] = None  # Position X dans la matrice 3D
    loc_y: Optional[float] = None  # Position Y dans la matrice 3D
    loc_z: Optional[float] = None  # Position Z dans la matrice 3D
class Piece(BaseModel):
    id: Optional[int] = None  # ID de la pièce, généré automatiquement
    id_l: int  # Référence du logement
    nom: str  # Nom de la pièce
    loc_x: Optional[float] = None  # Position X dans la matrice 3D
    loc_y: Optional[float] = None  # Position Y dans la matrice 3D
    loc_z: Optional[float] = None  # Position Z dans la matrice 3D
    created_at: Optional[datetime] = None  # Date de création

# Modèle pour la table Type_Capteur
class requestType_Capteur(BaseModel):
    nom: str  # Nom du type de capteur
    unite_mesure: Optional[str] = None  # Unité de mesure du capteur
    description: Optional[str] = None  # Description du type de capteur
class Type_Capteur(BaseModel):
    id: Optional[int] = None  # ID du type de capteur, généré automatiquement
    nom: str  # Nom du type de capteur
    unite_mesure: Optional[str] = None  # Unité de mesure du capteur
    description: Optional[str] = None  # Description du type de capteur

# Modèle pour la table Capteur
class requestCapteur(BaseModel):
    id_tc: int  # Référence du type de capteur
    id_p: int  # Référence de la pièce
    ref_commerciale: Optional[str] = None  # Référence commerciale du capteur
    precision_min: Optional[float] = None  # Précision minimale du capteur
    precision_max: Optional[float] = None  # Précision maximale du capteur
    actif: Optional[bool] = None  # Capteur actif ou non
class Capteur(BaseModel):
    id: Optional[int] = None  # ID du capteur, généré automatiquement
    id_tc: int  # Référence du type de capteur
    id_p: int  # Référence de la pièce
    ref_commerciale: Optional[str] = None  # Référence commerciale du capteur
    precision_min: Optional[float] = None  # Précision minimale du capteur
    precision_max: Optional[float] = None  # Précision maximale du capteur
    actif: Optional[bool] = None  # Capteur actif ou non
    created_at: Optional[datetime] = None  # Date de création

# Modèle pour la table Mesure
class requestMesure(BaseModel):
    id_c: int  # Référence du capteur
    valeur: float  # Valeur mesurée par le capteur
class Mesure(BaseModel):
    id: Optional[int] = None  # ID de la mesure, généré automatiquement
    id_c: int  # Référence du capteur
    valeur: float  # Valeur mesurée par le capteur
    created_at: Optional[datetime] = None  # Date de création
class MesureInsert(BaseModel):
    id: Optional[int] = None  # ID de la mesure, généré automatiquement
    id_c: int  # Référence du capteur
    valeur: float  # Valeur mesurée par le capteur
    status_capteur: Optional[bool] = None  # Statut du capteur
    created_at: Optional[datetime] = None  # Date de création

# Modèle pour la table Type_Facture
class Type_Facture(BaseModel):
    id: Optional[int] = None  # ID du type de facture, généré automatiquement
    nom: str  # Nom du type de facture
    description: Optional[str] = None  # Description du type de facture

# Modèle pour la table Facture
class requestFacture(BaseModel):
    id_l: int  # Référence du logement
    id_tc: int  # Référence du type de facture
    date_facture: datetime  # Date de la facture
    montant: Optional[float] = None  # Montant de la facture
    valeur_consommee: Optional[float] = None  # Valeur consommée
class Facture(BaseModel):
    id: Optional[int] = None  # ID de la facture, généré automatiquement
    id_l: int  # Référence du logement
    id_tc: int  # Référence du type de facture
    date_facture: datetime  # Date de la facture
    montant: Optional[float] = None  # Montant de la facture
    valeur_consommee: Optional[float] = None  # Valeur consommée
    created_at: Optional[datetime] = None  # Date de création

class requestGeneric(BaseModel):
    query: str  # Requête SQL
    params: Optional[list] = None  # Paramètres de la requête