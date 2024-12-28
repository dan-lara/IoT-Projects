from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, List
from collections import defaultdict
import random
import httpx
import os

router = APIRouter()

# Configurer le chemin pour les templates Jinja2
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates/"))
templates = Jinja2Templates(directory=folder_path)

# URL de base pour la communication avec l'API backend
BACKEND_BASE_URL = "http://localhost:8000" 

@router.get("/example/", response_class=HTMLResponse)
async def read_home(request: Request):
    # Données simulées pour envoyer au template
    data = {
        "sensor": "Temperature",
        "value": f"{random.randint(20, 30)}°C",  # Génère une valeur aléatoire pour simuler la température
        "status": "Active",
        "consumption": [
            ["Eau", random.randint(20, 50)],
            ["Électricité", random.randint(30, 60)],
            ["Déchets", random.randint(10, 30)]
        ]
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})

async def fetch_data(endpoint: str, params: dict = None):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"  # Ajouté '/' à la fin
    async with httpx.AsyncClient(follow_redirects=True) as client:  # Activation de follow_redirects
        # print(f"Faisant requête pour: {url} avec params: {params}")
        try:
            response = await client.get(url, params=params)
            # print(f"Status code: {response.status_code}")
            # print(f"Réponse de {endpoint}: {response.text[:200]}...")
            
            if response.status_code == 200:
                return response.json()
            else:
                # print(f"Erreur dans la requête: Status {response.status_code}")
                return []
                
        except Exception as e:
            # print(f"Erreur dans la requête pour {endpoint}: {e}")
            return []

@router.get("/", response_class=HTMLResponse)
async def visualize_factures(
    request: Request,
    id_l: Optional[int] = Query(None, description="Filtrer par logement")
):
    # print("\n=== Début de la visualisation ===")
    # print(f"ID Logement: {id_l}")

    # Récupérer les données des APIs
    try:
        factures = await fetch_data("facture", {"id_l": id_l} if id_l else None)
        # print(f"\nFactures reçues: {len(factures)}")
        # print(f"Exemple de facture: {factures[0] si factures else 'Aucune facture'}")
    except Exception as e:
        print(f"Erreur lors de la récupération des factures: {e}")
        factures = []

    try:
        types_facture = await fetch_data("type_facture")
        # print(f"\nTypes de facture reçus: {len(types_facture)}")
        # print(f"Types: {types_facture}")
    except Exception as e:
        print(f"Erreur lors de la récupération des types de facture: {e}")
        types_facture = []

    try:
        logements = await fetch_data("logement")
        # print(f"\nLogements reçus: {len(logements)}")
        # print(f"Exemple de logement: {logements[0] si logements else 'Aucun logement'}")
    except Exception as e:
        print(f"Erreur lors de la récupération des logements: {e}")
        logements = []

    # Créer un dictionnaire de types de facture
    type_facture_dict = {}
    for tf in types_facture:
        try:
            type_facture_dict[tf["id"]] = tf["nom"]
        except Exception as e:
            print(f"Erreur lors du traitement du type de facture {tf}: {e}")

    print(f"\nDictionnaire des types de facture: {type_facture_dict}")

    # Traiter les données pour le graphique
    consumption_by_type = defaultdict(float)
    total_montant = 0
    total_consommation = 0

    for facture in factures:
        try:
            type_id = facture["id_tc"]
            type_nom = type_facture_dict.get(type_id, f"Type {type_id}")
            valeur_consommee = float(facture["valeur_consommee"])
            montant = float(facture["montant"])

            consumption_by_type[type_nom] += valeur_consommee
            total_montant += montant
            total_consommation += valeur_consommee
        except Exception as e:
            print(f"Erreur lors du traitement de la facture {facture}: {e}")

    # Préparer les données pour le template
    chart_data = [
        {"type_nom": type_nom, "total_consommation": round(total, 2)}
        for type_nom, total in consumption_by_type.items()
    ]

    # print("\n=== Données traitées ===")
    # print(f"Chart data: {chart_data}")
    
    stats = {
        "num_factures": len(factures),
        "total_montant": round(total_montant, 2),
        "total_consommation": round(total_consommation, 2)
    }
    
    # print(f"Stats: {stats}")

    template_data = {
        "request": request,
        "logements": logements,
        "selected_logement": id_l,
        "chart_data": chart_data,
        "stats": stats
    }

    # print("\n=== Données envoyées au template ===")
    # print(f"Logements: {len(logements)} items")
    # print(f"Chart data: {len(chart_data)} items")
    # print(f"Stats: {stats}")

    return templates.TemplateResponse("facture.html", template_data)