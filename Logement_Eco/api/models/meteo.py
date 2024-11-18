from pydantic import BaseModel
from typing import Optional

# Modèle pour représenter les données météorologiques
class WeatherData(BaseModel):
    city: str  # Nom de la ville
    temperature: float  # Température actuelle en °C
    feels_like: float  # Ressenti en °C
    temp_min: float  # Température minimale en °C
    temp_max: float  # Température maximale en °C
    pressure: int  # Pression atmosphérique en hPa
    humidity: int  # Humidité en %
    sea_level: Optional[int] = None  # Niveau de la mer en hPa
    ground_level: Optional[int] = None  # Pression au sol en hPa
    description: str  # Description du temps