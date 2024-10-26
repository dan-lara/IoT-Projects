import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import json
import os
from trilateration import estimate_position
from localisateur import *
from gestion_bdd import persist_data

DEBUG = False
BDD = 'postgres' # 'sqlite' ou 'postgres'

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configurations MQTT à partir du .env
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')
MQTT_PORT = os.getenv('MQTT_PORT')

def get_location_df(wifis):
    # Lire la base de données à partir d'un fichier CSV
    bdd = read_DB_csv_file('BDD.csv')
    wifis = json.dumps(wifis)
    # Récupérer les localisations à partir de la base de données
    location_df = fetch_locations(bdd, wifis)
    return location_df

def on_connect(client, userdata, flags, rc):
    """Callback lors de la connexion au broker MQTT"""
    if rc == 0:
        print("Connecté au broker MQTT!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Échec de la connexion. Code de retour:", rc)

def on_message(client, userdata, msg):
    """Callback lors de la réception d'un message"""
    try:
        # Décoder le payload du message en JSON
        payload = json.loads(msg.payload.decode())
        
        # Extraire 'device_id'
        device_id = payload.get('end_device_ids', {}).get('device_id', None)
        if DEBUG:
            print("Device ID:", device_id)
        # Extraire 'received_at'
        received_at = payload.get('received_at', None)
        if DEBUG:
            print("Reçu:", received_at)
        # Extraire 'Uplink_message -> decoded_payload'
        decoded_payload = payload.get('uplink_message', {}).get('decoded_payload', {})
        
        # Exemple de manipulation des données du payload
        if decoded_payload:
            if DEBUG:
                print(f"Payload Décodé: {decoded_payload}")
            # Exemple: itérer sur une liste de WiFis dans le decoded_payload, si elle existe
            wifis = decoded_payload.get('Networks', [])
            wifi_count = len(wifis)
            
            # Convertir la liste de WiFis en chaîne JSON
            wifi_json = json.dumps(wifis)
            # print(f"WiFi JSON: {wifi_json}")
            # Traiter chaque point d'accès Wi-Fi (RSSI, BSSID, etc.)
            if DEBUG:
                for wifi in wifis:
                    bssid = wifi.get('MAC')
                    signal_strength = wifi.get('RSSI')
                    print(f"WiFi MAC: {bssid}, RSSI: {signal_strength}")
        
            location_df = get_location_df(wifis)

            if DEBUG:
                print("Taille du DataFrame de Localisation: \n", location_df.shape[0])
            if location_df.shape[0] < 3:
                print("Le DataFrame de localisation doit avoir au moins 3 lignes.")
                return
            position = estimate_position(location_df)[0:2]
            persist_data(device_id, float(position[0]), float(position[1]), wifi_json, received_at, BDD)
            print(f"Données reçues et sauvegardées pour {device_id} à {received_at}: Payload Décodé avec {wifi_count} WiFis")
            return position
        else:
            print("Payload décodé absent ou vide.")
            wifi_json = json.dumps([])  # En cas d'absence de réseaux, sauvegarder une liste vide

        
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage JSON: {e}")
    except KeyError as e:
        print(f"Erreur de clé manquante dans le JSON: {e}")

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Se connecter au broker et démarrer la boucle
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
