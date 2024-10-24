import numpy as np
from scipy.optimize import minimize
from localisateur import *

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

def estimate_position(ap_data):
    """
    Estime la position d'un dispositif basé sur les points d'accès détectés.
    
    Paramètres:
    - ap_data: DataFrame avec les informations des APs (MAC, SSID, RSSI, Latitude, Longitude, Altitude).
    
    Retourne:
    - Latitude, Longitude et Altitude estimées du dispositif.
    """
    # Extraire les positions et les distances
    positions = np.array(list(zip(ap_data['Latitude'], ap_data['Longitude'], ap_data['Altitude'])))
    distances = np.array([rssi_to_distance(rssi) for rssi in ap_data['RSSI']])
    
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

def estimate_position_2d(ap_data):
    """
    Estime la position d'un dispositif basé sur les points d'accès détectés.
    
    Paramètres:
    - ap_data: DataFrame avec les informations des APs (MAC, SSID, RSSI, Latitude, Longitude).
    
    Retourne:
    - Latitude et Longitude estimées du dispositif.
    """
    # Extraire les positions (latitude et longitude) et les distances des APs
    positions = np.array(list(zip(ap_data['Latitude'], ap_data['Longitude'])))
    distances = np.array([rssi_to_distance(rssi) for rssi in ap_data['RSSI']])
    
    # Définir la fonction d'erreur à minimiser (méthode des moindres carrés)
    def error_function(x, positions, distances):
        estimated_distances = np.sqrt(np.sum((positions - x) ** 2, axis=1))
        return np.sum((estimated_distances - distances) ** 2)
    
    # Point initial de recherche (moyenne des positions des APs)
    initial_guess = np.mean(positions, axis=0)
    
    # Optimisation pour trouver la meilleure position (latitude et longitude)
    result = minimize(error_function, initial_guess, args=(positions, distances), method='L-BFGS-B')
    
    # Retourne la position estimée (latitude et longitude)
    return result.x

# # Testar a função de estimativa de posição
# bdd = read_DB_csv_file('BDD.csv')
# wifi = read_WiFi_json_file('wifi_data.json')
# location_df = fetch_locations(bdd, wifi)
# print("Location DataFrame: \n", location_df)

# # Extrair informações dos pontos de acesso
# position = estimate_position(location_df)
# print("Estimated Position:", position)

# position_2d = estimate_position_2d(location_df)
# print("Estimated 2D Position:", position_2d)
