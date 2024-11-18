from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, List
from collections import defaultdict
import random
import httpx
import json
router = APIRouter()

# Configurer le chemin pour les templates Jinja2
templates = Jinja2Templates(directory="templates")

# URL de base pour la communication avec l'API backend
BACKEND_BASE_URL = "http://localhost:8000" 

@router.get("/example/", response_class=HTMLResponse, tags=["Facture"])
async def read_home(request: Request):
    # Dados simulados para enviar ao template
    data = {
        "sensor": "Temperature",
        "value": f"{random.randint(20, 30)}°C",  # Gera um valor aleatório para simular a temperatura
        "status": "Active",
        "consumption": [
            ["Eau", random.randint(20, 50)],
            ["Eléctricite", random.randint(30, 60)],
            ["Déchets", random.randint(10, 30)]
        ]
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})

async def fetch_data(endpoint: str, params: dict = None):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"  # Adicionado '/' no final
    async with httpx.AsyncClient(follow_redirects=True) as client:  # Habilitado follow_redirects
        print(f"Fazendo requisição para: {url} com params: {params}")
        try:
            response = await client.get(url, params=params)
            print(f"Status code: {response.status_code}")
            print(f"Resposta de {endpoint}: {response.text[:200]}...")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição: Status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erro na requisição para {endpoint}: {e}")
            return []

@router.get("/", response_class=HTMLResponse, tags=["Facture"])
async def visualize_factures(
    request: Request,
    id_l: Optional[int] = Query(None, description="Filtrer par logement")
):
    # print("\n=== Iniciando visualização ===")
    # print(f"ID Logement: {id_l}")

    # Buscar dados das APIs
    try:
        factures = await fetch_data("facture", {"id_l": id_l} if id_l else None)
        # print(f"\nFactures recebidas: {len(factures)}")
        # print(f"Exemplo de fatura: {factures[0] if factures else 'Nenhuma fatura'}")
    except Exception as e:
        print(f"Erro ao buscar faturas: {e}")
        factures = []

    try:
        types_facture = await fetch_data("type_facture")
        # print(f"\nTypes de facture recebidos: {len(types_facture)}")
        # print(f"Types: {types_facture}")
    except Exception as e:
        print(f"Erro ao buscar tipos de fatura: {e}")
        types_facture = []

    try:
        logements = await fetch_data("logement")
        # print(f"\nLogements recebidos: {len(logements)}")
        # print(f"Exemplo de logement: {logements[0] if logements else 'Nenhum logement'}")
    except Exception as e:
        print(f"Erro ao buscar logements: {e}")
        logements = []

    # Criar dicionário de tipos de fatura
    type_facture_dict = {}
    for tf in types_facture:
        try:
            type_facture_dict[tf["id"]] = tf["nom"]
        except Exception as e:
            print(f"Erro ao processar tipo de fatura {tf}: {e}")

    print(f"\nDicionário de tipos de fatura: {type_facture_dict}")

    # Processar dados para o gráfico
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
            print(f"Erro ao processar fatura {facture}: {e}")

    # Preparar dados para o template
    chart_data = [
        {"type_nom": type_nom, "total_consommation": round(total, 2)}
        for type_nom, total in consumption_by_type.items()
    ]

    # print("\n=== Dados processados ===")
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

    # print("\n=== Dados enviados para o template ===")
    # print(f"Logements: {len(logements)} itens")
    # print(f"Chart data: {len(chart_data)} itens")
    # print(f"Stats: {stats}")

    return templates.TemplateResponse("facture.html", template_data)