import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from .tools import BACKEND_BASE_URL, fetch_data
from ..models.bff_models import Ville, Adresse, Mesure, Capteur, Piece, Logement, Facture

router = APIRouter()

@router.get("/logement_data/{logement_id}", response_model=Logement)
def get_logement_details(logement_id: int):
    """
    Obtém todos os detalhes de um logement a partir do logement_id.
    """
    query = """
    SELECT 
        logement.id AS logement_id,
        logement.numero_telephone,
        logement.adresse_ip,
        logement.created_at AS logement_created_at,
        adresse.id AS adresse_id,
        adresse.Numero AS adresse_numero,
        adresse.Voie AS adresse_voie,
        adresse.Nom_voie AS adresse_nom_voie,
        adresse.Code AS adresse_code,
        ville.Code AS ville_code,
        ville.Nom AS ville_nom,
        piece.id AS piece_id,
        piece.nom AS piece_nom,
        piece.loc_x,
        piece.loc_y,
        piece.loc_z,
        piece.created_at AS piece_created_at,
        capteur.id AS capteur_id,
        capteur.ref_commerciale,
        capteur.precision_min,
        capteur.precision_max,
        capteur.actif,
        capteur.created_at AS capteur_created_at,
        type_capteur.nom AS type_capteur_nom,
        type_capteur.unite_mesure AS type_capteur_unite_mesure,
        mesure.id AS mesure_id,
        mesure.valeur AS mesure_valeur,
        mesure.created_at AS mesure_created_at
    FROM logement
    INNER JOIN adresse ON logement.id_adresse = adresse.id
    INNER JOIN ville ON adresse.Code = ville.Code
    LEFT JOIN piece ON logement.id = piece.id_l
    LEFT JOIN capteur ON piece.id = capteur.id_p
    LEFT JOIN type_capteur ON capteur.id_tc = type_capteur.id
    LEFT JOIN mesure ON capteur.id = mesure.id_c
    WHERE logement.id = ?
    """
    try:
        response = requests.post(
            f"{BACKEND_BASE_URL}/generic",
            json={"query": query, "params": [logement_id]},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro ao consultar dados do backend: {response.text}",
            )
        raw_data = response.json().get("data", [])
        if not raw_data:
            raise HTTPException(status_code=404, detail="Logement não encontrado")

        logement_data = build_logement_from_raw_data(raw_data)
        return logement_data
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro de comunicação com o backend: {str(e)}",
        )

def build_logement_from_raw_data(raw_data: List[dict]) -> Logement:
    """
    Constrói o objeto Logement a partir dos dados brutos retornados pela query.
    """
    logement_info = raw_data[0]

    adresse = Adresse(
        id=logement_info["adresse_id"],
        Numero=logement_info["adresse_numero"],
        Voie=logement_info["adresse_voie"],
        Nom_voie=logement_info["adresse_nom_voie"],
        Code=logement_info["adresse_code"],
        Ville=Ville(
            Code=logement_info["ville_code"],
            Nom=logement_info["ville_nom"],
        )
    )
    adresse.ligne = f"{adresse.Numero} {adresse.Voie} {adresse.Nom_voie}, {adresse.Code} - {adresse.Ville.Nom}"
    pieces_dict = {}
    for info in raw_data:
        piece_id = info["piece_id"]
        if piece_id not in pieces_dict:
            pieces_dict[piece_id] = Piece(
                id=piece_id,
                nom=info["piece_nom"],
                loc_x=info["loc_x"],
                loc_y=info["loc_y"],
                loc_z=info["loc_z"],
                created_at=info["piece_created_at"],
                capteurs=[],
            )
        capteur_id = info["capteur_id"]
        if capteur_id:
            capteur = Capteur(
                id=capteur_id,
                ref_commerciale=info["ref_commerciale"],
                precision_min=info["precision_min"],
                precision_max=info["precision_max"],
                actif=info["actif"],
                created_at=info["capteur_created_at"],
                type_capteur=info["type_capteur_nom"],
                unite_mesure=info["type_capteur_unite_mesure"],
                mesures=[],
            )
            mesure_id = info["mesure_id"]
            if mesure_id:
                mesure = Mesure(
                    id=mesure_id,
                    valeur=info["mesure_valeur"],
                    created_at=info["mesure_created_at"],
                )
                capteur.mesures.append(mesure)
            pieces_dict[piece_id].capteurs.append(capteur)

    return Logement(
        id=logement_info["logement_id"],
        numero_telephone=logement_info["numero_telephone"],
        adresse_ip=logement_info["adresse_ip"],
        created_at=logement_info["logement_created_at"],
        adresse=adresse,
        pieces=list(pieces_dict.values()),
    )
    
