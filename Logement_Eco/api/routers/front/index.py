from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from tools import get_db
from models.database import Capteur, Mesure, Facture


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def get_index(request: Request):
    # Rendre la page avec les données ou sans données si les filtres ne sont pas fournis
    # return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse(
            "index.html",  # Template base para a página inicial
            {
                "request": request,
                "title": "Accueil - Éco-Logement",
                "active_page": "home",  # Identificador da página ativa
                "year": datetime.now().year,  # Ano dinâmico no footer
            }
        )

@router.get("/dashboard", response_class=HTMLResponse, tags=["Frontend"])
def dashboard(request: Request):
    return templates.TemplateResponse(
            "dash.html",  # Template base para a página inicial
            {
                "request": request,
                "title": "DashBoard - Éco-Logement",
                "active_page": "dashboard",  # Identificador da página ativa
                "year": datetime.now().year,  # Ano dinâmico no footer
            }
        )

@router.get("/base", response_class=HTMLResponse, tags=["Frontend"])
def dashboard(request: Request):
    return templates.TemplateResponse(
            "base.html",  # Template base para a página inicial
            {
                "request": request,
                "title": "DashBoard - Éco-Logement",
                "active_page": "dashboard",  # Identificador da página ativa
                "year": datetime.now().year,  # Ano dinâmico no footer
            }
        )