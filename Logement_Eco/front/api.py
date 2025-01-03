import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .routers import pages, bff
from .routers.bff import decode_token
DEBUG = True

static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static/"))

# Métadonnées pour la documentation OpenAPI
tags_metadata = [
    {"name": "Pages", "description": "Routes pour les pages de l'application"},
]
tags_metadata.append({"name": "Back-For-Front", "description": "Routes pour le Back-For-Front de l'application"}) if DEBUG else None

# Création de l'application FastAPI avec des informations de base et des tags pour la documentation
app = FastAPI(
    title="Logement Éco-Responsable Frontend",
    description="Application pour la gestion éco-responsable des logements",
    version="0.2.0",
    openapi_tags=tags_metadata
)
app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

app.include_router(pages.router, tags=["Pages"])
app.include_router(bff.router, tags=["Back-For-Front"], prefix="/bff") if DEBUG else None


@app.middleware("http")
async def dispatch(request: Request, call_next):
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            user_data = await decode_token(access_token)
            request.state.username = user_data["username"]
            user_data = await decode_token(access_token)
            if user_data:
                request.state.username = user_data["username"]
                request.state.user_logements = user_data["user_logements"]
                request.state.user_api_keys = user_data["user_api_keys"]
            else:
                response = RedirectResponse("/login")
                response.delete_cookie("access_token")
                return response
          
        except HTTPException as e:
            if e.status_code == 401:
                response = RedirectResponse("/login")
                response.delete_cookie("access_token")
                return response
            raise e 
    else:
        if request.url.path not in ["/login", "/static"]:
            return RedirectResponse("/login")
    
    
    logement_id = request.cookies.get("logement_id")
    user_logements_list = request.cookies.get("user_logements_list")
    current_logement = request.cookies.get("current_logement")
    
    if logement_id:
        request.state.logement_id = logement_id
    if current_logement:
        request.state.current_logement = current_logement
    if user_logements_list:
        request.state.user_logements_list = user_logements_list
    
    response = await call_next(request)
    return response