@router.post("/list_logements", response_model=List[Logement])
def list_logements(logement_ids: List[int]):
    """
    Retorna os dados principais dos logements a partir de uma lista de IDs.
    Faz join com as tabelas piece e adresse.
    """
    if not logement_ids:
        raise HTTPException(status_code=400, detail="A lista de logement_ids não pode estar vazia.")
    
    # Construir consulta SQL com filtro para os IDs fornecidos
    placeholders = ", ".join(["?"] * len(logement_ids))  # Placeholders para os IDs
    query = f"""
    SELECT 
        logement.id AS logement_id,
        logement.numero_telephone,
        logement.adresse_ip,
        logement.created_at AS logement_created_at,
        adresse.id AS adresse_id,
        adresse.Numero AS adresse_numero,
        adresse.Voie AS adresse_voie,
        adresse.Nom_voie AS adresse_nom_voie,
        adresse.Code AS adresse_code,
        ville.Code AS ville_code,
        ville.Nom AS ville_nom,
        piece.id AS piece_id,
        piece.nom AS piece_nom,
        piece.loc_x AS piece_loc_x,
        piece.loc_y AS piece_loc_y,
        piece.loc_z AS piece_loc_z,
        piece.created_at AS piece_created_at
    FROM logement
    INNER JOIN adresse ON logement.id_adresse = adresse.id
    INNER JOIN ville ON adresse.Code = ville.Code
    LEFT JOIN piece ON piece.id_l = logement.id
    WHERE logement.id IN ({placeholders})
    ORDER BY logement.id, piece.id
    """
    try:
        # Envio da consulta SQL para o backend
        response = requests.post(
            f"{BACKEND_BASE_URL}/generic",
            json={"query": query, "params": logement_ids},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro ao consultar dados do backend: {response.text}",
            )
        raw_data = response.json().get("data", [])

        logements_dict = {}
        for info in raw_data:
            log_id = info["logement_id"]
            # print(info)
            if log_id not in logements_dict:
                logements_dict[log_id] = Logement(
                    id=log_id,
                    numero_telephone=info["numero_telephone"],
                    adresse_ip=info["adresse_ip"],
                    adresse = Adresse(
                        id=info["adresse_id"],
                        Numero=info["adresse_numero"],
                        Voie=info["adresse_voie"],
                        Nom_voie=info["adresse_nom_voie"],
                        Code=info["adresse_code"],
                        Ville=Ville(
                            Code=info["ville_code"],
                            Nom=info["ville_nom"],
                        )
                    ),
                    created_at=info["logement_created_at"],
                    pieces=[],
                    photo_url="",
                )
                logements_dict[log_id].adresse.ligne = f"{logements_dict[log_id].adresse.Numero} {logements_dict[log_id].adresse.Voie} {logements_dict[log_id].adresse.Nom_voie}, {logements_dict[log_id].adresse.Code} - {logements_dict[log_id].adresse.Ville.Nom}"
            if info["piece_id"]:
                logements_dict[log_id].pieces.append(
                    Piece(
                        id=info["piece_id"],
                        nom=info["piece_nom"],
                        loc_x=info["piece_loc_x"],
                        loc_y=info["piece_loc_y"],
                        loc_z=info["piece_loc_z"],
                        created_at=info["piece_created_at"]
                    )
                )

        return list(logements_dict.values())

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro de comunicação com o backend: {str(e)}",
        )


