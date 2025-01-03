from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from typing import List
import datetime
import requests
import os
import httpx
from ..models.meteo import WeatherData, ForecastData

router = APIRouter()

# Définir les variables globales nécessaires
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# URL de base pour l'API météo
BACKEND_BASE_URL = "http://localhost:8001/meteo"  # Remplacez par l'URL correcte de l'API backend

folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates/"))
templates = Jinja2Templates(directory=folder_path)

# Route pour obtenir les données météorologiques
@router.get("/data", response_model=WeatherData)
async def get_weather(
    postal_code: str = Query(..., description="Code postal pour la requête"),
    country_code: str = Query("fr", description="Code du pays, par défaut 'fr'")
):
    # Construire l'URL de la requête
    url = f"{BASE_URL}/weather?zip={postal_code},{country_code}&appid={API_KEY}&units=metric"
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
    
@router.get("/forecast", response_model=List[ForecastData])
async def get_weather_forecast(
    postal_code: str = Query(..., description="Code postal pour la requête"),
    country_code: str = Query("fr", description="Code du pays, par défaut 'fr'"),
):
    # Construire l'URL de la requête pour la prévision sur 5 jours
    url = f"{BASE_URL}/forecast?zip={postal_code},{country_code}&appid={API_KEY}&units=metric"
    try:
        # Effectuer une requête GET
        response = requests.get(url)
        
        if response.status_code == 200:
            # Analysez les données JSON reçues
            forecast_data = response.json()
            forecast_list = forecast_data.get("list", [])
            
            # Extraire des informations utiles pour chaque période de prévision
            weather_forecast = []
            for index, period in enumerate(forecast_list):
                main_data = period.get("main", {})
                weather_forecast.append(
                    ForecastData(
                        date=(datetime.datetime.now() + datetime.timedelta(days=index)).strftime("%d/%m/%Y"),
                        data=WeatherData(
                            city=forecast_data.get("city", {}).get("name", "Unknown"),
                            temperature=main_data.get("temp", 0.0),
                            feels_like=main_data.get("feels_like", 0.0),
                            temp_min=main_data.get("temp_min", 0.0),
                            temp_max=main_data.get("temp_max", 0.0),
                            pressure=main_data.get("pressure", 0),
                            humidity=main_data.get("humidity", 0),
                            sea_level=main_data.get("sea_level"),
                            ground_level=main_data.get("grnd_level"),
                            description=period["weather"][0]["description"]
                        )
                    )
                )
            return weather_forecast[:7]  # Retourner uniquement les 5 premières périodes
        else:
            # En cas d'erreur, lever une exception HTTP avec un message
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )
    except Exception as e:
        # En cas d'erreur inattendue, lever une exception HTTP 500
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_class=HTMLResponse)
async def get_weather_page(request: Request,
    postal_code: str = Query(..., description="Code postal pour la requête"),
    country_code: str = Query("fr", description="Code du pays, par défaut 'fr'")
):
    weather = None
    if postal_code:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BACKEND_BASE_URL + "/data",
                    params={"postal_code": postal_code, "country_code": country_code}
                )
            # print(response)
            if response.status_code == 200:
                weather = response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching weather data.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BACKEND_BASE_URL + "/forecast",
                    params={"postal_code": postal_code, "country_code": country_code}
                )
            if response.status_code == 200:
                forecast = response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching weather data.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
        

    return templates.TemplateResponse("meteo_form.html", {"request": request, "weather": weather, "forecast": forecast})
