from fastapi import APIRouter, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import requests
import os
import httpx
from fastapi import Request, Form

from models.meteo import WeatherData

router = APIRouter()

# Définir les variables globales nécessaires
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

templates = Jinja2Templates(directory="templates")

# Route pour obtenir les données météorologiques
@router.get("/data", response_model=WeatherData, tags=["Meteo"])
async def get_weather(
    postal_code: str = Query(..., description="Code postal pour la requête"),
    country_code: str = Query("fr", description="Code du pays, par défaut 'fr'")
):
    # Construire l'URL de la requête
    url = f"{BASE_URL}?zip={postal_code},{country_code}&appid={API_KEY}&units=metric"
    try:
        # Effectuer une requête GET
        response = requests.get(url)
        
        if response.status_code == 200:
            # Analysez les données JSON reçues
            weather_data = response.json()
            
            # Extraire des informations utiles
            main_data = weather_data.get("main", {})
            return WeatherData(
                city=weather_data.get("name", "Unknown"),
                temperature=main_data.get("temp", 0.0),
                feels_like=main_data.get("feels_like", 0.0),
                temp_min=main_data.get("temp_min", 0.0),
                temp_max=main_data.get("temp_max", 0.0),
                pressure=main_data.get("pressure", 0),
                humidity=main_data.get("humidity", 0),
                sea_level=main_data.get("sea_level"),
                ground_level=main_data.get("grnd_level"),
                description=weather_data["weather"][0]["description"]
            )
        else:
            # En cas d'erreur, lever une exception HTTP avec un message
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )
    except Exception as e:
        # En cas d'erreur inattendue, lever une exception HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
    
templates = Jinja2Templates(directory="templates")

# URL de base pour l'API météo
BACKEND_BASE_URL = "http://localhost:8005/meteo/data/"  # Remplacez par l'URL correcte de l'API backend

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=["Meteo"])
async def get_weather_page(request: Request, postal_code: str = None, country_code: str = "fr"):
    weather = None
    if postal_code:
        # Realizar a requisição para o backend de meteo
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BACKEND_BASE_URL,
                    params={"postal_code": postal_code, "country_code": country_code}
                )
            if response.status_code == 200:
                weather = response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching weather data.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")

    # Renderiza a página com os dados ou sem dados se postal_code não for fornecido
    return templates.TemplateResponse("meteo_form.html", {"request": request, "weather": weather})

@router.get("/base", response_class=HTMLResponse, tags=["Meteo"])
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})