def process_factures_data(factures):
    # Agrupa faturas por tipo
    factures_by_type = {}
    for facture in factures['factures']:
        type_facture = facture.type_facture
        if type_facture not in factures_by_type:
            factures_by_type[type_facture] = []
        factures_by_type[type_facture].append(facture)
    
    # Prepara dados para os gráficos
    chart_data = {}
    for type_facture, factures_list in factures_by_type.items():
        sorted_factures = sorted(factures_list, key=lambda x: x.date_facture)
        chart_data[type_facture] = {
            'labels': [facture.date_facture.strftime('%Y-%m-%d') for facture in sorted_factures],
            'montants': [facture.montant for facture in sorted_factures],
            'consommation': [facture.valeur_consommee for facture in sorted_factures]
        }
    processed_data = {
        'type_list': list(factures_by_type.keys()),
        'chart_data': chart_data,
        'total_by_type': {type_['type']: type_['total_consommation'] 
                         for type_ in factures['types_factures']}
    }
    # print(processed_data)
    return processed_data

@router.get("/factures/{logement_id}", response_model=dict)
def list_factures(logement_id: int):
    """
    Retorna todas as faturas de um logement específico.
    """
    # Consulta SQL para buscar as faturas e seus tipos
    query = """
    SELECT
        facture.id AS facture_id,
        facture.id_l AS logement_id,
        facture.date_facture,
        facture.montant,
        facture.valeur_consommee,
        facture.created_at AS facture_created_at,
        type_facture.id AS type_facture_id,
        type_facture.nom AS type_facture_nom,
        type_facture.description AS type_facture_description
    FROM facture
    INNER JOIN type_facture ON facture.id_tc = type_facture.id
    WHERE facture.id_l = ?
    ORDER BY facture.date_facture DESC
    """
    try:
        # Envia a consulta SQL para o backend
        response = requests.post(
            f"{BACKEND_BASE_URL}/generic",
            json={"query": query, "params": [logement_id]},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro ao consultar dados do backend: {response.text}",
            )
        raw_data = response.json().get("data", [])
        unites_consommation = {"Électricite": "kWh", "Eau": "m3", "Gaz": "m3", "Chauffage": "kWh", "Internet": "Mo", "Téléphone": "min"}
        # Monta as faturas no formato Pydantic
        factures = []
        montant = 0
        for row in raw_data:
            factures.append(
                Facture(
                    id=row["facture_id"],
                    logement_id=row["logement_id"],
                    type_facture=row["type_facture_nom"],
                    date_facture=row["date_facture"],
                    montant=row["montant"],
                    valeur_consommee=row.get("valeur_consommee"),
                    unite_consommation=unites_consommation.get(row["type_facture_nom"]),
                    created_at=row["facture_created_at"],
                )
            )            
            montant += row["montant"]
        # print(factures)
        types_factures = list(set(f.type_facture for f in factures))
        types_factures = [{"type": type_facture, "total_consommation": 0} for type_facture in types_factures]
        for type_facture in types_factures:
            type_facture["total_consommation"] = sum(
            f.valeur_consommee for f in factures if f.type_facture == type_facture["type"]
            )
        return {
            "factures": factures,
            "num_factures": len(factures),
            "montant": montant,
            "types_factures": types_factures,
            }

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro de comunicação com o backend: {str(e)}",
        )

