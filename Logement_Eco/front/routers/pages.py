import os
import json
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd

from .bff import get_logement_details, list_logements, list_factures, get_capteurs_data, bff_login

templates_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates/"))
templates = Jinja2Templates(directory=templates_folder_path)

router = APIRouter()

def ensure_login(request: Request):
    username = request.state.username
    if not username:
        return RedirectResponse("/login")

def base_context(request: Request, page_title: str, active_page: str):
    try:
        logement_id = request.state.logement_id
        user_logements = request.state.user_logements
        logement_data = list_logements(user_logements)
        user_logements_list = []
        current_logement = None
        for logement in logement_data:
            if logement.id == int(logement_id):
                current_logement = logement
            user_logements_list.append({
                'id': logement.id,
                'numero_telephone': logement.numero_telephone,
                'adresse_ip': logement.adresse_ip,
                'adresse': logement.adresse.ligne,
                'created_at': (logement.created_at).strftime("%d/%m/%Y à %H:%M"),
                'pieces': logement.pieces,
                'photo_url': logement.photo_url
            })
        current_logement=current_logement.dict() if current_logement else None
        request.state.current_logement = current_logement
        request.state.user_logements_list = user_logements_list
        return {
            "title": page_title,
            "active_page": active_page,
            
            "current_logement": current_logement,
            "user_logements_list": user_logements_list,
            "logement_id": logement_id,      
            "year": datetime.now().year,
        }
    except Exception as e:
        raise e
        return None

