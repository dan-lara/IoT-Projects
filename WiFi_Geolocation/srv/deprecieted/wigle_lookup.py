import requests
import pandas as pd

# Définir les informations d'authentification de l'API Wigle
WIGLE_API_URL = "https://api.wigle.net/api/v2/network/search"
WIGLE_AUTH = ("danlara", "9c83de2fec9eb587a40c4466857675c6")

def get_wigle_locations(wifi_points):
    """
    Interroger l'API Wigle pour obtenir l'emplacement géographique (latitude et longitude)
    des points d'accès Wi-Fi spécifiés.
    
    Paramètres:
        wifi_points (list[dict]): Liste de points d'accès avec 'mac' et 'signal_strength'.

    Retourne:
        pd.DataFrame: Cadre de données contenant les points d'accès avec coordonnées géographiques.
    """
    locations = []

    for point in wifi_points:
        mac = point['mac']
        params = {"netid": mac}

        # Interroger l'API Wigle
        response = requests.get(WIGLE_API_URL, params=params, auth=WIGLE_AUTH)

        if response.status_code == 200:
            data = response.json()
            # Extraire les informations de localisation du premier résultat
            if len(data['results']) > 0:
                result = data['results'][0]
                locations.append({
                    "ssid": point['ssid'],
                    "mac": point['mac'],
                    "signal_strength": point['signal_strength'],
                    "lat": result['trilat'],
                    "lon": result['trilong']
                })

    # Retourner les résultats sous forme de DataFrame
    return pd.DataFrame(locations)