@router.get("/capteurs_data/{logement_id}", response_model=List[Capteur])
def get_capteurs_data(logement_id: int):
    """
    Retorna a quantidade de medidas de cada capteur de um logement.
    """
    # Consulta SQL para buscar as medidas de cada capteur
    query = """
    SELECT
        capteur.id AS capteur_id,
        capteur.ref_commerciale,
        capteur.precision_min,
        capteur.precision_max,
        capteur.actif,
        capteur.created_at AS capteur_created_at,
        type_capteur.nom AS type_capteur_nom,
        type_capteur.unite_mesure AS type_capteur_unite_mesure,
        mesure.id AS mesure_id,
        mesure.valeur AS mesure_valeur,
        mesure.created_at AS mesure_created_at
    FROM capteur
    LEFT JOIN mesure ON capteur.id = mesure.id_c
    LEFT JOIN type_capteur ON capteur.id_tc = type_capteur.id
    WHERE capteur.id_p IN (
        SELECT id
        FROM piece
        WHERE id_l = ?
    )
    ORDER BY capteur.id, mesure.created_at DESC
    """
    try:
        # Envia a consulta SQL para o backend
        response = requests.post(
            f"{BACKEND_BASE_URL}/generic",
            json={"query": query, "params": [logement_id]},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro ao consultar dados do backend: {response.text}",
            )
        raw_data = response.json().get("data", [])

        # Monta as medidas no formato Pydantic
        capteurs_dict = {}
        for row in raw_data:
            capteur_id = row["capteur_id"]
            if capteur_id not in capteurs_dict:
                capteurs_dict[capteur_id] = Capteur(
                    id=capteur_id,
                    ref_commerciale=row["ref_commerciale"],
                    precision_min=row["precision_min"],
                    precision_max=row["precision_max"],
                    actif=row["actif"],
                    created_at=row["capteur_created_at"],
                    type_capteur=row["type_capteur_nom"],
                    unite_mesure=row["type_capteur_unite_mesure"],
                    mesures=[],
                )
            if row["mesure_id"]:
                capteurs_dict[capteur_id].mesures.append(
                    Mesure(
                        id=row["mesure_id"],
                        valeur=row["mesure_valeur"],
                        created_at=row["mesure_created_at"],
                    )
                )
        return list(capteurs_dict.values())

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro de comunicação com o backend: {str(e)}",
        )
        
@router.post("/toggle_capteur/{capteur_id}", response_model=dict)
def toggle_capteur(capteur_id: int):
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/capteur/{capteur_id}")
        if response.status_code != 200:
            raise HTTPException(
            status_code=response.status_code,
            detail=f"Erreur lors de la consultation des données du backend: {response.text}",
            )
        capteur_data = response.json()
        capteur_data["actif"] = not capteur_data["actif"]

        update_response = requests.put(
            f"{BACKEND_BASE_URL}/capteur/{capteur_id}",
            json=capteur_data,
        )
        if update_response.status_code != 200:
            raise HTTPException(
            status_code=update_response.status_code,
            detail=f"Erreur lors de la mise à jour des données du backend: {update_response.text}",
            )

        updated_response = requests.get(f"{BACKEND_BASE_URL}/capteur/{capteur_id}")
        if updated_response.status_code != 200:
            raise HTTPException(
            status_code=updated_response.status_code,
            detail=f"Erreur lors de la consultation des données du backend: {updated_response.text}",
            )
        updated_capteur_data = updated_response.json()

        return {
            "status": "ok",
            "message": "Capteur mis à jour avec succès",
            "actif": updated_capteur_data["actif"],
            # "data": updated_capteur_data,
        }
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de communication avec le backend: {str(e)}",
        )

@router.post("/login")
async def bff_login(username: str, password: str):
    try:
        response = requests.post(f"{BACKEND_BASE_URL}/auth/login", params={"username": username, "password": password})
        if response.status_code != 200:
            raise HTTPException(
            status_code=response.status_code,
            detail=f"Erreur lors de la consultation des données du backend: {response.text}",
            )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de communication avec le backend: {str(e)}",
        )


@router.post("/decode_token")
async def decode_token(token: str):
    try:
        response = requests.post(f"{BACKEND_BASE_URL}/auth/decode", params={"token": token})
        if response.status_code != 200:
            raise HTTPException(
            status_code=response.status_code,
            detail=f"Erreur lors de la consultation des données du backend: {response.text}",
            )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de communication avec le backend: {str(e)}",
        )
        
@router.post("/create_key")
async def create_key(token: str, name: str, description: Optional[str] = None):
    try:
        response = requests.post(f"{BACKEND_BASE_URL}/auth/api_key", params={"token": token, "name": name, "description": description})
        if response.status_code != 200:
            raise HTTPException(
            status_code=response.status_code,
            detail=f"Erreur lors de la consultation des données du backend: {response.text}",
            )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de communication avec le backend: {str(e)}",
        )