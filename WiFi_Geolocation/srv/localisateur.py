import pandas as pd
from io import StringIO
import json
import os

DEBUG = False

def read_DB_csv_file(csv_file):
    """
    Charger un fichier CSV (d'un chemin local ou d'une URL GitHub) et l'analyser dans un DataFrame pandas.
    """
    # Vérifier si l'entrée est une URL ou un chemin de fichier local
    if csv_file.startswith('http://') or csv_file.startswith('https://') or os.path.isfile(csv_file):
        df = pd.read_csv(csv_file, delimiter=';', encoding='ISO-8859-1')
    else:
        # Lever une exception si le chemin du fichier n'existe pas
        raise FileNotFoundError(f"Le chemin du fichier '{csv_file}' n'existe pas.")
    return df

def read_WiFi_json_file(json_file):
    # Lire le fichier JSON
    with open(json_file, 'r') as f:
        wifi_data = json.load(f)
    
    # Initialiser une liste pour stocker les réseaux WiFi
    wifi_networks = []

    # Itérer à travers chaque élément dans les données JSON pour créer une structure de type JSON
    for element in wifi_data.get("Networks", []):
        network = {
            'MAC': element.get('MAC'),  # Adresse MAC du réseau WiFi
            'RSSI': element.get('RSSI'),  # Puissance du signal du réseau WiFi
        }
        wifi_networks.append(network)
    
    # Convertir la liste des réseaux WiFi en une chaîne JSON formatée
    wifi_json = json.dumps(wifi_networks, indent=4)
    return wifi_json

def fetch_locations(df, wifi_json):
    # Charger les données JSON dans un DataFrame
    if DEBUG:
        print(type(wifi_json))
    wifi_df = pd.read_json(StringIO(wifi_json))
    if DEBUG:
        print(wifi_df)  
    
    # Définir les colonnes du DataFrame de localisation
    df.columns = ['MAC', 'SSID', 'RSSI', 'Latitude', 'Longitude', 'Altitude', 'Acuracy', 'Type']
    
    # Fusionner le DataFrame WiFi avec le DataFrame de localisation en fonction de l'adresse MAC
    merged_df = pd.merge(wifi_df, df, on='MAC', how='inner')
    if DEBUG:
        print("Merged DataFrame: \n", merged_df)
        print(merged_df.size)
    
    # Renommer la colonne RSSI pour éviter les conflits
    merged_df.rename(columns={'RSSI_x': 'RSSI'}, inplace=True)
    
    # Supprimer les colonnes inutiles
    merged_df.drop(['RSSI_y', 'Type'], axis=1, inplace=True)
    
    # Convertir les colonnes de localisation en type float
    merged_df[['Latitude', 'Longitude', 'Altitude', 'Accuracy']] = merged_df[['Latitude', 'Longitude', 'Altitude', 'Acuracy']].astype(float)
    
    # Convertir la colonne RSSI en type int
    merged_df['RSSI'] = merged_df['RSSI'].astype(int)
    
    return merged_df

if DEBUG:
    # bdd = read_DB_csv_file('data/BDD.csv')
    bdd = read_DB_csv_file('https://github.com/dan-lara/IoT-Projects/raw/refs/heads/master/WiFi_Geolocation/srv/data/BDD.csv')
    print("BDD CSV:", bdd)

    wifi = read_WiFi_json_file('data/wifi_data.json')
    print("WiFi JSON: \n", wifi)

    location_df = fetch_locations(bdd, wifi)
    print("DataFrame de localisation: \n", location_df)
