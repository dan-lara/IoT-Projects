from scipy.optimize import minimize
import numpy as np
from localisateur import *

DEBUG = True

def rssi_to_distance(rssi, rssi_0=-30, n=2.5):
    """
    Convertit la valeur RSSI en distance.

    Paramètres:
    - rssi: Valeur RSSI mesurée.
    - rssi_0: Valeur RSSI à 1 mètre (par défaut -30 dBm).
    - n: Exposant de perte de chemin (par défaut 2.5).

    Retourne:
    - Distance estimée en mètres.
    """
    distance = 10 ** ((rssi_0 - rssi) / (10 * n))
    return distance

def estimate_position(location_data):
    """
    Estime la position d'un dispositif basé sur les points d'accès détectés.
    
    Paramètres:
    - location_data: DataFrame avec les informations des APs (MAC, SSID, RSSI, Latitude, Longitude, Altitude).
    
    Retourne:
    - Latitude, Longitude et Altitude estimées du dispositif.
    """
    # Extraire les positions et les distances
    positions = np.array(list(zip(location_data['Latitude'], location_data['Longitude'], location_data['Altitude'])))
    distances = np.array([rssi_to_distance(rssi) for rssi in location_data['RSSI']])
    
    # Définir la fonction d'erreur à minimiser (méthode des moindres carrés)
    def error_function(x, positions, distances):
        estimated_distances = np.sqrt(np.sum((positions - x) ** 2, axis=1))
        return np.sum((estimated_distances - distances) ** 2)
    
    # Point initial de recherche
    initial_guess = np.mean(positions, axis=0)
    
    # Optimisation pour trouver la meilleure position
    result = minimize(error_function, initial_guess, args=(positions, distances), method='L-BFGS-B')
    
    # Retourne la position estimée
    return result.x

if DEBUG:
    # bdd = read_DB_csv_file('data/BDD.csv')
    bdd = read_DB_csv_file('https://github.com/dan-lara/IoT-Projects/raw/refs/heads/master/WiFi_Geolocation/srv/data/BDD.csv')
    print("BDD CSV:", bdd)

    wifi = read_WiFi_json_file('data/wifi_data.json')
    print("WiFi JSON: \n", wifi)

    location_df = fetch_locations(bdd, wifi)
    print("DataFrame de localisation: \n", location_df)

    position = estimate_position(location_df)
    print("Latitude estimée:", position[0])
    print("Longitude estimée:", position[1])
