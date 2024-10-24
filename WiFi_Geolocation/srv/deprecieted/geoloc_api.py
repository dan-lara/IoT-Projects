from fastapi import FastAPI
from pydantic import BaseModel
import wigle_lookup
import triangulation

# Définir un modèle pour recevoir les données WiFi depuis l'ESP
class WifiData(BaseModel):
    mac: str
    rssi: int

class WifiDataList(BaseModel):
    wifi_points: list[WifiData]

# Créer une instance de l'application FastAPI
app = FastAPI()

# Définir un endpoint pour recevoir les données des points d'accès WiFi
@app.post("/locate")
def locate_device(wifi_data_list: WifiDataList):
    """
    Recevoir un ensemble de points d'accès Wi-Fi détectés par l'ESP, 
    interroger Wigle pour obtenir leurs coordonnées, 
    et utiliser la triangulation pour calculer l'emplacement du dispositif.
    """
    # Convertir les données reçues en un format exploitable
    wifi_points = [
        {"ssid": point.ssid, "mac": point.mac, "signal_strength": point.signal_strength}
        for point in wifi_data_list.wifi_points
    ]

    # Interroger Wigle pour obtenir les emplacements
    access_points_df = wigle_lookup.get_wigle_locations(wifi_points)

    # Effectuer la triangulation pour déterminer l'emplacement de l'ESP8266
    esp_location = triangulation.triangulate_location(access_points_df)

    return esp_location

# Lancer le serveur (uniquement pour le test local, sinon utiliser `uvicorn` en production)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
