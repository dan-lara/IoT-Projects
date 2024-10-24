import pandas as pd
import numpy as np

def triangulate_location(access_points_df):
    """
    Utiliser une méthode de triangulation pour estimer l'emplacement de l'ESP8266
    en se basant sur les points d'accès détectés.

    Paramètres:
        access_points_df (pd.DataFrame): Cadre de données avec colonnes 'lat', 'lon' et 'signal_strength'.

    Retourne:
        dict: Coordonnées estimées (latitude, longitude).
    """
    # Vérifier que le DataFrame contient les colonnes nécessaires
    if access_points_df.empty or not {'lat', 'lon', 'signal_strength'}.issubset(access_points_df.columns):
        return {"latitude": None, "longitude": None, "error": "Insufficient data"}

    # Pondérer les positions des points d'accès par la force du signal
    access_points_df['weight'] = access_points_df['signal_strength'].apply(lambda x: 1 / abs(x))

    # Calculer la position pondérée moyenne
    weighted_lat = np.average(access_points_df['lat'], weights=access_points_df['weight'])
    weighted_lon = np.average(access_points_df['lon'], weights=access_points_df['weight'])

    return {"latitude": weighted_lat, "longitude": weighted_lon}