@router.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    
    ensure_login(request)
    logement_id = request.state.logement_id
    username = request.state.username
       
    context = base_context(request, "Accueil", "accueil")
    print(request.state.user_api_keys)
    print(request.state.logement_id)
    print(request.state.user_logements)
    print(request.state.current_logement)
    print(request.state.user_logements_list)
    if logement_id: 
        capteurs_data = get_capteurs_data(logement_id)
        logement_data = get_logement_details(logement_id)
        quantite_mesures = sum(len(capteur.mesures) for capteur in capteurs_data)
        active_sensors = sum(1 for capteur in capteurs_data if capteur.actif)
        total_sensors = len(capteurs_data)
        quantite_pieces = len(logement_data.pieces)
        mesures = []
        for piece in logement_data.pieces:
            for capteur in piece.capteurs:
                for mesure in capteur.mesures:
                    mesures.append({
                    'id': mesure.id,
                    'piece': piece.nom,
                    'capteur_type': capteur.type_capteur,
                    'valeur': mesure.valeur,
                    'unite_mesure': capteur.unite_mesure,
                    'datetime': mesure.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        mesures = sorted(mesures, key=lambda x: x['datetime'], reverse=True)[:10]
        context.update({
            "request": request,
            "savings": 100,
            "active_sensors": active_sensors,
            "total_sensors": total_sensors,
            "quantite_pieces": quantite_pieces,
            "quantite_mesures": quantite_mesures,
            "mesures": mesures,
            "username": username,
        })
    else:
        context.update({
            "request": request,
        })
    response = templates.TemplateResponse("accueil.html", context)
    
    response.set_cookie(key="logement_id", value=str(logement_id) if logement_id else "")    
    response.set_cookie(key="current_logement", value=context["current_logement"] or "")
    response.set_cookie(key="user_logements_list", value=context["user_logements_list"])
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
        
    ensure_login(request)
    logement_id = request.state.logement_id
    username = request.state.username
       
    context = base_context(request, "Dashboard", "dashboard")
    
    capteurs_table = []
    capteur_graph = []
    if logement_id:
        capteurs_data = get_capteurs_data(logement_id)
        
        for capteur in capteurs_data:
            last_mesure = capteur.mesures[-1] if capteur.mesures else None
            capteurs_table.append({
            'id': capteur.id,
            'actif': capteur.actif,
            'last_mesure_valeur': last_mesure.valeur if last_mesure else None,
            'last_mesure_date': last_mesure.created_at if last_mesure else None,
            'type': capteur.type_capteur,
            'unite_mesure': capteur.unite_mesure,
            'ref_commerciale': capteur.ref_commerciale
            })
            mesures_list = []
            for mesure in capteur.mesures:
                mesures_list.append({
                    'x': mesure.created_at.strftime('%Y-%m-%dT%H:%M:%S'), 
                    'y': float(mesure.valeur) 
                })
        
            capteur_graph.append({
                'id': capteur.id,
                'type': capteur.type_capteur,
                'unite_mesure': capteur.unite_mesure,
                'actif': capteur.actif,
                'mesures': sorted(mesures_list, key=lambda x: x['x']) 
            })
       
    context.update({
        "request": request,
        "capteurs_table": capteurs_table,
        "capteur_graph": capteur_graph,
    })
    return templates.TemplateResponse(
        "dashboard.html",
        context
    )


@router.get("/economies", response_class=HTMLResponse)
async def economies(request: Request):
    
    ensure_login(request)
    logement_id = request.state.logement_id
    context = base_context(request, "Economies", "economies")
    
    factures_table = []
    bar_chart_data = [] 
    general_chart_data = []
    info = {}
    if logement_id:
        factures = list_factures(logement_id)        
        
        for facture in factures.get("factures"):
            factures_table.append({
                'id': facture.id,
                'date': facture.date_facture,
                'montant': facture.montant,
                'type': facture.type_facture,
                'consommation': facture.valeur_consommee
            })
        
        
        types_factures = factures.get("types_factures")
        for element in types_factures:
            type_facture = element.get("type")
            total_consommation = element.get("total_consommation")
            general_chart_data.append({
                "type_nom": type_facture,
                "total_consommation": total_consommation
            })
        
        info = {
            'num_factures': factures.get("num_factures"),
            'total_montant': factures.get("montant"),
            'types_factures': types_factures,
            'type_list': [element.get("type") for element in types_factures],
        }
        
               
        chart_data = {type_facture["type"]: [] for type_facture in factures["types_factures"]}

        for facture in factures["factures"]:
            type_facture = facture.type_facture
            date = facture.date_facture
            montant = facture.montant
            consommation = f"{facture.valeur_consommee} {facture.unite_consommation}"
            chart_data[type_facture].append({
                "date": date.strftime("%m/%Y"),
                "montant": montant,
                "consommation": consommation
            })

        for key in chart_data.keys():
            chart_data[key].sort(key=lambda x: x["date"])

        bar_chart_data = {
            key: {
                "labels": [item["date"] for item in values],
                "data": [item["montant"] if item["montant"] is not None else 0 for item in values],
                "consommation": [item["consommation"] if item["consommation"] is not None else "" for item in values]
            } for key, values in chart_data.items()
        }
        
    context.update({
        "request": request,
        "factures_table": factures_table,
        "info": info,
        "general_chart_data": general_chart_data,
        "bar_chart_data": bar_chart_data,
    })
    return templates.TemplateResponse(
        "economies.html",
        context
    )


@router.get("/logements", response_class=HTMLResponse)
async def logements(request: Request):
    
    ensure_login(request)

    logement_ids = request.state.user_logements
    logement_data = list_logements(logement_ids)
    user_logements = []
    for logement in logement_data:
        user_logements.append({
            'id': logement.id,
            'numero_telephone': logement.numero_telephone,
            'adresse_ip': logement.adresse_ip,
            'adresse': logement.adresse.ligne,
            'created_at': (logement.created_at).strftime("%d/%m/%Y à %H:%M"),
            'pieces': logement.pieces,
            'photo_url': logement.photo_url
        })
    return templates.TemplateResponse(
        "logements.html", 
        {
            "request": request, 
            "title": "Logements", 
            "year": datetime.now().year,
            "current_logement": None,
            "user_logements": user_logements,
        }
    )

@router.get("/configuration", response_class=HTMLResponse)
async def configuration(request: Request):
    
    ensure_login(request)
    user_api_keys = request.state.user_api_keys
    context = base_context(request, "Configuration", "configuration")
    
    context.update({
        "request": request,
        "user_api_keys": user_api_keys,
    })
    return templates.TemplateResponse(
        "configuration.html",
        context
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = await bff_login(form_data.username, form_data.password)
    print(user)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    

    response = RedirectResponse("/logements", status_code=303)
    response.set_cookie(key="access_token", value=str(user["access_token"]), httponly=True, secure=True)

    return response

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("logement_id")
    response.delete_cookie("current_logement")
    response.delete_cookie("user_logements_list")
    return response